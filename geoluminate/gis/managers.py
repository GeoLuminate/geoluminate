from django.contrib.gis.db import models as geomodels
from django.contrib.gis.utils import LayerMapping
import os
from django.db.models.query import QuerySet
from django.contrib.postgres.aggregates import JSONBAgg
from geoluminate.gis.db_functions import AsGeoFeature

DATA_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), 'data'))


class SiteManager(QuerySet):

    def get_feature(*args, **kwargs):
        return self.annotate(feature=AsGeoFeature(*args)).get(*args, **kwargs)

    def features(self, *args):
        if not args:
            args = [f.name for f in self.model._meta.fields]
        return self.annotate(feature=AsGeoFeature(*args))

    def feature_collection(self, *args):
        return self.features(*args).aggregate(features=JSONBAgg('feature'))

    def as_feature_collection(self, *args):
        """Converts a queryset in a geojson spec FeatureCollection"""
        return dict(type='FeatureCollection', **self.feature_collection())


class GISManager(geomodels.Manager):

    def count_in(self, model, field='geom'):
        for instance in self.model.objects.all():
            sites = model.objects.filter(**{f'{field}__within': instance.poly})
            print(f"{sites.count()} {model._meta.verbose_name}/s within {instance}")
            instance.sites.add(*sites)

    def load(self, data_dir, verbose=True, strict=True, transform=False):
        data_folder = os.path.join(DATA_DIR, data_dir)
        # data_folder = data_dir
        shp_file = [f for f in os.listdir(data_folder) if f.endswith('.shp')]
        if len(shp_file) == 1:
            lm = LayerMapping(self.model,
                              os.path.join(
                                  data_folder,
                                  shp_file[0]),
                              self.model.mapping,
                              transform=transform)
            lm.save(strict=strict, verbose=verbose)
        elif len(shp_file) > 1:
            raise ValueError('Multiple shapefiles found in directory')
        else:
            raise ValueError('No shapefiles found in directory')
