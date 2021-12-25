from django import forms
from .models import Listing, Category, Comment, Bid


class ListingForm(forms.ModelForm):
    class Meta:
        model = Listing
        fields = ['title', 'description', 'starting_bid', 'photo_url', 'category']
        widgets = {
            'description': forms.Textarea(attrs={'cols':80}),
        }



class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']
        widgets = {'text': forms.Textarea(attrs={'cols':80})}


class BidForm(forms.ModelForm):
    class Meta:
        model = Bid
        fields = ['bid']

