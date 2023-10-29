from django.contrib import admin

from vacancies.models import Employment, Vacancy, Wage, WorkLocation

admin.site.register(Vacancy)
admin.site.register(WorkLocation)
admin.site.register(Employment)
admin.site.register(Wage)
