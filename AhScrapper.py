import os
import requests
import re
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from colorama import Fore, init
import time

init(autoreset=True)

ascii_art = f"""
                ==============================================================                                                                                              
                            {Fore.YELLOW}  -> ({Fore.CYAN}https://guns.lol/j_hoover{Fore.YELLOW})))) <-                
                            {Fore.YELLOW}  -> ({Fore.CYAN}https://guns.lol/asterfion{Fore.YELLOW}))) <-           
                            {Fore.YELLOW}  -> ({Fore.CYAN}Made by Asterfion and Hades{Fore.YELLOW})) <-                  
                            {Fore.YELLOW}  -> ({Fore.CYAN}Guns.lol | Scrapper | Goated{Fore.YELLOW}) <- 
            
                ==============================================================                                          
{Fore.CYAN}                           
                                                                       


 ▄▄▄       ██░ ██      ██████  ▄████▄   ██▀███   ▄▄▄       ██▓███   ██▓███  ▓█████  ██▀███  
▒████▄    ▓██░ ██▒   ▒██    ▒ ▒██▀ ▀█  ▓██ ▒ ██▒▒████▄    ▓██░  ██▒▓██░  ██▒▓█   ▀ ▓██ ▒ ██▒
▒██  ▀█▄  ▒██▀▀██░   ░ ▓██▄   ▒▓█    ▄ ▓██ ░▄█ ▒▒██  ▀█▄  ▓██░ ██▓▒▓██░ ██▓▒▒███   ▓██ ░▄█ ▒
░██▄▄▄▄██ ░▓█ ░██      ▒   ██▒▒▓▓▄ ▄██▒▒██▀▀█▄  ░██▄▄▄▄██ ▒██▄█▓▒ ▒▒██▄█▓▒ ▒▒▓█  ▄ ▒██▀▀█▄  
 ▓█   ▓██▒░▓█▒░██▓   ▒██████▒▒▒ ▓███▀ ░░██▓ ▒██▒ ▓█   ▓██▒▒██▒ ░  ░▒██▒ ░  ░░▒████▒░██▓ ▒██▒
 ▒▒   ▓▒█░ ▒ ░░▒░▒   ▒ ▒▓▒ ▒ ░░ ░▒ ▒  ░░ ▒▓ ░▒▓░ ▒▒   ▓▒█░▒▓▒░ ░  ░▒▓▒░ ░  ░░░ ▒░ ░░ ▒▓ ░▒▓░
  ▒   ▒▒ ░ ▒ ░▒░ ░   ░ ░▒  ░ ░  ░  ▒     ░▒ ░ ▒░  ▒   ▒▒ ░░▒ ░     ░▒ ░      ░ ░  ░  ░▒ ░ ▒░
  ░   ▒    ░  ░░ ░   ░  ░  ░  ░          ░░   ░   ░   ▒   ░░       ░░          ░     ░░   ░ 
      ░  ░ ░  ░  ░         ░  ░ ░         ░           ░  ░                     ░  ░   ░     
                              ░                                                             

                             
"""

print(Fore.YELLOW + ascii_art)

def sanitize_filename(filename):
    sanitized_name = re.sub(r'[<>:"/\\|?*]', '_', filename)
    
    max_filename_length = 200  
    if len(sanitized_name) > max_filename_length:
        sanitized_name = sanitized_name[:max_filename_length] 
    
    return sanitized_name

def update_file_name(media_info, file_url):
    gun_name = media_info['page_title'].replace(" ", "_")  
    sanitized_gun_name = sanitize_filename(gun_name) 
    
    file_name = file_url.split("/")[-1]
    sanitized_name = sanitize_filename(file_name)
    
    new_file_name = f"{sanitized_gun_name}__AH-GUNS.LOL-SCRAPPER__{sanitized_name}"
    return new_file_name

def get_url():
    url = input(Fore.YELLOW + f"-> Enter the URL:{Fore.WHITE} ")
    return url

def create_folder(url):
    folder_name = url.split("/")[-1]
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)
    return folder_name

def initialize_driver():
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--log-level=3")
    chrome_options.add_argument("--disable-extensions")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    return driver

def download_file(url, file_name, log_file_name):
    if len(file_name) > 240: 
        file_name = file_name[:240]  
    folder = os.path.dirname(file_name)
    
    if not os.path.exists(folder):
        os.makedirs(folder)
    
    try:
        response = requests.get(url, stream=True)
        response.raise_for_status()
        
        total_size = int(response.headers.get('content-length', 0))
        
        with open(file_name, 'wb') as f:
            if total_size == 0:
                f.write(response.content)
            else:
                downloaded = 0
                for data in response.iter_content(chunk_size=1024):
                    downloaded += len(data)
                    f.write(data)
                    percent = (downloaded / total_size) * 100
                    print(Fore.GREEN + f"\r-> Downloading: {file_name} [{percent:.2f}%]", end="")
                print()
    
    except requests.exceptions.RequestException as e:
        print(Fore.RED + f"\n-> Error downloading {file_name}: {e}")
        with open(log_file_name, 'a') as log_file:
            log_file.write(f"-> Error downloading {file_name}: {e}\n")


