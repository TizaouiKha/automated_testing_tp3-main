from django.contrib.auth.models import User
import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from core.models import Form, Question


@pytest.fixture
def user(db):
    return User.objects.create_user(username="alice", password="password123")


def test_user_can_create_form_with_question(selenium, live_server, user):
    """
    Given a registered user
    When  they log in and submit the create form page with a question
    Then  the form and its question are persisted in the database
    """
    # ── Given: user logs in ────────────────────────────────────────────
    selenium.get(f"{live_server.url}/accounts/login/")

    selenium.find_element(By.ID, "id_username").send_keys("alice")
    selenium.find_element(By.ID, "id_password").send_keys("password123")
    selenium.find_element(By.CSS_SELECTOR, "button[type=submit]").click()

    WebDriverWait(selenium, 5).until(EC.url_contains("/forms/create/"))

    # ── When: user fills in the form title and one question ────────────
    selenium.find_element(By.ID, "id_title").send_keys("My First Form")

    # The page starts with one question row pre-filled by JS
    selenium.find_element(By.NAME, "question_label").send_keys("What is your name?")

    current_url = selenium.current_url
    selenium.find_element(By.CSS_SELECTOR, "button[type=submit]").click()

    WebDriverWait(selenium, 5).until(EC.url_changes(current_url))

    # ── Then: form and question exist in the database ──────────────────
    form = Form.objects.get(title="My First Form")
    assert form is not None

    question = Question.objects.get(form=form, label="What is your name?")
    assert question.question_type == "text"


def test_alice_can_create_private_form(selenium, live_server, user):
    """
    Given Alice is logged in
    When she creates a private form with bob@example.com as access token
    Then the form is private and bob@example.com is the access token
    """
    # ── Given: Alice logs in ───────────────────────────────────────────
    selenium.get(f"{live_server.url}/accounts/login/")
    selenium.find_element(By.ID, "id_username").send_keys("alice")
    selenium.find_element(By.ID, "id_password").send_keys("password123")
    selenium.find_element(By.CSS_SELECTOR, "button[type=submit]").click()
    WebDriverWait(selenium, 5).until(EC.url_contains("/forms/create/"))

    # ── When: Alice fills the form and marks it private for bob ────────
    selenium.find_element(By.ID, "id_title").send_keys("Alice Private Form")
    selenium.find_element(By.NAME, "question_label").send_keys("Secret question")
    selenium.find_element(By.ID, "id_is_private").click()
    selenium.find_element(By.ID, "id_access_token").send_keys("bob@example.com")
    current_url = selenium.current_url
    selenium.find_element(By.CSS_SELECTOR, "button[type=submit]").click()
    WebDriverWait(selenium, 5).until(EC.url_changes(current_url))

    # ── Then: form is private with bob's email as access token ─────────
    form = Form.objects.get(title="Alice Private Form")
    assert form.is_private is True
    assert form.access_token == "bob@example.com"
