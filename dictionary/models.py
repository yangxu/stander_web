from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils.text import slugify

class Keyword(models.Model):
    value = models.CharField(max_length=100,unique=True)
    subnav_order = models.IntegerField(unique=True, null=True, blank=True)
    slug = models.SlugField()

    def save(self, *args, **kwargs):
        self.slug = slugify(self.value)
        super(Keyword, self).save(*args, **kwargs)

    def __str__(self):
        return self.value


class DataSource(models.Model):
    short = models.CharField(max_length=11)
    short_name = models.CharField(max_length=12) # to display in lists, etc
    name = models.CharField(max_length=100)
    url = models.URLField()
    icon_file = models.ImageField(upload_to='datasource_icons', blank=True, null=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name

    def icon_path(self):
        return self.icon_file.url


class SubAgency(models.Model):
    """A sub-department of a DataSource. For example, the Lead department
       at the Department of Health. """
    datasource = models.ForeignKey(DataSource, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=200)
    contact_name = models.CharField(max_length=50, null=True,blank=True)
    contact_street = models.CharField(max_length=200, null=True,blank=True)
    contact_city = models.CharField(max_length=50, null=True,blank=True)
    contact_zip = models.CharField(max_length=10, null=True,blank=True)
    contact_phone = models.CharField(max_length=20, null=True,blank=True)

    class Meta:
        verbose_name_plural = 'sub agencies'

    def __str__(self):
        return u'%s (%s)' % (self.name, self.datasource.name)

class DataValue(models.Model):
    datacolumn = models.ForeignKey('dictionary.DataColumn', on_delete=models.CASCADE)
    value = models.CharField(max_length=256)
    description = models.TextField(blank=True, null=True)
    count = models.IntegerField(null=True)

    def __str__(self):
        return self.value

class DataColumn(models.Model):
    dataset = models.ForeignKey('dictionary.DataSet', on_delete=models.CASCADE)
    order = models.IntegerField(null=True, blank=True)
    hide = models.BooleanField(default=False)
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    column_type = models.CharField(max_length=100, null=True)
    max_value = models.CharField(max_length=128, blank=True, null=True, help_text='Max value of Integers or Dates')
    min_value = models.CharField(max_length=128, blank=True, null=True, help_text='Min value of Integers of Dates')
    column_allow_null = models.BooleanField(default=False)
    column_allow_blank = models.BooleanField(default=False)
    column_max_length = models.IntegerField(blank=True, null=True)

    @property
    def datavalues(self):
        return DataValue.objects.filter(datacolumn=self).order_by('value')

    def save(self, *args, **kwargs):
        if self.name == 'individualdatarow_ptr':
           self.name = 'individualdatarow_ptr_id'
        if self.name == 'peripheraldatarow_ptr':
           self.name = 'peripheraldatarow_ptr_id'
        super(DataColumn, self).save(*args, **kwargs)

    def __str__(self):
        return self.name


class DataSet(models.Model):
    "An individual set of data provided by a DataSource"
    sub_agency = models.ForeignKey(SubAgency, on_delete=models.CASCADE, null=True,blank=True)
    model_name = models.CharField(max_length=200)
    user_friendly_name = models.CharField(max_length=200,null=True,blank=True)
    description = models.TextField(blank=True)
    index_dimension = models.CharField(max_length=256, blank=True, null=True)
    min_dimension_value = models.CharField(max_length=256, blank=True, null=True)
    max_dimension_value = models.CharField(max_length=256, blank=True, null=True)
    last_received = models.DateField(blank=True,null=True)
    last_update = models.DateField(blank=True,null=True)
    next_update = models.DateField(blank=True,null=True)
    number_of_rows = models.IntegerField(null=True, blank=True)
    last_refreshed = models.DateTimeField(null=True, blank=True)

    template_name = models.CharField(
        _('template name'),
        default='content.html',
        max_length=70,
        blank=True,
        help_text=_(
            'Example: “flatpages/contact_page.html”. If this isn’t provided, '
            'the system will use “flatpages/default.html”.'
        ),
    )


    FREQUENCY_CHOICES = (
        ('INTERMITTENT', 'Intermittent'),
        ('ANNUALLY', 'Annually'),
        ('BIANNUALLY', 'Bi-Annually'),
        ('QUARTERLY', 'Quarterly'),
        ('MONTHLY', 'Monthly'),
        ('WEEKLY', 'Weekly'),
        ('DAILY', 'Daily'),
    )
    update_frequency = models.CharField(max_length=12, choices=FREQUENCY_CHOICES, null=True,db_index=True, blank=True)

    
    @property
    def datacolumns(self):
        return DataColumn.objects.filter(dataset=self).order_by('order')


    def __str__(self):
        if self.user_friendly_name:
           return u'%s' % (self.user_friendly_name)
        else:
           return u'%s' % (self.model_name)

class Group(models.Model):
    name = models.CharField(max_length=200)
    dataset = models.ManyToManyField(DataSet)
    order = models.IntegerField(null=True)
    
    class Meta:
        ordering = ('name',)

    def __str__(self):
        return self.name



