from django.db.models import Value
from django.db.models.functions import Replace


def unaccent(a):
    return \
        Replace(
        Replace(
        Replace(
        Replace(
        Replace(
        Replace(
        Replace(a,
        Value('Á'), Value('Azzz')),
        Value('É'), Value('Ezzz')),
        Value('Í'), Value('Izzz')),
        Value('Ö'), Value('Ozzz')),
        Value('Ú'), Value('Uzz1')),
        Value('Ű'), Value('Uzz2')),
        Value('Ü'), Value('Uzz3'))
