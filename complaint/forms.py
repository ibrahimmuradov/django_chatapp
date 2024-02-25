from django import forms
from .models import Complaint
from django.contrib.auth import get_user_model

Users = get_user_model()


class ComplaintForm(forms.ModelForm):
    content = forms.CharField(max_length=500, min_length=5, widget=forms.Textarea(attrs={
        'class': 'form-control', 'rows': 3,
    }))

    class Meta:
        model = Complaint
        fields = ('compliant_reason', 'content', )

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super().__init__(*args, **kwargs)


    def clean(self):
        get_room_user = Users.objects.get(id=self.data.get('room_user_id'))

        if Complaint.objects.filter(from_user=self.request.user, to_user=get_room_user):
            raise forms.ValidationError('You can only report the user once')

