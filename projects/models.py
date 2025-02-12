from django.db import models
from users.models import Profile
import uuid

# Create your models here.

# By default in Django, inheriting models automatically applies id. 
class Project(models.Model):
    # Projects to user is many to one relationship, use foreign key to get them to communicate with each other.
    # Won't let migration run unless have null=True.
    owner = models.ForeignKey(Profile, null=True, blank=True, on_delete=models.CASCADE)
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
    # Orders in order of list in ordering. 
    class Meta:
        ordering = ['-vote_ratio', '-vote_total', 'title']

    # Fixes issue where if user deletes featured image, would break page since not found. 
    @property
    def imageURL(self):
        try:
            # If image doesn't exist, move to next.
            url = self.featured_image.url
        except:
            url = ''
        return url

    @property
    def reviewers(self):
        # Grab all reviewers. Instead of getting queryset of all, it will be list of ids, flat=True converting it into a true list. 
        queryset = self.review_set.all().values_list('owner__id', flat=True)
        return queryset

    # Property decorator allows it to run without (), able to run it as a method. 
    @property
    def getVoteCount(self):
        # Grab all reviews
        reviews = self.review_set.all()
        # Filter to get all upvotes.
        upVotes = reviews.filter(value='up').count()
        totalVotes = reviews.count()

        ratio = (upVotes/totalVotes) * 100

        # Update Project model.
        self.vote_total = totalVotes
        self.vote_ratio = ratio

        self.save()

class Review(models.Model):

    VOTE_TYPE = (
        ('up', 'Up Vote'),
        ('down', 'Down Vote'),
    )

    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    # One to many relationship
    owner = models.ForeignKey(Profile, on_delete=models.CASCADE, null=True)
    body = models.TextField(null=True, blank=True)
    value = models.CharField(max_length=200, choices=VOTE_TYPE)
    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)

    class Meta:
        # Creating a list and set two attributes to bind together. This way, no instance of review can have same owner and same project.
        # Prevents someone from leaving multiple reviews for same project. 
        unique_together = [['owner', 'project']]

    def __str__(self):
        return self.value

class Tag(models.Model):
    name = models.CharField(max_length=200)
    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)

    def __str__(self):
        return self.name