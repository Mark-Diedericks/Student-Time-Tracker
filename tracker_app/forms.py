from django.forms import ModelForm
import tracker_app.models as models

class GroupForm(ModelForm):
    class Meta:
        model = models.Group
        fields = '__all__'

class GroupMemberForm(ModelForm):
    class Meta:
        model = models.GroupMember
        fields = '__all__'