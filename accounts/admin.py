# accounts/admin.py

from django import forms
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import User, Role, TokenBlackList
from students.models import Institution   # 👈 Агар institution дар app “students” бошад


# ✅ Custom Add Form бо institution ва roles
class CustomUserCreationForm(UserCreationForm):
    institution = forms.ModelChoiceField(
        queryset=Institution.objects.all(),
        required=False,
        label="Institution"
    )
    roles = forms.ModelMultipleChoiceField(
        queryset=Role.objects.all(),
        required=False,
        label="Roles"
    )

    class Meta:
        model = User
        fields = (
            'username', 'email', 'password1', 'password2',
            'institution', 'roles', 'is_staff', 'is_superuser', 'status'
        )

    # ⛏ override save() барои ManyToMany ва FK
    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.save()
            self.save_m2m()
        return user


# ✅ Custom change form
class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = User
        fields = '__all__'


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm

    list_display = ('username', 'email', 'institution', 'is_staff', 'status')
    list_filter = ('is_staff', 'is_superuser', 'status', 'institution')
    search_fields = ('username', 'email')
    ordering = ('username',)

    fieldsets = (
        (None, {'fields': ('username', 'email', 'password')}),
        ('Institution & Roles', {'fields': ('institution', 'roles')}),
        ('Permissions', {'fields': ('is_staff', 'is_superuser', 'status')}),
        ('Important dates', {'fields': ('last_login',)}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                'username', 'email', 'password1', 'password2',
                'institution', 'roles', 'is_staff', 'is_superuser', 'status'
            ),
        }),
    )


admin.site.register(Role)
admin.site.register(TokenBlackList)
