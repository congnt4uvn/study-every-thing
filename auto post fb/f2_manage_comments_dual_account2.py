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
import f1_facebook_login
import f2_facebook_login_account2

# Configuration
POST_URLS = [


"https://www.facebook.com/share/p/1EXKLYWXMP/",
"https://www.facebook.com/share/p/17j6iMPFPy/",
"https://www.facebook.com/share/p/1BNzab5Kig/",
"https://www.facebook.com/share/p/1Hw5L49YsE/",
"https://www.facebook.com/share/p/199mXYe3FD/",
"https://www.facebook.com/share/p/1C2XPTZnbT/",
"https://www.facebook.com/share/p/1BncCspwEj/",
"https://www.facebook.com/share/p/19L4ZFkcXJ/",
"https://www.facebook.com/share/p/1K962dv7tA/",
"https://www.facebook.com/share/p/1GQ7vJvDQA/",
"https://www.facebook.com/share/p/1EH6pszAAF/",
"https://www.facebook.com/share/p/1BqFCk7GA3/",
"https://www.facebook.com/share/p/1BMp9DdAVY/",
"https://www.facebook.com/share/p/19BQfjWYUa/",
"https://www.facebook.com/share/p/1CmrgcCcEf/",
"https://www.facebook.com/share/p/1BT7zTuhsm/",
"https://www.facebook.com/share/p/1cnAbq1kTE/",
"https://www.facebook.com/share/p/19FTPF54ww/",
"https://www.facebook.com/share/p/18uVUFpkf1/",
"https://www.facebook.com/share/p/1BknfAbQ52/",
"https://www.facebook.com/share/p/1PJQrepyte/",
"https://www.facebook.com/share/p/1H2SLSGSmm/",
"https://www.facebook.com/share/p/1JNBF6Dv9G/"
]

COMMENTS = [
    "inbox",
    "ib"
]

# Which accounts to use: "account1", "account2", or "both"
# USE_ACCOUNTS: Literal["account1", "account2", "both"] = "both"

# only use account1
#USE_ACCOUNTS: Literal["account1", "account2", "both"] = "account1"

# only use account2
USE_ACCOUNTS: Literal["account1", "account2", "both"] = "account2"

