import logging
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from django.contrib import admin
from django.db.models import F
from . import models
from .utils import unaccent


class ProfileInline(admin.StackedInline):
    model = models.Profile
    can_delete = False
    verbose_name_plural = _('user profile')
    fk_name = 'user'
    readonly_fields = ('weight',)


class USERAdmin(UserAdmin):
    inlines = (ProfileInline,)
    list_display = ['username', 'is_active', 'first_name', 'last_name', 'email', 'last_login']
    list_filter = (
        'is_staff',
        'is_superuser',
        'is_active',
    )

    def get_inline_instances(self, request, obj=None):
        if not obj:
            return list()
        return super().get_inline_instances(request, obj)


admin.site.unregister(User)
admin.site.register(User, USERAdmin)


#class UserProfileAdmin(admin.ModelAdmin):
#    search_fields = ('user__username', 'user__email',)
#
#    def get_queryset(self, request):
#        return super().get_queryset(request).select_related('user')

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'position',)
    ordering = ('position', 'name')


class FileAdmin(admin.ModelAdmin):

    @admin.display(description="ének")
    def linked_card(self, obj):
        return obj.card_set.first() or '-'

    @admin.display(description="ok")
    def is_active(self, obj):
        return not obj.is_deprecated

    readonly_fields = ['linked_card']
    search_fields = ('directory', 'name', 'file', 'file_url',)
    list_display = ('__str__', 'description', 'position', 'modified_at', 'linked_card', 'is_active')
    ordering = (unaccent('name'), 'position',)


class GrammarAdmin(admin.ModelAdmin):
    @admin.display(description="ének")
    def linked_card(self, obj):
        return obj.card_set.first() or '-'

    @admin.display(description="ok")
    def is_active(self, obj):
        return not obj.is_deprecated

    @admin.display(description="papírra")
    def for_print(self, obj):
        return not obj.only_for_web

    is_active.boolean = True
    for_print.boolean = True
    readonly_fields = ['linked_card']
    list_display = ('__str__', 'description', 'is_active', 'for_print', 'is_html', 'position', 'modified_at', 'linked_card')
    search_fields = ('name', 'description',)
    ordering = ('position',)


category_name_1 = models.Category.objects.get(id=1).name
category_name_2 = models.Category.objects.get(id=2).name
category_name_3 = models.Category.objects.get(id=3).name
category_name_4 = models.Category.objects.get(id=4).name
category_name_5 = models.Category.objects.get(id=5).name
category_name_6 = models.Category.objects.get(id=6).name


@admin.action(description="Kiválasztott Kártyák láthatóságának invertálása")
def invert_status(modeladmin, request, queryset):
    logging.info("Kártyák invertálva")  # has no effect
    queryset.update(is_deprecated=~F("is_deprecated"))


@admin.action(description="Kiválasztott Kártyák láthatóvá állítása")
def status_ok(modeladmin, request, queryset):
    logging.info("Kártyák láthatóak")  # has no effect
    queryset.update(is_deprecated=False)


@admin.action(description="Kiválasztott Kártyák nem láthatóvá állítása")
def status_not_ok(modeladmin, request, queryset):
    logging.info("Kártyák láthatatlanok")  # has no effect
    queryset.update(is_deprecated=True)


@admin.action(description="1. kategóriába sorolás (" + category_name_1 + ")")
def category_1(modeladmin, request, queryset):
    queryset.update(category=1)


@admin.action(description="2. kategóriába sorolás (" + category_name_2 + ")")
def category_2(modeladmin, request, queryset):
    queryset.update(category=2)


@admin.action(description="3. kategóriába sorolás (" + category_name_3 + ")")
def category_3(modeladmin, request, queryset):
    queryset.update(category=3)


@admin.action(description="4. kategóriába sorolás (" + category_name_4 + ")")
def category_4(modeladmin, request, queryset):
    queryset.update(category=4)


@admin.action(description="5. kategóriába sorolás (" + category_name_5 + ")")
def category_5(modeladmin, request, queryset):
    queryset.update(category=5)


@admin.action(description="6. kategóriába sorolás (" + category_name_6 + ")")
def category_6(modeladmin, request, queryset):
    queryset.update(category=6)


class CardAdmin(admin.ModelAdmin):

    @admin.display(description="ok")
    def is_active(self, obj):
        return not obj.is_deprecated

    is_active.boolean = True
    list_display = ('text1', 'text2', 'is_active', 'is_learned', 'category', 'comment', 'user', 'position', 'modified_at')
    list_filter = ('user', 'category', 'created_at')
    search_fields = ('text1', 'text2', 'comment')
    autocomplete_fields = ('files', 'grammars')
    ordering = ('position', unaccent('text1'), unaccent('text2'))
    actions = [invert_status, status_ok, status_not_ok, category_1, category_2,
               category_3, category_4, category_5, category_6]

    def get_changeform_initial_data(self, request):
        return {'category': 2, 'user': 3}


class VoteAdmin(admin.ModelAdmin):
    search_fields = ('score', 'card', 'user')
    list_display = ('score', 'card', 'user')
    autocomplete_fields = ('card',)
    ordering = ('score',)
    exclude = ('user',)

    def has_change_permission(self, request, obj=None):
        user = request.user
        if user.is_superuser:
            return True
        return obj and obj.user == user

    def save_model(self, request, obj, form, change):
        if not change:  # Only set on creation
            obj.user = request.user
        super().save_model(request, obj, form, change)


class IdeaAdmin(admin.ModelAdmin):

    @admin.display(description="bevez.")
    def preface(self, obj):
        return obj.description[:40]

    search_fields = ('description', 'user')
    list_display = ('user', 'preface', 'idea_url', 'position',)
    ordering = ('position',)
    exclude = ('user',)

    def has_change_permission(self, request, obj=None):
        user = request.user
        if user.is_superuser:
            return True
        return obj and obj.user == user

    def save_model(self, request, obj, form, change):
        if not change:  # Only set on creation
            obj.user = request.user
        super().save_model(request, obj, form, change)


class BannerAdmin(admin.ModelAdmin):
    list_display = ('content', 'user')
    ordering = ('id',)
    exclude = ('user',)

    def save_model(self, request, obj, form, change):
        if not change:  # Only set on creation
            obj.user = request.user
        super().save_model(request, obj, form, change)


# admin.site.register(models.Profile, UserProfileAdmin)
admin.site.register(models.Category, CategoryAdmin)
admin.site.register(models.File, FileAdmin)
admin.site.register(models.Grammar, GrammarAdmin)
admin.site.register(models.Card, CardAdmin)
admin.site.register(models.Vote, VoteAdmin)
admin.site.register(models.Idea, IdeaAdmin)
admin.site.register(models.Banner, BannerAdmin)
