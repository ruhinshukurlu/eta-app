"""
Models for the system include Expectation, Project
"""

from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import gettext_lazy as _

User = get_user_model()  # retriving default User model


class Project(models.Model):
    name = models.CharField(_("Name"), max_length=100)

    def __str__(self):
        return self.name


class Expectation(models.Model):
    user = models.ForeignKey(User, verbose_name=_("User"), on_delete=models.CASCADE, related_name="expectations")
    project = models.ForeignKey(
        Project, verbose_name=_("Project"), on_delete=models.CASCADE, related_name="expectations"
    )
    issue = models.CharField(_("Issue"), max_length=100)

    created_at = models.DateTimeField(_("Created At"), auto_now=True)
    expected_at = models.DateTimeField(_("Expected At"))
    done_at = models.DateTimeField(_("Done At"), blank=True, null=True)

    def __str__(self):
        return self.user.username + self.project.name
