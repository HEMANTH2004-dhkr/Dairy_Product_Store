from django import forms

class CancelOrderForm(forms.Form):
    reason = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 4, 'class': 'form-control', 'placeholder': 'Write your reason here...'}),
        label='Reason for Cancellation',
        max_length=500,
        required=True,
    )

class ReturnOrderForm(forms.Form):
    reason = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 4, 'class': 'form-control', 'placeholder': 'Write your reason here...'}),
        label='Reason for Return',
        max_length=500,
        required=True,
     )