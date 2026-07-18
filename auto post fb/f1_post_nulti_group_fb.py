from __future__ import annotations


import random
import time
from datetime import datetime
from pathlib import Path


from selenium import webdriver
from selenium.common.exceptions import StaleElementReferenceException, TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


# Import login functionality
from f1_facebook_login import build_driver, login_and_save


# Configuration
G = """
https://www.facebook.com/groups/785225373106811/
https://www.facebook.com/groups/1116390892661061/
https://www.facebook.com/groups/6688909131219490
https://www.facebook.com/groups/6010773078979303/
https://www.facebook.com/groups/744635730390896/
https://www.facebook.com/groups/895293681714864/
https://www.facebook.com/groups/batdongsansaigon3/
https://www.facebook.com/groups/nhachinhchutphochiminh/
https://www.facebook.com/groups/3643861382324918/
https://www.facebook.com/groups/520865190229284/
https://www.facebook.com/groups/204882203644959/
https://www.facebook.com/groups/1359445864770043/
https://www.facebook.com/share/g/1J4wtjjQdW/
https://www.facebook.com/groups/1620447884651557/
https://www.facebook.com/groups/206767735704497/
https://www.facebook.com/groups/nhadatquan7namsaigon/
https://www.facebook.com/groups/1194594703901281/
https://www.facebook.com/groups/1067196077772747/
https://www.facebook.com/groups/1384960275389807/
https://www.facebook.com/groups/1154086175278915/
https://www.facebook.com/groups/744635730390896/
https://www.facebook.com/groups/2006136186389604/
https://www.facebook.com/groups/745712154058340/
https://www.facebook.com/groups/3643861382324918/
https://www.facebook.com/groups/380792843023840/

"""
GROUP_URLS = [url.strip() for url in G.split("\n") if url.strip()]

POSTS_DIR = Path(r"D:\job\study-every-thing\auto post fb\posts")
GROUP_LOAD_TIMEOUT_SECONDS = 30
POST_DIALOG_TIMEOUT_SECONDS = 30
POST_INTERVAL_MIN_SECONDS = 300  # Minimum wait time between posts
POST_INTERVAL_MAX_SECONDS = 400  # Maximum wait time between posts




def remove_non_bmp_chars(text: str) -> str:
    """
    Remove characters outside the Basic Multilingual Plane (BMP).
    ChromeDriver only supports characters in the BMP (U+0000 to U+FFFF).
    This filters out emojis and other characters that would cause errors.
    """
    return ''.join(char for char in text if ord(char) <= 0xFFFF)




def find_first_element(driver: webdriver.Chrome, selectors: list[tuple[str, str]], timeout_seconds: int, mode: str = 'clickable'):
    wait = WebDriverWait(driver, timeout_seconds, ignored_exceptions=(StaleElementReferenceException,))
    condition_map = {
        'clickable': EC.element_to_be_clickable,
        'visible': EC.visibility_of_element_located,
        'present': EC.presence_of_element_located
    }
    condition = condition_map.get(mode, EC.element_to_be_clickable)
   
    for by, value in selectors:
        try:
            return wait.until(condition((by, value)))
        except TimeoutException:
            continue
    raise TimeoutException(f"No {mode} element matched the provided selectors.")




def dismiss_popups(driver: webdriver.Chrome) -> None:
    print("[UI] Checking for popups...")
    popup_close_selectors = [
        (By.XPATH, "//div[@role='dialog']//div[@aria-label='Close']"),
        (By.XPATH, "//div[@role='dialog']//button[@aria-label='Close']"),
        (By.XPATH, "//*[contains(@aria-label, 'Close') and @role='button']"),
    ]
    for by, value in popup_close_selectors:
        try:
            WebDriverWait(driver, 2).until(EC.element_to_be_clickable((by, value))).click()
            print("[UI] ✓ Dismissed popup")
            time.sleep(1)
            return
        except:
            continue
    print("[UI] No popups found")




