from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import *

class CustomUserAdmin(UserAdmin):
    model = User
    list_display = ('username', 'email', 'user_contact', 'user_role')
    list_filter = ('user_role', 'is_superuser', 'tags')
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal Info', {'fields': ('first_name', 'last_name', 'email', 'user_contact', 'user_role', 'tags')}),
        ('Permissions', {'fields': ('is_active', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')})
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2', 'user_role', 'user_contact', 'tags'),
        }),
    )
admin.site.register(User, CustomUserAdmin)

class StudentAdmin(CustomUserAdmin):
    model = Student
    list_display = ('roll_no', 'username', 'email', 'user_contact', 'dept')
    list_filter = ('dept', 'tags')
    
    fieldsets = CustomUserAdmin.fieldsets + (
        ('Student Info', {'fields': ('roll_no', 'dept', 'CV')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'roll_no', 'dept', 'email', 'password1', 'password2', 'user_role', 'user_contact'),
        }),
    )
admin.site.register(Student, StudentAdmin)

class AlumniAdmin(CustomUserAdmin):
    model = Alumni
    list_display = ('username', 'email', 'user_contact', 'dept', 'graduating_year')
    list_filter = ('graduating_year', 'dept', 'tags')

    fieldsets = CustomUserAdmin.fieldsets + (
        ('Alumnus Info', {'fields': ('graduating_year', 'dept')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'graduating_year', 'dept', 'email', 'password1', 'password2', 'user_role', 'user_contact'),
        }),
    )
admin.site.register(Alumni, AlumniAdmin)

class CompanyAdmin(CustomUserAdmin):
    model = Company
    list_display = ('username', 'company_name',  'email', 'user_contact')
    list_filter = ('tags',)

    fieldsets = CustomUserAdmin.fieldsets + (
        ('Company Info', {'fields': ('company_name', 'desc')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'company_name', 'email', 'password1', 'password2', 'user_role', 'user_contact', 'desc'),
        }),
    )
admin.site.register(Company, CompanyAdmin)

class NotificationAdmin(admin.ModelAdmin):
    model = Notification
    list_display = ('posted_on',)

    readonly_fields = ('posted_on',)

    fieldsets = (
        ('Notification', {'fields': ('posted_on', 'message')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('message',)
        })
    )
admin.site.register(Notification, NotificationAdmin)

class ChatAdmin(admin.ModelAdmin):
    model = Chat
    list_display = ('sender_username', 'receiver_username', 'timestamp')

    def sender_username(self, obj):
        return obj.sender.username
    
    def receiver_username(self, obj):
        return obj.receiver.username

    sender_username.short_description = 'Sender'
    receiver_username.short_description = 'Receiver'
admin.site.register(Chat, ChatAdmin)

class ContactAdmin(admin.ModelAdmin):
    model = Contact
    list_display = ('sender_mail', 'subject')
    list_filter = ('sender_mail',)

    readonly_fields = ('timestamp',)

    fieldsets = (
        (None, {'fields': ('sender_mail', 'subject', 'mail_content', 'timestamp')}),
    )
admin.site.register(Contact, ContactAdmin)