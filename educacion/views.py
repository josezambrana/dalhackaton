# -*- coding: utf-8 -*-
import logging
from common.views import CreateView
from common.views import DetailView
from common.views import ListView
from common.views import LoginRequiredMixin

from educacion.models import Course
from educacion.forms import CourseForm

logger = logging.getLogger('project.simple')


class CreateCourse(LoginRequiredMixin, CreateView):
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
        Retorna los parametros para el formulario.
        """
        
        logger.info('**** get_form_kwargs')

        kwargs = super(CreateCourse, self).get_form_kwargs()
        kwargs['user'] = self.request.user
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
