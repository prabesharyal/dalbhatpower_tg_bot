import os, requests, json
from utils.loader import Loader


class tt_dlp(object):
    """An Instagram Downloader Module You Can't Ignore

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
        try:
            response = requests.get(url)
            response.raise_for_status()  # Raise an exception for bad status codes (4xx and 5xx)

            # Find the position of the opening and closing <title> tags
            start_index = response.text.find("<title>")
            end_index = response.text.find("</title>")

            if start_index != -1 and end_index != -1:
                start_index += len("<title>")
                return response.text[start_index:end_index]
            else:
                return None  # No title tag found

        except requests.exceptions.RequestException as e:
            print("Couldn't Get Caption so replacing with ✨")
            return "✨"

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
            if response.status_code == 200:
                if mydict["status"] == "redirect":
                    download_list = [mydict["url"]]
                    print(download_list)
                    downloadType = mydict["status"]
                elif mydict["status"] == "picker":
                    download_list = [obj["url"] for obj in mydict["picker"]]
                    downloadType = mydict["status"]
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
            return False, None, []


# url = "https://www.instagram.com/reels/CufCAL1p7Ub/"  # reels
# url = "https://www.instagram.com/reel/Cs1afZSr_Ci/?utm_source=ig_web_copy_link&igshid=MzRlODBiNWFlZA=="  # reel
# url = "https://www.instagram.com/p/CwRX29MI0Hq/?utm_source=ig_web_copy_link&igshid=MzRlODBiNWFlZA=="  # post, sigle
# url = "https://www.instagram.com/p/CrveD1XPau5/?utm_source=ig_web_copy_link&igshid=MzRlODBiNWFlZA=="  # carousel
# url = "https://www.instagram.com/p/Cg9BeutMPm3URpBNFVyH1c_et4C3Mm_IDXv1V40/?img_index=1"
# url = 'https://www.instagram.com/stories/evaaa.g__/3174965177308244912/'

url = "https://vt.tiktok.com/ZSNsaAATp/"  # tiktok carousel
# url = "https://www.tiktok.com/@jacobppt/video/7282391678760111366?is_from_webapp=1&sender_device=pc"
# url = "https://vt.tiktok.com/ZSNsauubR/"
instance = tt_dlp(url)
check, caption, filelist = instance.download()
print(check)
print(caption)
print(filelist)
