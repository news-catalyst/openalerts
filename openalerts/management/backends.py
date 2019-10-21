"""
Backend to support OIDC login
"""

# Django
import os

# Third Party
from social_core.backends.open_id_connect import OpenIdConnectAuth

class PressPassBackend(OpenIdConnectAuth):
    """Authentication backend for PressPass OpenId"""
    name = 'presspass'
    OIDC_ENDPOINT = os.getenv("PRESSPASS_BACKEND_URL", 'https://passpass.it/openid')
    DEFAULT_SCOPE = ['openid', 'profile', 'email', 'organizations']

    def get_user_details(self, response):
        details = super().get_user_details(response)
        details["organizations"] = response["organizations"]
        return details
