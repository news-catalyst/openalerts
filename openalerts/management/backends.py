"""
Backend to support OIDC login
"""

# Django
from django.conf import settings

# Third Party
from social_core.backends.open_id_connect import OpenIdConnectAuth

class PressPassBackend(OpenIdConnectAuth):
    """Authentication Backend for PressPass OpenId"""
    name = 'presspass'
    OIDC_ENDPOINT = settings.PRESSPASS_URL + '/openid'
    CLIENT_ID = "147292"
    DEFAULT_SCOPE = ['openid', 'profile', 'email', 'organizations']