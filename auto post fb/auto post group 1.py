from __future__ import annotations




import json
import random
import time
from datetime import datetime
from pathlib import Path


# code/.venv/Scripts/python.exe -m pip install selenium


from selenium import webdriver
from selenium.common.exceptions import (
    ElementClickInterceptedException,
    InvalidCookieDomainException,
    NoSuchElementException,
    StaleElementReferenceException,
    TimeoutException,
    WebDriverException,
)

from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait








facebook_URL = "https://www.facebook.com/"
GROUP_URL = "https://www.facebook.com/groups/984940111090551"
SESSION_DIR = Path("session_data")
COOKIES_FILE = SESSION_DIR / "cookies.txt"
STORAGE_FILE = SESSION_DIR / "storage.txt"
IMAGES_DIR = Path("images")
CHROMEDRIVER_PATH = Path("chromedriver-win64") / "chromedriver-win64" / "chromedriver.exe"
LOGIN_TIMEOUT_SECONDS = 300
GROUP_LOAD_TIMEOUT_SECONDS = 30
POST_DIALOG_TIMEOUT_SECONDS = 20
POST_INTERVAL_SECONDS = 60
MAX_POST_IMAGES = 5
POST_TEMPLATES = [
    "Group update",
    "Daily check-in",
    "News for members",
    "Reminder for everyone",
]








def build_driver() -> webdriver.Chrome:
    options = Options()
    options.add_argument("--start-maximized")
    service = Service(executable_path=str(CHROMEDRIVER_PATH.resolve()))
    return webdriver.Chrome(service=service, options=options)








def ensure_session_dir() -> None:
    SESSION_DIR.mkdir(parents=True, exist_ok=True)








def save_json(path: Path, data: object) -> None:
    path.write_text(json.dumps(data, indent=2), encoding="utf-8")








def load_json(path: Path) -> object | None:
    if not path.exists():
        return None
    return json.loads(path.read_text(encoding="utf-8"))








def collect_storage(driver: webdriver.Chrome) -> dict[str, dict[str, str]]:
    local_storage = driver.execute_script(
        """
        const data = {};
        for (let i = 0; i < window.localStorage.length; i += 1) {
            const key = window.localStorage.key(i);
            data[key] = window.localStorage.getItem(key);
        }
        return data;
        """
    )
    session_storage = driver.execute_script(
        """
        const data = {};
        for (let i = 0; i < window.sessionStorage.length; i += 1) {
            const key = window.sessionStorage.key(i);
            data[key] = window.sessionStorage.getItem(key);
        }
        return data;
        """
    )
    return {
        "localStorage": local_storage,
        "sessionStorage": session_storage,
    }








def restore_storage(driver: webdriver.Chrome, storage_data: dict[str, dict[str, str]]) -> None:
    local_storage = storage_data.get("localStorage", {})
    session_storage = storage_data.get("sessionStorage", {})




    driver.execute_script("window.localStorage.clear();")
    driver.execute_script("window.sessionStorage.clear();")




    for key, value in local_storage.items():
        driver.execute_script(
            "window.localStorage.setItem(arguments[0], arguments[1]);",
            key,
            value,
        )




    for key, value in session_storage.items():
        driver.execute_script(
            "window.sessionStorage.setItem(arguments[0], arguments[1]);",
            key,
            value,
        )








def save_session(driver: webdriver.Chrome) -> None:
    ensure_session_dir()
    save_json(COOKIES_FILE, driver.get_cookies())
    save_json(STORAGE_FILE, collect_storage(driver))








def restore_cookies(driver: webdriver.Chrome) -> bool:
    cookies = load_json(COOKIES_FILE)
    if not cookies:
        return False




    restored_any = False
    for cookie in cookies:
        cookie = dict(cookie)
        cookie.pop("sameSite", None)
        try:
            driver.add_cookie(cookie)
            restored_any = True
        except InvalidCookieDomainException:
            continue
        except WebDriverException:
            continue
    return restored_any








def restore_session(driver: webdriver.Chrome) -> bool:
    driver.get(facebook_URL)
    time.sleep(2)




    restored_cookies = restore_cookies(driver)
    storage_data = load_json(STORAGE_FILE)




    if restored_cookies:
        driver.refresh()
        time.sleep(2)




    if isinstance(storage_data, dict):
        restore_storage(driver, storage_data)
        driver.refresh()
        time.sleep(2)




    return is_logged_in(driver)








def is_logged_in(driver: webdriver.Chrome) -> bool:
    cookie_names = {cookie["name"] for cookie in driver.get_cookies()}
    current_url = driver.current_url.lower()
    return "c_user" in cookie_names and "login" not in current_url








