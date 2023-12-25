from google.cloud import recaptchaenterprise_v1
from google.cloud.recaptchaenterprise_v1 import Assessment
from django.conf import settings
from .utils import console_log
from secrets import compare_digest


DEBUG = settings.DEBUG
RECAPTCHA_ENTERPRISE_SITE_KEY = settings.RECAPTCHA_ENTERPRISE_SITE_KEY
RECAPTCHA_ENTERPRISE_PROJECT_ID = settings.RECAPTCHA_ENTERPRISE_PROJECT_ID
RECAPTCHA_ENTERPRISE_SERVICE_ACCOUNT_CREDENTIALS = settings.RECAPTCHA_ENTERPRISE_SERVICE_ACCOUNT_CREDENTIALS
RECAPTCHA_ENTERPRISE_BYPASS_TOKEN = settings.RECAPTCHA_ENTERPRISE_BYPASS_TOKEN


def create_assessment(project_id: str, recaptcha_site_key: str, token: str, recaptcha_action: str) -> Assessment | None:
    """Create an assessment to analyze the risk of a UI action.
    Args:
        project_id: GCloud Project ID
        recaptcha_site_key: Site key obtained by registering a domain/app to use recaptcha services.
        token: The token obtained from the client on passing the recaptchaSiteKey.
        recaptcha_action: Action name corresponding to the token.
    """

    client = recaptchaenterprise_v1.RecaptchaEnterpriseServiceClient(
        credentials=RECAPTCHA_ENTERPRISE_SERVICE_ACCOUNT_CREDENTIALS
    )

    # Set the properties of the event to be tracked.
    event = recaptchaenterprise_v1.Event()
    event.site_key = recaptcha_site_key
    event.token = token

    assessment = recaptchaenterprise_v1.Assessment()
    assessment.event = event

    project_name = f"projects/{project_id}"

    # Build the assessment request.
    request = recaptchaenterprise_v1.CreateAssessmentRequest()
    request.assessment = assessment
    request.parent = project_name

    response = client.create_assessment(request)

    # Check if the token is valid.
    if not response.token_properties.valid:
        console_log(
            "The CreateAssessment call failed because the token was "
            + "invalid for for the following reasons: "
            + str(response.token_properties.invalid_reason)
        )
        return

    # Check if the expected action was executed.
    if response.token_properties.action != recaptcha_action:
        console_log(
            "The action attribute in your reCAPTCHA tag does"
            + "not match the action you are expecting to score"
        )
        return
    else:
        # Get the risk score and the reason(s)
        # For more information on interpreting the assessment,
        # see: https://cloud.google.com/recaptcha-enterprise/docs/interpret-assessment
        for reason in response.risk_analysis.reasons:
            console_log(reason)
        console_log(f"The reCAPTCHA score for this token is: {str(response.risk_analysis.score)}")
        # Get the assessment name (id). Use this to annotate the assessment.
        assessment_name = client.parse_assessment_path(response.name).get("assessment")
        console_log(f"Assessment name: {assessment_name}")
    return response


def assess_token(token: str, recaptcha_action: str = None) -> bool:
    """Create an assessment of a token for a given action.
    Args:
        :param token: The token obtained from the client on passing the recaptchaSiteKey.
        :param recaptcha_action: The action name used to assess the token.
    """
    if DEBUG and RECAPTCHA_ENTERPRISE_BYPASS_TOKEN:
        if compare_digest(token, RECAPTCHA_ENTERPRISE_BYPASS_TOKEN):
            return True

    response = create_assessment(RECAPTCHA_ENTERPRISE_PROJECT_ID, RECAPTCHA_ENTERPRISE_SITE_KEY, token, recaptcha_action)

    if response:
        return response.token_properties.valid
    return False
