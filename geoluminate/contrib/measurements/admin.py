from django.contrib.gis import admin
from polymorphic.admin import PolymorphicChildModelAdmin, PolymorphicChildModelFilter, PolymorphicParentModelAdmin

from geoluminate.utils import get_subclasses

from .models import Date, Description, Measurement


class DescriptionInline(admin.TabularInline):
    model = Description
    fields = ["type", "text"]
    extra = 0
    max_num = 2


class DateInline(admin.TabularInline):
    model = Date
    extra = 0
    fields = ["type", "date"]


@admin.register(Measurement)
class MeasurementParentAdmin(PolymorphicParentModelAdmin):
    base_model = Measurement
    child_models = get_subclasses(Measurement, include_self=False)
    list_filter = (PolymorphicChildModelFilter,)


class MeasurementAdmin(PolymorphicChildModelAdmin):
    base_model = Measurement
    inlines = [DescriptionInline, DateInline]
