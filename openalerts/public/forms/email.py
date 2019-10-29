from django import forms
from subscriptions.models import EmailSubscription
from alerts.models import Channel


class EmailSignupForm(forms.Form):
    email = forms.EmailField(
        widget=forms.EmailInput(
            attrs={"placeholder": "Enter your email..."}
        ),
        label="",
    )


class EmailSettingsForm(forms.ModelForm):
    class Meta:
        model = EmailSubscription
        fields = ["channels"]

    channels = forms.ModelMultipleChoiceField(
        widget=forms.CheckboxSelectMultiple, queryset=Channel.objects.all()
    )

    def __init__(self, *args, **kwargs):
        super(EmailSettingsForm, self).__init__(*args, **kwargs)
        self.fields["channels"].queryset = Channel.objects.filter(
            organization=kwargs["instance"].organization
        )