def navigate_to_group(driver: webdriver.Chrome, group_url: str) -> None:
    """Navigate to a specific group page"""
    print(f"[NAV] Loading group page: {group_url}")
    driver.get(group_url)
    WebDriverWait(driver, GROUP_LOAD_TIMEOUT_SECONDS).until(
        lambda d: "groups" in d.current_url.lower()
    )
    print("[NAV] ✓ Group page loaded")
    time.sleep(2)
    dismiss_popups(driver)




def scroll_to_composer_area(driver: webdriver.Chrome) -> None:
    """Scroll to the post composer"""
    print("[UI] Scrolling to composer area...")
    driver.execute_script("window.scrollTo(0, 0);")
    time.sleep(0.5)
    dismiss_popups(driver)
    driver.execute_script("window.scrollTo(0, 400);")
    time.sleep(1)
    print("[UI] ✓ At composer area")




def wait_for_post_dialog(driver: webdriver.Chrome):
    dialog_selectors = [
        (By.XPATH, "//div[@role='dialog' and .//div[@role='textbox' and @contenteditable='true']]"),
        (By.XPATH, "//form[.//div[@role='textbox' and @contenteditable='true']]"),
    ]
    return find_first_element(driver, dialog_selectors, POST_DIALOG_TIMEOUT_SECONDS, 'visible')




def open_post_dialog(driver: webdriver.Chrome) -> None:
    scroll_to_composer_area(driver)
   
    composer_selectors = [
        (By.XPATH, "//span[contains(text(), 'Bạn viết gì đi')]/ancestor::*[@role='button'][1]"),
        (By.XPATH, "//*[@role='button'][contains(., 'Bạn viết gì đi')]"),
        (By.XPATH, "//div[@role='button' and contains(@aria-label, 'Create')]"),
        (By.XPATH, "//div[@role='button' and contains(@aria-label, 'Write')]"),
        (By.XPATH, "//span[contains(text(), 'Write something')]/ancestor::*[@role='button'][1]"),
        (By.XPATH, "//*[@role='button'][contains(., 'Write something')]"),
        (By.XPATH, "//div[contains(@aria-label, \"What's on your mind\")]"),
    ]
   
    try:
        print("[UI] Looking for post composer button...")
        composer_button = find_first_element(driver, composer_selectors, POST_DIALOG_TIMEOUT_SECONDS)
        print("[UI] ✓ Found composer button, clicking...")
        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", composer_button)
        time.sleep(0.5)
        driver.execute_script("arguments[0].click();", composer_button)
        wait_for_post_dialog(driver)
        print("[UI] ✓ Post dialog opened")
    except TimeoutException:
        print("[UI] ✗ Failed to find composer button")
        driver.save_screenshot("debug_composer_not_found.png")
        raise




def load_all_posts() -> list[dict]:
    """Load all posts from the posts directory"""
    posts = []
    if not POSTS_DIR.exists():
        print(f"[ERROR] Posts directory not found: {POSTS_DIR}")
        return posts
   
    # Get all numbered folders
    post_folders = sorted([d for d in POSTS_DIR.iterdir() if d.is_dir()], key=lambda x: x.name)
   
    for post_folder in post_folders:
        content_file = post_folder / "content.txt"
        image_folder = post_folder / "image"
       
        if not content_file.exists():
            print(f"[WARNING] No content.txt in {post_folder.name}, skipping")
            continue
       
        # Read content
        try:
            content = content_file.read_text(encoding="utf-8").strip()
        except Exception as e:
            print(f"[WARNING] Error reading {content_file}: {e}")
            continue
       
        # Get images
        image_paths = []
        if image_folder.exists() and image_folder.is_dir():
            image_paths = [
                path for path in image_folder.iterdir()
                if path.is_file() and path.suffix.lower() in {".jpg", ".jpeg", ".png", ".gif", ".webp"}
            ]
       
        posts.append({
            "folder": post_folder.name,
            "content": content,
            "images": image_paths
        })
       
        print(f"[LOAD] Post {post_folder.name}: {len(image_paths)} image(s), {len(content)} chars")
   
    return posts




