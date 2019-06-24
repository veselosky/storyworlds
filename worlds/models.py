from django.contrib.gis.db import models as geomodels
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from taggit.managers import TaggableManager


# ------------------------------------------------------------------------------
# Start by defining the handful of models that practically everything will use.
# ------------------------------------------------------------------------------
class Temporal(models.Model):
    """Temporal is an abstract base class for things that can be placed on a timeline.
    """

    # An Instant will have only a start date. Spans have a start and end.
    time_type = models.TextField(_("Time type"), choices=(("span", "Span"), ("instant", "Instant")), default="span")

    # NOTE: Timeline.js breaks time down into separate hr, min, sec, ms fields.
    # An event must have a year to be placed on a timeline.
    # Date fields are broken out to make it easier to enter e.g. just a year.
    # Dates are optional. Missing dates are treated as "unknown".
    start_year = models.IntegerField(_("start year"), blank=True, null=True)
    start_month = models.IntegerField(_("start month"), blank=True, null=True)
    start_day = models.IntegerField(_("start day"), blank=True, null=True)
    start_time = models.TimeField(_("start time"), auto_now=False, auto_now_add=False, blank=True, null=True)

    end_year = models.IntegerField(_("end year"), blank=True, null=True)
    end_month = models.IntegerField(_("end month"), blank=True, null=True)
    end_day = models.IntegerField(_("end day"), blank=True, null=True)
    end_time = models.TimeField(_("end time"), auto_now=False, auto_now_add=False, blank=True, null=True)

    class Meta:
        abstract = True
        indexes = [
            models.Index(fields=["start_year", "start_month", "start_day", "start_time"]),
            models.Index(fields=["end_year", "end_month", "end_day", "end_time"]),
        ]
        # Ordering does not accept index names, only column names
        ordering = [
            "start_year",
            "start_month",
            "start_day",
            "start_time",
            "end_year",
            "end_month",
            "end_day",
            "end_time",
        ]


class Reference(models.Model):

    url = models.URLField(_("url"), max_length=255)
    cite = models.CharField(_("cite"), max_length=255)

    class Meta:
        verbose_name = _("reference")
        verbose_name_plural = _("references")

    def __str__(self):
        return self.cite

    def get_absolute_url(self):
        return reverse("reference_detail", kwargs={"pk": self.pk})


class World(models.Model):
    """World is the top of the food chain.

    Everything lives inside a world, and so everything has a link to a world.
    """

    name = models.CharField(_("name"), max_length=255)
    slug = models.SlugField(_("slug"), max_length=255)

    class Meta:
        verbose_name = _("world")
        verbose_name_plural = _("worlds")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("world_detail", kwargs={"slug": self.slug})


# TODO Add geographic framework
class Place(geomodels.Model):

    world = models.ForeignKey("worlds.world", on_delete=models.CASCADE)
    name = models.CharField(_("name"), max_length=255)
    slug = models.SlugField(_("slug"), max_length=255)
    notes = models.TextField(_("notes"), blank=True, null=True)
    tags = TaggableManager(blank=True)

    point_location = geomodels.PointField(_("point location"), blank=True, null=True)
    geo_detail = geomodels.MultiPolygonField(_("detailed geography"), blank=True, null=True)

    class Meta:
        verbose_name = _("place")
        verbose_name_plural = _("places")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("place_detail", kwargs={"slug": self.slug})


class Setting(models.Model):

    world = models.ForeignKey("worlds.World", on_delete=models.CASCADE)
    name = models.CharField(_("name"), max_length=255)
    slug = models.SlugField(_("slug"), max_length=255)
    notes = models.TextField(_("notes"), blank=True, null=True)
    tags = TaggableManager(blank=True)

    class Meta:
        verbose_name = _("setting")
        verbose_name_plural = _("settings")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("setting_detail", kwargs={"slug": self.slug})


class Event(Temporal):
    """Event is an occurrence at a fixed place and time (even if place and time are unknown)."""

    world = models.ForeignKey("worlds.World", on_delete=models.CASCADE)
    name = models.CharField(_("name"), max_length=255)
    slug = models.SlugField(_("slug"), max_length=255)
    notes = models.TextField(_("notes"), blank=True, null=True)
    tags = TaggableManager(blank=True)

    participants = models.ManyToManyField("worlds.Character", through="worlds.EventParticipation", blank=True)
    place = models.ForeignKey("worlds.Place", on_delete=models.CASCADE, blank=True, null=True)

    class Meta(Temporal.Meta):
        verbose_name = _("event")
        verbose_name_plural = _("events")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("event_detail", kwargs={"pk": self.pk})


