from django.db import models


class WorkLocationType(models.TextChoices):
    ONSITE = "Офис"
    HYBRID = "Гибрид"
    REMOTE = "Удалённо"


class EmploymentType(models.TextChoices):
    SELF_EMPLOYMENT = "Самозанятость"
    CIVIL_CONTRACT = "ГПХ"
    LABOR_CONTRACT = "ТК"


class CurrencyType(models.TextChoices):
    USD = "USD"
    EUR = "EUR"
    RUB = "RUB"


class VacancyStatus(models.TextChoices):
    ACTIVE = "Активная"
    UNPUBLISHED = "Неопубликованная"
    ARCHIVED = "Архивированная"
