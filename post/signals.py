from django.db.models.signals import pre_save
from django.dispatch import receiver
from .models import Post
from django.utils.text import slugify

@receiver(pre_save, sender=Post)
def pre_save_hanlder(sender, instance, **kwargs):
    instance.slug = slugify(instance.title)
    if len(instance.content) >= 200:
          instance.excerpt = instance.content[0:200]
    else:
        instance.excerpt = instance.content

    return instance
         
      