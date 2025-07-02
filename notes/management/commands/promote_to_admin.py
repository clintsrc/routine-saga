# pylint: disable=W0613
#
# Granting Admin access: http://<url>/admin/
#   <project_root>$ python manage.py promote_to_admin username
#

from django.core.management.base import BaseCommand
from django.contrib.auth.models import User


class Command(BaseCommand):
    help = "Promote a user to admin"

    def add_arguments(self, parser):
        parser.add_argument("username", type=str, help="Username to promote")

    def handle(self, *args, **options):
        username = options["username"]
        try:
            user = User.objects.get(username=username)
            user.is_staff = True
            user.is_superuser = True
            user.save()
            self.stdout.write(self.style.SUCCESS(f"User {username} promoted to admin."))
        except User.DoesNotExist:
            self.stdout.write(self.style.ERROR(f"User {username} does not exist."))
