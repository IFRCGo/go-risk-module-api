import factory
from factory import fuzzy
from factory.django import DjangoModelFactory

from oddrin.models import (
    Oddrin,
    RiskFile
)


class RiskFileFactory(DjangoModelFactory):
    class Meta:
        model = RiskFile


class OddrinFactory(DjangoModelFactory):
    hazard_title = factory.Sequence(lambda n: 'hazard%s' % n)
    hazard_type = factory.Iterator([Oddrin.HazardType.EARTHQUAKE])
    glide_number = fuzzy.FuzzyText(length=10)
    latitude = fuzzy.FuzzyFloat(-90, 90)
    longitude = fuzzy.FuzzyFloat(-180, 180)
    people_exposed = fuzzy.FuzzyInteger(0, 1000000)
    people_displaced = fuzzy.FuzzyInteger(0, 1000000)
    buildings_exposed = fuzzy.FuzzyInteger(0, 1000000)

    class Meta:
        model = Oddrin
