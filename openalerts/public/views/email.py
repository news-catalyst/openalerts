from django.views.generic import TemplateView

class EmailSignUpView(TemplateView):
    template_name = "public/email/signup.html"