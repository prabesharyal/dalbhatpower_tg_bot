import os,time
from utils.loader import Loader
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
import urllib.request
from mytelegrammodules.commandhandlers.commonimports import *
import subprocess

class twiiter_dl(object):
        
    def __init__(self)->None:
        pass
        
    def extract_tweettext(self,driver):
        try:
            bio = driver.find_element(
                By.CSS_SELECTOR, 'div[data-testid="tweetText"]')
            bio = bio.text
            return bio
        except Exception as e:
            print('No Bio')
            bio = None
            return bio

    def extract_tweetimgs(self,driver):
        try:
            images = driver.find_elements(
                By.CLASS_NAME, 'css-9pa8cd')
            image_srcs = [image.get_attribute("src") for image in images]
            return image_srcs
        except Exception as e:
            print('No Links')
            image = None
            image_srcs = None
            return image_srcs
        
    def extract_m3u8_urls(self, driver):
        try:
            # Capture network requests
            performance = driver.execute_script(
                "return window.performance.getEntries()")
            m3u8_urls = [entry['name']
                        for entry in performance if entry['name'].endswith("fmp4")]
        except Exception as e:
            print('Error extracting M3U8 URLs:', e)
            m3u8_urls = None
        return m3u8_urls

    def selenium_extractor(self,link):
        options= webdriver.ChromeOptions()
        options.add_experimental_option('excludeSwitches', ['enable-logging'])
        options.add_argument("--no-sandbox")
        options.add_argument("--headless")
        driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)
        driver.get(link)
        driver.implicitly_wait(20)
        print("Sleeping 10 Seconds.")
        time.sleep(5)
        CAPTION = "✨" if self.extract_tweettext(
            driver) == None else self.extract_tweettext(driver)
        images = self.extract_tweetimgs(driver)
        if images != None and len(images)>1:
            images = images[1:]
        else:
            images = None
        videos = self.extract_m3u8_urls(driver) 
        if videos != None:
            total_extraction = len(videos)
            bestquality = videos[total_extraction-1:]
        else:
            bestquality=None
        return CAPTION, images, bestquality
    
    def scrape_download_tweet(self, url):
        print(url)
        try:
            CAPTION, e_images, e_videos = self.selenium_extractor(url)
            if e_images != None and len(e_images) != 0:
                imagelist=[]
                for imgs in e_images:
                    imgurl = imgs.split('webp')[0]+'jpg'
                    imgname = imgurl.split('/')[-1].split('?')[0] + '.jpg'
                    output_directory = os.path.join(os.getcwd(), 'downloads')
                    if not os.path.exists(output_directory):
                        os.makedirs(output_directory)
                    imgpath = os.path.join(
                        output_directory, imgname)
                    urllib.request.urlretrieve(imgurl, imgpath)
                    imagelist.append(imgpath)
                return 'images',CAPTION,imagelist
            elif e_videos != None and len(e_videos) != 0:
                videolist = []
                for video in e_videos:
                    url = video.split('?')[0]
                    video_name = video.split('/')[-1].split('.')[0]
                    output_directory = os.path.join(os.getcwd(), 'downloads')
                    output_file = os.path.join(output_directory, f'{video_name}.mp4')
                    if not os.path.exists(output_directory):
                        os.makedirs(output_directory)
                
                    with Loader("Downloading and Converting Video: ","Download Status : "):
                        command = f'ffmpeg -i "{url}" -c copy -y "{output_file}"'
                        process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                        stdout, stderr = process.communicate()
                        if process.returncode != 0 or "Error" in stderr.decode('utf-8'):
                            print("An error occurred during conversion:")
                            print(stderr.decode('utf-8'))
                            return False, None, None
                    print("Conversion successful!")
                    videolist.append(output_file)
                return 'video', CAPTION, videolist
            else:
                imagelist= None
                videolist= None
            if CAPTION != "✨":
                return 'empty', CAPTION, None
            else:
                return False, None, None
        except Exception as e:
            print(e)
            return False, None, None
        
                
# url = "https://twitter.com/isro/status/1694248755594436829" # 2
# url = "https://twitter.com/HumansNoContext/status/1694231831489462468" #-1
# url = "https://twitter.com/stqnerTTV/status/1694231891413537199" #-nopix
# url = "https://twitter.com/NoContextHumans/status/1694114389626867891?s=20" #notworking
# url = "https://twitter.com/isro/status/1694327198394863911?s=20" #only tweet
# url = 'https://twitter.com/isro/status/1693911595720823129?s=20'
# url = "https://twitter.com/neuzboy/status/1694211537647640800?s=20"

# instance = twiiter_dl()  
# typpe, cap, liist = instance.scrape_download_tweet(url)       
# print(typpe)
# print(cap)
# print(liist)        
        

        
        


    

