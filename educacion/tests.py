# -*- coding: utf-8 -*-
import logging
from os import path

from django.contrib.auth.models import User
from django.test import TestCase
from django.core.urlresolvers import reverse
from django.utils import simplejson

from common.tests import TestBase

from educacion.models import Course

logger = logging.getLogger('project.simple')


class CourseTest(TestBase):
    """
    Tests para los cursos.
    """
    fixtures = ['users', 'courses', 'programs']

    def setUp(self):
        """
        Se añade valores.
        """
        super(CourseTest, self).setUp()

        self.data = {
            'name': 'Como construir una bomba atomica',
            'description': 'Este curso permite introducirte en la creación de una bomba atómica',
        }
    
    def test_show_course(self):
        """
        Como visitante debo ser capaz de ver la información de un curso.
        """

        response = self.client_get('educacion_courseshow', args=['fisica-nuclear-como-para-tontos'])
        assert response.status_code == 200

    def test_create_course(self):
        """
        Como usuario debo ser capaz de crear cursos.
        """
        
        # Verificamos que los usuarios visitantes no puedan ingresar al formulario
        self.assertLoginRequired('educacion_coursecreate')

        self.login('admin', 'fakepass')

        # Verificamos que se muestre la vista de creacion
        response = self.client_get('educacion_coursecreate')
        assert response.status_code == 200
        
        # Verificamos que se pueda crea un nuevo curso.
        response = self.client_post('educacion_coursecreate', data=self.data)
        self.assertRedirects(response, reverse('educacion_courseshow', args=['como-construir-una-bomba-atomica']), host=self.server_name)

        # Se verifica que se pueda crear un nuevo curso dentro de un programa
        data = {
            'name': 'Otra cosa',
            'description': 'cosa'
        }
        response = self.client_post('educacion_program_coursecreate', args=['tecnico-en-agronomia'], data=data)
        self.assertRedirects(response, reverse('educacion_courseshow', args=['otra-cosa']), host=self.server_name)
        course = Course.objects.get(slug='otra-cosa')
        assert course.program is not None
        logger.info('Program: %s ' % course.program.name)
    
    def test_get_course_index(self):
        """
        Como usuario debo ser capaz de ver la lista de cursos registrados.
        """

        response = self.client_get('educacion_courselist')
        assert response.status_code == 200

    def test_signin_course(self):
        """
        Como usuario debo ser capaz de inscribirme en un curso.
        """
        
        course = Course.objects.get(pk=1)
        
        # Verifica que el usuario esta loguedo
        response = self.client_post_ajax('educacion_courseenroll', args=[course.id])
        assert not response['success']
        
        self.login('zero', 'fakepass')
        user = User.objects.get(username='zero')
         
        # Verificar que se puede inscribir.
        response = self.client_post_ajax('educacion_courseenroll', args=[course.id])
        assert response['success']
        
        course = self._update(course) 
        assert course.is_enrolled(user)
        
        # Si ya esta registrado mostrar error
        response = self.client_post_ajax('educacion_courseenroll', args=[course.id])
        assert not response['success']


class ProgramTest(TestBase):
    """
    Verifica el funcionamiento del gestor de programas.
    """
    
    fixtures = ['courses', 'programs', 'users']
    
    def setUp(self):
        super(ProgramTest, self).setUp()
        self.data = {
            'name': 'Ciudadano modelo',
            'description': 'Programa para formar al conjunto de la ciudadania en los conceptos básicos de seguridad y respeto de las leyes'
        }
    
    def test_create_program(self):
        """
        Como usuario debo ser capaz de crear un programa.
        """

        # Se verifica que los usuarios visitantes no puedan ingresar al formulario
        self.assertLoginRequired('educacion_programcreate')
        
        self.login('admin', 'fakepass')

        # Se verifica que se pueda acceder al formulario.
        response = self.client_get('educacion_programcreate')
        assert response.status_code == 200

        # Se verifica que se pueda pueda crear un nuevo programa
        response = self.client_post('educacion_programcreate', data=self.data)
        self.assertRedirects(response, reverse('educacion_programshow', args=['ciudadano-modelo']), host=self.server_name)
    
    def test_show_program(self):
        """
        Verifica que muestra un programa.
        """
        
        # Se verifica que el usuario pueda ver los detalles de un programa
        response = self.client_get('educacion_programshow', args=['tecnico-en-agronomia']) 
        assert response.status_code == 200


class LessonTest(TestBase):
    """
    Verifica el funcionamiento del gestor de lecciones.
    """
    
    fixtures = ['courses', 'programs', 'users']
    
    def setUp(self):
        super(LessonTest, self).setUp()
        self.data = {
            'name': 'Leccion 1',
            'description': 'Introduccion',
            'orden': 1,
            'course': 1,
        }
    
    def test_create_lesson(self):
        """
        Como usuario debo ser capaz de crear una lección.
        """

        # Se verifica que los usuarios visitantes no puedan ingresar al formulario
        self.assertLoginRequired('educacion_lessoncreate')
        
        self.login('admin', 'fakepass')

        # Se verifica que se pueda acceder al formulario.
        response = self.client_get('educacion_lessoncreate')
        assert response.status_code == 200
        
        # Se verifica que se pueda pueda crear un nuevo programa
        response = self.client_post_ajax('educacion_lessoncreate', data=self.data)
        assert response['success']


