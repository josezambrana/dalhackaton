# -*- coding: utf-8 -*-
import logging

from django.views.generic.detail import SingleObjectMixin
from django.utils.translation import ugettext_lazy as _
from django.shortcuts import get_object_or_404, redirect

from common.views import ActionView
from common.views import CreateView
from common.views import DetailView
from common.views import ListView
from common.views import LoginRequiredMixin

from educacion.models import Course
from educacion.forms import CourseForm
from educacion.models import Program
from educacion.forms import ProgramForm


logger = logging.getLogger('project.simple')


class WithOwnerMixin(object):
    """
    Mixin para las vistas create
    """

    def get_form_kwargs(self):
        """
        Retorna los parametros para el formulario.
        """
        kwargs = super(WithOwnerMixin, self).get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs


class CreateCourse(LoginRequiredMixin, WithOwnerMixin, CreateView):
    """
    Vista para crear un curso.
    """

    app_name = 'courses'
    view_name = 'course_create'

    model = Course
    form_class = CourseForm

    templates = {
        'html': 'page.course_create.html'
    }
    
    def get_form_kwargs(self):
        """
        Añade el programa al curso si este esta referenciado
        """
        kwargs = super(CreateCourse, self).get_form_kwargs()

        if 'program_slug' in self.kwargs:
            self.program = get_object_or_404(Program, slug=self.kwargs['program_slug'])
            kwargs['program'] = self.program
        
        return kwargs


class DetailCourse(DetailView):
    """
    Muestra los detalles de un curso.
    """

    app_name = 'courses'
    view_name = 'course_detail'

    model = Course

    templates = {
        'html': 'page.course_detail.html'
    }
    

class ListCourse(ListView):
    """
    Muestra la lista de cursos registrados en el sistema
    """

    app_name = 'courses'
    view_name = 'course_detail'
    paginate_by = 10

    model = Course

    templates = {
        'html': 'page.course_list.html'
    }


class EnrollView(LoginRequiredMixin, ActionView, SingleObjectMixin):
    """
    Inscribe un usuario dentro de un curso.
    """
    confirm_message = _(u'Deseas inscribirte en este curso?')
    confirm = False
    
    success_message = _(u'En hora buena, te inscribiste')
    fail_message = _(u'Hubo un problema, no se pudo inscribir')
    show_success_message = False
    show_fail_message = True
   
    def get_object(self):
        """
        Retorna el objeto
        """

        self.object = get_object_or_404(Course, pk=self.kwargs['pk'])
        return self.object

    def action(self, request, direction=None, **kwargs):
        """
        Ejecuta la acción
        """

        self.object = self.get_object()

        if not self.object.is_enrolled(request.user):
            self.object.enrolled.add(request.user)
            return True
        
        self.fail_message = _(u'Ya estas inscrito')
        return False


class CreateProgram(LoginRequiredMixin, WithOwnerMixin, CreateView):
    """
    Vista para mostrar el formulario y crear un programa de estudios.
    """

    app_name = 'programs'
    view_name = 'program_create'
    model = Program
    form_class = ProgramForm

    templates = {
        'html': 'page.program_create.html'
    }


class DetailProgram(DetailView):
    """
    Muestra los detalles de un programa
    """

    app_name = 'programs'
    view_name = 'program_detail'
    
    model = Program
    
    templates = {
        'html': 'page.program_detail.html'
    }

    
class CreateLesson(LoginRequiredMixin, CreateView):
    """
    Vista para crear una lección.
    """

    app_name = 'lessons'
    view_name = 'lesson_create'

    model = Lesson
    form_class = LessonForm

    templates = {
        'html': 'page.lesson_create.html'
    }
    