POST_LOAD_TIMEOUT_SECONDS = 3000
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
            # Look for button with "Edit or delete" aria-label (English priority)
            (By.XPATH, "//div[@role='button' and @aria-haspopup='menu' and contains(@aria-label, 'Edit')]"),
            (By.XPATH, "//div[@role='button' and @aria-haspopup='menu' and contains(@aria-label, 'delete')]"),
            (By.XPATH, "//div[@role='button' and @aria-haspopup='menu' and contains(@aria-label, 'More')]"),
            (By.XPATH, "//div[contains(@aria-label, 'More')][@role='button']"),
            # Look inside the container div
            (By.XPATH, "//div[contains(@class, 'x1rg5ohu') and contains(@class, 'xxymvpz')]//div[@role='button' and @aria-haspopup='menu']"),
            # Button with specific class combination
            (By.XPATH, "//div[contains(@class, 'x1i10hfl') and contains(@class, 'xjbqb8w') and contains(@class, 'x1n2onr6') and @role='button' and @aria-haspopup='menu']"),
            # Generic menu button
            (By.XPATH, "//div[@role='button' and @aria-haspopup='menu']"),
            # Fallback: Vietnamese
            (By.XPATH, "//div[contains(@aria-label, 'Chỉnh sửa')][@role='button']"),
            (By.XPATH, "//div[contains(@aria-label, 'Khác')][@role='button']"),
            (By.CSS_SELECTOR, "div[role='button'][aria-haspopup='menu']"),
        ]
        
        print(f"{prefix}Looking for comment menu button (...)...")
        menu_button = find_first_element(driver, menu_selectors, timeout_seconds=10, mode='present')
        
        # Ensure we have the actual button element with role='button'
        try:
            if menu_button.get_attribute('role') != 'button':
                print(f"{prefix}Found container div, searching for the actual button inside...")
                # Try to find the button inside the container
                inner_button = menu_button.find_element(By.XPATH, ".//div[@role='button' and @aria-haspopup='menu']")
                menu_button = inner_button
                print(f"{prefix}Found button inside container")
        except Exception as e:
            print(f"{prefix}Using found element as-is: {e}")
        
        # Log what we found
        try:
            aria_label = menu_button.get_attribute('aria-label') or 'No label'
            print(f"{prefix}Button found - Role: {menu_button.get_attribute('role')}, Label: {aria_label}")
        except:
            pass
        
        # Scroll the menu button into view
        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", menu_button)
        time.sleep(1)
        
        # Remove any overlays that might block the click
        driver.execute_script("""
            var element = arguments[0];
            element.style.pointerEvents = 'auto';
            element.style.zIndex = '9999';
        """, menu_button)
        
        # Try multiple click methods
        print(f"{prefix}Clicking menu button (Tag: {menu_button.tag_name}, Role: {menu_button.get_attribute('role')})...")
        clicked = False
        try:
            # First try: JavaScript click
            driver.execute_script("arguments[0].click();", menu_button)
            clicked = True
            print(f"{prefix}Clicked with JavaScript")
        except Exception as e:
            print(f"{prefix}JS click failed: {e}")
            try:
                # Second try: Regular click after waiting
                WebDriverWait(driver, 5).until(EC.element_to_be_clickable(menu_button))
                menu_button.click()
                clicked = True
                print(f"{prefix}Clicked with Selenium")
            except Exception as e2:
                print(f"{prefix}Selenium click failed: {e2}")
                try:
                    # Third try: Action chains
                    from selenium.webdriver.common.action_chains import ActionChains
                    ActionChains(driver).move_to_element(menu_button).click().perform()
                    clicked = True
                    print(f"{prefix}Clicked with ActionChains")
                except Exception as e3:
                    print(f"{prefix}ActionChains click failed: {e3}")
        
        if not clicked:
            print(f"{prefix}WARNING: All click methods failed, attempting to continue...")
        time.sleep(2)
        
        # Find and click the Delete option (English)
        delete_selectors = [
            # Try menuitem role with Delete text (English priority)
            (By.XPATH, "//div[@role='menuitem']//span[text()='Delete']"),
            (By.XPATH, "//div[@role='menuitem' and contains(., 'Delete')]"),
            (By.XPATH, "//span[text()='Delete']//ancestor::div[@role='menuitem']"),
            (By.XPATH, "//span[contains(text(), 'Delete')]//ancestor::div[@role='menuitem']"),
            # Specific span classes with text
            (By.XPATH, "//span[@class='x193iq5w xeuugli x13faqbe x1vvkbs x1xmvt09 x1lliihq x1s928wv xhkezso x1gmr53x x1cpjm7i x1fgarty x1943h6x xudqn12 x3x7a5m x6prxxf xvq8zen xk50ysn xzsf02u x1yc453h' and text()='Delete']"),
            (By.XPATH, "//span[contains(@class, 'x193iq5w') and contains(@class, 'xeuugli') and text()='Delete']"),
            # Fallback: Vietnamese (in case language setting changes)
            (By.XPATH, "//div[@role='menuitem']//span[text()='Xóa']"),
            (By.XPATH, "//span[text()='Xóa']//ancestor::div[@role='menuitem']"),
        ]
        
        print(f"{prefix}Looking for delete option (Delete)...")
        delete_option = find_first_element(driver, delete_selectors, timeout_seconds=1, mode='present')
        
        # Log what we found
        try:
            delete_text = delete_option.text or 'No text'
            delete_role = delete_option.get_attribute('role') or 'No role'
            print(f"{prefix}Delete option found - Role: {delete_role}, Text: {delete_text}")
        except:
            pass
        
        # Scroll and prepare delete option
        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", delete_option)
        time.sleep(0.5)
        
        # Try multiple click methods for delete option
        print(f"{prefix}Clicking delete option...")
        delete_clicked = False
        try:
            driver.execute_script("arguments[0].click();", delete_option)
            delete_clicked = True
            print(f"{prefix}Delete option clicked with JavaScript")
        except Exception as e:
            print(f"{prefix}JS click failed: {e}")
            try:
                delete_option.click()
                delete_clicked = True
                print(f"{prefix}Delete option clicked with Selenium")
            except Exception as e2:
                print(f"{prefix}Selenium click failed: {e2}")
                try:
                    from selenium.webdriver.common.action_chains import ActionChains
                    ActionChains(driver).move_to_element(delete_option).click().perform()
                    delete_clicked = True
                    print(f"{prefix}Delete option clicked with ActionChains")
                except Exception as e3:
                    print(f"{prefix}ActionChains click failed: {e3}")
        
        if not delete_clicked:
            print(f"{prefix}WARNING: All delete click methods failed")
        time.sleep(2)
        
        # Confirm deletion if a confirmation dialog appears
        confirm_selectors = [
            # Look for Delete button in confirmation dialog/popup (English priority)
            (By.XPATH, "//div[@role='dialog']//div[@role='button' and @aria-label='Delete']"),
            (By.XPATH, "//div[@role='dialog']//div[@role='button']//span[text()='Delete']"),
            (By.XPATH, "//div[@role='dialog']//span[text()='Delete']//ancestor::div[@role='button']"),
            # Look for button with specific classes in dialog
            (By.XPATH, "//div[@role='dialog']//div[contains(@class, 'x1i10hfl') and @role='button' and @aria-label='Delete']"),
            # Generic confirmation button selectors with container
            (By.XPATH, "//div[contains(@class, 'x1rg5ohu') and contains(@class, 'xxymvpz')]//div[@role='button' and @aria-label='Delete']"),
            (By.XPATH, "//div[contains(@class, 'x1i10hfl') and contains(@class, 'xjbqb8w') and @role='button' and @aria-label='Delete']"),
            # Direct button selectors
            (By.XPATH, "//div[@aria-label='Delete'][@role='button']"),
            (By.XPATH, "//div[@role='button']//span[text()='Delete']"),
            (By.XPATH, "//span[text()='Delete']//ancestor::div[@role='button']"),
            # CSS selectors
            (By.CSS_SELECTOR, "div[role='dialog'] div[role='button'][aria-label='Delete']"),
            (By.CSS_SELECTOR, "div[role='button'][aria-label='Delete']"),
            (By.CSS_SELECTOR, "div[class*='x1rg5ohu'] div[role='button']"),
            # Fallback: Vietnamese (in case language setting changes)
            (By.XPATH, "//div[@role='dialog']//div[@role='button' and @aria-label='Xóa']"),
            (By.XPATH, "//div[@role='dialog']//span[text()='Xóa']//ancestor::div[@role='button']"),
            (By.XPATH, "//div[@aria-label='Xóa'][@role='button']"),
            (By.XPATH, "//span[text()='Xóa']//ancestor::div[@role='button']"),
        ]
        
        try:
            print(f"{prefix}Looking for confirmation button...")
            confirm_button = find_first_element(driver, confirm_selectors, timeout_seconds=5, mode='present')
            
            # Try to verify we're in a confirmation dialog
            try:
                dialog = driver.find_element(By.XPATH, "//div[@role='dialog']")
                dialog_text = dialog.text
                if 'sure' in dialog_text.lower() or 'confirm' in dialog_text.lower() or 'delete' in dialog_text.lower():
                    print(f"{prefix}Confirmation dialog detected: {dialog_text[:50]}...")
            except:
                pass
            
            # Check if we found a parent container instead of the button itself
            try:
                if confirm_button.get_attribute('role') != 'button':
                    print(f"{prefix}Found container, searching for button inside...")
                    inner_button = confirm_button.find_element(By.XPATH, ".//div[@role='button']")
                    confirm_button = inner_button
            except:
                pass
            
            # Log what we found
            try:
                confirm_label = confirm_button.get_attribute('aria-label') or 'No label'
                confirm_text = confirm_button.text or 'No text'
                print(f"{prefix}Confirm button found - Label: {confirm_label}, Text: {confirm_text}")
            except:
                pass
            
            # Scroll to confirmation button
            driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", confirm_button)
            time.sleep(0.5)
            
            # Remove any overlays
            driver.execute_script("""
                var element = arguments[0];
                element.style.pointerEvents = 'auto';
                element.style.zIndex = '9999';
            """, confirm_button)
            
            # Try multiple click methods
            print(f"{prefix}Clicking confirmation button (Tag: {confirm_button.tag_name}, Role: {confirm_button.get_attribute('role')})...")
            clicked = False
            try:
                driver.execute_script("arguments[0].click();", confirm_button)
                clicked = True
                print(f"{prefix}Confirmation clicked with JavaScript")
            except Exception as e:
                print(f"{prefix}JS click failed: {e}")
                try:
                    WebDriverWait(driver, 5).until(EC.element_to_be_clickable(confirm_button))
                    confirm_button.click()
                    clicked = True
                    print(f"{prefix}Confirmation clicked with Selenium")
                except Exception as e2:
                    print(f"{prefix}Selenium click failed: {e2}")
                    try:
                        from selenium.webdriver.common.action_chains import ActionChains
                        ActionChains(driver).move_to_element(confirm_button).click().perform()
                        clicked = True
                        print(f"{prefix}Confirmation clicked with ActionChains")
                    except Exception as e3:
                        print(f"{prefix}ActionChains click failed: {e3}")
            
            if not clicked:
                print(f"{prefix}WARNING: All confirmation click methods failed")
            
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
            stats = process_posts_with_account(f2_facebook_login_account2, "Account 2")
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
    while True:
        main()