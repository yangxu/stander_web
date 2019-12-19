# datahub-portal3

pip install
> pip install -r requirements.txt

create suepruser for login (http://localhost:8000/admin)
>./manage.py createsuperuser



### Running
You can start a development/testing service on port 8000 from the command line by using the following command.
```bash
python manage.py runserver
```


### Static assets
If you make changes to any of the static assets within sci-wms, run the following command and commit the results:
```bash
python manage.py collectstatic
```


### Locking down the deployment
You should edit the `Datahub_Portal/local_settings.py` file after deployment and replace the `*` in `ALLOWED_HOSTS` with specific host(s) that that server should be accessible on. Example:
```python
#ALLOWED_HOSTS  = ["*"]
ALLOWED_HOSTS  = ["external-host.com", "YOUR_IP_ADDRESS"]
```


### API Example GET
http://localhost:8000/dictionary/get?type=index
```
[{
   name: "General",
   records: [{
         name: "RIDE_GED_Test",
         user_friendly_name: null,
         description: "",
         index_dimension: null,
         min_dimension_value: null,
         max_dimension_value: null,
         last_received: null,
         last_update: null,
         next_update: null,
         number_of_rows: null,
         last_refreshed: "2019-12-17 16:19"
   }]
}]
```

http://localhost:8000/dictionary/get?type=project
```
[{
   model: "project.project",
   pk: 1,
         fields: {
                  title: "An Early Warning Story: Youth at Risk of DCYF-Schools Involvement",
                  short_title: "An Early Warning Story",
                  slug: "an-early-warning-story",
                  description: "A profile of at risk youth in schools can help us help them.",
                  image: "images/iStock_000004650212XSmall.jpg",
                  publish: true,
                  created_by: null,
                  created_at: "2019-12-18T16:05:30.079Z",
                  keywords: [ ],
                  related_project: [2,3],
                  data_sources__name: "DCYF"
         }
}]
```

### API Example POST to update data dictionary
API Post URL: http://localhost:8000/dictionary/receive
```
{ api_key: "YOUR SETTING KEY",
  save_type: "doc",
  user_friendly_name: "",
  description: "",
  ... 
  rootHeader: ["name", "order", ect],
  row: ["name_value", "order_value", ect],
}
```

### Use monaco editor on flatpage.content and template.content
forms.py
```python
class TemplateForm(forms.ModelForm):
    file_name = forms.CharField(label='Name', max_length=200, required=True)
    content = forms.CharField(label='HTML', widget=forms.Textarea, required=False)
    
    file_name.widget.attrs.update({'class': 'form-control form-control-lg'})
    content.widget.attrs.update({'class': 'form-control form-control-lg', 'style':'display:none;'})

    class Meta:
        model = Template
        fields = ('file_name', 'content')
```

view.py
```python
@staff_member_required(login_url='/accounts/login/')
def edit_template(request, template_id):
    template = get_object_or_404(Template, id=template_id)
    if request.method == "POST":
        form = TemplateForm(request.POST or None, instance=template)
        if form.is_valid():
            template = form.save(commit=False)
            template.save()
            return JsonResponse({"message":"Saved"}, safe=False)
    else:
        form = TemplateForm(request.POST or None, instance=template)

    context = {'form': form,
               'template':template,
               'edit':'content'}
    return render(request, 'flatpages/editor.html', context)
```

admin.py
```python
class TemplateAdmin(admin.ModelAdmin):
    change_form_template = 'template/change_form.html'
```

add change_form.html to template
```
{% extends 'admin/change_form.html' %}

{% block object-tools-items %}
      <li><a href="{% url 'edit_template' original.id %}" class="historylink">Editor</a></li>
      {{ block.super }}
{% endblock %}
```

url.py
```python
        path('template/<template_id>/edit/', views.edit_template, name='edit_template'),
```

http://localhost:8000/flatpage/1/edit/ \
http://localhost:8000/template/8/edit/ \
Use ```Ctrl + s``` to save data


