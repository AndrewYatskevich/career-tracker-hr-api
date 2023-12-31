from rest_framework import serializers
from rest_framework.fields import SerializerMethodField

from api.utils import extract_domain
from applicants.models import Applicant, Skill, Specialization, User
from vacancies.models import Vacancy


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("company_name", "image")


class VacancySerializer(serializers.ModelSerializer):
    company_name = serializers.SlugRelatedField(
        source="user", read_only=True, slug_field="company_name"
    )

    class Meta:
        model = Vacancy
        fields = ("id", "name", "city", "workplace", "company_name")


class VacancyDetailSerializer(serializers.ModelSerializer):
    company_name = serializers.SlugRelatedField(
        source="user", read_only=True, slug_field="company_name"
    )
    skills = serializers.SlugRelatedField(
        queryset=Skill.objects.all(), many=True, slug_field="name"
    )

    class Meta:
        model = Vacancy
        fields = "__all__"
        read_only_fields = ("user",)


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


class SpecializationSerializer(serializers.ModelSerializer):
    """Сериализатор для специализаций."""

    class Meta:
        model = Specialization
        fields = ("name", "position")


class ApplicantSerializer(serializers.ModelSerializer):
    """Сериализатор для соискателей."""

    specialization = SpecializationSerializer(
        read_only=True,
    )
    skills = SerializerMethodField()
    is_liked = SerializerMethodField()
    resume_domain = SerializerMethodField()

    class Meta:
        model = Applicant
        fields = (
            "id",
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

    def get_skills(self, specialization: Specialization) -> list[str]:
        """Возвращает список связанных со специализацией навыков."""

        return list(specialization.skills.values_list("name", flat=True))

    def get_is_liked(self, applicant: Applicant) -> bool:
        """Проверяет добавлен ли соискатель в избранное."""

        user = self.context["request"].user

        if user.is_authenticated:
            return user.favorites.filter(applicant=applicant).exists()
        else:
            return False

    def get_resume_domain(self, applicant: Applicant) -> str | None:
        """Возвращает доменное имя url-адреса резюме."""

        received_url = applicant.resume_url

        if received_url:
            return extract_domain(received_url)
