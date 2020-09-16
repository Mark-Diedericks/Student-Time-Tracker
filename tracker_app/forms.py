from django.forms import ModelForm
import tracker_app.models as models

class GroupForm(ModelForm):
    class Meta:
        model = models.Group
        fields = '__all__'

class MemberEntryForm(ModelForm):
    class Meta:
        model = models.MemberEntry
        fields = [
            # fields here
        ]