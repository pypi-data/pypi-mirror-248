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
from google.oauth2 import service_account
credentials = service_account.Credentials.from_service_account_file("YOUR_RECAPTCHA_CREDENTIALS_SERVICE_ACCOUNT_FILE")

RECAPTCHA_ENTERPRISE_SITE_KEY = 'your-site-key'
RECAPTCHA_ENTERPRISE_PROJECT_ID = 'your-project-id'
RECAPTCHA_ENTERPRISE_SERVICE_ACCOUNT_CREDENTIALS = credentials
RECAPTCHA_ENTERPRISE_BYPASS_TOKEN = 'your-bypass-token' # Optional, only for debug and development usage. Don't use in production.
```

In your view:

```python
from gdmty_django_recaptcha_enterprise.recaptcha import assess_token

def my_view(request):
    token = request.POST.get('token')
    action = 'action-to-verify'
    if assess_token(token, action):
        # Token is valid
        pass
    else:
        # Token is invalid
        pass
```
