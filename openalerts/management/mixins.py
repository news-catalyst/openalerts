from django.contrib.auth.mixins import AccessMixin
from django.shortcuts import redirect

class SessionAuthenticationRequiredMixin(AccessMixin):
    """Verify that the current user is authenticated."""
    def dispatch(self, request, *args, **kwargs):
        if not request.session.get("authenticated", False) == True:
            return redirect("management:login")
        return super().dispatch(request, *args, **kwargs)