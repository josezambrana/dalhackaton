from django.contrib import admin

from educacion.models import Course
from educacion.models import Program


class CourseAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}
    list_display = ('__unicode__', 'program')


class ProgramAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}
    list_display = ('__unicode__', )


admin.site.register(Course, CourseAdmin)
admin.site.register(Program, ProgramAdmin)
