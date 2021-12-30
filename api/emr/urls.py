from django.urls import include, path
from rest_framework import routers

from .views import person_view, visit_view, \
    ConceptViewSet, PersonViewSet, ConditionOccurrenceViewSet, \
    DeathViewSet, DrugExposureViewSet, VisitOccurrenceViewSet

router = routers.DefaultRouter()
router.register('concept', ConceptViewSet, basename='concept')
router.register('person', PersonViewSet, basename='person')
router.register('condition-occurrence', ConditionOccurrenceViewSet, basename='condition-occurrence')
router.register('death', DeathViewSet, basename='death')
router.register('drug-exposure', DrugExposureViewSet, basename='drug-exposure')
router.register('visit-occurrence', VisitOccurrenceViewSet, basename='visit-occurrence')

urlpatterns = [
    path('person/count/', person_view),
    path('visit/count/', visit_view),
    path('', include(router.urls)),
]
