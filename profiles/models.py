# from django.contrib.auth import get_user_model
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

from random import choice
from os.path import join as path_join
from os import listdir
from os.path import isfile

import accounts.models


# User = get_user_model()

def upload_update_image(instance, filename):
    return "avatar/{user}/{filename}".format(user=instance.user, filename=filename)


def random_img():
    dir_path = 'static/random_avatar'
    files = [content for content in listdir(dir_path) if isfile(path_join(dir_path, content))]
    print(path_join(dir_path, choice(files)))
    return path_join(dir_path, choice(files))


class UserProfile(models.Model):
    user = models.OneToOneField('accounts.User', on_delete=models.CASCADE, primary_key=True, related_name='profile')
    # profile_image = models.FileField(upload_to=upload_update_image, null=True, blank=True, default=random_img)
    profile_image = models.FileField(upload_to=upload_update_image, null=True, blank=True, default=None)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.user.username)
        # return str(self.pk)

    # def get_image_uri(self):
    #     if self.profile_image:
    #         # print(self.profile_image.url)
    #         # print(type(self.profile_image.url))
    #         url_img = self.profile_image
    #         url_img = url_img[6:]
    #         print("Striped URL", url_img)
    #     return url_img


@receiver(post_save, sender=accounts.models.User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)


@receiver(post_save, sender=accounts.models.User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()
