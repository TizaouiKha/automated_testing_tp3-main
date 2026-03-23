from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

URL = "http://localhost:8000"


def test_user_can_fill_form(selenium):
    """
    Given a running server with survey-form seeded
    When a user fills and submits the form
    Then they are redirected to the success page
    """
    selenium.get(f"{URL}/forms/survey-form/")

    field = selenium.find_element(By.CSS_SELECTOR, "input[type=text]")
    field.send_keys("Alice")
    field.send_keys(Keys.TAB)

    current_url = selenium.current_url
    selenium.find_element(By.CSS_SELECTOR, "button[type=submit]").click()
    WebDriverWait(selenium, 5).until(EC.url_changes(current_url))

    assert "success" in selenium.current_url


def test_creator_can_see_stats(selenium):
    """
    Given a running server with survey-form seeded (1 pre-existing response)
    When Alice goes to the stats page
    Then she sees the response count and the pre-existing answer
    """
    selenium.get(f"{URL}/forms/survey-form/stats/")

    body = selenium.find_element(By.TAG_NAME, "body")
    assert "1" in body.text
    assert "Pre-existing Answer" in body.text


def test_private_form__ok(selenium):
    """
    Given a private form with access_token = allowed@example.com
    When a user accesses with the correct token
    Then they see the form questions
    """
    selenium.get(f"{URL}/forms/private-form/?token=allowed@example.com")

    body = selenium.find_element(By.TAG_NAME, "body")
    assert "access denied" not in body.text.lower()
    assert selenium.find_element(By.CSS_SELECTOR, "input, textarea")


def test_private_form__denied(selenium):
    """
    Given a private form with access_token = allowed@example.com
    When a user accesses with a wrong token
    Then they see "access denied"
    """
    selenium.get(f"{URL}/forms/private-form/?token=wrong@example.com")

    body = selenium.find_element(By.TAG_NAME, "body")
    assert "access denied" in body.text.lower()
