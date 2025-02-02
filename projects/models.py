from django.db import models

import uuid

# Create your models here.



# By default in Django, inheriting models automatically applies id. 
class Project(models.Model):
    # Title by default will be required. 
    title = models.CharField(max_length=200)
    # null=True means this data can be created without an initial value. 
    description = models.TextField(null=True, blank=True)
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