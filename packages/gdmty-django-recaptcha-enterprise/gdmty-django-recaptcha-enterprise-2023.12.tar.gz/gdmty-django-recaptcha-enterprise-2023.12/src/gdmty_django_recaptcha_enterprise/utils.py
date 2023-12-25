from django.conf import settings


def console_log(*message):
    if settings.DEBUG:
        print(*message)