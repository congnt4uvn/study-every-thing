from __future__ import annotations

import random
import time
from pathlib import Path
from typing import Literal

from selenium import webdriver
from selenium.common.exceptions import StaleElementReferenceException, TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

# Import login functionality for both accounts
import facebook_login
import facebook_login_account2

# Configuration
POST_URLS = [
"https://www.facebook.com/share/p/1CmrgcCcEf/",
"https://www.facebook.com/share/p/1BT7zTuhsm/",
"https://www.facebook.com/share/p/1cnAbq1kTE/",
"https://www.facebook.com/share/p/19FTPF54ww/",
"https://www.facebook.com/share/p/19L4ZFkcXJ/",
"https://www.facebook.com/share/p/1K962dv7tA/",
"https://www.facebook.com/share/p/1GQ7vJvDQA/",
"https://www.facebook.com/share/p/1EH6pszAAF/",
"https://www.facebook.com/share/p/1BqFCk7GA3/",
"https://www.facebook.com/share/p/1BMp9DdAVY/",
"https://www.facebook.com/share/p/1EXKLYWXMP/",
"https://www.facebook.com/share/p/17j6iMPFPy/",
"https://www.facebook.com/share/p/1BNzab5Kig/",
"https://www.facebook.com/share/p/1Hw5L49YsE/",
"https://www.facebook.com/share/p/199mXYe3FD/",
"https://www.facebook.com/share/p/1C2XPTZnbT/",
"https://www.facebook.com/share/p/1BncCspwEj/",
"https://www.facebook.com/share/p/19BQfjWYUa/",
"https://www.facebook.com/share/p/18uVUFpkf1/",
"https://www.facebook.com/share/p/1BknfAbQ52/",
"https://www.facebook.com/share/p/1PJQrepyte/",
"https://www.facebook.com/share/p/1H2SLSGSmm/",
"https://www.facebook.com/share/p/1JNBF6Dv9G/"
    # Add more URLs here
]

COMMENTS = [
    "inbox",
    "ib"
]

# Which accounts to use: "account1", "account2", or "both"
# USE_ACCOUNTS: Literal["account1", "account2", "both"] = "both"

# only use account1
USE_ACCOUNTS: Literal["account1", "account2", "both"] = "account1"

# only use account2
#USE_ACCOUNTS: Literal["account1", "account2", "both"] = "account2"

POST_LOAD_TIMEOUT_SECONDS = 30
COMMENT_BOX_TIMEOUT_SECONDS = 15
DELAY_BETWEEN_COMMENTS_SECONDS = 100
DELAY_BETWEEN_ACCOUNTS_SECONDS = 3


def find_first_element(driver: webdriver.Chrome, selectors: list[tuple[str, str]], timeout_seconds: int, mode: str = 'clickable'):
    """Find the first matching element from a list of selectors."""
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
    """Dismiss any popup dialogs that may appear."""
    try:
        close_selectors = [
            (By.XPATH, "//div[@aria-label='Close']"),
            (By.XPATH, "//div[@role='button' and contains(text(), 'Not Now')]"),
            (By.XPATH, "//div[@role='button' and contains(text(), 'Close')]"),
        ]
        close_button = find_first_element(driver, close_selectors, timeout_seconds=3, mode='clickable')
        close_button.click()
        time.sleep(1)
    except TimeoutException:
        pass