STATIC_PATH = path.join(path.abspath(path.dirname(__file__)), 'static')
NOT_SUPPORTED_PATH = path.join(STATIC_PATH, 'file.txt')
DOC_PATH = path.join(STATIC_PATH, 'document.pdf')
VIDEO_PATH = path.join(STATIC_PATH, 'video.jpg')

class ResourceTest(TestBase):
    """
    Verifica el funcionamiento del gestor de recursos.
    """
    
    fixtures = ['courses', 'programs', 'users', 'lessons']
    
    def setUp(self):
        super(ResourceTest, self).setUp()
        self.data = {
            "file": open(DOC_PATH),
            "lesson": 1,
        }
    
    def test_create_resource(self):
        """
        Como usuario debo ser capaz de cargar un recurso a una lección.
        """

        # Se verifica que los usuarios visitantes no puedan ingresar al formulario
        self.assertLoginRequired('educacion_resourcecreate')
        
        self.login('admin', 'fakepass')

        # Se verifica que se pueda acceder al formulario.
        response = self.client_get('educacion_resourcecreate')
        assert response.status_code == 200
        
        # Se verifica que se pueda pueda crear un nuevo programa
        response = self.client_post('educacion_resourcecreate', args=['json'], data=self.data)
        response_json = simplejson.loads(response.content)
        assert response.status_code == 200
        assert response_json['success']
        assert 'type' in response_json
        assert response_json['type'] == 'DOC'


class ExamTest(TestBase):
    """
    Verifica el funcionamiento de los examenes
    """
    
    fixtures = ['courses', 'programs', 'users', 'lessons', 'resources']
    
    def setUp(self):
        super(ExamTest, self).setUp()
        self.data = {
            "resource": 2,
            "max_value": 100,
            "seconds": 10
        }
    
    def test_create_exam(self):
        """
        Como usuario debo ser capaz de crear un examen para un recurso.
        """
        
        # Se verifica que los usuarios visitantes no puedan ingresar al formulario
        self.assertLoginRequired('educacion_examcreate')
        
        self.login('admin', 'fakepass')

        # Se verifica que se pueda acceder al formulario.
        response = self.client_get('educacion_examcreate')
        assert response.status_code == 200
        
        # Se verifica que se pueda pueda crear un nuevo programa
        response = self.client_post_ajax('educacion_examcreate', data=self.data)
        assert response['success']
        logger.info(' response: %s ' % response)


class QuestionTest(TestBase):
    """
    Verifica el funcionamiento del gestor de preguntas.
    """
    
    fixtures = ['courses', 'programs', 'users', 'lessons', 'resources', 'exams']
    
    def setUp(self):
        super(QuestionTest, self).setUp()
        self.data = {
            "question": "Como se hace esto?",
            "percent": 50,
            "exam": 1,
            "reply": "facil, como si nada",
            "explanation": "solo tienes que mirar y esperar",
            "weight": 10
        }
    
    def test_create_question(self):
        """
        Como usuario debo ser capaz de crear una pregunta en un examen.
        """
        
        # Se verifica que los usuarios visitantes no puedan ingresar al formulario
        self.assertLoginRequired('educacion_questioncreate')
        
        self.login('admin', 'fakepass')

        # Se verifica que se pueda acceder al formulario.
        response = self.client_get('educacion_questioncreate')
        assert response.status_code == 200
        
        # Se verifica que se pueda pueda crear una nueva pregunta
        response = self.client_post_ajax('educacion_questioncreate', data=self.data)
        assert response['success']
        logger.info(' response: %s ' % response)


class OptionTest(TestBase):
    """
    Verifica el funcionamiento del gestor de opciones
    """
    
    fixtures = ['courses', 'programs', 'users', 'lessons', 'resources', 'exams', 'questions']
    
    def setUp(self):
        super(OptionTest, self).setUp()
        self.data = {
            "value": "A",
            "correct": True,
            "question": "1",
            "weight": 1
        }
    
    def test_create_option(self):
        """
        Como usuario debo ser capaz de crear la opción de respuesta para una pregunta.
        """
        
        # Se verifica que los usuarios visitantes no puedan ingresar al formulario
        self.assertLoginRequired('educacion_optioncreate')
        
        self.login('admin', 'fakepass')
        
        # Se verifica que se pueda acceder al formulario.
        response = self.client_get('educacion_optioncreate')
        assert response.status_code == 200
        
        # Se verifica que se pueda pueda crear una opcion para una pregunta
        response = self.client_post_ajax('educacion_optioncreate', data=self.data)
        assert response['success']
        logger.info(' response: %s ' % response)


