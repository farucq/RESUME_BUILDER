from django import forms
from .models import Feedback

class FeedbackForm(forms.ModelForm):
    class Meta:
        model = Feedback
        fields = ['username', 'email', 'message']
        widgets = {
            'message': forms.Textarea(attrs={'rows': 4, 'cols': 40}),
        }