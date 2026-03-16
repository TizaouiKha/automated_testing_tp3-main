import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from core.models import Form, Question


# ---------------------------------------------------------------------------
# Page Object
# ---------------------------------------------------------------------------

class FormPage:
    def __init__(self, selenium, live_server, form):
        self.selenium = selenium
        self.selenium.get(f"{live_server.url}/forms/{form.slug}/")

    def get_input(self, question):
        return self.selenium.find_element(By.ID, f"question_{question.id}")

    def get_error(self, question):
        return self.selenium.find_element(By.ID, f"error_{question.id}")

    def write_in_input(self, question, text):
        field = self.get_input(question)
        field.send_keys(text)
        field.send_keys(Keys.TAB)

    def assert_has_error(self, question, message):
        error = self.get_error(question)
        WebDriverWait(self.selenium, 3).until(EC.visibility_of(error))
        assert error.is_displayed()
        assert error.text == message

    def assert_no_error(self, question):
        error = self.get_error(question)
        WebDriverWait(self.selenium, 3).until(EC.invisibility_of_element(error))
        assert not error.is_displayed()


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

@pytest.fixture
def required_name_form(db):
    """A published form with a single required text question."""
    form = Form.objects.create(
        title="Test Form",
        slug="test-required-field",
        is_active=True,
    )
    Question.objects.create(
        form=form,
        label="What is your name?",
        question_type="text",
        is_required=True,
        order=1,
    )
    return form


@pytest.fixture
def email_form(db):
    """A form with a single email question."""
    form = Form.objects.create(
        title="Email Form",
        slug="test-email-field",
        is_active=True,
    )
    Question.objects.create(
        form=form,
        label="What is your email?",
        question_type="email",
        is_required=True,
        order=1,
    )
    return form


@pytest.fixture
def phone_form(db):
    """A form with a single phone number question."""
    form = Form.objects.create(
        title="Phone Form",
        slug="test-phone-field",
        is_active=True,
    )
    Question.objects.create(
        form=form,
        label="What is your phone number?",
        question_type="phone_number",
        is_required=True,
        order=1,
    )
    return form


def test_mandatory_field__ok(selenium, live_server, required_name_form):
    """
    Given a mandatory question "What is your name?"
    When question is replied
    Then no error is shown
    """
    question = required_name_form.questions.first()
    page = FormPage(selenium, live_server, required_name_form)
    page.write_in_input(question, "Alice")
    page.assert_no_error(question)


def test_mandatory_field__error_shown(selenium, live_server, required_name_form):
    """
    Given a mandatory question "What is your name?"
    When question is not replied
    Then error message is shown
    """
    question = required_name_form.questions.first()
    page = FormPage(selenium, live_server, required_name_form)
    page.write_in_input(question, "")
    page.assert_has_error(question, "Mandatory field")


def test_email_field__error(selenium, live_server, email_form):
    """
    Given an email question
    When the user types "bob" (invalid email)
    Then "Invalid email address" is displayed
    """
    question = email_form.questions.first()
    page = FormPage(selenium, live_server, email_form)
    page.write_in_input(question, "bob")
    page.assert_has_error(question, "Invalid email address")


def test_email_field__ok(selenium, live_server, email_form):
    """
    Given an email question
    When the user types a valid email
    Then no error is displayed
    """
    question = email_form.questions.first()
    page = FormPage(selenium, live_server, email_form)
    page.write_in_input(question, "alice@example.com")
    page.assert_no_error(question)


def test_field_phone_number__error(selenium, live_server, phone_form):
    """
    Given a phone number question
    When the user types an invalid phone number
    Then "Invalid phone number" is displayed
    """
    question = phone_form.questions.first()
    page = FormPage(selenium, live_server, phone_form)
    page.write_in_input(question, "abc-def")
    page.assert_has_error(question, "Invalid phone number")


def test_field_phone_number__ok(selenium, live_server, phone_form):
    """
    Given a phone number question
    When the user types a valid phone number
    Then no error is displayed
    """
    question = phone_form.questions.first()
    page = FormPage(selenium, live_server, phone_form)
    page.write_in_input(question, "+33 06-12-34-56-78")
    page.assert_no_error(question)

def test_private_form__ok(selenium, live_server, db):
    """
    Given a private form with a single text question
    When the user accesses the form with the correct token
    Then the form is displayed
    """
    form = Form.objects.create(
        title="Private Form",
        slug="test-private-form",
        is_active=True,
        is_private=True,
        access_token="secret-token",
    )
    Question.objects.create(
        form=form,
        label="What is your secret?",
        question_type="text",
        is_required=True,
        order=1,
    )
    selenium.get(f"{live_server.url}/forms/{form.slug}/?token=secret-token")
    input_field = selenium.find_element(By.ID, f"question_{form.questions.first().id}")
    assert input_field.is_displayed()


def test_private_form__denied(selenium, live_server, db):
    """
    Given a private form
    When the user accesses the form with a wrong token
    Then "access denied" is displayed
    """
    form = Form.objects.create(
        title="Private Form",
        slug="test-private-form-denied",
        is_active=True,
        is_private=True,
        access_token="secret-token",
    )
    selenium.get(f"{live_server.url}/forms/{form.slug}/?token=wrong-token")
    body = selenium.find_element(By.TAG_NAME, "body")
    assert "access denied" in body.text.lower()