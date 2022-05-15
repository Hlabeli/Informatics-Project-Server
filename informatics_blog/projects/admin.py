from django.contrib import admin
from .models import Project, Comment, Category

# Register your models here.

class ProjectAdmin(admin.ModelAdmin):
    list_display = ('title', 'category')
    list_filter = ('title', 'category')
    prepopulated_fields = {'slug': ('title', ) }

class CategoryAdmin(admin.ModelAdmin):
    list_display = ['category']

admin.site.register(Project, ProjectAdmin)
admin.site.register(Comment)
admin.site.register(Category, CategoryAdmin)


