from django.contrib import admin

from .models import StudyPlan, Subject, Course, Goal, Content


admin.site.register(StudyPlan)
admin.site.register(Subject)
admin.site.register(Course)
admin.site.register(Goal)
admin.site.register(Content)
