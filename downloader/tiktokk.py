import requests, re, json, os
from utils.loader import Loader


class tt_dlp(object):
    """An Tiktok Downloader Module You Can't Ignore

    usage:
    tt_dlp(link) : returns bool, caption, filepath_list
    Type = Post-Video, Post-Image, Carousel, Public-Story, None"""

    def __init__(self, link) -> None:
        # self.link = link
        self.method = "cobalt"
        self.link = link
        if self.method == "cobalt":
            self.headers = {
                "content-type": "application/json",
                "accept": "application/json",
            }
            self.body = {
                "url": link,
                "vCodec": "h264",
                "vQuality": "max",
                "isNoTTWatermark": True,
            }
            self.api = "https://co.wuk.sh/api/json"

    def get_page_title(self, url):
        title = Tiktok_Title_Extractor.title_extractor(url)
        return title

    def download_media(self, url):
        try:
            response = requests.get(url)
            response.raise_for_status()

            filename = url.split("/")[-1].split("?")[0]
            download_path = os.path.join("downloads", filename)

            # Create the 'downloads' directory if it doesn't exist
            os.makedirs("downloads", exist_ok=True)

            with open(download_path, "wb") as file:
                file.write(response.content)
            return os.path.join(os.getcwd(), download_path)

        except requests.exceptions.RequestException as e:
            print("Error:", e)
            raise FileNotFoundError

    def here_we_download(self, all_links):
        filepath = []
        for media_link in all_links:
            file = self.download_media(media_link)
            filepath.append(file)
        return filepath

    def download(self):
        try:
            with Loader("Requesting API....", "API Response Received✅"):
                response = requests.post(
                    self.api, headers=self.headers, data=json.dumps(self.body)
                )
                mydict = response.json()
                # print(mydict)
            if response.status_code == 200:
                if mydict["status"] == "redirect" or "stream":
                    download_list = [mydict["url"]]
                    # print(download_list)
                    downloadType = mydict["status"]
                elif mydict["status"] == "picker":
                    download_list = [obj["url"] for obj in mydict["picker"]]
                    downloadType = mydict["status"]
                    # print(download_list)

                with Loader("Getting Caption", "Caption Extracted ✅"):
                    CAPTION = self.get_page_title(self.link)

                with Loader(
                    f"Downloading {len(download_list)} Files",
                    f"Downloaded {len(download_list)} Files ✅",
                ):
                    files = self.here_we_download(download_list)
                return downloadType, CAPTION, files
            else:
                print("\nAPI responded failure: " + str(response.status_code))
                return False, None, []
        except Exception as e:
            print(e)
            print("main exception occurred")
            return False, None, []


class Tiktok_Title_Extractor:
    """A Tiktok Title extraction Module"""

    def title_extractor(url):
        full_link = url
        if full_link != 0:
            from selenium import webdriver
            from selenium.common.exceptions import NoSuchElementException
            from selenium.webdriver.chrome.service import Service as ChromeService
            from webdriver_manager.chrome import ChromeDriverManager

            options = webdriver.ChromeOptions()
            options.add_experimental_option("excludeSwitches", ["enable-logging"])
            # options.add_argument("--no-sandbox")
            options.add_argument("--disable-gpu")
            options.add_argument("window-size=1920x1080")  # Adjust the size as needed
            options.add_argument(
                "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
            )

            options.add_argument("--headless")
            options.add_argument("--disable-features=NetworkService")
            options.add_argument(
                "--disable-web-security"
            )  # Disable web security to prevent redirects
            options.add_argument("--disable-javascript")  # Disable JavaScript execution

            driver = webdriver.Chrome("chromedriver.exe")
            # # driver = webdriver.Chrome(
            # #     service=ChromeService(ChromeDriverManager().install()), options=options
            # # )

            driver.get(full_link)
            webpage_title = driver.title
            driver.implicitly_wait(5)
            desc = driver.find_element_by_xpath(
                '//*[@id="main-content-video_detail"]/div/div[2]/div[1]/div[1]/div[2]/div[2]/div[1]/div/h1'
            )
            page_title = desc.text
            # driver.implicitly_wait(5)
            try:
                heading = driver.find_element_by_xpath(
                    '//*[@id="main-content-video_detail"]/div/div[2]/div/div[1]/div[2]/div[2]/h1'
                )
            except NoSuchElementException as e:
                heading = None

            # print("Page title:", page_title)
            video_title = (
                heading.text + "\n" + page_title if heading is not None else page_title
            )
            driver.quit()
            return video_title if video_title else webpage_title
        else:
            print("Link is not working!")
            return 0, 0


## Test Links
# link = "https://www.tiktok.com/@ruang.rakyat/video/7311900622423362848?is_from_webapp=1&sender_device=pc"  #
# link = "https://vt.tiktok.com/ZSNs3eATL/"  # story
# link = "https://vt.tiktok.com/ZSasdsadNs3eGAp/"  # - pictures
# link = "https://www.tiktok.com/@cinnamon_girlll0/video/7305513849812208898"
# link = "https://www.tiktok.com/@comal_bissta/video/73019192323483034127623"


# Working Links
# link = "https://vt.tiktok.com/ZSNGNPF8s/"
# link = "https://vt.tiktok.com/ZSNGN8hvB/"
# link = "https://vt.tiktok.com/ZSNGNyJqr/"
# link = "https://vt.tiktok.com/ZSNGNBaCu/"
# # link = "https://vt.tiktok.com/ZSNGNLKAB/"
# # test = Tiktok_Title_Extractor(link)
# # testreturn = test.title_extractor()
# # print(testreturn)
# # link = "https://www.tiktok.com/@_sicparvismagna_/video/7315130414534888736"
# insatnces = tt_dlp(link)
# check, caption, filelist = insatnces.download()
# print(check)
# print(caption)
# print(filelist)
