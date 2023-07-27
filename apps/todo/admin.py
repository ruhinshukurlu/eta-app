"""
Admin registration
"""
from django.contrib import admin

from .models import Expectation, Project

admin.site.register(Expectation)
admin.site.register(Project)
