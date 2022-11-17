from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db.models import Q
from django.apps import apps
from django.db.models import OneToOneField, ForeignKey, ManyToManyField


class ChoiceFieldBase:
    """Field mixin that allows choice to be defined in a tree structure
    """

    def __init__(self, verbose_name=None, choice_type=None,
                 allow_unspec=True, *args, **kwargs):
        """
        Args:
            verbose_name (_type_, optional): _description_. Defaults to None.
            root_code (str): Must match a value in the 'code' field of
            `database.models.Choice`. This is used to restrict the available
            choices for this field by limiting it to the
            matching node and all descendants.
            allow_unspec (bool, optional): Setting allow_unspec to False will
            prevent users being able to select "unspecified" as a value.
            Defaults to True.
        """
        kwargs['to'] = "database.Choice"
        kwargs['limit_choices_to'] = self.choice_limiter
        kwargs['related_name'] = '+'
        kwargs['verbose_name'] = verbose_name
        self.choice_type = choice_type
        self.allow_unspecified = allow_unspec
        super().__init__(*args, **kwargs)

    def get_choice(self):
        return self.choice_type if self.choice_type else self.name

    def choice_limiter(self):
        return Q(type=self.get_choice())

    def deconstruct(self):
        name, path, args, kwargs = super().deconstruct()
        if "limit_choices_to" in kwargs:
            del kwargs['limit_choices_to']
        return name, path, args, kwargs


class ChoicesOneToOne(ChoiceFieldBase, OneToOneField):
    """Defines a one-to-one relationship with `database.models.Choice`
    """
    pass


class ChoicesForeignKey(ChoiceFieldBase, ForeignKey):
    """Defines a foreign relationship with `database.models.Choice`
    """
    pass


class ChoicesManyToMany(ChoiceFieldBase, ManyToManyField):
    """Defines a many-to-many relationship with `database.models.Choice`
    """
    pass


class RangeField(models.FloatField):

    def __init__(self, *args, **kwargs):

        validators = kwargs.pop('validators', [])

        if kwargs.get('max_value') is not None:
            validators.append(MaxValueValidator(kwargs.pop('max_value')))

        if kwargs.get('min_value') is not None:
            validators.append(MinValueValidator(kwargs.pop('min_value')))

        super().__init__(validators=validators, *args, **kwargs)
