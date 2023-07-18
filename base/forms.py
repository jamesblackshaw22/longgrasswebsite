from django.forms import DateInput, ModelChoiceField, ModelForm
from .models import Indecision, Status, Field


class IndecisionForm(ModelForm):
    class Meta:
        model = Indecision
        fields = ["title", "description", "no_earlier_than", "status", "field"]
        widgets = {
            "no_earlier_than": DateInput(
                attrs={
                    "type": "date",
                    "placeholder": "dd-mm-yyy (NET)",
                    "class": "form-control",
                }
            )
        }
        status = ModelChoiceField(queryset=Status.objects.all())

    def __init__(self, user, *args, **kwargs):
        super(IndecisionForm, self).__init__(*args, **kwargs)
        self.fields["field"].queryset = Field.objects.filter(participants__id=user.id)


class StatusForm(ModelForm):
    class Meta:
        model = Status
        fields = ["name"]


class FieldForm(ModelForm):
    class Meta:
        model = Field
        fields = ["name", "description"]
