from django.contrib import admin

from educacion.models import Course
from educacion.models import Program
from educacion.models import Lesson
from educacion.models import Resource
from educacion.models import Exam
from educacion.models import Question
from educacion.models import Option


class CourseAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}
    list_display = ('__unicode__', 'program')


class ProgramAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}
    list_display = ('__unicode__', )


class LessonAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}
    list_display = ('__unicode__', )


class ResourceAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}
    list_display = ('__unicode__', )


class ExamAdmin(admin.ModelAdmin):
    list_display = ('__unicode__', )


class QuestionAdmin(admin.ModelAdmin):
    list_display = ('question', 'weight')


class OptionAdmin(admin.ModelAdmin):
    list_display = ('question', 'value')


admin.site.register(Course, CourseAdmin)
admin.site.register(Program, ProgramAdmin)
admin.site.register(Lesson, LessonAdmin)
admin.site.register(Resource, ResourceAdmin)
admin.site.register(Exam, ExamAdmin)
admin.site.register(Question, QuestionAdmin)
admin.site.register(Option, OptionAdmin)
