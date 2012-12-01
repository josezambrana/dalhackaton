# -*- coding: utf-8 -*-
import logging
from django.db import models
from django.utils.translation import ugettext_lazy as _

from common.models import Content


logger = logging.getLogger('project.simple')

class Course(Content):
    """
    Formulario para crear cursos
    """
    
    #: Descripción del curso
    description = models.TextField(_(u'Descripción'))


    class Meta:
        verbose_name = _(u'Curso')
        verbose_name_plural = _(u'Cursos')
    
    def save(self, *args, **kwargs):
        logger.info("    * Course.content.save")
        obj = super(Course, self).save(*args, **kwargs)
        return obj

    @models.permalink
    def get_absolute_url(self):
        logger.info('**** get_absolute_url: %s ')
        logger.info('   * slug: %s ' % self.slug)
        logger.info('   * name: %s ' % self.name)
        return ('educacion_courseshow', [self.slug])
