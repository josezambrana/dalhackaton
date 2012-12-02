# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Lesson'
        db.create_table('educacion_lesson', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('slug', self.gf('django.db.models.fields.SlugField')(max_length=50)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('updated_at', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('published_at', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('description', self.gf('django.db.models.fields.TextField')()),
            ('orden', self.gf('django.db.models.fields.IntegerField')()),
            ('course', self.gf('django.db.models.fields.related.ForeignKey')(related_name='Lessons', to=orm['educacion.Course'])),
        ))
        db.send_create_signal('educacion', ['Lesson'])

        # Adding model 'Option'
        db.create_table('educacion_option', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('value', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('correct', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('weight', self.gf('django.db.models.fields.IntegerField')()),
            ('question', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['educacion.Question'])),
        ))
        db.send_create_signal('educacion', ['Option'])

        # Adding model 'Question'
        db.create_table('educacion_question', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('question', self.gf('django.db.models.fields.CharField')(max_length=512)),
            ('percent', self.gf('django.db.models.fields.FloatField')()),
            ('exam', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['educacion.Exam'])),
            ('reply', self.gf('django.db.models.fields.CharField')(max_length=512)),
            ('explanation', self.gf('django.db.models.fields.TextField')()),
            ('weight', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal('educacion', ['Question'])

        # Adding model 'Resource'
        db.create_table('educacion_resource', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('file', self.gf('django.db.models.fields.files.FileField')(max_length=100)),
            ('type', self.gf('django.db.models.fields.CharField')(max_length=5)),
            ('lesson', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['educacion.Lesson'])),
        ))
        db.send_create_signal('educacion', ['Resource'])

        # Adding model 'Exam'
        db.create_table('educacion_exam', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('resource', self.gf('django.db.models.fields.related.ForeignKey')(related_name='exams', to=orm['educacion.Resource'])),
            ('max_value', self.gf('django.db.models.fields.IntegerField')(default=100)),
            ('seconds', self.gf('django.db.models.fields.IntegerField')(null=True)),
        ))
        db.send_create_signal('educacion', ['Exam'])


    def backwards(self, orm):
        # Deleting model 'Lesson'
        db.delete_table('educacion_lesson')

        # Deleting model 'Option'
        db.delete_table('educacion_option')

        # Deleting model 'Question'
        db.delete_table('educacion_question')

        # Deleting model 'Resource'
        db.delete_table('educacion_resource')

        # Deleting model 'Exam'
        db.delete_table('educacion_exam')


    models = {
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'ordering': "('content_type__app_label', 'content_type__model', 'codename')", 'unique_together': "(('content_type', 'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'educacion.course': {
            'Meta': {'object_name': 'Course'},
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {}),
            'enrolled': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'courses'", 'symmetrical': 'False', 'to': "orm['auth.User']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'program': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'courses'", 'null': 'True', 'to': "orm['educacion.Program']"}),
            'published_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"}),
            'username': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'educacion.exam': {
            'Meta': {'object_name': 'Exam'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'max_value': ('django.db.models.fields.IntegerField', [], {'default': '100'}),
            'resource': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'exams'", 'to': "orm['educacion.Resource']"}),
            'seconds': ('django.db.models.fields.IntegerField', [], {'null': 'True'})
        },
        'educacion.lesson': {
            'Meta': {'object_name': 'Lesson'},
            'course': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'Lessons'", 'to': "orm['educacion.Course']"}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'orden': ('django.db.models.fields.IntegerField', [], {}),
            'published_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"})
        },
        'educacion.option': {
            'Meta': {'object_name': 'Option'},
            'correct': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'question': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['educacion.Question']"}),
            'value': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'weight': ('django.db.models.fields.IntegerField', [], {})
        },
        'educacion.program': {
            'Meta': {'object_name': 'Program'},
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'published_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"}),
            'username': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'educacion.question': {
            'Meta': {'object_name': 'Question'},
            'exam': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['educacion.Exam']"}),
            'explanation': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'percent': ('django.db.models.fields.FloatField', [], {}),
            'question': ('django.db.models.fields.CharField', [], {'max_length': '512'}),
            'reply': ('django.db.models.fields.CharField', [], {'max_length': '512'}),
            'weight': ('django.db.models.fields.IntegerField', [], {})
        },
        'educacion.resource': {
            'Meta': {'object_name': 'Resource'},
            'file': ('django.db.models.fields.files.FileField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lesson': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['educacion.Lesson']"}),
            'type': ('django.db.models.fields.CharField', [], {'max_length': '5'})
        }
    }

    complete_apps = ['educacion']