# This script must be located in: <project_root>/<app_dir>/management/commands/
# Run it: <project_root>$ python manage.py seed

from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from notes.models import Topic, Entry


class Command(BaseCommand):
    help = "Reset and seed the database with test data"

    def handle(self, *args, **kwargs):
        test_user = "testuser"
        test_pwd = "testpass123"

        # Clear existing data
        Entry.objects.all().delete()
        Topic.objects.all().delete()
        User.objects.filter(username=test_user).delete()

        # Create test user
        user = User.objects.create_user(username=test_user, password=test_pwd)
        self.stdout.write(self.style.SUCCESS("----- USERS SEEDED -----"))

        # Create topics
        topic1 = Topic.objects.create(text="Using Virtual Environments", owner=user)
        topic2 = Topic.objects.create(text="Effective Use of Logging", owner=user)

        # Create entries
        Entry.objects.create(
            topic=topic1,
            text="Virtual environments help isolate project dependencies, "
            "preventing conflicts between packages across different projects. By "
            "creating a dedicated environment, you can manage package versions easily "
            "and keep your global Python installation clean.",
        )
        Entry.objects.create(
            topic=topic2,
            text="Instead of using print statements, the logging module offers a "
            "flexible way to record runtime information at different severity "
            "levels (debug, info, warning, error, critical). This helps track "
            "application behavior and diagnose issues in development and production "
            "environments.",
        )
        Entry.objects.create(
            topic=topic2,
            text="Catching and handling exceptions thoughtfully ensures your "
            "program can recover from unexpected errors without crashing. Use "
            "try-except blocks to manage known failure points, and avoid bare "
            "excepts to prevent masking bugs. Also, clean up resources properly using "
            "'finally' or context managers.",
        )

        self.stdout.write(self.style.SUCCESS("----- DATABASE SYNCED -----"))
