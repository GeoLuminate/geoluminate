from django.contrib.gis.db import models
from django.contrib.gis.geos import Point
from django.contrib.gis.measure import Distance
from django.urls import reverse
from django.utils.encoding import force_str
from django.utils.translation import gettext_lazy as _

from geoluminate.db.fields import RangeField
from geoluminate.db.models import Base

from .managers import SiteManager


class AbstractSite(Base):
    """An abstract GIS class for building more complex concrete models."""

    geom_precision = 5

    objects = SiteManager.as_manager()

    IGSN = models.IntegerField(
        "IGSN",
        help_text=_("An International Generic Sample Number for the site."),
        blank=True,
        null=True,
    )

    geom = models.PointField()
    name = models.CharField(
        verbose_name=_("name"),
        null=True,
        help_text=_("Specified site name for the related database entry"),
        max_length=255,
    )
    elevation = RangeField(
        _("elevation (m)"),
        help_text=_("elevation with reference to mean sea level (m)"),
        max_value=9000,
        min_value=-12000,
        blank=True,
        null=True,
    )
    # admin_0
    # admin_1
    # ocean/water_body
    # geographic_region

    # include shapefile info such as country, continent, etc. here?

    class Meta:
        abstract = True
        verbose_name = _("Geographic site")
        verbose_name_plural = _("Geographic sites")
        default_related_name = "sites"
        db_table = "geographic_site"

    def save(self, *args, **kwargs):
        # round coordinates to the specified precision
        # self.lat = round(self.lat, self.geom_precision)
        # self.lon = round(self.lon, self.geom_precision)
        return super().save(*args, **kwargs)

    @property
    def latitude(self):
        """Convenience method for retrieving the site's latitude ordinate.

        Returns:
            Float: the site latitude
        """
        return self.geom.y

    @latitude.setter
    def latitude(self, val):
        self.geom.y = val

    @property
    def longitude(self):
        """Convenience method for retrieving the site's longitude ordinate.

        Returns:
            Float: the site longitude
        """
        return self.geom.x

    @longitude.setter
    def longitude(self, val):
        self.geom.x = val

    @property
    def lon(self):
        """Alias of self.longitude"""
        return self.longitude

    @lon.setter
    def lon(self, val):
        self.geom.x = val

    @property
    def lat(self):
        """Alias of self.latitude"""
        return self.latitude

    @lat.setter
    def lat(self, val):
        self.geom.y = val

    def __unicode__(self):
        return "%s" % (self.name)

    def __str__(self):
        if self.name:
            return force_str(self.name)
        elif self.geom:
            return f"{self.lat}, {self.lon}"
        return self._meta.verbose_name

    def get_absolute_url(self):
        return reverse("site", kwargs={"pk": self.pk})

    def nearby(self, radius=25):
        """Gets nearby sites within x km radius"""
        Point(self.lon, self.lat)
        return self.objects.filter(geom__distance_lt=(self.geom, Distance(km=radius)))

    # def project_location2utm(self):
    #     """
    #     project location coordinates into meters given the reference ellipsoid,
    #     for now that is constrained to WGS84

    #     Returns East, North, Zone
    #     """
    #     utm_point = gis_tools.project_point_ll2utm(self._latitude, self._longitude, datum=self.datum)

    #     self.easting = utm_point[0]
    #     self.northing = utm_point[1]
    #     self.utm_zone = utm_point[2]

    # def utm_zone(self):
    #     """
    #     Gets the utm zone for the given site geom

    #     :param latitude: latitude in [ 'DD:mm:ss.ms' | 'DD.decimal' | float ]
    #     :type latitude: [ string | float ]

    #     :param longitude: longitude in [ 'DD:mm:ss.ms' | 'DD.decimal' | float ]
    #     :type longitude: [ string | float ]

    #     :return: zone number
    #     :rtype: int

    #     :return: is northern
    #     :rtype: [ True | False ]

    #     :return: UTM zone
    #     :rtype: string

    #     :Example: ::

    #         >>> lat, lon = ('-34:17:57.99', 149.2010301)
    #         >>> zone_number, is_northing, utm_zone = gis_tools.get_utm_zone(lat, lon)
    #         >>> print(zone_number, is_northing, utm_zone)
    #         (55, False, '55H')
    #     """

    #     zone_number = int(1 + (self.lon + 180.0) / 6.0)
    #     is_northern = bool(self.lat >= 0)
    #     n_str = self.get_utm_letter()

    #     return zone_number, is_northern, f"{zone_number:02.0f}{n_str}"

    # def _get_utm_letter(self):
    #     """Get the UTM zone letter designation for a given latitude"""
    #     utm_letters = {
    #         "C": (-80, -72),
    #         "D": (-72, -64),
    #         "E": (-64, -56),
    #         "F": (-56, -48),
    #         "G": (-48, -40),
    #         "H": (-40, -32),
    #         "J": (-32, -24),
    #         "K": (-24, -16),
    #         "L": (-16, -8),
    #         "M": (-8, 0),
    #         "N": (0, 8),
    #         "P": (8, 16),
    #         "Q": (16, 24),
    #         "R": (24, 32),
    #         "S": (32, 40),
    #         "T": (40, 48),
    #         "U": (48, 56),
    #         "V": (56, 64),
    #         "W": (64, 72),
    #         "X": (72, 84),
    #     }

    #     for key, value in utm_letters.items():
    #         if value[1] >= self.lat >= value[0]:
    #             return key

    #     return "Z"