def log_media_info(media_info, log_file_name):
    with open(log_file_name, 'a') as log_file:
        if media_info['videos']:
            log_file.write("\n-> Videos found:\n")
            for video in media_info['videos']:
                log_file.write(f"  - {video}\n")
        if media_info['audios']:
            log_file.write("\n-> Audios found:\n")
            for audio in media_info['audios']:
                log_file.write(f"  - {audio}\n")
        if media_info['images']:
            log_file.write("\n-> Images found:\n")
            for image in media_info['images']:
                log_file.write(f"  - {image}\n")
        if media_info['cursor']:
            log_file.write(f"\n-> Custom cursor found: {media_info['cursor']}\n")
        log_file.write(f"-> Metadata: {media_info['metadata']}\n")

def scrape_media(driver, url):
    driver.get(url)
    driver.implicitly_wait(10)

    media_info = {
        'videos': [],
        'audios': [],
        'images': [],
        'cursor': None,
        'page_title': driver.title,
        'metadata': {}
    }

    images = driver.find_elements(By.TAG_NAME, 'img')
    for image in images:
        img_src = image.get_attribute('src')
        if img_src:
            media_info['images'].append(img_src)

    videos = driver.find_elements(By.TAG_NAME, 'video')
    for video in videos:
        media_info['videos'].append(video.get_attribute('src'))

    audios = driver.find_elements(By.TAG_NAME, 'audio')
    for audio in audios:
        media_info['audios'].append(audio.get_attribute('src'))

    style_elements = driver.find_elements(By.TAG_NAME, "style")
    for style in style_elements:
        style_content = style.get_attribute("innerHTML")
        if "cursor:" in style_content and "url(" in style_content:
            cursor_start = style_content.find("url(") + len("url(")
            cursor_end = style_content.find(")", cursor_start)
            cursor_url = style_content[cursor_start:cursor_end]
            media_info['cursor'] = cursor_url
            break

    meta_tags = driver.find_elements(By.TAG_NAME, 'meta')
    for meta in meta_tags:
        meta_name = meta.get_attribute('name')
        meta_content = meta.get_attribute('content')
        if meta_name and meta_content:
            media_info['metadata'][meta_name] = meta_content

    return media_info

def login_if_needed(driver):
    try:
        login_button = driver.find_element(By.XPATH, "//button[contains(text(), 'Login')]")
        if login_button:
            print(Fore.YELLOW + "-> Login required, proceeding with login...")
            login_button.click()
            time.sleep(5)  
    except Exception as e:
        print(Fore.GREEN + "-> No login required, proceeding with scraping...")

def main():
    while True:
        url = get_url()
        folder_name = create_folder(url)
        log_file_name = os.path.join(folder_name, "AH-Scraping_log-AH.txt")
        
        with open(log_file_name, 'w') as log_file:
            log_file.write(f"-> Made by Asterfion and Hades - https://guns.lol/asterfion - https://guns.lol/j_hoover \n-> Scraping started for {url} on {datetime.now()}\n\n")

        driver = initialize_driver()
        login_if_needed(driver) 
        media_info = scrape_media(driver, url)

        log_media_info(media_info, log_file_name)

        for video in media_info['videos']:
            video_name = os.path.join(folder_name, update_file_name(media_info, video))
            print(Fore.CYAN + f"\n-> Downloading video: {video}")
            download_file(video, video_name, log_file_name)

        for audio in media_info['audios']:
            audio_name = os.path.join(folder_name, update_file_name(media_info, audio))
            print(Fore.CYAN + f"\n-> Downloading audio: {audio}")
            download_file(audio, audio_name, log_file_name)

        for image in media_info['images']:
            image_name = os.path.join(folder_name, update_file_name(media_info, image))
            print(Fore.CYAN + f"\n-> Downloading image: {image}")
            download_file(image, image_name, log_file_name)

        if media_info['cursor']:
            cursor_name = os.path.join(folder_name, "AHSCRAPPER-Cursor.cur")
            print(Fore.CYAN + f"\n-> Downloading cursor: {media_info['cursor']}")
            download_file(media_info['cursor'], cursor_name, log_file_name)

        with open(log_file_name, 'a') as log_file:
            log_file.write(f"\n-> Download completed for {url} on {datetime.now()}\n")
            log_file.write("-> Files downloaded successfully:\n")
            log_file.write(f"-> Videos: {len(media_info['videos'])}\n")
            log_file.write(f"-> Audios: {len(media_info['audios'])}\n")
            log_file.write(f"-> Images: {len(media_info['images'])}\n")
            if media_info['cursor']:
                log_file.write(f"-> Custom Cursor: {media_info['cursor']}\n")
            log_file.write("\n")

        driver.quit()  
        print(Fore.GREEN + "\n-> Scraping and downloading completed successfully!")

        restart = input(Fore.YELLOW + f"\n-> Do you want to scrape another URL? (y/n):{Fore.WHITE} ")
        if restart.lower() != 'y':
            print(Fore.GREEN + "\n-> Exiting the program...")
            break

if __name__ == "__main__":
    main()
