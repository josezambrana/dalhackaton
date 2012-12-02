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
from educacion.models import Program
from educacion.models import Lesson
from educacion.models import Resource
from educacion.models import Exam
from educacion.models import Question
from educacion.models import Option

from educacion.forms import CourseForm
from educacion.forms import ProgramForm
from educacion.forms import LessonForm
from educacion.forms import ResourceForm
from educacion.forms import ExamForm
from educacion.forms import QuestionForm
from educacion.forms import OptionForm


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

    
class CreateLesson(LoginRequiredMixin, WithOwnerMixin, CreateView):
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
    template_object = 'obj.lesson.html'
    

class CreateResource(LoginRequiredMixin, CreateView):
    """
    Vista para cargar un recurso.
    """
    
    app_name = 'resources'
    view_name = 'resource_create'
    
    model = Resource
    form_class = ResourceForm

    templates = {
        'html': 'page.resource_create.html'
    }

    template_object = 'obj.resource.html'

    def get_context_data(self, *args, **kwargs):
        logger.info('***** get_context_data')
        context = super(CreateResource, self).get_context_data(*args, **kwargs)
        
        if self.get_format() == 'json':
            logger.info("    * content_type?: %s " % self.object.type)
            context['type'] = self.object.type
        
        return context
    

class CreateExam(LoginRequiredMixin, CreateView):
    """
    Vista para cargar un Examen.
    """
    
    app_name = 'exams'
    view_name = 'exam_create'
    
    model = Exam
    form_class = ExamForm

    templates = {
        'html': 'page.exam_create.html'
    }


class CreateQuestion(LoginRequiredMixin, CreateView):
    """
    Vista para cargar una pregunta.
    """
    
    app_name = 'questions'
    view_name = 'question_create'
    
    model = Question
    form_class = QuestionForm

    templates = {
        'html': 'page.question_create.html'
    }


class CreateOption(LoginRequiredMixin, CreateView):
    """
    Vista para cargar una opcion para una pregunta.
    """
    
    app_name = 'options'
    view_name = 'option_create'
    
    model = Option
    form_class = OptionForm

    templates = {
        'html': 'page.option_create.html'
    }
    
