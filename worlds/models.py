from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from taggit.managers import TaggableManager


# ------------------------------------------------------------------------------
# Start by defining the handful of models that practically everything will use.
# ------------------------------------------------------------------------------
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
        return reverse("world_detail", kwargs={"pk": self.pk})


class Setting(models.Model):

    name = models.CharField(_("name"), max_length=255)
    slug = models.SlugField(_("slug"), max_length=255)
    notes = models.TextField(_("notes"), blank=True, null=True)

    world = models.ForeignKey("worlds.World", on_delete=models.CASCADE)
    tags = TaggableManager()

    class Meta:
        verbose_name = _("setting")
        verbose_name_plural = _("settings")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("setting_detail", kwargs={"slug": self.slug})


class Event(models.Model):
    """Event is an occurrence at a fixed place and time (even if place and time are unknown).
    """

    name = models.CharField(_("name"), max_length=255)
    slug = models.SlugField(_("slug"), max_length=255)

    # NOTE: Timeline.js breaks time down into separate hr, min, sec, ms fields.
    year = models.IntegerField(
        _("year"), blank=True, null=True, help_text=_("An event must have a year to be placed on a timeline.")
    )
    month = models.IntegerField(_("month"), blank=True, null=True)
    day = models.IntegerField(_("day"), blank=True, null=True)
    time = models.TimeField(_("time"), auto_now=False, auto_now_add=False, blank=True, null=True)

    notes = models.TextField(_("notes"), blank=True, null=True)
    # Length must be constrained to 15 for compatibility with GEDCOM. Do we care?
    # "The length of the GEDCOM TAG is a maximum of 31 characters, with the first 15 characters being unique."
    # TODO Each world may have unique event types. Event types should have a table.
    event_type = models.CharField(_("Event type"), max_length=15, blank=True, null=True)

    world = models.ForeignKey("worlds.World", on_delete=models.CASCADE)
    setting = models.ForeignKey("worlds.Setting", on_delete=models.SET_NULL, blank=True, null=True)
    participants = models.ManyToManyField("Character", through="EventParticipation")

    tags = TaggableManager(blank=True)

    class Meta:
        verbose_name = _("event")
        verbose_name_plural = _("events")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("event_detail", kwargs={"pk": self.pk})


class Timespan(models.Model):

    name = models.CharField(_("name"), max_length=255)
    notes = models.TextField(_("notes"), blank=True, null=True)

    world = models.ForeignKey("worlds.World", on_delete=models.CASCADE)
    start = models.ForeignKey("worlds.Event", on_delete=models.SET_NULL, blank=True, null=True, related_name="+")
    end = models.ForeignKey("worlds.Event", on_delete=models.SET_NULL, blank=True, null=True, related_name="+")

    tags = TaggableManager(blank=True)

    class Meta:
        verbose_name = _("timespan")
        verbose_name_plural = _("timespans")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("timespan_detail", kwargs={"pk": self.pk})


# TODO Events and Timespans should have Sources, references and/or citations
# for fact-checking.

# ------------------------------------------------------------------------------
# Characters and their relationships
# ------------------------------------------------------------------------------
class Union(models.Model):
    """A union between characters that did or could result in offspring.

    Equivalent to GEDCOM Family. Characters are linked to their parents through
    Unions. Tracing these links is how family trees are generated.
    """

    union_type = models.CharField(_("Union type"), max_length=15, default="Marriage")
    timespan = models.ForeignKey("worlds.Timespan", on_delete=models.SET_NULL, blank=True, null=True)
    notes = models.TextField(_("notes"), blank=True, null=True)

    characters = models.ManyToManyField("worlds.Character", through="UnionParticipation")

    tags = TaggableManager(blank=True)

    class Meta:
        verbose_name = _("union")
        verbose_name_plural = _("unions")

    def __str__(self):
        return " and ".join(c.name for c in self.characters)

    def get_absolute_url(self):
        return reverse("union_detail", kwargs={"pk": self.pk})


class Character(models.Model):

    name = models.CharField(_("Common name (how it will normally be displayed)"), max_length=255)
    slug = models.SlugField(_("slug"))
    notes = models.TextField(_("notes"), blank=True, null=True)

    world = models.ForeignKey("worlds.World", on_delete=models.CASCADE)
    lifetime = models.ForeignKey("worlds.Timespan", on_delete=models.SET_NULL, blank=True, null=True)
    parents = models.ForeignKey(
        "worlds.Union", on_delete=models.SET_NULL, blank=True, null=True, related_name="children"
    )

    unions = models.ManyToManyField("worlds.Union", through="UnionParticipation")
    # events through EventParticipation created from other side of relationship

    tags = TaggableManager(blank=True)

    class Meta:
        verbose_name = _("character")
        verbose_name_plural = _("characters")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("character_detail", kwargs={"slug": self.slug})


class EventParticipation(models.Model):
    """Characters participate in Events via roles.
    """

    character = models.ForeignKey("worlds.Character", on_delete=models.CASCADE)
    event = models.ForeignKey("worlds.Event", on_delete=models.CASCADE)
    role = models.CharField(_("role"), max_length=15, blank=True, default="Primary")
    notes = models.TextField(_("notes"), blank=True, null=True)

    class Meta:
        verbose_name = _("event_participation")
        verbose_name_plural = _("event_participations")

    def __str__(self):
        return self.role

    def get_absolute_url(self):
        return reverse("event_participation_detail", kwargs={"pk": self.pk})


class UnionParticipation(models.Model):
    """Characters participate in Unions via roles.

    There can be many participants in a Union. This allows modeling unconventional
    union types, like a species with three sexes, or a couple and a surrogate mother.
    """

    character = models.ForeignKey("worlds.Character", on_delete=models.CASCADE)
    union = models.ForeignKey("worlds.Union", on_delete=models.CASCADE)
    timespan = models.ForeignKey("worlds.Timespan", on_delete=models.SET_NULL, blank=True, null=True)
    role = models.CharField(_("role"), max_length=15, blank=True, default="Spouse")
    notes = models.TextField(_("notes"), blank=True, null=True)

    class Meta:
        constraints = [models.UniqueConstraint(fields=["character", "union"], name="character_union")]
        verbose_name = _("union_participation")
        verbose_name_plural = _("union_participations")

    def __str__(self):
        return self.role

    def get_absolute_url(self):
        return reverse("union_participation_detail", kwargs={"pk": self.pk})
