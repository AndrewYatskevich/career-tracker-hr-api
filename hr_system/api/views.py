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
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet,
):
    """Вьюсет для вакансий."""

    queryset = Vacancy.objects.all()
    queryset = (
        Vacancy.objects.all()
        .select_related("user")
        .prefetch_related("location_type")
    )
    serializer_class = VacancyDetailSerializer
    http_method_names = ("get", "post", "patch", "delete")

    def get_serializer_class(self):
        if self.action == "list":
            return VacancySerializer
        return super().get_serializer_class()

    def perform_create(self, serializer):
        user = User.objects.all()[0]
        serializer.save(user=user)

    @action(
        detail=False,
        methods=("get",),
        url_path="my",
    )
    def get_my_vacancies(self, request):
        """Получение вакансий пользователя."""

        serializer = VacancySerializer(request.user.vacancies.all(), many=True)
        queryset = (
            request.user.vacancies.all()
            .select_related("user")
            .prefetch_related(
                "location_type",
                "employment_type",
                "skills",
            )
        )
        serializer = VacancySerializer(queryset, many=True)
        return Response(serializer.data)


class SpecializationViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    """
    Вьюсет для специализаций.
    Получение списка специализаций и связанных с ними навыков.
    """

    queryset = Specialization.objects.all().prefetch_related("skills")
    serializer_class = SpecializationSkillSerializer
    permission_classes = (IsAuthenticated,)


class ApplicantsViewSet(
    mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet
):
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
