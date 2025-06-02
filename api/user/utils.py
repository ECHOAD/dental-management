from typing import Type, Optional
from django.contrib.auth.models import AbstractUser
from django.db.models import Model, QuerySet
from django.apps import apps


def get_dentist_from_user(user):
    if user.groups.filter(name="Assistant").exists():
        try:
            dentist = user.assistant_profile.dentist
            if not dentist:
                raise Exception("The assistant does not have an assigned dentist.")
            return dentist
        except AttributeError:
            raise Exception("The assistant does not have a dentist profile configured.")
    elif user.groups.filter(name__in=["Dentist", "Admin"]).exists():
        return user
    else:
        raise Exception("User is not authorized to perform this action.")


def get_queryset_for_user(
        user: AbstractUser,
        model_ref: str,
        user_field: str
) -> QuerySet:
    """Get a queryset for the given user based on their group membership."""

    model_class = apps.get_model(*model_ref.split('.'))

    if user.groups.filter(name="Admin").exists():
        return model_class.objects.all()

    if user.groups.filter(name="Dentist").exists():
        return model_class.objects.filter(**{user_field: user})

    if user.groups.filter(name="Assistant").exists():
        assigned_dentist = getattr(user, "assigned_dentist", None)
        if assigned_dentist:
            return model_class.objects.filter(**{user_field: assigned_dentist})

    return model_class.objects.all()
