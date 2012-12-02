# -*- coding: utf-8 -*-
import logging

from django import template
from django.conf import settings


register = template.Library()


@register.filter(name="is_enrolled")
def is_rolled(user, course):
    """
    Verifica si un usuario esta inscrito en un curso
    """
    return course.is_enrolled(user)


