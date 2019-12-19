from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import User
from simple_history.models import HistoricalRecords
from django.utils.text import slugify

class Page(models.Model):
    project = models.ForeignKey('project.Project', on_delete=models.PROTECT, null=True, blank=True)
    number = models.PositiveIntegerField()
    title = models.CharField(max_length=100)
    content = models.TextField(blank=True, help_text="HTML CODE")



    subheading = models.CharField(max_length=300, null=True, blank=True)
    text = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='datastory_page_images',blank=True)
    embed = models.TextField(blank=True, help_text="embed code")
    notes = models.TextField(blank=True,  help_text="This field is for internal use only.")
    history = HistoricalRecords()


    @property
    def next_page(self):
        next_pages = Page.objects.filter(data_story=self.data_story,
                                     number__gt=self.number).order_by('number')
        if len(next_pages) == 0:
            return None
        else:
            return next_pages[0]

    @property
    def previous_page(self):
        next_pages = Page.objects.filter(data_story=self.data_story,
                                     number__lt=self.number).order_by('-number')
        if len(next_pages) == 0:
            return None
        else:
            return next_pages[0]

    def __str__(self):
           return "%s: Page %s" % (self.project, self.number)



class Project(models.Model):

    title = models.CharField(max_length=100)
    short_title = models.CharField(max_length=80) # to display in lists, etc
    slug = models.SlugField(_('slug'),unique=True, blank=True)
    description = models.TextField(_('description'),blank=True, null=True)
    image = models.ImageField(upload_to='images', blank=True, null=True)
    publish = models.BooleanField(default = True)
    data_sources = models.ForeignKey('dictionary.DataSource', on_delete=models.CASCADE)
    created_by = models.ForeignKey(User, on_delete=models.PROTECT, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    keywords = models.ManyToManyField('dictionary.Keyword',blank=True)
    related_project = models.ManyToManyField("self", blank=True)
    template_name = models.CharField(
        _('template name'),
        max_length=70,
        blank=True,
        help_text=_(
            'Example: “flatpages/contact_page.html”. If this isn’t provided, '
            'the system will use “flatpages/default.html”.'
        ),
    )
    
    history = HistoricalRecords()

    @property
    def pages(self):
        return Page.objects.filter(project=self).order_by('number')


    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        self.slug = slugify(self.short_title)
        super(Project, self).save(*args, **kwargs)



