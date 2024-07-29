from django.views.generic import TemplateView
from react.mixins import ReactMixin
from .models import Card, File, Grammar, Banner
from django.contrib.auth.models import User
from rest_framework import serializers
from .strings import webpage_texts
from django.db.models import Prefetch
from .utils import unaccent


class FileSerializer(serializers.ModelSerializer):

    class Meta:
        model = File
        fields = ('id', 'name', 'file', 'file_url', 'language', 'description')


class GrammarSerializer(serializers.ModelSerializer):
    # grammars = serializers.SerializerMethodField()

    class Meta:
        model = Grammar
        fields = ('id', 'grammars', 'language', 'description', 'is_html')

    # def get_grammars(self, grammar) -> str:
    #     if grammar.is_html:
    #         return HTMLSerializer(grammar.grammars)
    #     return grammar.grammars


class CardSerializer(serializers.ModelSerializer):
    files = FileSerializer(many=True)
    grammars = GrammarSerializer(many=True)
    grammars = GrammarSerializer(many=True)

    class Meta:
        model = Card
        fields = ('id', 'text1', 'text2', 'categories', 'files', 'grammars', 'description')


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('id', 'username', 'first_name')


class CardShortSerializer(serializers.ModelSerializer):
    class Meta:
        model = Card
        fields = ('id', 'text1', 'text2', 'categories', 'description')


class IndexView(ReactMixin, TemplateView):
    template_name = 'languagecards/react.html'
    # did not work: app_root = 'languagecards/components/languagecards.tsx'
    app_root = 'languagecards/components/languagecards.jsx'

    def get_props_data(self):
        banner = Banner.objects.last().content if Banner.objects.count() else ''
        cards = Card.objects.prefetch_related(
            Prefetch('files', queryset=File.objects.filter(is_deprecated=False)),
            Prefetch('grammars', queryset=Grammar.objects.filter(is_deprecated=False)),
            'categories').filter(
            is_deprecated=False).order_by(
            'position', unaccent('text2'))
        serializer = CardSerializer(cards, many=True)
        webpage_texts[0]['t0'] = banner
        return webpage_texts + serializer.data


class BriefView(ReactMixin, TemplateView):
    template_name = 'languagecards/react.html'
    app_root = 'languagecards/components/languagecards2.jsx'

    def get_props_data(self):
        cards = Card.objects.prefetch_related(
            Prefetch('grammars', queryset=Grammar.objects.filter(is_deprecated=False, only_for_web=False)),
            'categories').filter(
            is_deprecated=False).order_by(
            'position', unaccent('text2'))
        serializer = CardSerializer(cards, many=True)
        return webpage_texts + serializer.data


class UnfilteredView(ReactMixin, TemplateView):  # still not in use
    template_name = 'languagecards/react.html'
    app_root = 'languagecards/components/all.jsx'

    def get_props_data(self):
        banner = Banner.objects.last().content if Banner.objects.count() else ''
        cards = Card.objects.prefetch_related(
            'grammars', 'files', 'grammars', 'categories').order_by(
            'position', unaccent('text2'))
        serializer = CardSerializer(cards, many=True)
        webpage_texts[0]['t0'] = banner
        return webpage_texts + serializer.data
