from django.db.models import Count
from django_filters.filterset import CharFilter, FilterSet

from applicants.models import Applicant


class SkillFilter(FilterSet):
    skills = CharFilter(method="filter_skills")

    class Meta:
        model = Applicant
        fields = ("skills",)

    def filter_skills(self, queryset, name, value):
        skills = self.request.query_params.getlist("skills")
        return (
            queryset.filter(skills__name__in=skills)
            .annotate(num_skills=Count("skills"))
            .filter(num_skills=len(skills))
        )
