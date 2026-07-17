from __future__ import annotations

import json
import time
from pathlib import Path

from selenium import webdriver
from selenium.common.exceptions import InvalidCookieDomainException, WebDriverException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait

# Configuration
FACEBOOK_URL = "https://www.facebook.com/"
SESSION_DIR = Path("session_data")
COOKIES_FILE = SESSION_DIR / "cookies.txt"
STORAGE_FILE = SESSION_DIR / "storage.txt"
CHROMEDRIVER_PATH = Path("chromedriver-win64") / "chromedriver-win64" / "chromedriver.exe"
LOGIN_TIMEOUT_SECONDS = 300


def build_driver() -> webdriver.Chrome:
    options = Options()
    options.add_argument("--start-maximized")
    user_data_dir = SESSION_DIR / "chrome_profile"
    user_data_dir.mkdir(parents=True, exist_ok=True)
    options.add_argument(f"--user-data-dir={user_data_dir.resolve()}")
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
    return {"localStorage": local_storage, "sessionStorage": session_storage}


def restore_storage(driver: webdriver.Chrome, storage_data: dict[str, dict[str, str]]) -> None:
    local_storage = storage_data.get("localStorage", {})
    session_storage = storage_data.get("sessionStorage", {})
    
    driver.execute_script("window.localStorage.clear();")
    driver.execute_script("window.sessionStorage.clear();")
    
    for key, value in local_storage.items():
        driver.execute_script(
            "window.localStorage.setItem(arguments[0], arguments[1]);", key, value
        )
    
    for key, value in session_storage.items():
        driver.execute_script(
            "window.sessionStorage.setItem(arguments[0], arguments[1]);", key, value
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
        except (InvalidCookieDomainException, WebDriverException):
            continue
    return restored_any


def is_logged_in(driver: webdriver.Chrome) -> bool:
    cookie_names = {cookie["name"] for cookie in driver.get_cookies()}
    current_url = driver.current_url.lower()
    return "c_user" in cookie_names and "login" not in current_url


def restore_session(driver: webdriver.Chrome, group_url: str) -> bool:
    print("[LOGIN] Navigating to group page...")
    driver.get(group_url)
    time.sleep(2)
    
    print("[LOGIN] Restoring cookies...")
    restored_cookies = restore_cookies(driver)
    storage_data = load_json(STORAGE_FILE)
    
    if restored_cookies and isinstance(storage_data, dict):
        print("[LOGIN] Restoring storage and refreshing once...")
        restore_storage(driver, storage_data)
        driver.refresh()
        time.sleep(2)
    elif restored_cookies:
        print("[LOGIN] Refreshing page...")
        driver.refresh()
        time.sleep(2)
    
    logged_in = is_logged_in(driver)
    print(f"[LOGIN] Login status: {'✓ Success' if logged_in else '✗ Failed'}")
    return logged_in


def wait_for_manual_login(driver: webdriver.Chrome, timeout_seconds: int = LOGIN_TIMEOUT_SECONDS) -> bool:
    driver.get(FACEBOOK_URL)
    print(f"Please log in manually (timeout: {timeout_seconds}s)")
    try:
        WebDriverWait(driver, timeout_seconds, poll_frequency=2).until(lambda d: is_logged_in(d))
        return True
    except:
        return False


def login_and_save(driver: webdriver.Chrome, group_url: str) -> bool:
    """Attempt to restore session or perform manual login. Returns True if logged in."""
    if restore_session(driver, group_url):
        print("Session restored")
        return True
    else:
        if not wait_for_manual_login(driver):
            print("Login timeout")
            return False
        save_session(driver)
        print("Session saved")
        return True


if __name__ == "__main__":
    # Test login functionality
    driver = build_driver()
    try:
        test_group_url = "https://www.facebook.com/groups/984940111090551"
        if login_and_save(driver, test_group_url):
            print("Successfully logged in!")
            input("Press Enter to close...")
    finally:
        driver.quit()


