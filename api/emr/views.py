from datetime import datetime
from django.db.models import Count, F
from django.utils.decorators import method_decorator
from drf_yasg.openapi import Parameter, IN_QUERY, TYPE_STRING
from drf_yasg.utils import swagger_auto_schema
from rest_framework.decorators import api_view
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK
from rest_framework.viewsets import GenericViewSet

from .models import Concept, ConditionOccurrence, Death, DrugExposure, Person, VisitOccurrence
from .serializers import \
    ConceptSerializer, ConditionOccurrenceSerializer, DeathSerializer, \
    DrugExposureSerializer, PersonSerializer, VisitOccurrenceSerializer


@api_view(http_method_names=['GET'])
def person_view(request):
    queryset = Person.objects.all()
    return Response({
        'all': queryset.count(),
        'female': queryset.filter(gender_concept__concept_name='FEMALE').count(),
        'male': queryset.filter(gender_concept__concept_name='MALE').count(),
        'race': queryset.values('race_concept__concept_name').annotate(count=Count('race_concept__concept_name')),
        'ethnicelty': queryset.values(
            'ethnicity_concept__concept_name').annotate(count=Count('ethnicity_concept__concept_name')),
        'death': queryset.filter(death__isnull=False).count()
    }, HTTP_200_OK)


@api_view(http_method_names=['GET'])
def visit_view(request):
    queryset = VisitOccurrence.objects.all()
    now_year = datetime.now().year
    return Response({
        'visit_type': queryset.values(
            'visit_concept__concept_name').annotate(count=Count('visit_concept__concept_name')),
        'female': queryset.filter(person__gender_concept__concept_name='FEMALE').count(),
        'male': queryset.filter(person__gender_concept__concept_name='MALE').count(),
        'race': queryset.values('person__race_concept__concept_name').annotate(
            count=Count('person__race_concept__concept_name')),
        'ethnicelty': queryset.values(
            'person__ethnicity_concept__concept_name').annotate(count=Count('person__ethnicity_concept__concept_name')),
        'age_by_ten': Person.objects.annotate(
            age_by_ten=(now_year - F('year_of_birth')) / 10 * 10
        ).values('age_by_ten').annotate(count=Count('age_by_ten')).order_by('age_by_ten')
    }, HTTP_200_OK)


@method_decorator(name='list', decorator=swagger_auto_schema(
    manual_parameters=[
        Parameter(
            name='f', in_=IN_QUERY, type=TYPE_STRING, required=False,
            description='????????? ??????, ????????? ??????:??? ?????? ??????. '
                        '????????? ????????? ??? ????????? ?????? ?????? ???(=????????? ???????????? ?????? ??????...). '
                        '?????? ????????? ?????? ?????? ?????? ??????. ???????????? ???????????? ???????????? ??????. '
                        '?????? ?????? ????????? ?????? XX_concept__concept_name:????????????, XX_concept__concept_id:??????????????? ??? ????????????')
    ]))
class SearchGenericViewSet(ListModelMixin, RetrieveModelMixin, GenericViewSet):
    def get_f(self, value):
        q_filter = {}
        for v in value:
            try:
                filter_key, filter_value = v.split(':')
                q_filter[filter_key + '__icontains'] = filter_value
            except Exception:
                self.queryset = self.queryset.none()
        self.queryset = self.queryset.filter(**q_filter)

    def get_queryset(self):
        for key in self.request.GET.keys():
            method_name = 'get_%s' % key
            if hasattr(self, method_name):
                self_method = getattr(self, method_name)
                self_method(value=self.request.GET[key].split(','))
        return self.queryset


class ConceptViewSet(SearchGenericViewSet):
    model = Concept
    queryset = Concept.objects.all()
    serializer_class = ConceptSerializer

    def __date_search(self, value):
        if len(value) < 1 or len(value) > 2:
            self.queryset = self.queryset.none()
        try:
            return datetime.strptime(value[0], '%Y-%m-%d').date()
        except Exception:
            self.queryset = self.queryset.none()
        return None

    def get_start(self, value):
        start = self.__date_search(value)
        self.queryset = self.queryset.filter(
            valid_start_date=start
        )

    def get_end(self, value):
        end = self.__date_search(value)
        self.queryset = self.queryset.filter(
            valid_end_date=end
        )

    def get_ids(self, value):
        self.queryset = self.queryset.filter(concept_id__in=value)

    @method_decorator(name='list', decorator=swagger_auto_schema(
        manual_parameters=[
            Parameter(name='f', in_=IN_QUERY, type=TYPE_STRING, required=False,
                      description='????????? ??????, ????????? ??????:??? ?????? ??????(???: domain_id:Drug,concept_name:FILM COATED), '
                                  '????????? ????????? ??? ????????? ?????? ?????? ???(=????????? ???????????? ?????? ??????...). '
                                  '?????? ????????? ?????? ?????? ?????? ??????. ???????????? ???????????? ???????????? ??????. '),
            Parameter(
                name='ids', description='concept id ??????. ???????????? ???????????? ????????? ?????? ?????? ???',
                in_=IN_QUERY, type=TYPE_STRING, required=False),
            Parameter(name='start', description='valid_start_date ??????. yyyy-mm-dd ?????? ??????', in_=IN_QUERY, type=TYPE_STRING,
                      required=False),
            Parameter(name='end', description='valid_end_date ??????. yyyy-mm-dd ?????? ??????', in_=IN_QUERY, type=TYPE_STRING,
                      required=False),
        ]))
    def list(self, request, *args, **kwargs):
        return super(ConceptViewSet, self).list(request, *args, **kwargs)


class PersonViewSet(SearchGenericViewSet):
    model = Person
    queryset = Person.objects.all()
    serializer_class = PersonSerializer


class ConditionOccurrenceViewSet(SearchGenericViewSet):
    model = ConditionOccurrence
    queryset = ConditionOccurrence.objects.all()
    serializer_class = ConditionOccurrenceSerializer


class DeathViewSet(SearchGenericViewSet):
    model = Death
    queryset = Death.objects.all()
    serializer_class = DeathSerializer


class DrugExposureViewSet(SearchGenericViewSet):
    model = DrugExposure
    queryset = DrugExposure.objects.all()
    serializer_class = DrugExposureSerializer


class VisitOccurrenceViewSet(SearchGenericViewSet):
    model = VisitOccurrence
    queryset = VisitOccurrence.objects.all()
    serializer_class = VisitOccurrenceSerializer
