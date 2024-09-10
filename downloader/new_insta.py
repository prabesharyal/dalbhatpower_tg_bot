import re
import random
import requests
import string
import asyncio
import httpx
import re
from typing import Union, Dict, Tuple, Any
from bs4 import BeautifulSoup
import os
import aiofiles
import random
from aiohttp import ClientSession
from colorama.ansi import Fore as col
from rich.progress import (
    Progress,
    SpinnerColumn,
    BarColumn,
    TextColumn,
    DownloadColumn,
    TransferSpeedColumn,
    TimeRemainingColumn,
)
from rich.console import Console
from rich.progress import Progress
# Initialize rich console
console = Console()


class url_to_media_ID(object):
    def __init__(self, url) -> None:
        self.url = url
        self.insta_regex = (
            r"(https?:\/\/(?:(www|m)\.)?instagram\.com\/(p|reel(s)?)\/([^/?#&\s]+))"
        )

    def base64_to_base10(self, shortcode: str) -> int:
        """
        Convert a base64 encoded string to a base10 integer.

        Args:
        shortcode (str): The base64 encoded string.

        Returns:
        int: The decoded base10 integer.
        """
        base64_chars = (
            "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789-_"
        )
        base10_id = 0

        for char in shortcode:
            base10_id = base10_id * 64 + base64_chars.index(char)

        return base10_id

    def extract_instagram_media_id(self) -> int:
        """
        Extract and convert the Instagram media ID from a given URL.

        Args:
        url (str): The Instagram URL to extract the media ID from.
        pattern (raw) : The pattern of instagram regex

        Returns:
        int: The media ID.
        """

        # Extract only Required URL
        required_url = re.search(self.insta_regex, self.url)
        if required_url:
            required_url = required_url.group(0)
        else:
            return False
        # Extract the shortcode from the URL
        parts = required_url.split("/")
        shortcode = parts[-2] if parts[-1] == "" else parts[-1]

        # Convert the base64 shortcode to base10 media ID
        media_id = self.base64_to_base10(shortcode)

        return media_id


async def get_media_content(media_id: str) -> Union[Dict[str, Any], None]:
    base_url = "https://www.picuki.com"
    headers = {
        "Host": "www.picuki.com",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/114.0",
    }

    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"{base_url}/media/{media_id}", headers=headers, timeout=10
        )

        if response.status_code != 200:
            return None

        data: Dict[str, Any] = {"media": {}}
        page = response.text

        # Using BeautifulSoup if regex fails to find information

        soup = BeautifulSoup(page, "html.parser")

        # Using regex to extract media information
        if media_info := re.search(
            r"(?<=photo-nickname\">).*?\">(?P<name>[^>].*?)(?=</)[\s\S]*?(?<=photo-time\">)(?P<time>[^>].*?)(?=</)[\s\S]*?(?<=photo-description\">)(?P<caption>[\s\S]*?)(?=\s+(<a|</div>))",
            page,
        ):
            media_info = media_info.groupdict()
            if tags := re.findall(
                r"href=\"https?:\/\/(?:www\.)?picuki\.com\/tag\/([^>]*)\"", page
            ):
                media_info.update({"tags": ", ".join(tags)})

            if like := re.search(
                r"(?<=icon-thumbs-up-alt\">)(?P<likes_count>[^\"].*?)(?=\<\/span>)[\s\S]*(?<=commentsCount\">)(?P<comments_count>[^\<].*?)(?=\<\/span>)",
                page,
            ):
                data.update(like.groupdict())
            data.update(media_info)
        else:
            if media_info := soup.find("div", class_="single-profile-info"):
                data.update(
                    dict(
                        zip(
                            (
                                "username",
                                "time",
                                "caption",
                                "like_count",
                                "comments_count",
                            ),
                            (
                                media_info.find(class_=i).text.strip()
                                for i in (
                                    "single-photo-nickname",
                                    "single-photo-time",
                                    "single-photo-description",
                                    "icon-thumbs-up-alt",
                                    "icon-chat",
                                )
                            ),
                        )
                    )
                )

        # Extracting video URLs
        videos_list = []
        if html_video := re.findall(r"(\<video[\s\S]*?\<\/video)", page):
            for vid in html_video:
                if video := re.search(
                    r"(?:\<video[^>]+?poster\=\"(?P<thumbnail>[^<]*?)\"[\s\S]*src\=\"(?P<url>[^<]*?))\"",
                    vid,
                ):
                    videos_list.append(video.groupdict())
        else:
            for vid in soup.find_all("video"):
                video_data = {
                    "thumbnail": vid.attrs.get("poster"),
                    "url": vid.find("source").attrs.get("src"),
                }
                if video_data not in videos_list:
                    videos_list.append(video_data)

        # Extracting image URLs
        images_list = []
        if html_image := re.findall(r"<img[^\"]src\=\"([^<]*?)\"", page):
            images_list.extend(list(filter(None, html_image)))
        else:
            images_list.extend(
                list(
                    filter(
                        None, map(lambda x: x.attrs.get("src"), soup.find_all("img"))
                    )
                )
            )

        data["media"].update({"videos": videos_list, "images": images_list})

        if len(data) > 1:
            return data
        return None


