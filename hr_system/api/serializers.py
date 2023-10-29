from rest_framework import serializers
from rest_framework.fields import SerializerMethodField

from api.utils import extract_domain
from applicants.models import Applicant, Skill, Specialization


class SpecializationSerializer(serializers.ModelSerializer):
    """Сериализатор для специализаций."""

    class Meta:
        model = Specialization
        fields = ("name", "position")


class SkillSerializer(serializers.ModelSerializer):
    """Сериализатор для навыков."""

    class Meta:
        model = Skill
        fields = ("name",)


class SpecializationSkillSerializer(serializers.ModelSerializer):
    """Сериализатор для специализаций со связанными навыками."""

    related_skills = SerializerMethodField()

    class Meta:
        model = Specialization
        fields = ("name", "related_skills")

    def get_related_skills(self, specialization: Specialization) -> list[str]:
        """Возвращает список связанных со специализацией навыков."""

        return list(specialization.skills.values_list("name", flat=True))


class ApplicantSerializer(serializers.ModelSerializer):
    """Сериализатор для соискателей."""

    specialization = SpecializationSerializer(
        read_only=True,
    )
    skills = SkillSerializer(
        many=True,
    )
    is_liked = SerializerMethodField()
    resume_domain = SerializerMethodField()

    class Meta:
        model = Applicant
        fields = (
            "first_name",
            "last_name",
            "city",
            "country",
            "about_me",
            "phone",
            "email",
            "telegram",
            "specialization",
            "experience",
            "activity",
            "photo",
            "skills",
            "resume_pdf",
            "resume_url",
            "portfolio_url",
            "is_liked",
            "resume_domain",
        )

    def get_is_liked(self, applicant: Applicant) -> bool:
        """Проверяет добавлен ли соискатель в избранное."""

        user = self.context["request"].user

        return user.favorites.filter(applicant=applicant).exists()

    def get_resume_domain(self, applicant: Applicant) -> str | None:
        """Возвращает доменное имя url-адреса резюме."""

        received_url = applicant.resume_url

        if received_url:
            return extract_domain(received_url)
