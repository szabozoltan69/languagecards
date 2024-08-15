from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from django.core.validators import MinValueValidator, MaxValueValidator


class Profile(models.Model):
    """ Holds identifying information about users """

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        verbose_name=_("user"),
        on_delete=models.CASCADE,
        related_name='profile',
        primary_key=True,
        editable=False,
    )
    role = models.CharField(verbose_name=_("role"), blank=True, max_length=100)
    weight = models.IntegerField(verbose_name=_("weight of vote"), default=1, validators=[MaxValueValidator(5)])
    phone_number = models.CharField(verbose_name=_("phone number"), blank=True, null=True, max_length=100)

    class Meta:
        verbose_name = _("user profile")
        verbose_name_plural = _("user profiles")

    def __str__(self):
        return self.user.username


class File(models.Model):
    """ The files belonging to cards """

    def file_path(instance, filename):
        return ('media/files/%s/%s' % (instance.directory, filename)).replace(' ', '_')

    name = models.CharField(verbose_name=_("name"), max_length=255)
    directory = models.CharField(verbose_name=_("directory"), max_length=255)
    file = models.FileField(verbose_name=_("file"), upload_to=file_path, blank=True, null=True)
    description = models.TextField(verbose_name=_("description"), blank=True, null=True)
    file_url = models.URLField(verbose_name=_("file url"), blank=True, null=True)
    position = models.IntegerField(verbose_name=_("position"), default=1)  # the bigger is downer
    created_at = models.DateTimeField(verbose_name=_("created at"), auto_now_add=True)
    modified_at = models.DateTimeField(verbose_name=_("modified at"), auto_now=True)
    is_deprecated = models.BooleanField(verbose_name=_("is deprecated"), default=False, help_text=_("Check this, when this file file is to be hidden."))

    class Meta:
        ordering = ("position", "created_at", "name")
        verbose_name = _("file")
        verbose_name_plural = _("files")

    def __str__(self):
        if self.file_url:
            return ('%s > %s' % (self.name, self.file_url[8:]))  # 8 = len('https://')
        return ('%s' % self.file.url[13:])  # 13 = len('media/files/')


class Grammar(models.Model):
    """ The Grammar optionally belonging to cards """

    name = models.CharField(verbose_name=_("name"), max_length=255)
    grammar = models.TextField(verbose_name=_("grammar"))
    description = models.TextField(verbose_name=_("description"), blank=True, null=True)
    position = models.IntegerField(verbose_name=_("position"), default=1)  # the bigger is downer
    created_at = models.DateTimeField(verbose_name=_("created at"), auto_now_add=True)
    modified_at = models.DateTimeField(verbose_name=_("modified at"), auto_now=True)
    is_html = models.BooleanField(verbose_name=_("is HTML"), default=False, help_text=_("Is this an HTML encoded text?"))
    only_for_web = models.BooleanField(verbose_name=_("only for web"), default=False, help_text=_("Check if this text is not for print page."))
    is_deprecated = models.BooleanField(verbose_name=_("is deprecated"), default=False, help_text=_("Check this, when this text is to be hidden."))

    class Meta:
        ordering = ("position", "name")
        verbose_name = _("grammar")  # !
        verbose_name_plural = _("grammar pages")

    def __str__(self):
        return "%s (%s)" % (self.name, self.id)


class Category(models.Model):
    """ The categories belonging to cards (only one to each) """

    name = models.CharField(verbose_name=_("name"), max_length=255)
    position = models.IntegerField(verbose_name=_("position"), default=1)  # the bigger is downer
    description = models.TextField(verbose_name=_("description"), blank=True, null=True)

    class Meta:
        ordering = ("position", "name")
        verbose_name = _("category")
        verbose_name_plural = _("categories")

    def __str__(self):
        return "%s" % self.name


