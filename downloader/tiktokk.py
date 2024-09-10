import requests, json, os
from utils.loader import Loader
import yt_dlp

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

    def download_media(self, url, typeofcontent):
        try:
            response = requests.get(url, allow_redirects=True)
            response.raise_for_status()
            # print(response)

            # filename = url.split("/")[-1].split("?")[0]
            filename = filename = url.split("/")[-1].split("?")[0].split("~")[0] if typeofcontent == "picker" else url.split("/")[-1].split("?")[1].split("=")[2][:-2]
            extension = ".mp4" if typeofcontent != "picker" else '.jpg'
            download_path = os.path.join("downloads", filename + extension)

            # Create the 'downloads' directory if it doesn't exist
            os.makedirs("downloads", exist_ok=True)

            with open(download_path, "wb") as file:
                file.write(response.content)
            return os.path.join(os.getcwd(), download_path)

        except requests.exceptions.RequestException as e:
            print("Error:", e)
            raise FileNotFoundError

    def here_we_download(self, all_links, typeofcontent):
        filepath = []
        for media_link in all_links:
            file = self.download_media(media_link, typeofcontent)
            filepath.append(file)
        return filepath

    def download(self):
        try:
            with Loader("Requesting API....", "API Response Received✅"):
                response = requests.post(
                    self.api, headers=self.headers, data=json.dumps(self.body)
                )
                mydict = response.json()
                typeofcontent = mydict["status"]
                # print(mydict)
            if response.status_code == 200:
                if typeofcontent == "redirect" or typeofcontent == "stream":
                    download_list = [mydict["url"]]
                elif typeofcontent == "picker":
                    download_list = [obj["url"] for obj in mydict["picker"]]
                with Loader("Getting Caption", "Caption Extracted ✅"):
                    CAPTION = self.get_page_title(self.link)

                with Loader(
                    f"Downloading {len(download_list)} Files",
                    f"Downloaded {len(download_list)} Files ✅",
                ):
                    files = self.here_we_download(download_list, typeofcontent)
                return typeofcontent, CAPTION, files
            else:
                print("\nAPI responded failure: " + str(response.status_code))
                return False, None, []
        except Exception as e:
            print(e)
            print("main exception occurred")
            return False, None, []


class Tiktok_Title_Extractor:
    """A Tiktok Title extraction Module"""

    def title_extractor(link):
        ydl_opts = {
            "ignoreerrors": True,
            "no_playlist": True,
            "no_warnings": True,
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(link, download=False)
            video_title = info["title"]
            return video_title




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
