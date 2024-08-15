from django.db.models import Value
from django.db.models.functions import Replace, Lower


def unaccent(a):
    return \
        Lower(
        Replace(
        Replace(
        Replace(
        Replace(
        Replace(
        Replace(
        Replace(
        Replace(
        Replace(
        Replace(
        Replace(
        Replace(
        Replace(
        Replace(
        Replace(
        Replace(
        Replace(
        Replace(
        Replace(
        Replace(
        Replace(a,
        Value('('), Value('')),
        Value('-'), Value('')),
        Value('/'), Value('')),
        Value('Á'), Value('azzz')),
        Value('É'), Value('ezzz')),
        Value('Í'), Value('izzz')),
        Value('Ó'), Value('ozz1')),
        Value('Ö'), Value('ozz2')),
        Value('Ő'), Value('ozz3')),
        Value('Ú'), Value('uzz1')),
        Value('Ü'), Value('uzz2')),
        Value('Ű'), Value('uzz3')),
        Value('á'), Value('azzz')),
        Value('é'), Value('ezzz')),
        Value('í'), Value('izzz')),
        Value('ó'), Value('ozz1')),
        Value('ö'), Value('ozz2')),
        Value('ő'), Value('ozz3')),
        Value('ú'), Value('uzz1')),
        Value('ü'), Value('uzz2')),
        Value('ű'), Value('uzz3')))
