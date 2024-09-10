import yt_dlp
import requests
import re

link = "https://www.tiktok.com/@ruang.rakyat/video/7311900622423362848?is_from_webapp=1&sender_device=pc"  #
# link = "https://vt.tiktok.com/ZSNs3eATL/"  # story
# # link = "https://vt.tiktok.com/ZSNs3eGAp/" - pictures
# link = "https://vt.tiktok.com/ZSNs3eGAp/"  # pictures
# //*[@id="main-content-video_detail"]/div/div[2]/div/div[1]/div[2]/div[2]/h1
# link = "https://www.tiktok.com/@cinnamon_girlll0/video/7305513849812208898"

# from selenium import webdriver

# from selenium.webdriver.chrome.service import Service as ChromeService
# from webdriver_manager.chrome import ChromeDriverManager

# # Ensure PhantomJS is installed and the path is correct
# driver = webdriver.Chrome("chromedriver.exe")

# options = webdriver.ChromeOptions()
# options.add_experimental_option("excludeSwitches", ["enable-logging"])
# options.add_argument("--no-sandbox")
# options.add_argument("--headless")
# # driver = webdriver.Chrome(
# #     service=ChromeService(ChromeDriverManager().install()), options=options
# # )


# driver.get(link)
# driver.implicitly_wait(30)

# page_title = driver.title
# try:
#     heading = driver.find_element_by_xpath(
#         '//*[@id="main-content-video_detail"]/div/div[2]/div/div[1]/div[2]/div[2]/h1'
#     )
# except Exception as e:
#     heading= ''

# print("Page title:", page_title)
# print(heading.text)

# driver.quit()


from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager

# Ensure PhantomJS is installed and the path is correct
driver = webdriver.Chrome("chromedriver.exe")

options = webdriver.ChromeOptions()
# options.add_experimental_option("excludeSwitches", ["enable-logging"])
options.add_argument("--no-sandbox")
options.add_argument("--headless")
options.add_argument("--disable-features=NetworkService")


driver.get(link)
driver.implicitly_wait(15)

page_title = driver.title
try:
    heading = driver.find_element_by_xpath(
        '//*[@id="main-content-video_detail"]/div/div[2]/div/div[1]/div[2]/div[2]/h1'
    )
except NoSuchElementException as e:
    heading = None

print("Page title:", page_title)
if heading is not None:
    print("Heading:", heading.text)
else:
    print("Heading not found.")

driver.quit()
