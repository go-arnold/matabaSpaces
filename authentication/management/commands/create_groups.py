from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from park.models import FoundObject

class Command(BaseCommand):
    help = 'Create default groups and assign permissions'

    def handle(self, *args, **options):
        # Création des groupes
        super_admin_group, _ = Group.objects.get_or_create(name='SuperAdmin')
        parking_manager_group, _ = Group.objects.get_or_create(name='ParkingManager')
        user_group, _ = Group.objects.get_or_create(name='User')

        # Attribution des permissions spécifiques
        content_type_found_object = ContentType.objects.get_for_model(FoundObject)

        # Créer les permissions et extraire uniquement les objets de permission
        permissions = [
            Permission.objects.get_or_create(codename='view_foundobject', name='Can view found object', content_type=content_type_found_object)[0],
            Permission.objects.get_or_create(codename='add_foundobject', name='Can add found object', content_type=content_type_found_object)[0],
            Permission.objects.get_or_create(codename='delete_foundobject', name='Can delete found object', content_type=content_type_found_object)[0],
        ]

        super_admin_group.permissions.add(*permissions)
        parking_manager_group.permissions.add(*permissions)

        self.stdout.write(self.style.SUCCESS('Successfully created groups and assigned permissions'))