def get_post_image_paths(post_data: dict) -> list[Path]:
    """Get image paths from a specific post"""
    return post_data.get("images", [])




def attach_post_images(driver: webdriver.Chrome, image_paths: list[Path]) -> None:
    """Attach images from a specific post"""
    if not image_paths:
        print("[UI] No images to attach")
        return
    print(f"[UI] Attaching {len(image_paths)} image(s)...")
    upload_selectors = [
        (By.XPATH, "//div[@role='dialog']//input[@type='file' and contains(@accept, 'image')]"),
        (By.XPATH, "//div[@role='dialog']//input[@type='file']"),
    ]
    upload_input = find_first_element(driver, upload_selectors, POST_DIALOG_TIMEOUT_SECONDS, 'present')
    upload_input.send_keys("\n".join(str(path.resolve()) for path in image_paths))
    print("[UI] ✓ Images attached, waiting 3s for upload...")
    time.sleep(3)




def fill_post_text(driver: webdriver.Chrome, post_text: str, image_paths: list[Path]) -> None:
    wait_for_post_dialog(driver)
    print("[UI] Finding text box...")
    textbox_selectors = [
        (By.XPATH, "//div[@role='dialog']//div[@role='textbox' and @contenteditable='true']"),
        (By.XPATH, "//form//div[@role='textbox' and @contenteditable='true']"),
    ]
    textbox = find_first_element(driver, textbox_selectors, POST_DIALOG_TIMEOUT_SECONDS, 'visible')
    print("[UI] ✓ Found text box, typing content...")
   
    # Filter out non-BMP characters that ChromeDriver can't handle
    clean_text = remove_non_bmp_chars(post_text)
   
    # Use JavaScript to set text and trigger events (more reliable for Facebook)
    driver.execute_script("""
        arguments[0].focus();
        arguments[0].textContent = arguments[1];
        arguments[0].dispatchEvent(new Event('input', { bubbles: true }));
        arguments[0].dispatchEvent(new Event('change', { bubbles: true }));
    """, textbox, clean_text)
   
    time.sleep(0.5)
   
    # Verify text was entered
    entered_text = driver.execute_script("return arguments[0].textContent;", textbox)
    if entered_text.strip():
        print(f"[UI] ✓ Text entered: {entered_text[:50]}...")
    else:
        print("[UI] ⚠ Warning: Text box appears empty, trying alternative method...")
        # Fallback: Click and use send_keys
        textbox.click()
        time.sleep(0.3)
        textbox.send_keys(clean_text)
        time.sleep(0.3)
        entered_text = driver.execute_script("return arguments[0].textContent;", textbox)
        print(f"[UI] ✓ Fallback text: {entered_text[:50]}...")
   
    # Wait 3 seconds after pasting content
    print("[UI] Waiting 3s after content paste...")
    time.sleep(3)
   
    attach_post_images(driver, image_paths)




def submit_post(driver: webdriver.Chrome) -> None:
    wait_for_post_dialog(driver)
    print("[UI] Looking for submit button...")
    submit_selectors = [
        (By.XPATH, "//div[@role='dialog']//div[@role='button'][.//span[normalize-space()='Đăng']]"),
        (By.XPATH, "//*[@role='button'][contains(., 'Đăng')]"),
        (By.XPATH, "//div[@role='dialog']//div[@role='button'][.//span[normalize-space()='Post']]"),
        (By.XPATH, "//div[@role='dialog']//button[normalize-space()='Post']"),
    ]
    submit_button = find_first_element(driver, submit_selectors, POST_DIALOG_TIMEOUT_SECONDS)
    print("[UI] ✓ Found submit button")
    print("[UI] Waiting 3s before clicking post button...")
    time.sleep(3)
    print("[UI] Clicking post button...")
    driver.execute_script("arguments[0].click();", submit_button)
    time.sleep(2)  # Wait for post to submit
    print("[UI] ✓ Post submitted")




