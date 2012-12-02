from django.contrib import admin

from educacion.models import Course
from educacion.models import Program
from educacion.models import Resource
from educacion.models import Exam
from educacion.models import Question


class CourseAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}
    list_display = ('__unicode__', 'program')


class ProgramAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}
    list_display = ('__unicode__', )


class ResourceAdmin(admin.ModelAdmin):
    list_display = ('__unicode__', )


class ExamAdmin(admin.ModelAdmin):
    list_display = ('__unicode__', )


class QuestionAdmin(admin.ModelAdmin):
    list_display = ('question', 'weight')


admin.site.register(Course, CourseAdmin)
admin.site.register(Program, ProgramAdmin)
admin.site.register(Resource, ResourceAdmin)
admin.site.register(Exam, ExamAdmin)
admin.site.register(Question, QuestionAdmin)
