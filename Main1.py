from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import os
import sys

# Path to your Chrome profile
home_directory = os.path.expanduser("~")

 # Construct the profile path
profile_path = os.path.join(home_directory, "AppData", "Local", "Google", "Chrome", "User  Data")
profile_name = "Default"  # Change this to your profile name

print(f"Profile Path: {profile_path}")
print(f"Profile Name: {profile_name}")
    
# Set up Chrome options
chrome_options = Options()
chrome_options.add_argument(f"--user-data-dir={profile_path}")  # Path to the User Data directory
chrome_options.add_argument(f"--profile-directory={profile_name}")  # Name of the profile
    
# Initialize the WebDriver
driver = webdriver.Chrome(options=chrome_options)
    
# Define Block Function (you can add your block function here)
 # ...


# You can now use the driver for further actions
def BlockPlayersFromFile(Usernames):
    print("blockplayerFromFile Started")
    # Get the current directory of the script
    current_directory = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(current_directory, Usernames)

    # Read profile links from the text file
    try:
        with open(file_path, 'r') as file:
            profile_links = file.readlines()
    except FileNotFoundError:
        print(f"Error: The file '{Usernames}' was not found in the directory '{current_directory}'.")
        return

    for link in profile_links:
        link = link.strip()  # Remove any whitespace or newline characters
        driver.get(link)
        driver.implicitly_wait(3)  # Increase wait time if necessary
        
        try:
            # Confirm the block action
            driver.execute_script("ConfirmBlock()")
            
            # Locate the button using its class name
            button = driver.find_element(By.CSS_SELECTOR, '.btn_green_steamui.btn_medium')
            # Click the button
            button.click()
            print(f"Button clicked successfully for {link}.")
            
            # Wait for confirmation message
            confirmation_text = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//div[contains(text(), 'You have blocked all communications with this player.')]"))
            )
            
            if confirmation_text:
                print(f"\033[31mBlock confirmed for {link}: You have blocked all communications with this player.\033[0m")
            else:
                print(f"Block not confirmed for {link}.")
        
        except Exception as e:
            print(f"An error occurred while blocking {link}: {e}")


def login():
    driver.get("https://store.steampowered.com/")
    driver.implicitly_wait(2)
    try:
        # Wait for the login link to be present
        login_link = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, 'global_action_link'))
    )
    
    # Check if the login link is visible
        if login_link.is_displayed() and "login" in login_link.text.lower():
            print("You are NOT logged in, something brokey :/)")
            while True:
                print("type 1 to close the application.")
                print("type 2 to redirect to manually log in")
                choice = input("Type Choice then press ENTER ")

                if choice == '1':
                    print("Closing the application.")
                    driver.quit()
                    sys.exit()
                    break
                elif choice == '2':
                    # Redirect to the login page
                    driver.get("https://store.steampowered.com/login/")
                    input("Press Enter to try again")
                    login()
                    break
        
        else:
            print("You are logged in.")
            driver.implicitly_wait(1)
            BlockPlayersFromFile("Usernames.txt")  # Pass the filename as a string
    

    except Exception as e:
        print("An error occurred:", e)
        input("Press Enter to close the browser...")


# Functions

login()

input("Press Enter to close the browser...")  # Keep the browser open until you press Enter
driver.quit()
sys.exit()