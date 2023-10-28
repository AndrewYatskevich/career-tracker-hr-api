from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from rest_framework import mixins, status, viewsets
from rest_framework.decorators import action
from rest_framework.request import Request
from rest_framework.response import Response

from api.serializers import ApplicantSerializer
from applicants.models import Applicant, Favorites

User = get_user_model()


class ListRetrievePutDeleteViewSet(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet,
):
    """Обобщенное представление для обработки GET, PUT, DELETE запросов."""

    pass


class ApplicantsViewSet(ListRetrievePutDeleteViewSet):
    """
    Вьюсет для соискателей.
    Получение соискателя или списка соискателей.
    """

    queryset = Applicant.objects.all()
    serializer_class = ApplicantSerializer

    @action(
        methods=["put", "delete"],
        detail=True,
    )
    def favorite(self, request: Request, pk: int | str) -> Response:
        """Добавление, удаление соискателя из избранного."""

        applicant = get_object_or_404(Applicant, pk=pk)
        user = request.user
        applicant_in_favorites = user.favorites.filter(applicant=applicant)

        if request.method == "PUT" and not applicant_in_favorites.exists():
            Favorites.objects.create(user=user, applicant=applicant)
            return Response(status=status.HTTP_201_CREATED)

        if request.method == "DELETE" and applicant_in_favorites.exists():
            applicant_in_favorites.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)

        return Response(
            data={"error": "Соискатель уже в избранном."},
            status=status.HTTP_400_BAD_REQUEST,
        )
