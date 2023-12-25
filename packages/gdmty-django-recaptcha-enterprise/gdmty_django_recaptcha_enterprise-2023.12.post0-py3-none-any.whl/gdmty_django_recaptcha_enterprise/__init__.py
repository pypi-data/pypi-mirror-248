""" Django reCAPTCHA Enterprise module.

This module provides a Django way to verify Google reCAPTCHA Enterprise

Usage:

    from gdmty_django_recaptcha_enterprise import assess_token
    ...
    # token is the token to verify and action is the name of the action to be verified
    if assess_token(token, action):
        # do something
        ...

"""

__version__ = "2023.12-post0"
