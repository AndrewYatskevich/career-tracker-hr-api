from rest_framework import mixins, viewsets

from hr_system.api.serializers import (
    ApplicantSerializer,
    ShortApplicantSerializer,
)
from hr_system.applicants.models import Applicant


class ListRetrieveViewSet(
    mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet
):
    """Обобщенное представление для обработки GET запросов."""

    pass


class ApplicantsViewSet(ListRetrieveViewSet):
    """
    Вьюсет для соискателей.
    Получение соискателя или списка соискателей.
    """

    queryset = Applicant.objects.all()
    serializer_class = ApplicantSerializer

    def get_serializer_class(self):
        if self.action == "retrieve":
            return ShortApplicantSerializer
        return super().get_serializer_class()
