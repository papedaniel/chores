from django.contrib import admin
from chores.models import Chores, Category

class BlogAdmin(admin.ModelAdmin):
    exclude = ['posted']
    prepopulated_fields = {'slug': ('title',)}

class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)}


admin.site.register(Chores, BlogAdmin)
admin.site.register(Category, CategoryAdmin)
