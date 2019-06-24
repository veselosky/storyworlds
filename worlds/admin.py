from adminsortable2.admin import SortableInlineAdminMixin
from django.contrib import admin
from django.contrib.gis import admin as geoadmin

from .models import (
    Character,
    Event,
    EventParticipation,
    FamilyTie,
    Honor,
    Organization,
    Place,
    Reference,
    Setting,
    Title,
    World,
)


# ======================================================================
# Inlines used in entity admins
# ======================================================================
class EventParticipationInline(admin.TabularInline):
    model = Event.participants.through
    # For the inline, just show and allow the event association. To edit timespans
    # or other properties, go to the Event Participation admin.
    fields = ("character", "role")


class ChildrenInline(SortableInlineAdminMixin, admin.TabularInline):
    model = Character.children.through
    fk_name = "parent"  # Relations where the current character is parent
    extra = 1


class ParentsInline(SortableInlineAdminMixin, admin.TabularInline):
    model = Character.parents.through
    fk_name = "child"  # Relations where the current character is child
    extra = 1


class HonorsInline(admin.TabularInline):
    model = Honor
    extra = 1
    fields = ("org", "start_year", "start_month", "start_day", "end_year", "end_month", "end_day")


class CharacterTitlesInline(admin.TabularInline):
    model = Title
    extra = 1


class ReferencesInline(admin.TabularInline):
    model = Reference
    extra = 1


# ======================================================================
# Admins for primary entities
# ======================================================================
@admin.register(World)
class WorldAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}


@admin.register(Place)
class PlaceAdmin(geoadmin.OSMGeoAdmin):
    prepopulated_fields = {"slug": ("name",)}
    search_fields = ("name",)


@admin.register(Setting)
class SettingAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}
    search_fields = ("name",)


@admin.register(Organization)
class OrgAdmin(geoadmin.OSMGeoAdmin):
    fields = (
        "world",
        ("name", "slug"),
        "time_type",
        ("start_year", "start_month", "start_day", "start_time"),
        ("end_year", "end_month", "end_day", "end_time"),
        "tags",
        "notes",
    )
    prepopulated_fields = {"slug": ("name",)}
    search_fields = ("name",)


@admin.register(Character)
class CharacterAdmin(admin.ModelAdmin):
    fields = (
        "world",
        ("name", "slug"),
        ("start_year", "start_month", "start_day", "start_time"),
        ("end_year", "end_month", "end_day", "end_time"),
        "tags",
        "notes",
    )
    prepopulated_fields = {"slug": ("name",)}
    search_fields = ("name",)

    inlines = [ParentsInline, ChildrenInline, CharacterTitlesInline, HonorsInline]


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    fields = (
        "world",
        ("name", "slug"),
        "time_type",
        ("start_year", "start_month", "start_day", "start_time"),
        ("end_year", "end_month", "end_day", "end_time"),
        "place",
        "tags",
        "notes",
    )
    prepopulated_fields = {"slug": ("name",)}
    search_fields = ("name",)
    inlines = [EventParticipationInline]

    list_display = ("start_year", "start_month", "start_day", "name")
    list_display_links = ("name",)


@admin.register(EventParticipation)
class EventParticipationAdmin(admin.ModelAdmin):
    empty_value_display = "unknown"


@admin.register(FamilyTie)
class FamilyTieAdmin(admin.ModelAdmin):
    empty_value_display = "unknown"


@admin.register(Reference)
class ReferenceAdmin(admin.ModelAdmin):
    pass
