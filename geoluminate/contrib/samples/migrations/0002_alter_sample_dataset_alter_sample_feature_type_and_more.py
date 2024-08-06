# Generated by Django 5.0.6 on 2024-07-30 12:21

import django.db.models.deletion
import geoluminate.contrib.samples.choices
import research_vocabs.fields
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("datasets", "0003_alter_contribution_roles"),
        ("samples", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="sample",
            name="dataset",
            field=models.ForeignKey(
                help_text="The dataset for which this sample was collected.",
                on_delete=django.db.models.deletion.CASCADE,
                related_name="samples",
                to="datasets.dataset",
                verbose_name="dataset",
            ),
        ),
        migrations.AlterField(
            model_name="sample",
            name="feature_type",
            field=research_vocabs.fields.ConceptField(
                default="site",
                verbose_name="feature",
                vocabulary=geoluminate.contrib.samples.choices.FeatureType,
            ),
        ),
        migrations.AlterField(
            model_name="sample",
            name="medium",
            field=research_vocabs.fields.ConceptField(
                default="solid",
                verbose_name="medium",
                vocabulary=geoluminate.contrib.samples.choices.SamplingMedium,
            ),
        ),
        migrations.AlterField(
            model_name="sample",
            name="parent",
            field=models.ForeignKey(
                blank=True,
                help_text="The sample from which this sample was derived.",
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="samples.sample",
                verbose_name="parent sample",
            ),
        ),
        migrations.AlterField(
            model_name="sample",
            name="specimen_type",
            field=research_vocabs.fields.ConceptField(
                default="theSpecimenTypeIsUnknown",
                verbose_name="specimen",
                vocabulary=geoluminate.contrib.samples.choices.SpecimenType,
            ),
        ),
        migrations.AlterField(
            model_name="sample",
            name="status",
            field=research_vocabs.fields.ConceptField(
                default="unknown",
                verbose_name="status",
                vocabulary=geoluminate.contrib.samples.choices.SampleStatus,
            ),
        ),
    ]
