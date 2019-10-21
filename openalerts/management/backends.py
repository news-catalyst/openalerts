"""
Backend to support OIDC login
"""

# Django
from django.conf import settings

# Third Party
from social_core.backends.open_id_connect import OpenIdConnectAuth

class SquareletBackend(OpenIdConnectAuth):
    """Authentication Backend for PressPass OpenId"""
    name = 'presspass'
    OIDC_ENDPOINT = settings.PRESSPASS_URL + '/openid'