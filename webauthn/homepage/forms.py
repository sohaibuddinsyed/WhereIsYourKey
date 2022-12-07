from django import forms


class RegistrationOptionsRequestForm(forms.Form):
    username = forms.CharField(required=True, max_length=64)
    require_user_verification = forms.BooleanField(required=False, initial=False)
    attestation = forms.ChoiceField(
        required=True,
        choices=[
            ("none", "None"),
            ("direct", "Direct"),
        ],
    )
    attachment = forms.ChoiceField(
        required=True,
        choices=[
            ("all", "All Supported"),
            ("cross_platform", "Cross-Platform"),
            ("platform", "Platform"),
        ],
    )
    algorithms = forms.MultipleChoiceField(
        required=False, choices=[("es256", "ES256"), ("rs256", "RS256")]
    )
    discoverable_credential = forms.ChoiceField(
        required=True,
        choices=[
            ("discouraged", "Discouraged"),
            ("preferred", "Preferred"),
            ("required", "Required"),
        ],
    )


class RegistrationResponseForm(forms.Form):
    username = forms.CharField(required=True, max_length=64)
    response = forms.JSONField(required=True)
    metadata = forms.JSONField()


class AuthenticationOptionsRequestForm(forms.Form):
    username = forms.CharField(required=False, max_length=64)
    require_user_verification = forms.BooleanField(required=False, initial=False)


class AuthenticationResponseForm(forms.Form):
    username = forms.CharField(required=False, max_length=64)
    response = forms.JSONField(required=True)
