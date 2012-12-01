# -*- coding: utf-8 -*-
import logging

from django.test import TestCase
from common.tests import TestBase
from django.core.urlresolvers import reverse

logger = logging.getLogger('project.simple')


class CourseTest(TestBase):
    """
    Tests para los cursos.
    """
    fixtures = ['users', 'courses']

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
        
        # Verificamos que se pueda crea un nuevo usuario.
        response = self.client_post('educacion_coursecreate', data=self.data)
        logger.info('response.location: %s ' % response.status_code)
        self.assertRedirects(response, reverse('educacion_courseshow', args=['como-construir-una-bomba-atomica']), host=self.server_name)
    
    def test_get_course_index(self):
        """
        Como usuario debo ser capaz de ver la lista de cursos registrados.
        """

        response = self.client_get('educacion_courselist')
        assert response.status_code == 200
