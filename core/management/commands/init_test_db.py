from django.core.management.base import BaseCommand
from django.core.management import call_command
from django.contrib.auth import get_user_model
from core.models import Form

class Command(BaseCommand):
    help = "Initialize test DB (flush + seed)"

    def handle(self, *args, **options):
        self.stdout.write("Empty database...")
        call_command("flush", verbosity=0, interactive=False)

        self.stdout.write("Writing test data test...")

        User = get_user_model()
        user = User.objects.create_user(
            username="Alice",
            email="alice@example.com",
            password="password123",
        )
        user.save()

        # Crée des questions et réponses de test
        form = Form(
            title="Hello", 
            slug="test_1",
        )
        form.save()

        self.stdout.write(self.style.SUCCESS("Test database created !"))
