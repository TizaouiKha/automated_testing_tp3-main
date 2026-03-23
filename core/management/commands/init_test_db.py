from django.core.management.base import BaseCommand
from django.core.management import call_command
from django.contrib.auth import get_user_model

from core.models import Form, Question, FormResponse, Answer


def add_case_fill_form():
    """Public form used for the 'fill form' and 'see stats' e2e tests."""
    form = Form.objects.create(
        title="Survey Form",
        slug="survey-form",
        is_active=True,
    )
    question = Question.objects.create(
        form=form,
        label="What is your name?",
        question_type="text",
        is_required=True,
        order=1,
    )
    # Pre-existing response so the stats page is not empty
    response = FormResponse.objects.create(form=form)
    Answer.objects.create(response=response, question=question, value="Pre-existing Answer")


def add_case_private_form():
    """Private form used for the 'private form ok/denied' e2e tests."""
    form = Form.objects.create(
        title="Private Form",
        slug="private-form",
        is_active=True,
        is_private=True,
        access_token="allowed@example.com",
    )
    Question.objects.create(
        form=form,
        label="What is your secret?",
        question_type="text",
        is_required=True,
        order=1,
    )


def add_seed_data():
    add_case_fill_form()
    add_case_private_form()


class Command(BaseCommand):
    help = "Initialize test DB (flush + seed)"

    def handle(self, *args, **options):
        self.stdout.write("Empty database...")
        call_command("flush", verbosity=0, interactive=False)

        self.stdout.write("Writing test data...")

        User = get_user_model()
        User.objects.create_user(
            username="Alice",
            email="alice@example.com",
            password="password123",
        )

        add_seed_data()

        self.stdout.write(self.style.SUCCESS("Test database created!"))