def wait_for_manual_login(driver: webdriver.Chrome, timeout_seconds: int) -> bool:
    driver.get(facebook_URL)
    print("facebook opened in Chrome.")
    print("Log in manually in the browser window.")
    print(f"Waiting up to {timeout_seconds} seconds for login success...")




    wait = WebDriverWait(driver, timeout_seconds, poll_frequency=2)
    try:
        wait.until(lambda current_driver: is_logged_in(current_driver))
        return True
    except Exception:
        return False








def open_group_page(driver: webdriver.Chrome, group_url: str) -> None:
    driver.get(group_url)
    WebDriverWait(driver, GROUP_LOAD_TIMEOUT_SECONDS).until(
        lambda current_driver: "groups" in current_driver.current_url.lower()
    )








def find_first_clickable(driver: webdriver.Chrome, selectors: list[tuple[str, str]], timeout_seconds: int):
    wait = WebDriverWait(driver, timeout_seconds, ignored_exceptions=(StaleElementReferenceException,))
    last_error: Exception | None = None




    for by, value in selectors:
        try:
            return wait.until(EC.element_to_be_clickable((by, value)))
        except TimeoutException as exc:
            last_error = exc




    if last_error is not None:
        raise last_error




    raise TimeoutException("No clickable element matched the provided selectors.")








def find_first_visible(driver: webdriver.Chrome, selectors: list[tuple[str, str]], timeout_seconds: int):
    wait = WebDriverWait(driver, timeout_seconds, ignored_exceptions=(StaleElementReferenceException,))
    last_error: Exception | None = None




    for by, value in selectors:
        try:
            return wait.until(EC.visibility_of_element_located((by, value)))
        except TimeoutException as exc:
            last_error = exc




    if last_error is not None:
        raise last_error




    raise TimeoutException("No visible element matched the provided selectors.")








def find_first_present(driver: webdriver.Chrome, selectors: list[tuple[str, str]], timeout_seconds: int):
    wait = WebDriverWait(driver, timeout_seconds, ignored_exceptions=(StaleElementReferenceException,))
    last_error: Exception | None = None




    for by, value in selectors:
        try:
            return wait.until(EC.presence_of_element_located((by, value)))
        except TimeoutException as exc:
            last_error = exc




    if last_error is not None:
        raise last_error




    raise TimeoutException("No present element matched the provided selectors.")








def click_element(driver: webdriver.Chrome, element) -> None:
    driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", element)
    try:
        element.click()
    except ElementClickInterceptedException:
        try:
            ActionChains(driver).move_to_element(element).click().perform()
        except Exception:
            driver.execute_script(
                "arguments[0].dispatchEvent(new MouseEvent('click', {bubbles: true, cancelable: true}));",
                element,
            )


def wait_for_post_dialog(driver: webdriver.Chrome):
    dialog_selectors = [
        (By.XPATH, "//div[@role='dialog' and .//div[@role='textbox' or @contenteditable='true' or @contenteditable='plaintext-plaintext']]"),
        (By.XPATH, "//form[.//div[@role='textbox' or @contenteditable='true' or @contenteditable='plaintext-plaintext']]"),
        (By.CSS_SELECTOR, "div[role='dialog'] div[role='textbox'], div[role='dialog'] div[contenteditable='true'], div[role='dialog'] div[contenteditable='plaintext-plaintext']"),
        (By.CSS_SELECTOR, "form div[role='textbox'], form div[contenteditable='true'], form div[contenteditable='plaintext-plaintext']"),
    ]
    return find_first_visible(driver, dialog_selectors, POST_DIALOG_TIMEOUT_SECONDS)








def open_post_dialog(driver: webdriver.Chrome) -> None:
    composer_selectors = [
        (By.XPATH, "//span[contains(normalize-space(), \"Write something\")]/ancestor::*[@role='button'][1]"),
        (By.XPATH, "//span[contains(normalize-space(), \"Create post\")]/ancestor::*[@role='button'][1]"),
        (By.XPATH, "//div[@role='button'][.//span[contains(normalize-space(), \"Write something\")]]"),
        (By.XPATH, "//div[@role='button'][.//span[contains(normalize-space(), \"Create post\")]]"),
        (By.CSS_SELECTOR, "div[aria-label='Create a post']"),
        (By.CSS_SELECTOR, "div[aria-label='Write something']"),
        (By.CSS_SELECTOR, "div[aria-label='Create post']"),
        (By.XPATH, "//*[self::div or self::button][@role='button' and contains(translate(@aria-label, 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'create a post')]"),
        (By.XPATH, "//*[self::div or self::button][@role='button' and contains(translate(@aria-label, 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'write something')]"),
    ]
    composer_button = find_first_clickable(driver, composer_selectors, POST_DIALOG_TIMEOUT_SECONDS)
    click_element(driver, composer_button)
    wait_for_post_dialog(driver)








