from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from applicants.models import Skill
from vacancies.enums import (
    CurrencyType,
    EmploymentType,
    VacancyStatus,
    WorkLocationType,
)

user = get_user_model()

WAGE_AMOUNT_VALIDATORS = [MinValueValidator(1), MaxValueValidator(10000000)]


class WorkLocation(models.Model):
    type = models.CharField(choices=WorkLocationType.choices)


class Employment(models.Model):
    type = models.CharField(choices=EmploymentType.choices)


class Vacancy(models.Model):
    user = models.ForeignKey(
        user, on_delete=models.CASCADE, related_name="vacancies"
    )
    department = models.CharField(max_length=settings.NAME_MAX_LENGTH)
    name = models.CharField(max_length=settings.NAME_MAX_LENGTH)
    city = models.CharField(max_length=settings.NAME_MAX_LENGTH)
    location_type = models.ManyToManyField(
        WorkLocation, related_name="vacancies"
    )
    description = models.TextField(max_length=settings.ABOUT_MAX_LENGTH)
    responsibilities = models.TextField(max_length=settings.ABOUT_MAX_LENGTH)
    requirements = models.TextField(max_length=settings.ABOUT_MAX_LENGTH)
    benefits = models.TextField(max_length=settings.ABOUT_MAX_LENGTH)
    skills = models.ManyToManyField(Skill, related_name="vacancies")
    employment_type = models.ManyToManyField(
        Employment, related_name="vacancies"
    )
    status = models.CharField(
        choices=VacancyStatus.choices, default=VacancyStatus.ACTIVE
    )


class Wage(models.Model):
    min_amount = models.IntegerField(validators=WAGE_AMOUNT_VALIDATORS)
    max_amount = models.IntegerField(validators=WAGE_AMOUNT_VALIDATORS)
    currency = models.CharField(choices=CurrencyType.choices)
    vacancy = models.OneToOneField(
        Vacancy, on_delete=models.CASCADE, related_name="wage"
    )

    class Meta:
        constraints = [
            models.CheckConstraint(
                check=models.Q(min_amount__lt=models.F("max_amount")),
                name="min_amount_lt_max_amount",
            )
        ]
