"""
This module provides custom profile  model.
"""

from django.db import models

from authentication.models import UserProfile


class CustomProfile(models.Model):
    """
    Attributes:
        bio(str):User's bio,
        hobby(str):Describe what user likes,
        birthday(date):User's birthday

    """
    user = models.ForeignKey(UserProfile, on_delete=True, related_name="profile")
    bio = models.CharField(max_length=1000, blank=True)
    hobby = models.CharField(max_length=50, blank=True)
    birthday = models.DateField(null=True)

    def update(self, bio=None, hobby=None, birthday=None):
        """
        Method which changes an information except email as it is an id of an user.
        """
        if bio:
            self.bio = bio
        if hobby:
            self.hobby = hobby
        if birthday:
            self.birthday = birthday
        self.save()

    @staticmethod
    def get_by_user(user):
        """
        Args:
            user: The first parameter.
        Returns:
            CustomProfile object if database contain user with id, None otherwise.

        """

        try:
            return CustomProfile.objects.get(user=user)

        except CustomProfile.DoesNotExist:
            return None
