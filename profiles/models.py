# from django.contrib.auth import get_user_model
from django.conf import settings
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

from random import choice
from os.path import join as path_join
from os import listdir
from urllib.parse import urljoin
from os.path import isfile

import accounts.models


# User = get_user_model()

def upload_update_image(instance, filename):
    return "avatar/{user}/{filename}".format(user=instance.user, filename=filename)


def random_img():
    dir_path = '/static/random_avatar'
    files = [content for content in listdir(dir_path) if isfile(urljoin(dir_path, content))]
    print(urljoin(dir_path, choice(files)))
    # print("Path" + dir_path + "/" + choice(files))
    # return path_join(dir_path, choice(files))
    return urljoin(dir_path, choice(files))


class UserProfile(models.Model):
    user = models.OneToOneField('accounts.User', on_delete=models.CASCADE, primary_key=True, related_name='profile')
    # profile_image = models.FileField(upload_to=upload_update_image, null=True, blank=True, )
    profile_image = models.ImageField(upload_to=upload_update_image, null=True, blank=True, default='random_avatar/avatar4.png')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.user.email)
        # return str(self.pk)

    def filename(self):
        return path_join.basename(self.profile_image.name)

    # @property
    # def default_picture(self):
    #     if self.profile_image:
    #         # return "{}{}".format(settings.MEDIA_URL, self.dp)
    #         return "avatar/{user}/{filename}".format(user=self.user, filename=self.filename)
    #     return 'static/random_avatar/avatar4.png'


@receiver(post_save, sender=accounts.models.User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)
        # UserProfile.default_picture()


@receiver(post_save, sender=accounts.models.User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()
