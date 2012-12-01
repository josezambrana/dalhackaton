# -*- coding: utf-8 -*-
from django import forms
from educacion.models import Course


class CourseForm(forms.ModelForm):
    """
    Formulario para crear cursos
    """

    class Meta:
        model = Course 
        fields = ('name', 'description')

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')
        super(CourseForm, self).__init__(*args, **kwargs)

    def save(self):
        course = super(CourseForm, self).save(commit=False)
        
        # Datos del autor
        course.user = self.user
        course.username = self.user.username

        course.save()

        return course
