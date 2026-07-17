from __future__ import annotations


import json
import random
import time
from datetime import datetime
from pathlib import Path

# code/.venv/Scripts/python.exe -m pip install selenium

from selenium import webdriver
from selenium.common.exceptions import (
    InvalidCookieDomainException,
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
GROUP_URL = "https://www.facebook.com/groups/1728522551728635"
SESSION_DIR = Path("session_data")
COOKIES_FILE = SESSION_DIR / "cookies.txt"
STORAGE_FILE = SESSION_DIR / "storage.txt"
IMAGES_DIR = Path("images")
CHROMEDRIVER_PATH = Path("chromedriver-win64") / "chromedriver-win64" / "chromedriver.exe"
LOGIN_TIMEOUT_SECONDS = 300
GROUP_LOAD_TIMEOUT_SECONDS = 30
POST_DIALOG_TIMEOUT_SECONDS = 30
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
    
    # Create a custom user data directory to avoid permission issues
    user_data_dir = SESSION_DIR / "chrome_profile"
    user_data_dir.mkdir(parents=True, exist_ok=True)
    options.add_argument(f"--user-data-dir={user_data_dir.resolve()}")
    
    # Additional stability options
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    
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
    # Go directly to the group URL to save time
    driver.get(GROUP_URL)
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




def dismiss_popups(driver: webdriver.Chrome) -> None:
    """Try to dismiss any popups or notifications that might be blocking the page."""
    popup_close_selectors = [
        (By.XPATH, "//div[@role='dialog']//div[@aria-label='Close']"),
        (By.XPATH, "//div[@role='dialog']//div[@aria-label='close']"),
        (By.XPATH, "//div[@role='dialog']//button[@aria-label='Close']"),
        (By.XPATH, "//div[@aria-label='Close' and @role='button']"),
        (By.XPATH, "//*[contains(@aria-label, 'Close') and (@role='button' or @role='img')]"),
    ]
    
    for by, value in popup_close_selectors:
        try:
            element = WebDriverWait(driver, 2).until(EC.element_to_be_clickable((by, value)))
            element.click()
            time.sleep(1)
            print("Dismissed a popup")
            return
        except (TimeoutException, Exception):
            continue


def open_group_page(driver: webdriver.Chrome, group_url: str) -> None:
    driver.get(group_url)
    print(f"Loading group page...")
    WebDriverWait(driver, GROUP_LOAD_TIMEOUT_SECONDS).until(
        lambda current_driver: "groups" in current_driver.current_url.lower()
    )
    print(f"Current URL: {driver.current_url}")
    # Wait for page to settle
    time.sleep(3)
    print("Page loaded, checking for popups...")
    # Try to dismiss any popups
    dismiss_popups(driver)




def find_first_clickable(driver: webdriver.Chrome, selectors: list[tuple[str, str]], timeout_seconds: int, debug: bool = False):
    wait = WebDriverWait(driver, timeout_seconds, ignored_exceptions=(StaleElementReferenceException,))
    last_error: Exception | None = None


    for idx, (by, value) in enumerate(selectors, 1):
        try:
            if debug:
                print(f"  [{idx}/{len(selectors)}] Trying: {by}={value[:80]}...")
            element = wait.until(EC.element_to_be_clickable((by, value)))
            if debug:
                print(f"  ✓ Found element with selector #{idx}")
            return element
        except TimeoutException as exc:
            if debug:
                print(f"  ✗ Selector #{idx} not found")
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




def wait_for_post_dialog(driver: webdriver.Chrome):
    dialog_selectors = [
        (By.XPATH, "//div[@role='dialog' and .//div[@role='textbox' and @contenteditable='true']]"),
        (By.XPATH, "//form[.//div[@role='textbox' and @contenteditable='true']]"),
    ]
    return find_first_visible(driver, dialog_selectors, POST_DIALOG_TIMEOUT_SECONDS)




def open_post_dialog(driver: webdriver.Chrome) -> None:
    print("Starting post dialog discovery...")
    # Scroll to top first
    print("Scrolling to top...")
    driver.execute_script("window.scrollTo(0, 0);")
    time.sleep(1)
    
    # Try to dismiss any blocking popups
    dismiss_popups(driver)
    
    # Scroll down a bit to load the composer area
    print("Scrolling down to composer area...")
    driver.execute_script("window.scrollTo(0, 400);")
    time.sleep(2)
    
    # Log available buttons for debugging
    try:
        buttons = driver.find_elements(By.XPATH, "//*[@role='button']")
        print(f"Found {len(buttons)} buttons on the page")
        for i, btn in enumerate(buttons[:10], 1):  # Show first 10
            try:
                aria_label = btn.get_attribute('aria-label') or 'N/A'
                text = btn.text[:50] if btn.text else 'N/A'
                print(f"  Button {i}: aria-label='{aria_label}', text='{text}'")
            except:
                pass
    except Exception as e:
        print(f"Could not enumerate buttons: {e}")
    
    composer_selectors = [
        # Vietnamese selectors
        (By.XPATH, "//span[contains(text(), 'Bạn viết gì đi')]/ancestor::*[@role='button'][1]"),
        (By.XPATH, "//*[@role='button'][contains(., 'Bạn viết gì đi')]"),
        (By.XPATH, "//div[@role='button'][.//span[contains(text(), 'Bạn viết gì đi')]]"),
        # Try contenteditable area directly (may be the input field itself)
        (By.XPATH, "//div[@role='button' and @tabindex='0' and contains(@aria-label, 'Create')]"),
        (By.XPATH, "//div[@role='button' and contains(@aria-label, 'Write')]"),
        (By.XPATH, "//span[contains(text(), 'Write something')]/ancestor::*[@role='button'][1]"),
        (By.XPATH, "//span[contains(text(), 'Create post')]/ancestor::*[@role='button'][1]"),
        (By.XPATH, "//*[@role='button'][contains(., 'Write something')]"),
        (By.XPATH, "//*[@role='button'][contains(., 'Create post')]"),
        # Try finding any button-like div near the top
        (By.XPATH, "//div[@role='button' and contains(@class, 'x1i10hfl')]"),
        # Try finding the input field itself
        (By.XPATH, "//div[contains(@aria-label, \"What's on your mind\")]"),
        (By.XPATH, "//div[starts-with(@aria-label, 'Create a')]"),
    ]
    
    print(f"\nSearching for post composer button ({len(composer_selectors)} selectors, timeout: {POST_DIALOG_TIMEOUT_SECONDS}s)...")
    try:
        composer_button = find_first_clickable(driver, composer_selectors, POST_DIALOG_TIMEOUT_SECONDS, debug=True)
        print("\n✓ Found composer button, clicking...")
        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", composer_button)
        time.sleep(1)
        driver.execute_script("arguments[0].click();", composer_button)
        print("Waiting for post dialog to appear...")
        wait_for_post_dialog(driver)
        print("✓ Post dialog opened successfully")
    except TimeoutException as e:
        print(f"\n✗ ERROR: Could not find post composer button after {POST_DIALOG_TIMEOUT_SECONDS} seconds")
        print("Saving screenshot and page source for debugging...")
        driver.save_screenshot("debug_composer_not_found.png")
        with open("debug_page_source.html", "w", encoding="utf-8") as f:
            f.write(driver.page_source)
        print("Screenshot saved to: debug_composer_not_found.png")
        print("Page source saved to: debug_page_source.html")
        raise




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
        (By.XPATH, "//div[@role='dialog']//div[@role='textbox' and @contenteditable='true']"),
        (By.XPATH, "//form//div[@role='textbox' and @contenteditable='true']"),
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
        # Vietnamese selectors
        (By.XPATH, "//div[@role='dialog']//div[@role='button'][.//span[normalize-space()='Đăng']]"),
        (By.XPATH, "//div[@role='dialog']//button[normalize-space()='Đăng']"),
        (By.XPATH, "//form//div[@role='button'][.//span[normalize-space()='Đăng']]"),
        (By.XPATH, "//form//button[normalize-space()='Đăng']"),
        (By.XPATH, "//*[@role='button'][contains(., 'Đăng')]"),
        # English selectors (fallback)
        (By.XPATH, "//div[@role='dialog']//div[@role='button'][.//span[normalize-space()='Post']]"),
        (By.XPATH, "//div[@role='dialog']//button[normalize-space()='Post']"),
        (By.XPATH, "//form//div[@role='button'][.//span[normalize-space()='Post']]"),
        (By.XPATH, "//form//button[normalize-space()='Post']"),
    ]
    submit_button = find_first_clickable(driver, submit_selectors, POST_DIALOG_TIMEOUT_SECONDS)
    driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", submit_button)
    driver.execute_script("arguments[0].click();", submit_button)




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
