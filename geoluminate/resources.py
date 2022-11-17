from import_export.resources import ModelResource
from django.utils.html import mark_safe
from tqdm import tqdm
from .widgets import ChoiceForeignKey, ChoiceManyToMany
from geoluminate.fields import ChoiceFieldBase


class ResourceMixin(ModelResource):
    """A mixin for django import export that displays a progress bar, prints an import summary to console and
        cleans the result by removing unneccesary columns"""

    WIDGETS_MAP = ModelResource.WIDGETS_MAP
    WIDGETS_MAP.update(**{
        "ChoicesOneToOne": ChoiceForeignKey,
        "ChoicesForeignKey": ChoiceForeignKey,
        "ChoicesManyToMany": ChoiceManyToMany,
    })

    @classmethod
    def field_from_django_field(cls, field_name, django_field, readonly):
        """
        Returns a Resource Field instance for the given Django model field.
        """

        FieldWidget = cls.widget_from_django_field(django_field)
        widget_kwargs = cls.widget_kwargs_for_field(field_name)
        if issubclass(django_field.__class__, ChoiceFieldBase):
            widget_kwargs.update(type=django_field.get_choice())
        field = cls.DEFAULT_RESOURCE_FIELD(
            attribute=field_name,
            column_name=field_name,
            widget=FieldWidget(**widget_kwargs),
            readonly=readonly,
            default=django_field.default,
        )
        return field

    def before_import(self, dataset, using_transactions, dry_run, **kwargs):
        self.pbar = tqdm(total=len(dataset))

    def after_import_row(self, row, row_result, **kwargs):
        self.pbar.update(1)

    def after_import(self, dataset, result,
                     using_transactions, dry_run, **kwargs):
        print('Import Summary:')
        for key, count in result.totals.items():
            if count:
                print('\t', key, ': ', count)

    def clean_result(self, result):
        """Cleans up the html diff by removing columns with no information"""
        # find the columns that do not contain any data and store the index
        remove_these = []
        if result.has_validation_errors():
            # loop through each column of the result
            for i, header in enumerate(result.diff_headers.copy()):
                has_data = False
                # look at each value in the column
                for row in result.invalid_rows:
                    if row.values:
                        # Applies a html background to field specific errors to
                        # help user identify issues
                        if header in row.field_specific_errors.keys():
                            row.values = list(row.values)
                            row.values[i] = mark_safe(
                                '<span class="bg-danger">{}</span>'.format(row.values[i]))
                        # if a values is found in this column then mark it as
                        # containing data
                        if row.values[i] and row.values[i] != '---':
                            has_data = True
                            break
                # if no data was found in the column, delete it
                if not has_data:
                    remove_these.append(i)
                    # result.diff_headers.remove(header)

            # result.diff_headers.pop()
            for i in sorted(remove_these, reverse=True):
                result.diff_headers.pop(i)
                for row in result.invalid_rows:

                    row.values = list(row.values)
                    row.values.pop(i)
                    # row.values.pop()

        else:
            for i, header in enumerate(result.diff_headers.copy()):
                has_data = False
                for row in result.rows:
                    if row.diff:
                        if row.diff[i]:
                            has_data = True
                            break
                if not has_data:
                    remove_these.append(i)

            for i in sorted(remove_these, reverse=True):
                result.diff_headers.pop(i)
                for row in result.rows:
                    # remove stored indices from each row of the result
                    if row.diff:
                        del row.diff[i]

        result.diff_headers = [
            h.replace(
                '_',
                ' ').capitalize() for h in result.diff_headers]
