from django.contrib import admin
from project.models import Project, Page
from django.utils.translation import gettext_lazy as _

class PageAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {'fields': ('project', 'number', 'title', 'content', 'image')}),
        (_('Advanced options'), {
            'classes': ('collapse',),
            'fields': ('subheading', 'text', 'embed', 'notes'),
        }),
    )
    list_display = ('title', 'number')
    list_filter = ('project',)
    search_fields = ('title', 'subheading')

admin.site.register(Page, PageAdmin)

class ProjectAdmin(admin.ModelAdmin):
    readonly_fields = ['slug', 'created_at']

admin.site.register(Project, ProjectAdmin)
