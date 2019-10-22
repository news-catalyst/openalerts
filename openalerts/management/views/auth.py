from django.views.generic import TemplateView, RedirectView
from django.shortcuts import redirect, reverse

class LoginView(TemplateView):
    template_name = "management/pages/login.html"

    def dispatch(self, request, *args, **kwargs):
        if self.request.session.get("authenticated", False) == True:
            return redirect("management:dashboard")
        return super().dispatch(request, *args, **kwargs)

class LogoutView(RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        return reverse("management:login")
    
    def dispatch(self, request, *args, **kwargs):
        request.session.flush()
        return super().dispatch(request, *args, **kwargs)