from django.contrib import admin
from portal.models import FlatPageAddon, FilePage, UploadFile, Template
from django.contrib.flatpages.admin import FlatPage
from django.contrib.flatpages.forms import FlatpageForm
from django.utils.translation import gettext_lazy as _
from django.core.files.base import ContentFile
from django.contrib import messages

## Actions ###
def save_to_template_file(modeladmin, request, queryset):
    for template in queryset:
        if template.file:
           template.file.delete()
        template.file.save(template.file_name, ContentFile(template.content))
    messages.add_message(request, messages.INFO, "Finish Create Template File")

def load_template_file(modeladmin, request, queryset):
    for template in queryset:
        with template.file.open('r') as f:
            template.content = f.read()
            template.save()
            f.close()
    messages.add_message(request, messages.INFO, "Finish Load Template File")


class FlatPageAddonInline(admin.StackedInline):
    model = FlatPageAddon

class UploadFileInline(admin.TabularInline):
    model = UploadFile
    readonly_fields = ['upload_by', 'upload_at']

class FlatPageAdmin(admin.ModelAdmin):
    change_form_template = 'flatpages/change_form.html'
    model = FlatPage
    form = FlatpageForm
    fieldsets = (
        (None, {'fields': ('url', 'title', 'content', 'sites')}),
        (_('Advanced options'), {
            'classes': ('collapse',),
            'fields': ('registration_required', 'template_name'),
        }),
    )
    list_display = ('url', 'title')
    list_filter = ('sites', 'registration_required')
    search_fields = ('url', 'title')
    inlines = [FlatPageAddonInline]

class FilePageAdmin(admin.ModelAdmin):
    readonly_fields = ['slug']
    list_display = ['name', 'slug', 'publish']
    fieldsets = (
        (None, {'fields': ('name', 'slug', 'publish', 'description', 'template_name')}),
    )
    inlines = [UploadFileInline]

    def save_model(self, request, obj, form, change):
        obj.upload_by = request.user
        super().save_model(request, obj, form, change)

    def save_formset(self, request, form, formset, change):
        instances = formset.save(commit=False)
        for obj in formset.deleted_objects:
            obj.delete()
        for instance in instances:
            instance.upload_by = request.user
            instance.save()
        formset.save_m2m()

class TemplateAdmin(admin.ModelAdmin):
    change_form_template = 'template/change_form.html'
    fieldsets = (
        (None, {'fields': ('file_name', 'content', 'file', 'created_at', 'last_saved_by')}),
    )
    readonly_fields = [ 'created_at', 'last_saved_by']
    list_display = ['file_name', 'file', 'created_at', 'last_saved_by']
    actions = [ save_to_template_file, load_template_file ]
    
    def save_model(self, request, obj, form, change):
        obj.last_saved_by = request.user
        super().save_model(request, obj, form, change)

    def save_formset(self, request, form, formset, change):
        instances = formset.save(commit=False)
        for obj in formset.deleted_objects:
            obj.delete()
        for instance in instances:
            instance.last_saved_by = request.user
            instance.save()
        formset.save_m2m()

admin.site.unregister(FlatPage)
admin.site.register(FlatPage, FlatPageAdmin)
admin.site.register(FilePage, FilePageAdmin)
admin.site.register(Template, TemplateAdmin)

