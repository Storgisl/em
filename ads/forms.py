from django import forms
from .models import ExchangeProposal, Ad
from .basefolder.choices import StatusChoices, ConditionChoices, CategoryChoices

class ExchangeProposalForm(forms.ModelForm):
    class Meta:
        model = ExchangeProposal
        fields = ['ad_sender', 'comment']

    def __init__(self, *args, user=None, **kwargs):
        super().__init__(*args, **kwargs)
        if user:
            self.fields['ad_sender'].queryset = user.ads.all()
            self.fields['ad_sender'].help_text = "Select one of your ads to offer in exchange"

        self.fields['comment'].required = True
        self.fields['comment'].widget.attrs.update({
            'placeholder': 'Explain why you want to exchange and any details...'
        })


class AdEditForm(forms.ModelForm):
    class Meta:
        model = Ad
        fields = ['title', 'description', 'image_url', 'category', 'condition']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
            'category': forms.Select(choices=CategoryChoices.choices()),
            'condition': forms.Select(choices=ConditionChoices.choices()),
        }

class AdCreateForm(forms.ModelForm):
    class Meta:
        model = Ad
        fields = ['title', 'description', 'image_url', 'category', 'condition']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Describe your item...'}),
            'category': forms.Select(choices=CategoryChoices.choices()),
            'condition': forms.Select(choices=ConditionChoices.choices()),
        }
        labels = {
            'image_url': 'Image URL (optional)'
        }