def get_random_image_paths(max_images: int) -> list[Path]:
    image_paths = [
        path for path in IMAGES_DIR.iterdir()
        if path.is_file() and path.suffix.lower() in {".jpg", ".jpeg", ".png", ".gif", ".webp"}
    ] if IMAGES_DIR.exists() else []




    if not image_paths:
        return []




    image_count = min(max_images, len(image_paths))
    return random.sample(image_paths, image_count)








def attach_random_images(driver: webdriver.Chrome, max_images: int) -> None:
    image_paths = get_random_image_paths(max_images)
    if not image_paths:
        return




    upload_selectors = [
        (By.XPATH, "//div[@role='dialog']//input[@type='file' and contains(@accept, 'image')]"),
        (By.XPATH, "//form//input[@type='file' and contains(@accept, 'image')]"),
        (By.XPATH, "//div[@role='dialog']//input[@type='file']"),
        (By.XPATH, "//form//input[@type='file']"),
    ]
    upload_input = find_first_present(driver, upload_selectors, POST_DIALOG_TIMEOUT_SECONDS)
    upload_input.send_keys("\n".join(str(path.resolve()) for path in image_paths))
    time.sleep(2)








def fill_post_text(driver: webdriver.Chrome, post_text: str) -> None:
    wait_for_post_dialog(driver)
    textbox_selectors = [
        (By.XPATH, "//div[@role='dialog']//div[@role='textbox' or @contenteditable='true' or @contenteditable='plaintext-plaintext']"),
        (By.XPATH, "//form//div[@role='textbox' or @contenteditable='true' or @contenteditable='plaintext-plaintext']"),
        (By.CSS_SELECTOR, "div[role='dialog'] div[role='textbox'], div[role='dialog'] div[contenteditable='true'], div[role='dialog'] div[contenteditable='plaintext-plaintext']"),
        (By.CSS_SELECTOR, "form div[role='textbox'], form div[contenteditable='true'], form div[contenteditable='plaintext-plaintext']"),
    ]
    textbox = find_first_visible(driver, textbox_selectors, POST_DIALOG_TIMEOUT_SECONDS)
    driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", textbox)
    driver.execute_script("arguments[0].focus();", textbox)
    textbox.send_keys(Keys.CONTROL, "a")
    textbox.send_keys(Keys.DELETE)
    textbox.send_keys(post_text)
    attach_random_images(driver, MAX_POST_IMAGES)








def submit_post(driver: webdriver.Chrome) -> None:
    wait_for_post_dialog(driver)
    submit_selectors = [
        (By.XPATH, "//div[@role='dialog']//div[@role='button'][.//span[normalize-space()='Post']]"),
        (By.XPATH, "//div[@role='dialog']//button[normalize-space()='Post']"),
        (By.XPATH, "//form//div[@role='button'][.//span[normalize-space()='Post']]"),
        (By.XPATH, "//form//button[normalize-space()='Post']"),
        (By.XPATH, "//*[self::div or self::button][contains(@aria-label, 'Post') or normalize-space()='Post']"),
    ]
    submit_button = find_first_clickable(driver, submit_selectors, POST_DIALOG_TIMEOUT_SECONDS)
    click_element(driver, submit_button)








def build_generated_post_text() -> str:
    template = random.choice(POST_TEMPLATES)
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return f"{template} - {timestamp}"








def maybe_create_group_post(driver: webdriver.Chrome) -> None:
    post_text = build_generated_post_text()
    print(f"Post text: {post_text}")
    print(f"Opening group: {GROUP_URL}")
    open_group_page(driver, GROUP_URL)
    print("Trying to open the post composer...")
    open_post_dialog(driver)
    print("Typing the post content...")
    fill_post_text(driver, post_text)
    print("Submitting the group post...")
    submit_post(driver)
    print("Post submitted.")








def run_group_post_loop(driver: webdriver.Chrome) -> None:
    cycle_number = 1
    while True:
        print(f"Starting post cycle #{cycle_number}...")
        maybe_create_group_post(driver)
        cycle_number += 1
        print(f"Waiting {POST_INTERVAL_SECONDS} seconds before the next post...")
        time.sleep(POST_INTERVAL_SECONDS)








def main() -> None:
    driver = build_driver()
    try:
        print("Trying to restore existing facebook session...")
        if restore_session(driver):
            print("Existing session restored. Login was not required.")
        else:
            print("No valid saved session found.")
            success = wait_for_manual_login(driver, LOGIN_TIMEOUT_SECONDS)
            if not success:
                print("Login was not detected before timeout.")
                return




            print("Login detected. Saving session data...")
            save_session(driver)
            print(f"Cookies saved to: {COOKIES_FILE.resolve()}")
            print(f"Storage saved to: {STORAGE_FILE.resolve()}")




        run_group_post_loop(driver)
    except KeyboardInterrupt:
        print("Stopping auto-post loop.")
    finally:
        driver.quit()


if __name__ == "__main__":
    main()
