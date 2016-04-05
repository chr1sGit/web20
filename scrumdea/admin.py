from django.contrib import admin

# Register your models here.

from .models import Project, Sprint, Task

class SprintInLine(admin.TabularInline):
	model = Sprint
	extra = 1

class ProjectAdmin(admin.ModelAdmin):
	fieldsets = [
		(None, {'fields': ['name', 'description']}),
	]
	inlines = [SprintInLine]

admin.site.register(Project, ProjectAdmin)

admin.site.register(Sprint)

admin.site.register(Task)