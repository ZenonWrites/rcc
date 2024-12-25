from django.db import models
from django.utils.translation import gettext_lazy as _
from django.conf import settings

class Model(models.Model):
    class Meta:
        abstract = True
        default_related_name = "%(class)s_list"


class CModel(Model):
    class Meta:
        abstract = True
        ordering = ("-created",)

    created = models.DateTimeField(
        auto_now_add=True,
    )


class MCModel(CModel):
    class Meta:
        abstract = True

    modified = models.DateTimeField(
        auto_now=True,
    )
    author = models.ForeignKey(
        to=settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        editable=False,
        null=True,
    )


class DescMixin(models.Model):
    class Meta:
        abstract = True

    description = models.TextField(
        blank=True,
        null=True,
    )


class TitleMixin(models.Model):


    class Meta:
        abstract = True

    title = models.CharField(
        max_length=256,
        verbose_name=_("title"),
    )

    def __str__(self) -> str:
        return self.title

