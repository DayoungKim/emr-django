from rest_framework import serializers

from .models import Concept, ConditionOccurrence, Death, DrugExposure, Person, VisitOccurrence


class ConceptSerializer(serializers.ModelSerializer):
    class Meta:
        model = Concept
        fields = '__all__'


class ConceptBriefSeraizlier(serializers.ModelSerializer):
    class Meta:
        model = Concept
        fields = ['concept_id', 'concept_name', ]


class PersonSerializer(serializers.ModelSerializer):
    gender_concept = ConceptBriefSeraizlier()
    race_concept = ConceptBriefSeraizlier()
    ethnicity_concept = ConceptBriefSeraizlier()
    gender_source_concept = ConceptBriefSeraizlier()
    race_source_concept = ConceptBriefSeraizlier()
    ethnicity_source_concept = ConceptBriefSeraizlier()

    class Meta:
        model = Person
        fields = '__all__'


class ConditionOccurrenceSerializer(serializers.ModelSerializer):
    condition_concept = ConceptBriefSeraizlier()
    condition_type_concept = ConceptBriefSeraizlier()
    condition_status_concept = ConceptBriefSeraizlier()
    condition_source_concept = ConceptBriefSeraizlier()

    class Meta:
        model = ConditionOccurrence
        fields = '__all__'


class DeathSerializer(serializers.ModelSerializer):
    death_type_concept = ConceptBriefSeraizlier()
    cause_concept = ConceptBriefSeraizlier()
    cause_source_concept = ConceptBriefSeraizlier()

    class Meta:
        model = Death
        fields = '__all__'


class DrugExposureSerializer(serializers.ModelSerializer):
    drug_concept = ConceptBriefSeraizlier()
    drug_type_concept = ConceptBriefSeraizlier()
    route_concept = ConceptBriefSeraizlier()
    drug_source_concept = ConceptBriefSeraizlier()
    quantity = serializers.FloatField()  # 너무 자리수 높아서 api 느려짐. float 로 대체

    class Meta:
        model = DrugExposure
        fields = '__all__'


class VisitOccurrenceSerializer(serializers.ModelSerializer):
    visit_concept = ConceptBriefSeraizlier()
    visit_type_concept = ConceptBriefSeraizlier()
    visit_source_concept = ConceptBriefSeraizlier()
    admitted_from_concept = ConceptBriefSeraizlier()
    discharge_to_concept = ConceptBriefSeraizlier()

    class Meta:
        model = VisitOccurrence
        fields = '__all__'
