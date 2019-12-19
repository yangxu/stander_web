from django.contrib import admin
from dictionary.models import Group, DataSet, DataColumn, DataSource, SubAgency

class DataColumnInline(admin.TabularInline):
    model = DataColumn

class GroupAdmin(admin.ModelAdmin):
   list_display = ('name','order')
   filter_horizontal = ('dataset',)
   ordering = ('order',)

admin.site.register(Group, GroupAdmin)

class DataSetAdmin(admin.ModelAdmin):
    change_form_template = 'dataset/change_form.html'
    list_display = ('model_name', 'user_friendly_name', 'number_of_rows', 'last_received', 'last_refreshed')
    list_filter = ('sub_agency', 'update_frequency')
    search_fields = ('model_name', "user_friendly_name")
    inlines = [DataColumnInline]

admin.site.register(DataSet, DataSetAdmin)
admin.site.register(DataSource)
admin.site.register(SubAgency)
