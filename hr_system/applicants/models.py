from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.validators import RegexValidator
from django.db import models

User = get_user_model()


class Specialization(models.Model):
    """Модель специализаций."""

    name = models.CharField(
        verbose_name="Название",
        max_length=settings.DESCRIPTION_MAX_LENGTH,
        unique=True,
        db_index=True,
    )
    position = models.CharField(
        verbose_name="Должность",
        max_length=settings.DESCRIPTION_MAX_LENGTH,
        unique=True,
    )

    class Meta:
        verbose_name = "Специализация"
        verbose_name_plural = "Специализации"
        ordering = ["name"]
        constraints = [
            models.UniqueConstraint(
                fields=["name", "position"], name="unique_specialization"
            ),
        ]

    def __str__(self) -> str:
        return f"{self.name}"


class Skill(models.Model):
    """Модель для навыков."""

    name = models.CharField(
        verbose_name="Название",
        max_length=settings.DESCRIPTION_MAX_LENGTH,
        unique=True,
        db_index=True,
    )
    specialization = models.ManyToManyField(
        to=Specialization,
        verbose_name="Специализация",
        related_name="skills",
    )

    class Meta:
        verbose_name = "Навык"
        verbose_name_plural = "Навыки"
        ordering = ["name"]

    def __str__(self) -> str:
        return f"{self.name}"


class Applicant(models.Model):
    """Модель для карточки соискателя."""

    first_name = models.CharField(
        verbose_name="Имя",
        max_length=settings.NAME_MAX_LENGTH,
    )
    last_name = models.CharField(
        verbose_name="Фамилия",
        max_length=settings.NAME_MAX_LENGTH,
    )
    city = models.CharField(
        verbose_name="Город",
        max_length=settings.NAME_MAX_LENGTH,
    )
    country = models.CharField(
        verbose_name="Страна",
        max_length=settings.NAME_MAX_LENGTH,
    )
    about_me = models.CharField(
        verbose_name="О себе",
        max_length=settings.DESCRIPTION_MAX_LENGTH,
    )
    email = models.EmailField(
        verbose_name="Адрес электронной почты",
        max_length=settings.EMAIL_MAX_LENGTH,
        unique=True,
        blank=True,
    )
    phone = models.CharField(
        verbose_name="Телефон",
        blank=True,
        validators=(
            RegexValidator(
                regex=(
                    "^(\+\d{1,4}\s?)?(\d{1,4}[\s-]?)?(\(\d{1,}\)"
                    "[\s-]?)?\d{1,}([\s-]?\d{1,}){1,}$"
                ),
                message="Введите номер телефона",
            ),
        ),
    )
    telegram = models.CharField(
        verbose_name="Telegram",
        blank=True,
        validators=(
            RegexValidator(
                regex="^@[\w\d_]{5,32}$",
                message="Введите логин telegram",
            ),
        ),
    )
    specialization = models.ForeignKey(
        to=Specialization,
        verbose_name="Специализация",
        on_delete=models.SET_NULL,
        null=True,
    )
    experience = models.PositiveSmallIntegerField(
        verbose_name="Опыт",
    )
    activity = models.PositiveSmallIntegerField(
        verbose_name="Активность",
    )
    photo = models.ImageField(
        verbose_name="Фотография соискателя",
        upload_to=settings.PHOTO_PATH,
        default=None,
        blank=True,
        null=True,
    )
    resume_pdf = models.FileField(
        verbose_name="Резюме в формате pdf",
        upload_to=settings.RESUME_PATH,
        default=None,
        blank=True,
        null=True,
    )
    resume_url = models.URLField(
        verbose_name="Ссылка на резюме",
        blank=True,
        null=True,
    )
    portfolio_url = models.URLField(
        verbose_name="Ссылка на портфолио",
        blank=True,
        null=True,
    )
    skills = models.ManyToManyField(
        to=Skill,
        verbose_name="Навыки",
        related_name="applicants",
        blank=True,
    )

    class Meta:
        verbose_name = "Соискатель"
        verbose_name_plural = "Соискатели"
        ordering = ["last_name"]

    def __str__(self) -> str:
        return f"{self.last_name} {self.first_name}"


class Favorites(models.Model):
    """Модель для избранного."""

    user = models.ForeignKey(
        to=User,
        verbose_name="Пользователь",
        on_delete=models.CASCADE,
    )
    applicant = models.ForeignKey(
        to=Applicant,
        verbose_name="Соискатель",
        on_delete=models.CASCADE,
    )

    class Meta:
        default_related_name = "favorites"
        verbose_name = "Избранное"
        verbose_name_plural = "Избранное"
        ordering = ("-id",)
        constraints = [
            models.UniqueConstraint(
                fields=["user", "applicant"], name="unique_favorites"
            ),
        ]

    def __str__(self) -> str:
        return f"{self.user}: {self.applicant}"
