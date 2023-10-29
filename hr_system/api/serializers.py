from rest_framework import serializers
from rest_framework.fields import SerializerMethodField

from applicants.models import Applicant, Skill, Specialization, User
from vacancies.models import Employment, Vacancy, Wage, WorkLocation


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("company_name", "image")


class WageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Wage
        fields = ("min_amount", "max_amount", "currency")


class SkillSerializer(serializers.ModelSerializer):
    """Сериализатор для навыков."""

    class Meta:
        model = Skill
        fields = ("name",)


class VacancySerializer(serializers.ModelSerializer):
    location_type = serializers.SlugRelatedField(
        read_only=True, many=True, slug_field="type"
    )

    class Meta:
        model = Vacancy
        fields = ("name", "city", "location_type")


class VacancyDetailSerializer(serializers.ModelSerializer):
    location_type = serializers.SlugRelatedField(
        queryset=WorkLocation.objects.all(), many=True, slug_field="type"
    )
    employment_type = serializers.SlugRelatedField(
        queryset=Employment.objects.all(), many=True, slug_field="type"
    )
    wage = WageSerializer()
    skills = serializers.SlugRelatedField(
        queryset=Skill.objects.all(), many=True, slug_field="name"
    )

    class Meta:
        model = Vacancy
        fields = "__all__"

    def create(self, validated_data):
        wage_data = validated_data.pop("wage")
        vacancy = super().create(validated_data)
        Wage.objects.create(vacancy=vacancy, **wage_data)
        return vacancy


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
    skills = SkillSerializer(
        many=True,
    )
    is_liked = SerializerMethodField()

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
        )

    def get_is_liked(self, applicant: Applicant) -> bool:
        """Проверяет добавлен ли соискатель в избранное."""

        user = self.context["request"].user

        return user.favorites.filter(applicant=applicant).exists()


class ShortApplicantSerializer(ApplicantSerializer):
    """Сериализатор для соискателей. Компактная версия."""

    class Meta:
        model = Applicant
        fields = (
            "first_name",
            "last_name",
            "email",
            "telegram",
            "specialization",
            "experience",
            "activity",
            "photo",
            "skills",
            "is_liked",
        )
