from django import forms
from .models import Order,Comment,Product

# class OrderForm(forms.Form): #forms.ModelForm
#     name = forms.CharField()
#     phone=  forms.CharField()
#     quantity = forms.IntegerField()

class OrderModelForm(forms.ModelForm):
    class Meta:
        model = Order
        # fields = ['name','phone','quantity']
        exclude = ('product',) # fields = '__all__'
        
        
class CommentModelForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = '__all__'
        

class ProductModelForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = '__all__'