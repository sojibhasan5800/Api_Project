from django.contrib import admin
from .models import Category
from django.utils.html import format_html

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('category_name', 'slug', 'url', 'cat_image_tag')
    prepopulated_fields = {'slug': ('category_name',)}
    search_fields = ('category_name', 'description')
    list_filter = ('category_name',)
    readonly_fields = ('cat_image_tag',)

    def cat_image_tag(self, obj):
        if obj.cat_image:
            return format_html('<img src="{}" style="height:50px;width:50px;border-radius:5px;" />', obj.cat_image.url)
        return "-"
    cat_image_tag.short_description = 'Category Image'