# Example usage
# url = "https://www.instagram.com/reel/C7ndJLFywBS/?igsh=MTRvNHI0ejh6bTRnYg=="
# media_id = url_to_media_ID(url).extract_instagram_media_id()
# print(f"Extracted Media ID: {media_id}")


async def initiate_ig_picuki(link):
    media_id = url_to_media_ID(link).extract_instagram_media_id()
    if media_id == False:
        return 'invalid_url'
    json = await get_media_content(media_id)
    if json == None:
        return 'post_not_found'
    return json

def generate_random_string(length=16):
    # Define the characters to choose from: uppercase, lowercase letters, and digits
    characters = string.ascii_letters + string.digits
    # Generate a random string of the specified length
    random_string = ''.join(random.choice(characters) for _ in range(length))
    return random_string


class ig_dlp(object):
    """An Instagram Downloader Module You Can't Ignore

    usage:
    ig_dlp(link) : returns bool, caption, filepath_list
    Type = Post-Video, Post-Image, Carousel, Public-Story, None"""

    def __init__(self, link) -> None:
        self.link = link

    async def compareLength(self, targetDir: str, currentLength: int) -> Union[str, bool]:
        """compare content length before iterate chunk to check alrdy downloaded or not.
        in general, different file size == different content.

        test with 2k+ of files it fastly: -0.2 sec, and average: -1.5 sec.
        dpend the CPU machine.

        :param str targetDir: dir target to iterate.
        :param int currentLength: current length before downloaded.
        :return bool
        """

        async def compare(file: str) -> Tuple[str, int]:
            return (file, await asyncio.to_thread(os.path.getsize, file))

        recursSize = await asyncio.gather(
            *map(lambda x: compare(f"{targetDir}/{x}"), os.listdir(targetDir))
        )
        for file, size in recursSize:
            if size == currentLength:
                return file
            else:
                continue
        return False

    def download_media(self, link):
        # url = link
        output_dir = os.path.join(os.getcwd(), "downloads")
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        extension = link.split('.')[-1]
        typeof = extension
        filename = generate_random_string()+'.'+extension
        local_filename = os.path.join(output_dir,filename)
        print(local_filename)
        try:
            console.clear()
            console.print(
                f"Downloading {typeof} {filename}...", style="bold blue"
            )
            with requests.get(link, stream=True) as r:
                r.raise_for_status()
                total_size = int(r.headers.get("content-length", 0))
                with open(local_filename, "wb") as f:
                    console.clear()
                    with Progress() as progress:
                        task = progress.add_task(
                            "[cyan]Downloading...", total=total_size
                        )
                        for chunk in r.iter_content(chunk_size=8192):
                            f.write(chunk)
                            progress.update(task, advance=len(chunk))
            console.print(
                f"{typeof} {filename} downloaded successfully.",
                style="bold green",
            )
            return local_filename
        except requests.RequestException as e:
            console.print(f"Download error: {e}", style="bold red")
            return False
    
    async def here_we_download(self, all_links):
        filepath = []
        for media_link in all_links:
            file = self.download_media(media_link)
            if os.path.getsize(file) != False:
                filepath.append(file)
            else:
                os.remove(file)
        return filepath

    def generate_caption(self, username, upload_time, just_desc, tags):
        # Initial caption creation
        caption = f"{username} | {upload_time} \n\n {'✨' if '</div>' in just_desc else just_desc} \n\n {tags}"
        
        # Check if the initial length is within the limit
        if len(caption) <= 1900:
            return caption
        
        # If the caption is too long, start removing unnecessary parts
        # Step 1: Try removing tags
        caption = f"{username} | {upload_time} \n\n {'✨' if '</div>' in just_desc else just_desc}"
        
        # Check if the length is now within the limit
        if len(caption) <= 1900:
            return caption
        
        # Step 2: Try removing username and upload_time
        caption = f"{'✨' if '</div>' in just_desc else just_desc}"
        
        # Check if the length is now within the limit
        if len(caption) <= 1900:
            return caption
        
        # Step 3: Trim the description to fit within the limit, ensuring some context is preserved
        max_desc_length = 1900 - len("... @dalbhatpowerbot")
        trimmed_desc = just_desc[:max_desc_length // 2] + "..." + just_desc[-max_desc_length // 2:]
        
        caption = f"{trimmed_desc} \n\n@dalbhatpowerbot"
        
        return caption
    
    async def download(self):
        try:
            console = Console()
            with console.status("[bold green]Getting Link Information") as status:
                mydict = await initiate_ig_picuki(self.link)
            # with Loader("Requesting API....", "API Response Received✅"):
            #     mydict = initiate_ig_picuki(url)
            # print(mydict)
            if mydict != "invalid_url" and mydict != "post_not_found":
                videos = [item["url"] for item in mydict["media"]["videos"] if "url" in item]
                photos = mydict['media']['images']
                download_list = set(photos)
                download_list = list(download_list.union(set(videos)))
                username = mydict['name']
                upload_time = mydict['time']
                just_desc = mydict['caption']
                if 'tags' in mydict:
                    tags = "#" + " #".join(mydict["tags"].split(", "))
                else:
                    tags = '@dalbhatpowerbot'
                CAPTION = self.generate_caption(username,upload_time,just_desc,tags)
                # print(download_list)
                downloaded = []
                if len(download_list) >= 1:
                    with console.status(f"[yellow]Downloading {len(download_list)} Items") as status:
                        downloaded += await self.here_we_download(download_list)
                    print(f"Downloaded {len(downloaded)} Items✅")
                else:
                    return False, None, []
                # if len(videos) >= 1:
                #     with Loader(
                #         f"Downloading {len(videos)} Videos",
                #         f"Downloaded {len(videos)} Videos ✅",
                #     ):
                #         downloaded += self.here_we_download('video', videos)
                # if len(photos)>=1:
                #     with Loader(
                #         f"Downloading {len(photos)} Images",
                #         f"Downloaded {len(photos)} Images ✅",
                #     ):
                #         downloaded += self.here_we_download("image", photos)
                if len(downloaded)<1:
                    return False, None, []
                return 'post', CAPTION, downloaded
            else: 
                Console.print(f"[red] API Response: [blue]{mydict} [reset]")
                return False, None, []
        except Exception as e:
            print('ig_dlp main Exception'+ str(e))
            return False, None, []


# url = "https://www.instagram.com/p/C7rosDCSrkn/?utm_source=ig_web_copy_link" #pass mixed
# url = "https://www.instagram.com/reel/C7R2JRBg-C3/?utm_source=ig_web_copy_link"  # Solved: 403 Client Error: Forbidden for url: https://cdn1.picuki.com/hosted-by-instagram/q/0exhNuNYnj
# url = "https://www.instagram.com/reel/C6arhdPKTqw/?utm_source=ig_web_copy_link"  # SOlved Error: 403 Client Error: Forbidden for url: https://cdn1.picuki.com/hosted-by-instagram/q/0exhNuNYnjBGZDHIdN5WmL9I2Pk2GAlRNucaS7j0nyZiNxIsbHWB58ltwdKg%7C%7CDlyIg1gASuSYzxj4IgiWVpZDj1zOEffQb2MRTtX76yaVufN0jZh8pVhkLgzLXQdZnOp98AlUwmYdS8ISqYvAajK9q8aoaWtKGdS5GLPKuIe3zkG%7C%7CJHqXqx0hJci4aaJzkXg%7C%7C8IOKj518Wo1eRh48pvlpDk1U%7C%7Czzb5dSppZ7UIIC05Qk2rjltTO%7C%7CNmgNL0pQUTWbt9bgr9E11HPNVhQZ2kDhRKo5chtT1BO0v0th4rMPsaSoAZogitk%7C%7C6Yn5bn9eUzhYsSFCorKts3SZZmSRxVRGzzbV1qW6V9os9MTBY%7C%7CyYCI2%7C%7CmQSRS5f4UoRCXkUcCfiLAQaFeffu.mp4
# url = "https://www.instagram.com/p/C7j371uoUzg/?utm_source=ig_web_copy_link" #- passes post carousel only vids
# url = "https://www.instagram.com/p/C7lp4YByAq-/?utm_source=ig_web_copy_link" # "passes mixed carousel"
# url = "https://www.instagram.com/p/C7rz-CLy0nU/?utm_source=ig_web_copy_link" #only imgs passed

# url = "https://www.instagram.com/reel/C6G1fHBRJaR/?utm_source=ig_web_copy_link"  # Forbidden for url:  reel

# url = "https://www.instagram.com/p/asasda/?utm_source=ig_web_copy_link" #fake

# instance = ig_dlp(url)
# check, caption, filelist = instance.download()
# print(check)
# print(caption)
# print(filelist)
