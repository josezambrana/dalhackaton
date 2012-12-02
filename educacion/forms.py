# -*- coding: utf-8 -*-
from django import forms

from educacion.models import Course
from educacion.models import Program


class WithOwnerMixin(object):
    """
    Modelo abstracto para contenidos que tienen propietario
    """

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')
        super(WithOwnerMixin, self).__init__(*args, **kwargs)

    def save(self):
        obj = super(WithOwnerMixin, self).save(commit=False)
        
        # Datos del autor
        obj.user = self.user
        obj.username = self.user.username
        obj.save()
        
        return obj


class CourseForm(WithOwnerMixin, forms.ModelForm):
    """
    Formulario para crear cursos
    """

    class Meta:
        model = Course 
        fields = ('name', 'description')

    def __init__(self, *args, **kwargs):
        self.program = kwargs.pop('program', None)
        super(CourseForm, self).__init__(*args, **kwargs)

    def save(self):
        obj = super(CourseForm, self).save()
        
        obj.program = self.program
        obj.save()

        return obj


class ProgramForm(WithOwnerMixin, forms.ModelForm):
    """
    Formulario para gestionar Programas
    """

    class Meta:
        model = Program
        fields = ('name', 'description')


class LessonForm(forms.ModelForm):
    """
    Formulario para crear y editar Lecciones
    """
    
    class Meta:
        model = Lesson
        fields = ('description', 'orden', 'course')


class ResourceForm(forms.ModelForm):
    """
    Formulario para crear recursos para una lección.
    """

    class Meta:
        model = Resource
        fields = ('file', 'lesson')


class ExamForm(forms.ModelForm):
    """
    Formulario para crear pruebas dentro de un recurso.
    """

    class Meta:
        model = Exam
        fields = ('resource', 'max_value', 'seconds')

class QuestionForm(forms.ModelForm):
    """
    Formulario para crear preguntas.
    """
    
    class Meta:
        model = Question
        fields = ('question', 'percent', 'exam', 'reply', 'explanation', 'weight')

class OptionForm(forms.ModelForm):
    """
    Formulario para crear opciones de respuesta para una pregunta.
    """

    class Meta:
        model = Option
        fields = ('value', 'correct', 'weight', 'question')
