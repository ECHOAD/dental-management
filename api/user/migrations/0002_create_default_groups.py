from django.db import migrations

GROUP_NAMES = ["Admin", "Dentist", "Assistant"]


def create_groups(apps, schema_editor):
    Group = apps.get_model("auth", "Group")
    for name in GROUP_NAMES:
        Group.objects.get_or_create(name=name)

def delete_groups(apps, schema_editor):
    Group = apps.get_model("auth", "Group")
    Group.objects.filter(name__in=GROUP_NAMES).delete()

class Migration(migrations.Migration):

    dependencies = [
        ("user", "0001_initial"),
    ]

    operations = [
        migrations.RunPython(create_groups, delete_groups),
    ]