from django.contrib import admin
from chores.models import Chores, Category, History

class BlogAdmin(admin.ModelAdmin):
    exclude = ['posted']
    prepopulated_fields = {'slug': ('title',)}

class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)}

class HistoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {}


admin.site.register(Chores, BlogAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(History, HistoryAdmin)