def post_to_group(driver: webdriver.Chrome, group_url: str, post_data: dict, group_index: int, total_groups: int, post_number: int) -> None:
    """Post to a specific group"""
    start_time = time.time()
    post_text = post_data["content"]
    image_paths = post_data["images"]
   
    print(f"\n{'='*60}")
    print(f"[POST] Group {group_index + 1}/{total_groups} | Post #{post_number}")
    print(f"[POST] URL: {group_url}")
    print(f"[POST] Folder: {post_data['folder']}")
    print(f"[POST] Content: {post_text[:80]}{'...' if len(post_text) > 80 else ''}")
    print(f"[POST] Images: {len(image_paths)}")
    print(f"{'='*60}")
   
    try:
        # Navigate to the group
        navigate_to_group(driver, group_url)
       
        # Open post dialog and create post
        open_post_dialog(driver)
        fill_post_text(driver, post_text, image_paths)
        submit_post(driver)
       
        elapsed = time.time() - start_time
        print(f"[POST] ✓ Completed in {elapsed:.1f}s")
        print(f"{'='*60}\n")
        return True
    except Exception as e:
        print(f"[POST] ✗ Error posting to group: {e}")
        driver.save_screenshot(f"error_group_{group_index}_post_{post_number}.png")
        return False




def run_multi_group_post_loop(driver: webdriver.Chrome) -> None:
    """Post to multiple groups in rotation using posts from the posts directory"""
    if not GROUP_URLS:
        print("[ERROR] No group URLs configured!")
        return
   
    # Load all posts
    print(f"\n[INIT] Loading posts from '{POSTS_DIR}'...")
    all_posts = load_all_posts()
   
    if not all_posts:
        print("[ERROR] No posts found! Please create posts in the 'posts' directory.")
        print("[ERROR] Each post should have: content.txt and image/ folder")
        return
   
    print(f"\n[INIT] Starting multi-group posting")
    print(f"[INIT] Total groups: {len(GROUP_URLS)}")
    print(f"[INIT] Total posts: {len(all_posts)}")
    print(f"[INIT] Delay between posts: {POST_INTERVAL_MIN_SECONDS}.000-{POST_INTERVAL_MAX_SECONDS}.000s (random float)")
    print(f"[INIT] Pattern: Each post goes to a different group in rotation")
    print(f"[INIT] Groups:")
    for i, url in enumerate(GROUP_URLS, 1):
        print(f"  {i}. {url}")
    print()
   
    post_index = 0
    group_index = 0
    post_counter = 0
   
    while True:
        # Get current post and group (both cycle independently)
        current_post = all_posts[post_index % len(all_posts)]
        current_group_url = GROUP_URLS[group_index % len(GROUP_URLS)]
        post_counter += 1
       
        print(f"\n{'#'*60}")
        print(f"[LOOP] Action #{post_counter}")
        print(f"[LOOP] Group: {group_index % len(GROUP_URLS) + 1}/{len(GROUP_URLS)} - {current_group_url}")
        print(f"[LOOP] Post: {current_post['folder']}")
        print(f"{'#'*60}")
       
        # Post to the current group
        success = post_to_group(driver, current_group_url, current_post, group_index % len(GROUP_URLS), len(GROUP_URLS), post_counter)
       
        # Move to next post and next group
        post_index += 1
        group_index += 1
       
        # Wait before next action
        wait_time = random.uniform(POST_INTERVAL_MIN_SECONDS, POST_INTERVAL_MAX_SECONDS)
        print(f"\n[LOOP] Waiting {wait_time:.3f}s before next post...\n")
        time.sleep(wait_time)




def main() -> None:
    driver = build_driver()
    try:
        # Login to Facebook using the first group URL as target
        if not login_and_save(driver, GROUP_URLS[0] if GROUP_URLS else "https://www.facebook.com"):
            return
       
        # Start posting to multiple groups
        run_multi_group_post_loop(driver)
    except KeyboardInterrupt:
        print("\n[STOP] Stopped by user (Ctrl+C)")
    except Exception as e:
        print(f"\n[ERROR] Unexpected error: {e}")
    finally:
        print("[CLEANUP] Closing browser...")
        driver.quit()




if __name__ == "__main__":
    while True:
        main()





