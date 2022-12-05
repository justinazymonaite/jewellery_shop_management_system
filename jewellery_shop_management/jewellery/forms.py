from django import forms 
from . models import ReviewProduct
from django.utils.timezone import timedelta, datetime


class ProductReviewForm(forms.ModelForm):
    def is_valid(self):
        valid = super().is_valid()
        if valid:
            customer = self.cleaned_data.get("customer")
            recent_posts = ReviewProduct.objects.filter(customer=customer, created_at__gte=(datetime.now() - timedelta(days=1)))
            if recent_posts:
                return False
        return valid
        
    class Meta:
        model = ReviewProduct
        fields = ('review', 'product', 'customer')
        widgets = {
            'product': forms.HiddenInput(),
            'customer': forms.HiddenInput(),
        }

