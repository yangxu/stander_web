from dictionary.models import DataSet, DataColumn, DataValue
import json
from datetime import datetime
__version__ = "0.1"


class Receive(object):

    def __init__(self, request = None):
        self.request = request
        self.save_type = request.POST.get('save_type', None) # Documentation vs. Aggregation (doc, agg)
        self.insert = request.POST.get('insert', None) # keep adding
        self.remove = request.POST.get('remove', None) # remove all
        self.publish = request.POST.get('publish', None) # change status to publish
        self.unpublish = request.POST.get('unpublish', None)
        self.data = request.POST.get('data', None)

        self.totalProperty = request.POST.get('totalProperty', None)
        self.aggregation_slug = request.POST.get('aggregation_slug', None)
        self.aggregation_name = request.POST.get('aggregation_name', None)
        self.aggregation_description = request.POST.get('aggregation_description', None)
        self.indicator_slug = request.POST.get('indicator_slug', None)
        self.indicator_name = request.POST.get('indicator_name', None)
        self.dimension_x = request.POST.get('dimension_x', None)
        self.dimension_y = request.POST.get('dimension_y', None)
        self.indicator_description = request.POST.get('indicator_description', None)
        self.rootProperty = request.POST.getlist('rootProperty', None)
    
        self.project_full_name = request.POST.get("project_full_name", None)
        self.project_name = request.POST.get("project_name", None)
        self.project_category = request.POST.get("project_category", None)
        self.dataset_full_name = request.POST.get("dataset_full_name", None)
        self.dataset_name = request.POST.get("dataset_name", None)
        self.description = request.POST.get("description", None)
        self.index_dimension = request.POST.get("index_dimension", None)
        self.min_dimension_value = request.POST.get("min_dimension_value", None)
        self.max_dimension_value = request.POST.get("max_dimension_value", None)

        self.last_received = request.POST.get("last_received",None)
        self.number_of_rows = request.POST.get("number_of_rows",None)
        self.last_update = request.POST.get("last_update",None)
        self.next_update = request.POST.get("next_update",None)

        self.rootHeader = request.POST.getlist('rootHeader', None)
        self.column_name = request.POST.get("column_name", None)

    def saveDoc(self):

        data_set, created = DataSet.objects.get_or_create(model_name=self.dataset_name)
        data_set.user_friendly_name = self.dataset_full_name
        data_set.description = self.description
        data_set.index_dimension = self.index_dimension
        data_set.min_dimension_value = self.min_dimension_value
        data_set.max_dimension_value = self.max_dimension_value
        data_set.last_refreshed = datetime.now()
        data_set.last_received = self.last_received
        data_set.number_of_rows = self.number_of_rows
        data_set.last_update = self.last_update
        data_set.next_update = self.next_update
        data_set.save()
        

        data_set.datacolumns.delete()
        for i in range(int(self.totalProperty)):
            row = self.request.POST.getlist(str(i), None)
            if row[self.rootHeader.index("column_allow_null")] == "True":
               column_allow_null = True
            else:
               column_allow_null = False
            if row[self.rootHeader.index("column_allow_blank")] == "True":
               column_allow_blank = True
            else:
               column_allow_blank = False
            if row[self.rootHeader.index("column_max_length")] == "None":
               column_max_length = None
            else:
               column_max_length = row[self.rootHeader.index("column_max_length")]
            description = row[self.rootHeader.index("description")]
            if row[self.rootHeader.index("order")] == "None":
               order = None
            else:
               order = row[self.rootHeader.index("order")]

            DataColumn.objects.get_or_create(dataset = data_set, name = row[self.rootHeader.index("name")], column_type = row[self.rootHeader.index("column_type")], column_allow_null=column_allow_null, column_allow_blank=column_allow_blank, column_max_length=column_max_length, description=description, order=order)

        return {"status": "success"}

    def saveDocValue(self):
        try:
           dataset = DataSet.objects.get(name=self.dataset_name)
           data_column = DataColumn.objects.get(dataset = dataset, name=self.column_name)
        except:
           return {"status":"can not find dataset or datacolumn"}
        data_column.datavalues.delete()
        for i in range(int(self.totalProperty)):
            row = self.request.POST.getlist(str(i), None)
            value = row[self.rootHeader.index("value")]
            description = row[self.rootHeader.index("description")]
            DataValue.objects.get_or_create(datacolumn = data_column, value=value, description=description)

        return {"status": "success"}


    def save(self):
        if self.save_type == 'doc':
           json = self.saveDoc()
        if self.save_type == "doc_values":
           json = self.saveDocValue()
        return json
