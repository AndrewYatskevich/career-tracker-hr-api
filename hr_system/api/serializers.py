from rest_framework import serializers

from hr_system.applicants.models import Applicant


class ApplicantSerializer(serializers.ModelSerializer):
    """Сериализатор для соискателей."""

    class Meta:
        model = Applicant
        fields = ("__all__",)


class ShortApplicantSerializer(serializers.ModelSerializer):
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
        )
