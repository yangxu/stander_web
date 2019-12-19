from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from django.http import JsonResponse
from dictionary.receive import Receive
from dictionary.models import Group, DataSet
from project.models import Project
from django.shortcuts import get_object_or_404
from django.core import serializers
import json

#from django.contrib.gis.serializers.geojson import Serializer
from django.db.models import Manager
# FYI: It can be any of the following as well:
# from django.core.serializers.pyyaml import Serializer
# from django.core.serializers.python import Serializer
from django.core.serializers.json import Serializer

JSON_ALLOWED_OBJECTS = (dict,list,tuple,str,int,bool)


class CustomSerializer(Serializer):

    def end_object(self, obj):
        for field in self.selected_fields:
            if field == 'pk':
                continue
            elif field in self._current.keys():
                continue
            else:
                try:
                    if '__' in field:
                        fields = field.split('__')
                        value = obj
                        for f in fields:
                            value = getattr(value, f)
                        if value != obj and isinstance(value, JSON_ALLOWED_OBJECTS) or value == None:
                            self._current[field] = value

                except AttributeError:
                    pass
        super(CustomSerializer, self).end_object(obj)


@csrf_exempt
def receive(request):
    API_KEY = request.POST.get("api_key", None)
    if API_KEY != settings.KEY:
         return JsonResponse({"message":"Error: Invalid Key"}, safe=False)
    receive = Receive(request)
    json = receive.save()
    return JsonResponse(json, safe=False)

def get(request):
    type = request.GET.get("type", None)
    if type == "index":
       groups = Group.objects.all().order_by('id')
       result = []
       for group in groups:
          g = {"name":group.name}
          records = []
          for d in group.dataset.all():

             if d.last_received:
                last_received = d.last_received.strftime('%Y-%m-%d')
             else:
                last_received = None

             if d.last_update:
                last_update = d.last_update.strftime('%Y-%m-%d')
             else:
                last_update = None

             if d.next_update:
                next_update = d.next_update.strftime('%Y-%m-%d')
             else:
                next_update = None

             if d.last_refreshed:
                last_refreshed = d.last_refreshed.strftime('%Y-%m-%d %H:%M')
             else:
                last_refreshed = None


             dataset = {"name":d.model_name,
                       "user_friendly_name": d.user_friendly_name,
                       "description":d.description,
                       "index_dimension":d.index_dimension,
                       "min_dimension_value":d.min_dimension_value,
                       "max_dimension_value":d.max_dimension_value,
                       "last_received":last_received,
                       "last_update":last_update,
                       "next_update":next_update,
                       "number_of_rows":d.number_of_rows,
                       "last_refreshed":last_refreshed}
             records.append(dataset)
          g.update({"records":records})
          result.append(g)
    elif type == "project":
       projects = Project.objects.all().order_by('created_at')
       serializers = CustomSerializer()
       json_data = serializers.serialize(projects, fields=('pk', 'title','short_title','slug','description','image','publish','data_sources__name','created_by','created_at','keywords','related_project'))

       j = json.loads(json_data)
       return JsonResponse(j, safe=False)
    else:
       return JsonResponse({"message":"Error: Invalid Request"}, safe=False)
    return JsonResponse(result, safe=False)

def dataset(request, model_name):
    dataset = get_object_or_404(DataSet, model_name=model_name)
    columns = dataset.datacolumns
    if dataset.template_name:
       template_name = dataset.template_name
    else:
       template_name = 'flatpages/default.html'
    content = """
                <table class="table">
                  <thead class="thead-light">
                    <tr>
                      <th scope="col">#</th>
                      <th scope="col">Field Name</th>
                      <th scope="col">Description</th>
                    </tr>
                  </thead>
                  <tbody>"""
    count = 0
    for i in columns:
        count = count + 1
        content = content + """
                    <tr>
                      <th scope="row">%s</th>
                      <td>%s</td>
                      <td>%s</td>
                    </tr>"""%(count, i.name, i.description)
    content = content + "</table>"
    filepage = {
                 "title": dataset.user_friendly_name,
                 "content": content,
                 "dataset": dataset,
               }
    return render(request, template_name, filepage)