def delete_comment(driver: webdriver.Chrome, account_name: str = "") -> bool:
    """Delete the most recent comment (the one just posted)."""
    prefix = f"[{account_name}] " if account_name else ""
    try:
        print(f"{prefix}Waiting 25 seconds before deleting comment...")
        time.sleep(25)
        
        # Find the most recent comment's menu button (three dots)
        menu_selectors = [
            (By.XPATH, "//span[@class='html-span xdj266r x14z9mp xat24cr x1lziwak xexx8yu xyri2b x18d9i69 x1c1uobl x1hl2dhg x16tdsg8 x1vvkbs x4k7w5x x1h91t0o x1h9r5lt x1jfb8zj xv2umb2 x1beo9mf xaigb6o x12ejxvf x3igimt xarpa2k xedcshv x1lytzrv x1t2pt76 x7ja8zs x1qrby5j']//ancestor::div[@role='button' and @aria-haspopup='menu']"),
            (By.XPATH, "//div[@aria-haspopup='menu'][@role='button']//span[contains(@class, 'xdj266r')]"),
            (By.XPATH, "//div[@aria-haspopup='menu'][@role='button']"),
            (By.XPATH, "//div[contains(@aria-label, 'Khác')][@role='button']"),
            (By.XPATH, "//div[contains(@aria-label, 'More')][@role='button']"),
        ]
        
        print(f"{prefix}Looking for comment menu button (...)...")
        menu_button = find_first_element(driver, menu_selectors, timeout_seconds=10, mode='present')
        
        # Scroll the menu button into view
        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", menu_button)
        time.sleep(1)
        
        # Use JavaScript click to avoid interception
        print(f"{prefix}Clicking menu button with JavaScript...")
        driver.execute_script("arguments[0].click();", menu_button)
        time.sleep(2)
        
        # Find and click the Delete option (Xóa in Vietnamese)
        delete_selectors = [
            (By.XPATH, "//span[@class='x193iq5w xeuugli x13faqbe x1vvkbs x1xmvt09 x1lliihq x1s928wv xhkezso x1gmr53x x1cpjm7i x1fgarty x1943h6x xudqn12 x3x7a5m x6prxxf xvq8zen xk50ysn xzsf02u x1yc453h' and text()='Xóa']"),
            (By.XPATH, "//span[contains(@class, 'x193iq5w') and contains(@class, 'xeuugli') and text()='Xóa']"),
            (By.XPATH, "//span[text()='Xóa']//ancestor::div[@role='menuitem']"),
            (By.XPATH, "//div[@role='menuitem']//span[text()='Xóa']"),
            (By.XPATH, "//span[contains(text(), 'Xóa')]//ancestor::div[@role='menuitem']"),
            (By.XPATH, "//span[text()='Delete']//ancestor::div[@role='menuitem']"),
            (By.XPATH, "//div[@role='menuitem']//span[text()='Delete']"),
            (By.XPATH, "//span[contains(text(), 'Delete')]//ancestor::div[@role='menuitem']"),
        ]
        
        print(f"{prefix}Looking for delete option (Xóa)...")
        delete_option = find_first_element(driver, delete_selectors, timeout_seconds=5, mode='present')
        
        # Use JavaScript click for delete option too
        driver.execute_script("arguments[0].click();", delete_option)
        time.sleep(2)
        
        # Confirm deletion if a confirmation dialog appears
        confirm_selectors = [
            (By.XPATH, "//div[@aria-label='Xóa'][@role='button']"),
            (By.XPATH, "//div[@role='button']//span[text()='Xóa']"),
            (By.XPATH, "//span[text()='Xóa']//ancestor::div[@role='button']"),
            (By.XPATH, "//div[@aria-label='Delete'][@role='button']"),
            (By.XPATH, "//div[@role='button']//span[text()='Delete']"),
            (By.XPATH, "//span[text()='Delete']//ancestor::div[@role='button']"),
        ]
        
        try:
            print(f"{prefix}Looking for confirmation button...")
            confirm_button = find_first_element(driver, confirm_selectors, timeout_seconds=3, mode='present')
            driver.execute_script("arguments[0].click();", confirm_button)
            time.sleep(2)
            print(f"{prefix}✓ Comment deleted successfully")
            return True
        except TimeoutException:
            # No confirmation needed, already deleted
            print(f"{prefix}✓ Comment deleted successfully (no confirmation needed)")
            return True
            
    except TimeoutException as e:
        print(f"{prefix}✗ Timeout while trying to delete comment: {e}")
        return False
    except Exception as e:
        print(f"{prefix}✗ Error deleting comment: {e}")
        return False


def add_comment_to_post(driver: webdriver.Chrome, post_url: str, comment_text: str, account_name: str = "", auto_delete: bool = True) -> bool:
    """Add a comment to a specific Facebook post."""
    prefix = f"[{account_name}] " if account_name else ""
    try:
        print(f"{prefix}Opening post: {post_url}")
        driver.get(post_url)
        time.sleep(2)
        
        # Scroll down a bit to ensure comment box is visible
        driver.execute_script("window.scrollBy(0, 300);")
        time.sleep(1)
        
        # Find the comment box - try multiple selectors
        comment_box_selectors = [
            (By.XPATH, "//div[contains(@class, 'x1n2onr6')][@role='textbox']"),
            (By.XPATH, "//div[@class='x1n2onr6'][@contenteditable='true']"),
            (By.XPATH, "//div[contains(@class, 'x1n2onr6') and @contenteditable='true']"),
        ]
        
        print(f"{prefix}Looking for comment box...")
        comment_box = find_first_element(driver, comment_box_selectors, COMMENT_BOX_TIMEOUT_SECONDS, mode='clickable')
        
        # Click on the comment box
        print(f"{prefix}Clicking comment box...")
        comment_box.click()
        time.sleep(1)
        
        # Type the comment
        print(f"{prefix}Typing comment: {comment_text}")
        comment_box.send_keys(comment_text)
        time.sleep(2)
        
        # Press Enter to submit the comment
        print(f"{prefix}Submitting comment...")
        comment_box.send_keys(Keys.RETURN)
        time.sleep(3)
        
        print(f"{prefix}✓ Successfully commented on post")
        
        # Delete the comment after 5 seconds if requested
        if auto_delete:
            delete_comment(driver, account_name)
        
        return True
        
    except TimeoutException as e:
        print(f"{prefix}✗ Timeout error on post {post_url}: {e}")
        return False
    except Exception as e:
        print(f"{prefix}✗ Error commenting on post {post_url}: {e}")
        return False


