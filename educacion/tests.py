# -*- coding: utf-8 -*-
import logging

from django.contrib.auth.models import User
from django.test import TestCase
from django.core.urlresolvers import reverse

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
        
