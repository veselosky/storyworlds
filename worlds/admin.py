from django.contrib import admin
from .models import World, Setting, Character, Event, Timespan, Union, EventParticipation, UnionParticipation


class EventParticipationInline(admin.TabularInline):
    model = Event.participants.through


class UnionParticipationInline(admin.TabularInline):
    model = Union.characters.through


class CharacterInline(admin.TabularInline):
    model = Character


class SettingInline(admin.StackedInline):
    model = Setting


class TimespanInline(admin.StackedInline):
    model = Timespan


@admin.register(World)
class WorldAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}


@admin.register(Setting)
class SettingAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}
    search_fields = ("name",)


@admin.register(Character)
class CharacterAdmin(admin.ModelAdmin):
    fields = ("world", ("name", "slug"), "lifetime", "parents")
    prepopulated_fields = {"slug": ("name",)}
    search_fields = ("name",)

    inlines = [UnionParticipationInline, EventParticipationInline]


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    fields = ("world", ("name", "slug"), ("year", "month", "day", "time"), "setting", "notes", "tags")
    prepopulated_fields = {"slug": ("name",)}
    search_fields = ("name",)
    inlines = [EventParticipationInline]


@admin.register(Timespan)
class TimespanAdmin(admin.ModelAdmin):
    empty_value_display = "unknown"


@admin.register(Union)
class UnionAdmin(admin.ModelAdmin):
    empty_value_display = "unknown"


@admin.register(EventParticipation)
class EventParticipationAdmin(admin.ModelAdmin):
    empty_value_display = "unknown"


@admin.register(UnionParticipation)
class UnionParticipationAdmin(admin.ModelAdmin):
    empty_value_display = "unknown"
