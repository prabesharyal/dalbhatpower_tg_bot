import re, requests, os, time, psutil
from utils.loader import Loader

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager




# def init_driver():
#     options= webdriver.ChromeOptions()
#     options.add_experimental_option('excludeSwitches', ['enable-logging'])
#     options.add_argument("--start-maximized")

#     # driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)
#     driver = webdriver.Chrome(options=options)
#     return driver


def init_driver():
    options= webdriver.ChromeOptions()
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    options.add_argument("--no-sandbox")
    options.add_argument("--headless")
    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)
    return driver

def force_exit_driver():
        PROCNAME = "geckodriver" # or chromedriver IEDriverServer
        for proc in psutil.process_iter():
            # check whether the process name matches
            if proc.name() == PROCNAME:
                proc.kill()

def wait_for_element(driver, class_name, timeout):
    start_time = time.time()
    while True:
        if time.time() - start_time > timeout:
            # Timeout reached, exit the loop
            break
        try:
            element = WebDriverWait(driver, 1).until(
                EC.presence_of_element_located((By.CLASS_NAME, class_name))
            )
            print("Element found:", class_name)
            break  # Exit the loop when the element is found
        except Exception as e:
            pass 

def extract_caption(driver):
    try:
        elements = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.CLASS_NAME, 'x1vvkbs'))
        )
        bio =  [alltexts.text for alltexts in elements]
        index = len(bio)-1
        if bio[3]=='Video' and bio[index-5]=='Discover more videos on Facebook':
            bio = bio[14]
            type = 'video'
        elif bio[len(bio)-1]=='Reels':
            bio = bio[3]
            type = 'reel'
        else:
            bio = bio[3] + '\n' + bio[6]
            type = 'unidentified'
        return bio, type
    except Exception as e:
        print("No Caption Maybe")
        print(e)
        bio = None
        return bio, False

def go_to(driver,link):
    driver.get(link)
    driver.implicitly_wait(5)
    time.sleep(2)
    return driver

def get_vid(driver, url):
    url_input = driver.find_element(By.XPATH, '//*[@id="url"]')
    url_input.send_keys(url)
    url_input.send_keys(Keys.ENTER)
    wait_for_element(driver, 'button is-success is-small', 10)
    try:
        # Capture network requests
        performance = driver.execute_script(
            "return window.performance.getEntries()")
        # Extract URLs containing '.mp4' in the middle
        mp4_urls = [entry['name']
                    for entry in performance if '.mp4' in entry['name']]
        if mp4_urls:
            return mp4_urls[0]
        time.sleep(1)
    except Exception as e:
        return None# Continue the loop if there's an exception


def extract_filename_from_url(url):
    # Split the URL by '/' and get the last part
    pattern = r'([\w]+\.mp4)'
    match = re.search(pattern, url)
    filename = match.group(1)
    return filename

def download_video(url):
    try:
        # Extract the filename from the URL
        filename = extract_filename_from_url(url)
        
        # Specify the local file path where you want to save the video
        local_dir =  os.path.join(os.getcwd(),"downloads")
        local_filepath = os.path.join(local_dir, filename)

        # Send an HTTP GET request to fetch the video content
        response = requests.get(url, stream=True)

        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            # Create the "downloads" directory if it doesn't exist
            os.makedirs(local_dir, exist_ok=True)

            # Open a local file for writing the video content
            with Loader("Downloading Video : ","Downloaded! "):
                with open(local_filepath, 'wb') as video_file:
                    for chunk in response.iter_content(chunk_size=1024):
                        if chunk:
                            video_file.write(chunk)
            print(f"Video saved as {local_filepath}")
            return local_filepath
        else:
            print(f"Failed to download video. Status code: {response.status_code}")
            return False
    except Exception as e:
        print(f"An error occurred: {str(e)}")


def main_fb_dl(url):
    try:
        force_exit_driver()
        with Loader("Running : ", "Done !"):
            DRIVER = init_driver()
            print(" Getting Caption ", end='', flush=True)
            biodriver = go_to(DRIVER,url)
            CAPTION, exists= extract_caption(biodriver)
            CAPTION = "✨" if exists==False else CAPTION
            print(" Getting Video Link ", end='', flush=True)
            driver = go_to(DRIVER,'https://snapsave.app')
            url = get_vid(driver, url)
            driver.quit()
            force_exit_driver()
            if url != None:
                print(" Successfully Acquired Video Link ", end='', flush=True)
                print("\n")
                filepath = [download_video(url)]
                return True, CAPTION, filepath
            else:
                return False, None, []
    except BaseException as e:
        print(e)
        return False, None, []
    