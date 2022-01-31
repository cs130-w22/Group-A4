from django.db import models
from django.contrib.auth.models import User # for extending django User Model
from django.db.models.signals import post_save
from django.dispatch import receiver


"""
UserProfile extends the functionality and stores extra information in addition to default
    Django User Model.
"""
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(max_length=500, blank=True, default="Edit this to be your bio.")
    location = models.CharField(max_length=30, blank=True)
    age = models.IntegerField(default=0)

    def __str__(self):
        """
        return user's name
        """
        return str(self.user) + "-profile"

@receiver(post_save, sender=User)
def create_uesr_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.userprofile.save()