def process_posts_with_account(account_module, account_name: str, auto_delete: bool = True) -> dict[str, int]:
    """Process all posts with a specific account."""
    print(f"\n{'='*60}")
    print(f"=== Processing with {account_name} ===")
    print(f"{'='*60}\n")
    
    driver = None
    try:
        driver = account_module.build_driver()
        
        # Login
        test_group_url = "https://www.facebook.com/groups/984940111090551"
        if not account_module.login_and_save(driver, test_group_url):
            print(f"\n{account_name}: Login failed!")
            return {"successful": 0, "failed": len(POST_URLS)}
        
        successful_comments = 0
        failed_comments = 0
        
        # Process each post URL
        for i, post_url in enumerate(POST_URLS, 1):
            print(f"\n[{account_name}] [{i}/{len(POST_URLS)}] Processing post...")
            
            # Select a random comment
            comment_text = random.choice(COMMENTS)
            
            # Add the comment
            success = add_comment_to_post(driver, post_url, comment_text, account_name, auto_delete)
            
            if success:
                successful_comments += 1
            else:
                failed_comments += 1
            
            # Wait before next comment (if not the last post)
            if i < len(POST_URLS):
                delay = random.randint(DELAY_BETWEEN_COMMENTS_SECONDS, DELAY_BETWEEN_COMMENTS_SECONDS + 5)
                print(f"[{account_name}] Waiting {delay} seconds before next comment...")
                time.sleep(delay)
        
        return {"successful": successful_comments, "failed": failed_comments}
        
    except Exception as e:
        print(f"[{account_name}] Error: {e}")
        import traceback
        traceback.print_exc()
        return {"successful": 0, "failed": len(POST_URLS)}
    finally:
        if driver:
            try:
                print(f"\n[{account_name}] Closing browser...")
                driver.quit()
            except Exception as e:
                print(f"[{account_name}] Error closing browser: {e}")


def main():
    """Main function to manage comments with dual accounts."""
    print("\n" + "="*60)
    print("=== Dual Account Comment Manager ===")
    print(f"=== Mode: {USE_ACCOUNTS.upper()} ===")
    print("="*60)
    
    total_stats = {
        "Account 1": {"successful": 0, "failed": 0},
        "Account 2": {"successful": 0, "failed": 0}
    }
    
    try:
        if USE_ACCOUNTS in ["account1", "both"]:
            stats = process_posts_with_account(facebook_login, "Account 1")
            total_stats["Account 1"] = stats
            
            if USE_ACCOUNTS == "both":
                print(f"\n\nWaiting {DELAY_BETWEEN_ACCOUNTS_SECONDS} seconds before switching accounts...")
                time.sleep(DELAY_BETWEEN_ACCOUNTS_SECONDS)
        
        if USE_ACCOUNTS in ["account2", "both"]:
            stats = process_posts_with_account(facebook_login_account2, "Account 2")
            total_stats["Account 2"] = stats
        
        # Final Summary
        print("\n" + "="*60)
        print("=== FINAL SUMMARY ===")
        print("="*60)
        print(f"Total posts to process: {len(POST_URLS)}")
        print()
        
        for account_name, stats in total_stats.items():
            if stats["successful"] > 0 or stats["failed"] > 0:
                print(f"{account_name}:")
                print(f"  ✓ Successful: {stats['successful']}")
                print(f"  ✗ Failed: {stats['failed']}")
                print()
        
        total_successful = sum(s["successful"] for s in total_stats.values())
        total_failed = sum(s["failed"] for s in total_stats.values())
        print(f"Overall Total:")
        print(f"  ✓ Successful: {total_successful}")
        print(f"  ✗ Failed: {total_failed}")
        print("="*60)
        
    except KeyboardInterrupt:
        print("\n\nStopped by user")
    except Exception as e:
        print(f"\n\nUnexpected error: {e}")
        import traceback
        traceback.print_exc()
    
    print("\n✓ Done!")


if __name__ == "__main__":
    main()
