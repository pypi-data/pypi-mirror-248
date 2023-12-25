# gdmty_django_recaptcha_enterprise

**Library for Django that implements Google's reCaptcha Enterprise**

This library is a draft but it works. Was made becasue there is no library for Django that implements Google's reCaptcha Enterprise. But now this library provides a way to verify tokens from reCaptcha Enterprise.

Installation:

```bash
pip install gdmty-django-recaptcha-enterprise
```

Usage:

In settings.py:

```python
# import service_account from google.oauth2 and instanciate a Credentials object from your service account file 

from google.oauth2 import service_account
credentials = service_account.Credentials.from_service_account_file("YOUR_RECAPTCHA_CREDENTIALS_SERVICE_ACCOUNT_FILE")


# put 'gdmty_django_recaptcha_enterprise' in INSTALLED_APPS

INSTALLED_APPS = [
    ...,
    'gdmty_django_recaptcha_enterprise',
    ...
]

# Set the following variables 

RECAPTCHA_ENTERPRISE_PROJECT_ID = 'your-project-id'
RECAPTCHA_ENTERPRISE_SERVICE_ACCOUNT_CREDENTIALS = credentials
RECAPTCHA_ENTERPRISE_SITE_KEY = 'your-site-key' # Additonal, maybe you want to use different keys for different actions; in that case you can use many variables like this one, and choose the right one on instanciate.
RECAPTCHA_ENTERPRISE_BYPASS_TOKEN = 'your-bypass-token' # Optional, only for debug and development usage. Don't use in production.


```

In your code:

```python


# import assess_token from gdmty_django_recaptcha_enterprise.recaptcha, then you can use it to assess tokens where you need it. In this excample we show a hypothetical view that receives a token from a POST request.

from gdmty_django_recaptcha_enterprise.recaptcha import RecaptchaEnterprise
from django.conf import settings


recaptcha = RecaptchaEnterprise(
    settings.RECAPTCHA_ENTERPRISE_PROJECT_ID, 
    settings.RECAPTCHA_ENTERPRISE_SITE_KEY, 
    settings.RECAPTCHA_ENTERPRISE_SERVICE_ACCOUNT_CREDENTIALS)


def my_view(request):
    ...
    token = request.POST.get('token')
    action = 'action-to-verify'
    if recaptcha.assess_token(token, action):
        # Token is valid
        pass
    else:
        # Token is invalid
        pass
    ...
```
