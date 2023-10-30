from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from applicants.models import Skill
from vacancies.enums import (
    CurrencyType,
    EmploymentType,
    VacancyStatus,
    WorkplaceType,
)

user = get_user_model()

WAGE_AMOUNT_VALIDATORS = [MinValueValidator(1), MaxValueValidator(10000000)]
EXPERIENCE_AMOUNT_VALIDATORS = [MinValueValidator(1), MaxValueValidator(100)]


class Vacancy(models.Model):
    user = models.ForeignKey(
        user, on_delete=models.CASCADE, related_name="vacancies"
    )
    department = models.CharField(max_length=settings.NAME_MAX_LENGTH)
    name = models.CharField(max_length=settings.NAME_MAX_LENGTH)
    city = models.CharField(max_length=settings.NAME_MAX_LENGTH)
    workplace = models.CharField(choices=WorkplaceType.choices)
    wage_min = models.IntegerField(validators=WAGE_AMOUNT_VALIDATORS)
    wage_max = models.IntegerField(validators=WAGE_AMOUNT_VALIDATORS)
    wage_currency = models.CharField(choices=CurrencyType.choices)
    experience_min = models.IntegerField(
        validators=EXPERIENCE_AMOUNT_VALIDATORS
    )
    experience_max = models.IntegerField(
        validators=EXPERIENCE_AMOUNT_VALIDATORS
    )
    description = models.TextField(max_length=settings.ABOUT_MAX_LENGTH)
    responsibilities = models.TextField(max_length=settings.ABOUT_MAX_LENGTH)
    requirements = models.TextField(max_length=settings.ABOUT_MAX_LENGTH)
    benefits = models.TextField(max_length=settings.ABOUT_MAX_LENGTH)
    skills = models.ManyToManyField(Skill, related_name="vacancies")
    employment_type = models.CharField(choices=EmploymentType.choices)
    status = models.CharField(
        choices=VacancyStatus.choices, default=VacancyStatus.ACTIVE
    )

    class Meta:
        constraints = [
            models.CheckConstraint(
                check=models.Q(wage_min__lt=models.F("wage_max")),
                name="wage_min_lt_wage_max",
            ),
            models.CheckConstraint(
                check=models.Q(experience_min__lt=models.F("experience_max")),
                name="experience_min_lt_experience_max",
            ),
        ]

    def __str__(self) -> str:
        return f"{self.name}"
