from rest_framework import serializers
from rest_framework.fields import SerializerMethodField

from hr_system.applicants.models import Applicant, Skill


class ApplicantSerializer(serializers.ModelSerializer):
    """Сериализатор для соискателей."""

    skills = serializers.PrimaryKeyRelatedField(
        queryset=Skill.objects.all(),
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
            "grade",
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
            "grade",
            "experience",
            "activity",
            "photo",
            "skills",
            "is_liked",
        )
