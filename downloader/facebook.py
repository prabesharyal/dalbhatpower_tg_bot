import re, requests, os, time, psutil
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager


def init_driver():
    options= webdriver.ChromeOptions()
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    options.add_argument("--no-sandbox")
    options.add_argument("--headless")
    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)
    return driver

def force_exit_driver():
        PROCNAME = "geckodriver" #chromedriver
        for proc in psutil.process_iter():
            # check whether the process name matches
            if proc.name() == PROCNAME:
                proc.kill()


def go_to_post(driver, link):
    driver.get(link)
    driver.implicitly_wait(20)
    time.sleep(2)
    return driver

def extract_caption(driver):
    try:
        bio = driver.find_elements(
            By.CLASS_NAME, 'x1vvkbs')
        bio =  [alltexts.text for alltexts in bio]
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

def single_image_return(driver):
    try:
        single_img= driver.find_element(By.CSS_SELECTOR, 'div[class="x6s0dn4 x78zum5 xdt5ytf xl56j7k x1n2onr6"] img[data-visualcompletion="media-vc-image"]')
        image = single_img.get_attribute("src")
        return image
    except Exception as e:
        print("Not a Single Image")
        return None
    
def get_images(driver, url):
    images = [single_image_return(driver)]
    # print(images)
    pattern = r"(facebook\.com)\/groups\/[\w\.]+\/permalink\/[\d]+"
    if re.search(pattern, url):
        print("A Group URL So, abit different approach")
        try:
            check = driver.find_element(By.CSS_SELECTOR, 'div[class="x1egiwwb x4l50q0"]')
            try:
                cross_button = driver.find_element(By.CSS_SELECTOR, 'div[class="x92rtbv x10l6tqk x1tk7jg1 x1vjfegm"]')
                cross_button.click()
                driver.implicitly_wait(5)
            except Exception as e:
                "No Cross Button to hide login"
        except Exception as e:
            print("No Login Div")
        try:
            image_elem = driver.find_element(By.XPATH, '//*[@id=":r4:"]/div[1]/a/div[1]/div')
            image_elem.click()
            driver.implicitly_wait(5)
            image=[single_image_return(driver)]
            return image
        except Exception as e:
            return []
    else:
        try:
            if images[0]==None:
                try:
                    check = driver.find_element(By.CSS_SELECTOR, 'div[class="x1egiwwb x4l50q0"]')
                    try:
                        cross_button = driver.find_element(By.CSS_SELECTOR, 'div[class="x92rtbv x10l6tqk x1tk7jg1 x1vjfegm"]')
                        cross_button.click()
                        driver.implicitly_wait(5)
                    except Exception as e:
                        "No Cross Button to hide login"
                        driver.refresh()
                except Exception as e:
                    print("No Login Div")
                imagelist = driver.find_elements(
                    By.XPATH, '//*[@id=":Rlakldd6knpapd5aqH3:"]/div[1]/div/div')
                all_a_links = [extractedaelems.find_elements(By.TAG_NAME, 'a') for extractedaelems in imagelist]
                # print(all_a_links)
                image_srcs = [image.get_attribute("href") for image in all_a_links[0]]
                # print(image_srcs)
                images = [single_image_return(go_to_post(driver,photourl)) for photourl in image_srcs]
        except Exception as e:
            print("Error while browsing image group")
            print(e)
            return []
    return images

def save_file_from_url(url):
    response = requests.get(url,allow_redirects=False)
    try:
        url = response.headers['Location']
    except KeyError as e:
        url = url
    if response.status_code == 200:
        # Extract the file name from the URL
        file_name = url.split('/')[-1].split('?')[0]
        save_path = os.path.join(os.getcwd(), 'downloads')
        
        # Create the 'downloads' directory if it doesn't exist
        os.makedirs(save_path, exist_ok=True)
        
        prepared_file = os.path.join(save_path, file_name)
        # Save the file to the specified path
        with open(prepared_file, 'wb') as file:
            file.write(response.content)
            # print(f"File saved as: {file_name}")
            return prepared_file
    else:
        print("Not a valid Facebook download")
        # return None
        # return False


def selenium_fb_extractor(url):
    force_exit_driver()
    DRIVER = init_driver()
    try:
        driver = go_to_post(DRIVER,url)
        CAPTION, type = extract_caption(driver)
        url = driver.current_url
        if type == 'video' or type == 'reel':
            driver.quit()
            force_exit_driver()
            return 'status', "Videos and Reels Are Not Supported Yet", []
        elif type == 'unidentified':
            all_images = get_images(driver, url)
            all_images = [img for img in all_images if img is not None] or []
            if len(all_images)!=0:
                filelist = [save_file_from_url(vidurls) for vidurls in all_images if vidurls is not None] or []
                driver.quit()
                force_exit_driver()
                if CAPTION==None:
                    CAPTION="✨"
                else:
                    CAPTION=CAPTION
                if len(filelist)== 0:
                    return 'status', CAPTION, []
                return 'photos',CAPTION, filelist
            else:
                if CAPTION!=None:
                    return 'status', CAPTION, []
    except Exception as e:
        DRIVER.quit()
        force_exit_driver()
        print(e)
        return False, '', []    
# url = "https://www.facebook.com/abhishek.khanal.56679/posts/pfbid021GiUmqJUKLNf2hcV9ZQJq3yKgAdE68mC4d9Quk6Gf3TPDSxNV8CPCm8MhJ7dpKxQl" #media carousel - PASSED
# url = "https://www.facebook.com/100015665556479/posts/pfbid0TB1ZEV4CicbwMjPVKpyaGqgcCviwnZM3uM8dN7zRdN8Y4QbaShNcL1s6Azee2ozsl/?mibextid=CDWPTG" #perosnal_post_videos PASS by failing vid dont download
# url = 'https://www.facebook.com/indepthstorynepal/videos/2004231033247597' #Watch Videos - FAAILEEDD
# url = "https://www.facebook.com/photo/?fbid=305832228667189&set=a.174480058469074" - PASSED
# url = "https://www.facebook.com/reel/621835930093433" #Failed passes
# url = "https://www.facebook.com/100094556295766/videos/1726145681167198/" #- PASSED by failing
# url = "https://fb.watch/mEa3M35TeV/" #-Failed
# url = "https://fb.watch/mEaeuXK0_U/"
# url = "https://www.facebook.com/groups/nepali.hashyachitra.sansthan/permalink/1710329026133967/" #grpphoto - Fail   
# url = "https://www.facebook.com/groups/2616981278627207/permalink/3619074515084540/" #grpposts _ PASSED
# url ="https://www.facebook.com/photo?fbid=4299040640320573&set=pcb.4299042270320410" #singlephoto - PASSED
# url = "https://www.facebook.com/100009312595278/videos/1376171086270491/" #grpVid - PASSED

# url = 'https://www.facebook.com/groups/2616981278627207/permalink/3619783845013607/' #"PASSEWD"

def selenium_fb_dl(url):
    try:
        a,b,c=selenium_fb_extractor(url)
        force_exit_driver()
        # print(a,b,c)
        return a,b,c
    except Exception as e:
        force_exit_driver()
        return False, '', []