class Card(models.Model):
    """ The cards themselves. 1 is the known language, 2 is the learned one. """

    text1 = models.TextField(verbose_name=_("mother tongue"), blank=True, null=True)
    text2 = models.TextField(verbose_name=_("foreign language"), blank=True, null=True)
    pronunciation = models.TextField(verbose_name=_("pronunciation"), blank=True, null=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name=_("user"), related_name="user", blank=True, null=True, on_delete=models.SET_NULL)
    grammars = models.ManyToManyField(Grammar, verbose_name=_("grammars"), blank=True)
    files = models.ManyToManyField(File, verbose_name=_("file tracks"), blank=True)
    category = models.ForeignKey(Category, verbose_name=_("category"), related_name='cards', null=True, blank=True, on_delete=models.SET_NULL)
    comment = models.TextField(verbose_name=_("comment"), blank=True, null=True)
    position = models.IntegerField(verbose_name=_("position"), default=1)  # the bigger is downer
    created_at = models.DateTimeField(verbose_name=_("created at"), auto_now_add=True)
    modified_at = models.DateTimeField(verbose_name=_("modified at"), auto_now=True)
    is_learned = models.BooleanField(verbose_name=_("is learned"), default=False, help_text=_("Check this, when you know this card."))
    is_deprecated = models.BooleanField(verbose_name=_("is deprecated"), default=False, help_text=_("Check this, when this card is to be hidden."))

    class Meta:
        ordering = ("text1", "text2")
        verbose_name = _("card")
#       verbose_name_plural = _("cards")
        verbose_name_plural = " " + _("cards").title()  # https://stackoverflow.com/questions/398163/ordering-admin-modeladmin-objects-in-django-admin
        unique_together = ('text1', 'user')
        unique_together = ('text2', 'user')

    def __str__(self):
        return "%s" % self.text1


class Vote(models.Model):
    """ The votes belonging to cards """

    created_at = models.DateTimeField(verbose_name=_("created at"), auto_now_add=True)
    modified_at = models.DateTimeField(verbose_name=_("modified at"), auto_now=True)
    score = models.IntegerField(verbose_name=_("score"), default=1, validators=[MaxValueValidator(5), MinValueValidator(-5)], help_text=_("-5 ... 5"))
    user = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name=_("user"), related_name='votes', null=True, blank=True, on_delete=models.SET_NULL)
    card = models.ForeignKey(Card, verbose_name=_("card"), related_name='votes', null=True, blank=True, on_delete=models.SET_NULL)
    description = models.TextField(verbose_name=_("description"), blank=True, null=True)

    class Meta:
        ordering = ("score", "created_at", "user")
        verbose_name = _("vote")
        verbose_name_plural = _("votes")

    def __str__(self):
        return "%s - %s" % (self.score, self.user)


class Idea(models.Model):
    """ The ideas of the choir """

    created_at = models.DateTimeField(verbose_name=_("created at"), auto_now_add=True)
    modified_at = models.DateTimeField(verbose_name=_("modified at"), auto_now=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name=_("user"), related_name='ideas', null=True, blank=True, on_delete=models.SET_NULL)
    description = models.TextField(verbose_name=_("description"), blank=True, null=True)
    idea_url = models.URLField(verbose_name=_("idea url"), blank=True, null=True)
    position = models.IntegerField(verbose_name=_("position"), default=1)  # the bigger is downer

    class Meta:
        ordering = ("position", "created_at", "user")
        verbose_name = _("idea")
        verbose_name_plural = _("ideas")

    def __str__(self):
        return "%s - %s" % (self.user, self.description[:40])


class Banner(models.Model):
    """ The banner text at the top of the page """

    created_at = models.DateTimeField(verbose_name=_("created at"), auto_now_add=True)
    modified_at = models.DateTimeField(verbose_name=_("modified at"), auto_now=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name=_("user"), related_name='my_banner', null=True, blank=True, on_delete=models.SET_NULL)
    content = models.TextField(verbose_name=_("content"), blank=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['id'], name='unique_banner'),  # did not prevent in sqlite the creation of the 2nd row.
        ]
        verbose_name = _("banner")
        verbose_name_plural = _("banners")

    def __str__(self):
        return "%s - %s" % (self.user, self.content[:40])
