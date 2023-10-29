from django.contrib import admin

from applicants.models import Applicant, Favorites, Skill, Specialization

admin.site.register(Specialization)
admin.site.register(Skill)
admin.site.register(Applicant)
admin.site.register(Favorites)
