from django.db import models
from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.db.models.signals import pre_save
from django.utils.text import slugify
from django.utils import timezone

from .utils import get_read_time
from comments.models import Comment

# Create your models here.
class PostManager(models.Manager):
    def active(self, *args, **kwargs):
        return super(PostManager, self).filter(draft=False).filter(publish__lte=timezone.now())

class Post(models.Model):
    STATUS = (
        (0, "Draft"),
        (1, "Publish"),
        (2, "Delete"),
    )
    title = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(max_length=200, unique=True)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='author', default=1, on_delete=models.PROTECT)
    updated_on = models.DateTimeField(auto_now=True)
    created_on = models.DateField(auto_now=True)
    content = models.TextField()
     # meta description for SEO benefits
    metades = models.CharField(default="new post", max_length=50)
    status = models.IntegerField(choices=STATUS, default=0)

    class Meta:
        ordering = ['-created_on', 'author']

    def __str__(self):
        return self.title

    def __unicode__(self):
        return self.title

    @property
    def comments(self):
        instance = self
        qs = Comment.objects.filter_by_instance(instance)
        return qs

    @property
    def get_content_type(self):
        instance = self
        content_type = ContentType.objects.get_for_model(instance.__class__)
        return content_type


def create_slug(instance, new_slug=None):
    slug = slugify(instance.title)
    if new_slug is not None:
        slug = new_slug
    qs = Post.objects.filter(slug=slug).order_by("-id")
    exists = qs.exists()
    if exists:
        new_slug = "%s-%s" %(slug, qs.first().id)
        return create_slug(instance, new_slug=new_slug)
    return slug

def pre_save_post_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = create_slug(instance)

    if instance.content:
        html_string = instance.get_markdown()
        read_time_var = get_read_time(html_string)
        instance.read_time = read_time_var

pre_save.connect(pre_save_post_receiver, sender=Post)