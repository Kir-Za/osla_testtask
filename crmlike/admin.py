from .models import StatusTask, Task
from django.contrib import admin
from django.db import models


class StatusModelAdmin(admin.ModelAdmin):
    fields = ['title', 'insert_after']

    def change_view(self, request, object_id, extra_context=None):
        self.fields = ['title']
        return super().change_view(request, object_id, extra_context)

    def add_view(self, request, form_url='', extra_context=None):
        self.fields = ['title', 'insert_after']
        return super().add_view(request, form_url='', extra_context=None)


class TaskAdmin(admin.ModelAdmin):
    list_display = ['title', 'body', 'time', 'moderated']
    list_display_links = ['title', 'body', 'time']

    formfield_overrides = {
        models.ForeignKey: {'empty_label': None},
    }


admin.site.register(StatusTask, StatusModelAdmin)
admin.site.register(Task, TaskAdmin)
