# -*- coding: utf-8 -*-
import logging

from django.views.generic.detail import SingleObjectMixin
from django.views.generic.list import MultipleObjectMixin
from django.utils.translation import ugettext_lazy as _
from django.shortcuts import get_object_or_404, redirect
from django.core.paginator import Paginator, InvalidPage
from django.http import Http404

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
from educacion.models import Selection

from educacion.forms import CourseForm
from educacion.forms import ProgramForm
from educacion.forms import LessonForm
from educacion.forms import ResourceForm
from educacion.forms import ExamForm
from educacion.forms import QuestionForm
from educacion.forms import OptionForm
from educacion.forms import SelectionForm


logger = logging.getLogger('project.simple')


class RelatedListMixin(object):
    """
    Agrega una lista de objetos relacionados
    """

    model_related = None
    paginate_by = 10

    def get_filters(self):
        raise NotImplementedError

    def related_queryset(self):
        return self.model_related.objects.filter(**self.get_filters())

    def paginate_queryset(self, queryset, page_size):
        """
        Paginate the queryset, if needed.
        """
        paginator = Paginator(queryset, page_size, allow_empty_first_page=True)
        page = self.kwargs.get('page') or self.request.GET.get('page') or 1

        try:
            page_number = int(page)
        except ValueError:
            if page == 'last':
                page_number = paginator.num_pages
            else:
                raise Http404(_(u"Page is not 'last', nor can it be converted to an int."))
        try:
            page = paginator.page(page_number)
            return (paginator, page, page.object_list, page.has_other_pages())
        except InvalidPage:
            raise Http404(_(u'Invalid page (%(page_number)s)') % {
                                'page_number': page_number
            })

    def get_context_data(self, **kwargs):
        context = DetailView.get_context_data(self, **kwargs)
        queryset = self.related_queryset()
        paginator, page, queryset, is_paginated = self.paginate_queryset(queryset, self.paginate_by)
        context.update({
            'paginator': paginator,
            'page_obj': page,
            'is_paginated': is_paginated,
            'object_list': queryset
        })
        return context


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


class DetailCourse(RelatedListMixin, DetailView):
    """
    Muestra los detalles de un curso.
    """

    app_name = 'courses'
    view_name = 'course_detail'

    model = Course
    model_related = Lesson
    
    templates = {
        'html': 'page.course_detail.html'
    }
    
    def get_filters(self):
        return dict(course__pk=self.object.id)

    def related_queryset(self):
        return self.model_related.objects.filter(**self.get_filters()).order_by('created_at')


class DetailLesson(RelatedListMixin, DetailView):
    """
    Muestra los detalles de una lección.
    """
    
    app_name = 'lessons'
    view_name = 'lesson_detail'
    
    model = Lesson
    model_related = Resource
    
    templates = {
        'html': 'page.lesson_detail.html'
    }
    
    def get_filters(self):
        return dict(lesson__pk=self.object.id)


class ListCourse(ListView):
    """
    Muestra la lista de cursos registrados en el sistema
    """

    app_name = 'courses'
    view_name = 'course_list'
    paginate_by = 10

    model = Course

    templates = {
        'html': 'page.course_list.html'
    }

class HomeView(ListCourse):
    """
    Muestra la página de inicio.
    """
    
    view_name = 'home'
    templates = {
        'html': 'page.home.html'
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


class UnrollView(LoginRequiredMixin, ActionView, SingleObjectMixin):
    """
    Inscribe un usuario dentro de un curso.
    """
    confirm_message = _(u'Deseas desinscribirte de este curso?')
    confirm = True
    
    success_message = _(u'Te perdimos, vamos a extrañarte')
    fail_message = _(u'Hubo un problema, no se pudo desinscribir')
    show_success_message = True
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

        if self.object.is_enrolled(request.user):
            self.object.enrolled.remove(request.user)
            return True
        
        self.fail_message = _(u'No estabas inscrito')
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


class DetailProgram(RelatedListMixin, DetailView):
    """
    Muestra los detalles de un programa
    """

    app_name = 'programs'
    view_name = 'program_detail'
    
    model = Program
    model_related = Course
    
    templates = {
        'html': 'page.program_detail.html'
    }
    
    def get_filters(self):
        return dict(program__pk=self.object.id)


class ListProgram(ListView):
    """
    Muestra la lista de programas registrados en el sistema.
    """
    
    app_name = 'programs'
    view_name = 'program_list'
    paginate_by = 10

    model = Program

    templates = {
        'html': 'page.program_list.html'
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
    

class CreateResource(LoginRequiredMixin, WithOwnerMixin, CreateView):
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
        context = super(CreateResource, self).get_context_data(*args, **kwargs)
        
        if self.get_format() == 'json' and self.object is not None:
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
    template_object = 'obj.exam.html'

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
    template_object = 'obj.question.html'


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
    
    template_object = 'obj.option.html'


class CreateSelection(LoginRequiredMixin, WithOwnerMixin,CreateView):
    """
    Vista para seleccionar una opción.
    """

    app_name = 'options'
    view_name = 'selection_create'

    model = Selection
    form_class = SelectionForm

    templates = {
        'html': 'page.selection_create.html'
    }

    template_object = 'obj.selection.html'
