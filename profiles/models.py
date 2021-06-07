from django.db import models
from django.contrib.auth.models import User
# Create your models here.
# Create your models here.
from django.db import models
import uuid
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save, post_delete
from posts.models import Follow

def user_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    return 'userprofile_{0}/{1}'.format(instance.userprofile.username, filename)



class profile(models.Model):
    userprofile=models.OneToOneField(User,on_delete=models.CASCADE)
    profileid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    profilepic= models.ImageField(upload_to=user_directory_path)
    bio=models.TextField()
    livesin=models.TextField()
    worksat=models.TextField()

    def get_absolute_url(self):
        return reverse('profile', args=[str(self.profileid)])

    def add_profile(sender, instance, *args, **kwargs):
        profileobj=profile.objects.create(userprofile=instance)
        profileobj.save()




post_save.connect(profile.add_profile, sender=User)