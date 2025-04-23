from selenium import webdriver
from selenium.webdriver.edge.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from urllib.parse import urlparse
import time

class LinkedinMember:
    def __init__(self, name, title, link):
        self.name = name
        self.title = title
        self.link = link

    def __repr__(self):
        return f"LinkedinMember(name={self.name}, title={self.title}, link={self.link})"


class LinkedinDirectory:
    def __init__(self):
        self.members = {}

    def add_member(self, member):
        if member.name in self.members:
            self.members[member.name].append(member)
        else:
            self.members[member.name] = [member]

    def get_members(self):
        return self.members

"""
Function that will login to Linkedin with the given email and password provided. 

def login(email, passwrd)

Parameters:
email: input linkedin account email
passwrd: input linkedin account password
"""
def login(driver, email, passwrd):
    print("Attempting to Login")
    try:
        username = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, 'username'))
        )
        password = driver.find_element(By.ID, 'password')

        username.send_keys(email)
        password.send_keys(passwrd)

        signin_button = driver.find_element(By.CLASS_NAME, 'btn__primary--large')
        signin_button.click()
    except Exception as e:
        print(f"Failed logging in: {e}")
        quit()

"""
Function that will search a random generated phrase and select the People tab

Manipulates the linkedin web page scructure to have the page filtered for only People.
"""
def set_up_search(driver):
    try:
        print("Setting up so People are the only results for searches.")
        driver.get("https://www.linkedin.com/search/results/people/") 
    except Exception as e:
        print(f"Failed to select People button to filter. Please rerun the script as maybe ")


"""
Function that will search the position title with the companies name. 

def searchName(title, company)

Parameters:
title: name of position
company: company's name
"""
def searchName(driver, title, company):
    search_string = f"{title} \"{company}\""
    print(f"Searching for: {search_string}")

    try:
        search_box = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'input[aria-label="Search"]'))
        )
        search_box.clear()
        search_box.send_keys(search_string)
        search_box.send_keys(Keys.RETURN)
    except Exception as e:
        print(f'Error searching for name: {e}')

"""
Function that will return the link of the top candidate from the search. 

def getLink()
"""
def wait_for_js_to_load(driver):
    """Function to wait until the JavaScript on the page has fully loaded."""
    WebDriverWait(driver, 10).until(
        lambda driver: driver.execute_script('return document.readyState') == 'complete'
    )

def getLink(driver):
    """Function that will return the link of the top candidate from the search."""
    print("Attempting to grab the profile link...")
    try:
        # Wait for JavaScript to finish rendering the search results
        wait_for_js_to_load(driver)

        # Wait for search results to appear on the page
        search_results = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.XPATH, '//a[contains(@href, "/in/")]'))  # Look for profile links
        )

        if search_results:
            link = search_results[0]  # Get the first profile link (or you could loop through them)
            href_value = link.get_attribute('href')
            
            try:
                # Find the <img> tag inside the <a> tag and get the alt attribute (which contains the name)
                img_element = link.find_element(By.XPATH, './/img')
                name = img_element.get_attribute('alt').strip()
                print(f"Profile name: {name}")
            except Exception as e:
                print(f"Error extracting name from alt attribute: {e}")
                try:
                    name_attribute = search_results[1]
                    name_span = name_attribute.find_element(By.XPATH, './/span[@aria-hidden="true"]')
                    name = name_span.text.strip()
                    print(f"Profile name from span: {name}")
                except Exception as e:
                    print(f"Error extracting name from <span>: {e}")
                    return None, None

            if href_value and '/in/' in href_value:
                parsed_url = urlparse(href_value)
                base_profile_url = f"{parsed_url.scheme}://{parsed_url.netloc}{parsed_url.path}"
                print(f"Profile link (base URL): {base_profile_url}")
                return name, base_profile_url

        else:
            print("No profile links found!")
            return None, None

    except Exception as e:
        print(f"Error pulling link: {e}")
        return None, None
