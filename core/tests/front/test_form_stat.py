import pytest
from selenium.webdriver.common.by import By

from core.models import Form, Question, FormResponse, Answer


@pytest.fixture
def form_with_responses(db):
    form = Form.objects.create(title="Test Form", slug="test-form", is_active=True)
    question = Question.objects.create(
        form=form, label="Your name?", question_type="text", is_required=True, order=1
    )

    r1 = FormResponse.objects.create(form=form)
    Answer.objects.create(response=r1, question=question, value="Alice")

    r2 = FormResponse.objects.create(form=form)
    Answer.objects.create(response=r2, question=question, value="Bob")

    return form


def test_form_stat(selenium, live_server, form_with_responses):
    """
    Given a form with 2 responses
    When Alice goes to the stats page
    Then she sees 2 responses and all answers given
    """
    form = form_with_responses
    selenium.get(f"{live_server.url}/forms/{form.slug}/stats/")

    body = selenium.find_element(By.TAG_NAME, "body")
    assert "2" in body.text
    assert "Alice" in body.text
    assert "Bob" in body.text
