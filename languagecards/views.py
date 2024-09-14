from django.views.generic import TemplateView
from react.mixins import ReactMixin
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.db.models import F, Prefetch, Value
from django.db.models.functions import Mod
from django.views.decorators.http import require_GET
from rest_framework import serializers
from .models import Card, File, Category, Grammar, Banner
from .strings import webpage_texts
from .utils import niceday, unaccent

class FileSerializer(serializers.ModelSerializer):

    class Meta:
        model = File
        fields = ('id', 'name', 'file', 'file_url', 'description')


class GrammarSerializer(serializers.ModelSerializer):

    class Meta:
        model = Grammar
        fields = ('id', 'grammar', 'description', 'is_html')


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('id', 'username', 'first_name')


class CardSerializer(serializers.ModelSerializer):
    files = FileSerializer(many=True)
    grammars = GrammarSerializer(many=True)
    grammars = GrammarSerializer(many=True)
    # user = UserSerializer(many=False)

    class Meta:
        model = Card
        fields = ('id', 'text1', 'text2', 'pronunciation', 'category', 'files', 'grammars', 'comment', 'is_learned')


class IndexView(ReactMixin, TemplateView):
    template_name = 'languagecards/react.html'
    # did not work: app_root = 'languagecards/components/languagecards.tsx'
    app_root = 'languagecards/components/languagecards.jsx'

    def get_props_data(self):
        banner = Banner.objects.last().content if Banner.objects.count() else ''
        cards = Card.objects.select_related('category').prefetch_related(
            Prefetch('files', queryset=File.objects.filter(is_deprecated=False)),
            Prefetch('grammars', queryset=Grammar.objects.filter(is_deprecated=False)),
            ).filter(
            is_deprecated=False).order_by(
            'position', unaccent('text2'))
        serializer = CardSerializer(cards, many=True)
        webpage_texts[0]['ba'] = banner
        return webpage_texts + serializer.data


class JndexView(ReactMixin, TemplateView):
    template_name = 'languagecards/react.html'
    app_root = 'languagecards/components/languagecards.jsx'

    def get_props_data(self):
        banner = Banner.objects.last().content if Banner.objects.count() else ''
        cards = Card.objects.select_related('category').prefetch_related(
            Prefetch('files', queryset=File.objects.filter(is_deprecated=False)),
            Prefetch('grammars', queryset=Grammar.objects.filter(is_deprecated=False)),
            ).filter(
            is_deprecated=False).order_by(
            'position', unaccent('text1'))
        serializer = CardSerializer(cards, many=True)
        webpage_texts[0]['ba'] = banner
        return webpage_texts + serializer.data


class UnfilteredView(ReactMixin, TemplateView):
    template_name = 'languagecards/react.html'
    app_root = 'languagecards/components/languagecards.jsx'

    def get_props_data(self):
        banner = Banner.objects.last().content if Banner.objects.count() else ''
        cards = Card.objects.select_related('category').prefetch_related(
            'grammars', 'files').order_by(
            'position', '?')  # unaccent('text2'))
        serializer = CardSerializer(cards, many=True)
        webpage_texts[0]['ba'] = banner
        return webpage_texts + serializer.data


class User2View(ReactMixin, TemplateView):  # TODO: not this duplicated way
    template_name = 'languagecards/react.html'
    app_root = 'languagecards/components/languagecards.jsx'

    def get_props_data(self):
        banner = Banner.objects.last().content if Banner.objects.count() else ''
        cards = Card.objects.select_related('category', 'user').prefetch_related(
            Prefetch('files', queryset=File.objects.filter(is_deprecated=False)),
            Prefetch('grammars', queryset=Grammar.objects.filter(is_deprecated=False)),
            ).annotate(
                id_mod=Mod('id', Value(4)),
                day_mod=Mod(niceday(), Value(4))
            ).filter(user_id=2, id_mod=F('day_mod')
            ).order_by('position', '?')
        serializer = CardSerializer(cards, many=True)
        webpage_texts[0]['ba'] = banner
        return webpage_texts + serializer.data


class User3View(ReactMixin, TemplateView):  # TODO: not this duplicated way
    template_name = 'languagecards/react.html'
    app_root = 'languagecards/components/languagecards.jsx'

    def get_props_data(self):
        banner = Banner.objects.last().content if Banner.objects.count() else ''
        cards = Card.objects.select_related('category', 'user').prefetch_related(
            Prefetch('files', queryset=File.objects.filter(is_deprecated=False)),
            Prefetch('grammars', queryset=Grammar.objects.filter(is_deprecated=False)),
            ).annotate(
                id_mod=Mod('id', Value(12)),
                day_mod=Mod(niceday(), Value(12))
            ).filter(user_id=3, id_mod=F('day_mod')
            ).order_by('position', '?')
        #    ).raw(
        #    "select id, id % 12 as x from languagecards_card where user_id = 3 and id % 12 = strftime('%d', date('now')) % 12 order by random()"
        #    )
        serializer = CardSerializer(cards, many=True)
        webpage_texts[0]['ba'] = banner
        return webpage_texts + serializer.data


class User4View(ReactMixin, TemplateView):  # TODO: not this duplicated way
    template_name = 'languagecards/react.html'
    app_root = 'languagecards/components/languagecards.jsx'

    def get_props_data(self):
        banner = Banner.objects.last().content if Banner.objects.count() else ''
        cards = Card.objects.select_related('category', 'user').prefetch_related(
            Prefetch('files', queryset=File.objects.filter(is_deprecated=False)),
            Prefetch('grammars', queryset=Grammar.objects.filter(is_deprecated=False)),
            ).annotate(
                id_mod=Mod('id', Value(1)),  # increase this 1 to the required figure
                day_mod=Mod(niceday(), Value(1))
            ).filter(user_id=4, id_mod=F('day_mod')
            ).order_by('position', '?')
        serializer = CardSerializer(cards, many=True)
        webpage_texts[0]['ba'] = banner
        return webpage_texts + serializer.data


class CategoryView(ReactMixin, TemplateView):
    template_name = 'languagecards/react.html'
    app_root = 'languagecards/components/languagecards.jsx'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category = self.kwargs.get('category')

        if category:
            try:
                category_name = Category.objects.get(pk=category).name
            except Category.DoesNotExist:
                context['error_message'] = 'Category not found.'
                category_name = ''

        banner = Banner.objects.last().content if Banner.objects.count() else ''
        cards = Card.objects.select_related('category', 'user').prefetch_related(
            Prefetch('files', queryset=File.objects.filter(is_deprecated=False)),
            Prefetch('grammars', queryset=Grammar.objects.filter(is_deprecated=False)),
            ).filter(category_id=category
            ).order_by('position', '?')
        serializer = CardSerializer(cards, many=True)
        webpage_texts[0]['ba'] = banner
        # webpage_texts[0]['cn'] = category_name # not great. Remains longer than needed
        context['props'] = webpage_texts + serializer.data

        return context


@require_GET
def robots_txt(request):
    return HttpResponse(robots_txt_content, content_type="text/plain")


robots_txt_content = """\
User-agent: *
Disallow: /
"""
