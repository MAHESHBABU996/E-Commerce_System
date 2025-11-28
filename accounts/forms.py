from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser, Role, VendorType


class CustomUserCreationForm(UserCreationForm):
    """
    Form for creating new users. Includes all required fields, plus custom fields.
    """
    role = forms.ModelChoiceField(queryset=Role.objects.all(), required=True, label="User Role")
    vendor_type = forms.ModelChoiceField(queryset=VendorType.objects.all(), required=False, label="Vendor Type (For Vendors Only)")

    class Meta:
        model = CustomUser
        fields = ["username", "email", "phone", "address", "role", "vendor_type", "password1", "password2"]

    def clean(self):
        cleaned_data = super().clean()
        role = cleaned_data.get("role")
        vendor_type = cleaned_data.get("vendor_type")

        if role:
            if role.name == "Vendor" and not vendor_type:
                self.add_error("vendor_type", "Vendors must select a Vendor Type.")
            elif role.name != "Vendor" and vendor_type:
                self.add_error("vendor_type", "Only Vendors should select a Vendor Type.")
        
        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])  # Encrypt password

        # Assign vendor type only for vendors
        if user.role.name == "Vendor":
            user.vendor_type = self.cleaned_data.get("vendor_type")

        if commit:
            user.save()
        return user


class CustomUserChangeForm(UserChangeForm):
    """
    Form for updating existing users. Includes all fields on the user model.
    """
    role = forms.ModelChoiceField(queryset=Role.objects.all(), required=True, label="User Role")
    vendor_type = forms.ModelChoiceField(queryset=VendorType.objects.all(), required=False, label="Vendor Type (For Vendors Only)")

    class Meta:
        model = CustomUser
        fields = ["username", "email", "phone", "address", "role", "vendor_type", "is_role_approved"]

    def clean(self):
        cleaned_data = super().clean()
        role = cleaned_data.get("role")
        vendor_type = cleaned_data.get("vendor_type")

        if role:
            if role.name == "Vendor" and not vendor_type:
                self.add_error("vendor_type", "Vendors must select a Vendor Type.")
            elif role.name != "Vendor" and vendor_type:
                self.add_error("vendor_type", "Only Vendors should select a Vendor Type.")
        
        return cleaned_data


class CustomUserEditForm(forms.ModelForm):
    """
    Form for editing existing users. Includes all fields on the user model.
    """
    role = forms.ModelChoiceField(queryset=Role.objects.all(), required=True, label="User Role")
    vendor_type = forms.ModelChoiceField(queryset=VendorType.objects.all(), required=False, label="Vendor Type (For Vendors Only)")

    class Meta:
        model = CustomUser
        fields = ["username", "email", "phone", "address", "role", "vendor_type", "is_role_approved"]

    def clean(self):
        cleaned_data = super().clean()
        role = cleaned_data.get("role")
        vendor_type = cleaned_data.get("vendor_type")

        if role:
            if role.name == "Vendor" and not vendor_type:
                self.add_error("vendor_type", "Vendors must select a Vendor Type.")
            elif role.name != "Vendor" and vendor_type:
                self.add_error("vendor_type", "Only Vendors should select a Vendor Type.")
        
        return cleaned_data


class CustomSignupForm(CustomUserCreationForm):
    """
    Signup form for new users, inheriting from CustomUserCreationForm.
    """
    pass  # Uses the logic from CustomUserCreationForm




# from django import forms
# from django.contrib.auth.forms import UserCreationForm, UserChangeForm
# from .models import CustomUser, Role, VendorType

# class CustomUserCreationForm(UserCreationForm):
#     """
#     Form for creating new users. Includes all required fields, plus custom fields.
#     """
#     role = forms.ModelChoiceField(queryset=Role.objects.all(), required=True)
#     vendor_type = forms.ModelChoiceField(queryset=VendorType.objects.all(), required=False)

#     class Meta:
#         model = CustomUser
#         fields = ["username", "email", "phone", "address", "role", "vendor_type", "password1", "password2"]

#     def clean(self):
#         cleaned_data = super().clean()
#         role = cleaned_data.get("role")
#         vendor_type = cleaned_data.get("vendor_type")

#         if role and role.name == "Vendor" and not vendor_type:
#             self.add_error("vendor_type", "Vendors must select a Vendor Type.")
#         return cleaned_data

# class CustomUserChangeForm(UserChangeForm):
#     """
#     Form for updating existing users. Includes all fields on the user model.
#     """
#     role = forms.ModelChoiceField(queryset=Role.objects.all(), required=True)
#     vendor_type = forms.ModelChoiceField(queryset=VendorType.objects.all(), required=False)

#     class Meta:
#         model = CustomUser
#         fields = ["username", "email", "phone", "address", "role", "vendor_type", "is_role_approved"]

# class CustomUserEditForm(forms.ModelForm):
#     """
#     Form for editing existing users. Includes all fields on the user model.
#     """
#     role = forms.ModelChoiceField(queryset=Role.objects.all(), required=True)
#     vendor_type = forms.ModelChoiceField(queryset=VendorType.objects.all(), required=False)

#     class Meta:
#         model = CustomUser
#         fields = ["username", "email", "phone", "address", "role", "vendor_type", "is_role_approved"]

# class CustomSignupForm(UserCreationForm):
#     """
#     Signup form for new users, including role selection and vendor type for vendors. 
#     """
#     role = forms.ModelChoiceField(queryset=Role.objects.all(), required=True)
#     vendor_type = forms.ModelChoiceField(queryset=VendorType.objects.all(), required=False)

#     class Meta:
#         model = CustomUser
#         fields = ["username", "email", "phone", "address", "role", "vendor_type", "password1", "password2"]

#     def clean(self):
#         cleaned_data = super().clean()
#         role = cleaned_data.get("role")
#         vendor_type = cleaned_data.get("vendor_type")

#         if role and role.name == "Vendor" and not vendor_type:
#             self.add_error("vendor_type", "Vendors must select a Vendor Type.")
#         return cleaned_data
