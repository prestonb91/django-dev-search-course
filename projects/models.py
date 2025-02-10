from django.db import models
from users.models import Profile
import uuid

# Create your models here.



# By default in Django, inheriting models automatically applies id. 
class Project(models.Model):
    # Projects to user is many to one relationship, use foreign key to get them to communicate with each other.
    # Won't let migration run unless have null=True.
    owner = models.ForeignKey(Profile, null=True, blank=True, on_delete=models.SET_NULL)
    # Title by default will be required. 
    title = models.CharField(max_length=200)
    # null=True means this data can be created without an initial value. 
    description = models.TextField(null=True, blank=True)
    # Django automatically picks up "default.jpg" if folder structure follows convention of static/images/file_name.
    featured_image = models.ImageField(null=True, blank=True, default="default.jpg")
    # Blank true means allowed to submit a form with value being empty. 
    demo_link = models.CharField(max_length=2000, null=True, blank=True)
    source_link = models.CharField(max_length=2000, null=True, blank=True)
    # With no quotations, requires function to be above, but with quotations hoists the function to the function.
    tags = models.ManyToManyField('Tag', blank=True)
    vote_total = models.IntegerField(default=0, null=True, blank=True)
    vote_ratio = models.IntegerField(default=0, null=True, blank=True)
    # auto_now_add automatically generates a timestamp when created. 
    created = models.DateTimeField(auto_now_add=True)
    # Overriding default id with uuid as the new primary key.
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)

    # Python function to refer to Project class and return the title instead of the object uuid.
    def __str__(self):
        return self.title
    
    # Order the projects model. Adding "-" changes from ascending to descending order. 
    class Meta:
        ordering = ['-created']

class Review(models.Model):

    VOTE_TYPE = (
        ('up', 'Up Vote'),
        ('down', 'Down Vote'),
    )

    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    # owner
    body = models.TextField(null=True, blank=True)
    value = models.CharField(max_length=200, choices=VOTE_TYPE)
    created = models.DateTimeField()
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)

    def __str__(self):
        return self.value

class Tag(models.Model):
    name = models.CharField(max_length=200)
    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)

    def __str__(self):
        return self.name