# TODO Events should have Sources, references and/or citations
# for fact-checking.


class Organization(Temporal):

    world = models.ForeignKey("worlds.World", on_delete=models.CASCADE)
    name = models.CharField(_("name"), max_length=255)
    slug = models.SlugField(_("slug"), max_length=255)
    notes = models.TextField(_("notes"), blank=True, null=True)
    tags = TaggableManager(blank=True)

    class Meta(Temporal.Meta):
        verbose_name = _("organization")
        verbose_name_plural = _("organizations")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("organization_detail", kwargs={"slug": self.slug})


# ------------------------------------------------------------------------------
# Characters and their relationships. Family relationships are fixed, all other
# relationships are Temporal.
# ------------------------------------------------------------------------------
class FamilyTie(models.Model):
    # No automated related_names, they are configured manually
    parent = models.ForeignKey("worlds.Character", on_delete=models.CASCADE, related_name="+")
    child = models.ForeignKey("worlds.Character", on_delete=models.CASCADE, related_name="+")
    birth_order = models.IntegerField(_("birth order"), default=0)

    class Meta:
        ordering = ("birth_order",)
        verbose_name = _("familytie")
        verbose_name_plural = _("familyties")

    def __str__(self):
        return self.parent.name + " -> " + self.child.name


class Character(Temporal):
    world = models.ForeignKey("worlds.World", on_delete=models.CASCADE)
    name = models.CharField(_("name"), max_length=255)
    slug = models.SlugField(_("slug"), max_length=255)
    notes = models.TextField(_("notes"), blank=True, null=True)
    tags = TaggableManager(blank=True)

    # No automated related_names, they are configured manually
    parents = models.ManyToManyField(
        "worlds.Character",
        verbose_name=_("parents"),
        through="worlds.FamilyTie",
        through_fields=["child", "parent"],
        related_name="+",
        blank=True,
    )
    children = models.ManyToManyField(
        "worlds.Character",
        verbose_name=_("children"),
        through="worlds.FamilyTie",
        through_fields=["parent", "child"],
        related_name="+",
        blank=True,
    )

    # events through EventParticipation created from other side of relationship

    class Meta(Temporal.Meta):
        ordering = ["name"]
        verbose_name = _("character")
        verbose_name_plural = _("characters")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("character_detail", kwargs={"slug": self.slug})


class Title(Temporal):
    """Title is a fief bestowed on a character."""

    character = models.ForeignKey("worlds.Character", on_delete=models.CASCADE)
    place = models.ForeignKey("worlds.Place", on_delete=models.CASCADE)
    rank = models.CharField(_("rank"), max_length=50)

    class Meta(Temporal.Meta):
        verbose_name = _("title")
        verbose_name_plural = _("titles")

    def __str__(self):
        return self.rank + " of " + self.place.name

    def get_absolute_url(self):
        return reverse("title_detail", kwargs={"pk": self.pk})


class Honor(Temporal):

    character = models.ForeignKey("worlds.Character", on_delete=models.CASCADE)
    org = models.ForeignKey("worlds.Organization", related_name="members", on_delete=models.CASCADE)

    class Meta(Temporal.Meta):
        verbose_name = _("honor")
        verbose_name_plural = _("honors")

    def __str__(self):
        return self.org.name

    def get_absolute_url(self):
        return reverse("honor_detail", kwargs={"pk": self.pk})


class EventParticipation(Temporal):
    """Characters participate in Events via roles."""

    character = models.ForeignKey("worlds.Character", on_delete=models.CASCADE)
    event = models.ForeignKey("worlds.Event", on_delete=models.CASCADE)
    role = models.CharField(_("role"), max_length=15, blank=True, default="participant")

    class Meta(Temporal.Meta):
        verbose_name = _("event_participation")
        verbose_name_plural = _("event_participations")

    def __str__(self):
        return self.role

    def get_absolute_url(self):
        return reverse("event_participation_detail", kwargs={"pk": self.pk})


class CharacterRelationship(Temporal):
    # No automated related_names, they are configured manually
    from_char = models.ForeignKey("worlds.Character", on_delete=models.CASCADE, related_name="+")
    to_char = models.ForeignKey("worlds.Character", on_delete=models.CASCADE, related_name="+")
    rel = models.CharField(_("relation"), max_length=50)
    rev = models.CharField(_("reverse relation"), max_length=50)

    class Meta(Temporal.Meta):
        verbose_name = _("characterrelationship")
        verbose_name_plural = _("characterrelationships")
