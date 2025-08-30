from django.contrib import admin
from django.utils.html import format_html
from .models import Account, UserProfile


# ---------------- Account Admin ----------------
class AccountAdmin(admin.ModelAdmin):
    list_display = ('email', 'username', 'role', 'is_active', 'is_staff', 'is_admin', 'date_joined')
    list_filter = ('role', 'is_active', 'is_staff', 'is_admin')
    search_fields = ('email', 'username')
    ordering = ('-date_joined',)
    readonly_fields = ('date_joined', 'last_login', 'username')

    fieldsets = (
        ('Account Info', {
            'fields': ('email', 'username', 'password')
        }),
        ('Personal Info', {
            'fields': ('role',)
        }),
        ('Permissions', {
            'fields': ('is_active', 'is_staff', 'is_admin', 'is_superadmin')
        }),
        ('Important Dates', {
            'fields': ('last_login', 'date_joined')
        }),
    )


# ---------------- User Profile Admin ----------------
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user','first_name','last_name', 'bio_short', 'address', 'phone_number', 'profile_pic_preview')
    search_fields = ('user__email', 'address', 'phone_number')
    readonly_fields = ('profile_pic_preview',)

    def profile_pic_preview(self, obj):
        if obj.profile_picture:
            return format_html('<img src="{}" style="width:40px; height:40px; border-radius:50%;" />', obj.profile_picture.url)
        return "-"
    profile_pic_preview.short_description = 'Profile Picture'

    def bio_short(self, obj):
        return (obj.bio[:30] + "...") if obj.bio else ""
    bio_short.short_description = 'Bio'


# ---------------- Register Models ----------------
admin.site.register(Account, AccountAdmin)
admin.site.register(UserProfile, UserProfileAdmin)

# ---------------- Customize Admin Header ----------------
admin.site.site_header = "Company Admin Dashboard"
admin.site.site_title = "Company Portal"
admin.site.index_title = "Welcome to Company Admin Panel"
