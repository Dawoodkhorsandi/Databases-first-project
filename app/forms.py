from django import forms
from django.contrib.auth.forms import AuthenticationForm

class HomeSuppliantForm(forms.Form):
    first_name = forms.CharField(max_length=256, required=True)
    last_name = forms.CharField(max_length=256, required=True)
    national_code = forms.IntegerField(required=True, widget=forms.TextInput)
    postal_code = forms.IntegerField(required=True, widget=forms.TextInput)
    phone_number = forms.IntegerField(required=True, widget=forms.TextInput)
    units = forms.IntegerField(required=True, widget=forms.TextInput)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['first_name'].widget.attrs.update({
            'class': 'fadeIn second',
            'placeholder': 'نام', })
        self.fields['last_name'].widget.attrs.update({
            'class': 'fadeIn second',
            'placeholder': 'نام خانوادگی', })
        self.fields['national_code'].widget.attrs.update({
            'class': 'fadeIn second',
            'placeholder': 'کد ملی', })
        self.fields['postal_code'].widget.attrs.update({
            'class': 'fadeIn second',
            'placeholder': 'کد پستی', })
        self.fields['phone_number'].widget.attrs.update({
            'class': 'fadeIn second',
            'placeholder': 'شماره تماس', })
        self.fields['units'].widget.attrs.update({
            'class': 'fadeIn second',
            'placeholder': 'تعداد واحد ساختمان', })


class HomeSuppliantEditForm(forms.Form):
    first_name = forms.CharField(max_length=256, required=False)
    last_name = forms.CharField(max_length=256, required=False)
    national_code = forms.IntegerField(required=False, widget=forms.TextInput)
    postal_code = forms.IntegerField(required=False, widget=forms.TextInput)
    phone_number = forms.IntegerField(required=False, widget=forms.TextInput)
    units = forms.IntegerField(required=False, widget=forms.TextInput)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['first_name'].widget.attrs.update({
            'class': 'fadeIn second',
            'placeholder': 'نام', })
        self.fields['last_name'].widget.attrs.update({
            'class': 'fadeIn second',
            'placeholder': 'نام خانوادگی', })
        self.fields['national_code'].widget.attrs.update({
            'class': 'fadeIn second',
            'placeholder': 'کد ملی', })
        self.fields['postal_code'].widget.attrs.update({
            'class': 'fadeIn second',
            'placeholder': 'کد پستی', })
        self.fields['phone_number'].widget.attrs.update({
            'class': 'fadeIn second',
            'placeholder': 'شماره تماس', })
        self.fields['units'].widget.attrs.update({
            'class': 'fadeIn second',
            'placeholder': 'تعداد واحد ساختمان', })


class AddressForm(forms.Form):
        address = forms.CharField(max_length=1000)
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.fields['address'].widget.attrs.update({
                'class': 'fadeIn second',
                'placeholder': 'آدرس', })

class HomeClientForm(forms.Form):
    subscription_number = forms.IntegerField(required=True, widget=forms.TextInput)
    first_name = forms.CharField(max_length=256, required=True)
    last_name = forms.CharField(max_length=256, required=True)
    national_code =forms.IntegerField(required=True, widget=forms.TextInput)
    address = forms.CharField(max_length=1000)
    phone_number = forms.IntegerField(required=True, widget=forms.TextInput)
    confirm_date = forms.DateField(required=False)
    units = forms.CharField(required=True)

class BillForm(forms.Form):
    subscription_number = forms.IntegerField(required=True)
    bill_id = forms.IntegerField(required=True)
    perivous_number = forms.IntegerField(required=True)
    current_number = forms.IntegerField(required=True)
    deadline = forms.DateField(required=False)
    


class PaymentForm(forms.Form):
    bill_id = forms.IntegerField(required=True)
    payment_fee = forms.IntegerField(required=True)
    payment_date = forms.DateField(required=True)

class MyAuthenticationForm(AuthenticationForm):
    # add your form widget here
    widget = {'password': 'text'}
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'class': 'fadeIn second form-control from-control-lg', 'placeholder': 'username', })
        self.fields['password'].widget.attrs.update({'class': 'fadeIn second form-control from-control-lg', 'placeholder': 'password', })

class LoginForm(forms.Form):
    username = forms.CharField(required=True)
    password = forms.CharField(required=True, widget=forms.PasswordInput)


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'class': 'fadeIn second', 'placeholder': 'username', })
        self.fields['password'].widget.attrs.update({'class': 'fadeIn second', 'placeholder': 'password', })
class SearchForm(forms.Form):
    text = forms.CharField(required=True, max_length=150)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['text'].widget.attrs.update({'class': 'form-control form-control-lg form-control-borderless', 'placeholder': 'اسم یا شماره اشتراک خود را جستجو کنید' })