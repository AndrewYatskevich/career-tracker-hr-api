from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from rest_framework import mixins, status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response

from api.serializers import (
    ApplicantSerializer,
    SpecializationSkillSerializer,
    UserSerializer,
    VacancyDetailSerializer,
    VacancySerializer,
)
from applicants.models import Applicant, Favorites, Specialization
from vacancies.models import Vacancy

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


class UserViewSet(mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class VacancyViewSet(
    mixins.CreateModelMixin, mixins.ListModelMixin, viewsets.GenericViewSet
):
    queryset = Vacancy.objects.all()
    serializer_class = VacancyDetailSerializer
    permission_classes = (IsAuthenticated,)

    def get_serializer_class(self):
        if self.action == "list":
            return VacancySerializer
        return super().get_serializer_class()

    @action(
        detail=False,
        methods=("get",),
        url_path="my",
    )
    def get_my_vacancies(self, request):
        serializer = VacancySerializer(request.user.vacancies.all(), many=True)
        return Response(serializer.data)


class SpecializationViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Вьюсет для специализаций.
    Получение списка специализаций и связанных с ними навыков.
    """

    queryset = Specialization.objects.all().prefetch_related("skills")
    serializer_class = SpecializationSkillSerializer
    permission_classes = (IsAuthenticated,)


class ApplicantsViewSet(ListRetrievePutDeleteViewSet):

    """
    Вьюсет для соискателей.
    Получение соискателя или списка соискателей.
    """

    queryset = (
        Applicant.objects.all()
        .select_related("specialization")
        .prefetch_related("skills")
    )
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
