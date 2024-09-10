import re
import asyncio
import re
from typing import Union, Dict, Tuple, Any
from bs4 import BeautifulSoup
import os
import random
from rich.console import Console
from urllib.parse import urlparse

import mimetypes

import subprocess


def get_website_source(url):
    try:
        # Use the -source option to get raw HTML
        result = subprocess.run(
            ["lynx", "-source", url], capture_output=True, text=True
        )
        result.check_returncode()  # Raise an error if the command failed
        return result.stdout
    except subprocess.CalledProcessError as e:
        print(f"Error running lynx: {e}")
    except FileNotFoundError as e:
        print(f"Lynx executable not found: {e}")
    except OSError as e:
        print(f"OS error: {e}")


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

    data: Dict[str, Any] = {"media": {}}
    base_url = "https://www.picuki.com"
    page = get_website_source(f"{base_url}/media/{media_id}")

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
            list(filter(None, map(lambda x: x.attrs.get("src"), soup.find_all("img"))))
        )

    data["media"].update({"videos": videos_list, "images": images_list})

    if len(data) > 1:
        return data
    return None

async def initiate_ig_picuki(link):
    media_id = url_to_media_ID(link).extract_instagram_media_id()
    if media_id == False:
        return "invalid_url"
    json = await get_media_content(media_id)
    if json == None:
        return "post_not_found"
    return json


class ig_dlp(object):
    """An Instagram Downloader Module You Can't Ignore

    usage:
    ig_dlp(link) : returns bool, caption, filepath_list
    Type = Post-Video, Post-Image, Carousel, Public-Story, None"""

    def __init__(self, link) -> None:
        self.link = link

    async def compareLength(
        self, targetDir: str, currentLength: int
    ) -> Union[str, bool]:
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

    def get_valid_filename(self, url: str) -> Union[None, str]:
        """noway for getting pretty filename, bcs one post have multiple media.
        it's skipped if url doesn't match.

        :param str url: raw content url.
        :return str: _description_
        """
        if basename := re.search(
            r"^https?\:\/\/[^<]+\/q\/(?P<filename>[^\"].*?)\|\|", url
        ):
            basename = list(basename.groupdict().get("filename")[:25])
            random.shuffle(basename)
            return "".join(basename)

        print(f"ValueError: Cannot find spesific name from url: {url}, skipped!")
        return None

    def download_file(self, url, directory=os.path.join(os.getcwd(), "downloads")):
        try:
            # Extract a base filename from the URL
            raw_filename = re.split(r"[\|\+\/]+", urlparse(url).path)[-1]
            base_filename, _ = os.path.splitext(
                raw_filename
            )  # Ignore the extension in URL

            # Ensure the directory exists
            os.makedirs(directory, exist_ok=True)

            # Temporary file path to save the downloaded content
            temp_file_path = os.path.join(directory, base_filename)

            # Use lynx to download the content
            result = subprocess.run(["lynx", "-source", url], capture_output=True)
            result.check_returncode()

            # Save the content to a temporary file
            with open(temp_file_path, "wb") as file:
                file.write(result.stdout)

            # Detect the file type using the `file` command
            mime_type = subprocess.run(
                ["file", "--mime-type", "-b", temp_file_path],
                capture_output=True,
                text=True,
            ).stdout.strip()
            extension = mimetypes.guess_extension(mime_type)

            # If an extension is detected, rename the file with the correct extension
            if extension:
                final_file_path = f"{temp_file_path}{extension}"
                os.rename(temp_file_path, final_file_path)
            else:
                # Default to .bin if unknown
                final_file_path = f"{temp_file_path}.bin"

            return final_file_path

        except subprocess.CalledProcessError as e:
            print(f"Error running command: {e}")
        except FileNotFoundError as e:
            print(f"Executable not found: {e}")
        except OSError as e:
            print(f"OS error: {e}")

    async def here_we_download(self, all_links):
        filepath = []
        for media_link in all_links:
            # file = await self.download_media(media_link)
            file = self.download_file(media_link)
            if os.path.getsize(file) != 0:
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
        trimmed_desc = (
            just_desc[: max_desc_length // 2]
            + "..."
            + just_desc[-max_desc_length // 2 :]
        )

        caption = f"{trimmed_desc} \n\n@dalbhatpowerbot"

        return caption

    async def download(self):
        try:
            console = Console()
            with console.status("[bold green]Getting Link Information") as status:
                mydict = await initiate_ig_picuki(self.link)

            # print(mydict)
            if mydict != "invalid_url" and mydict != "post_not_found":
                videos = [
                    item["url"] for item in mydict["media"]["videos"] if "url" in item
                ]
                photos = mydict["media"]["images"]
                download_list = set(photos)
                download_list = list(download_list.union(set(videos)))
                username = mydict["name"]
                upload_time = mydict["time"]
                just_desc = mydict["caption"]
                if "tags" in mydict:
                    tags = "#" + " #".join(mydict["tags"].split(", "))
                else:
                    tags = "@dalbhatpowerbot"
                CAPTION = self.generate_caption(username, upload_time, just_desc, tags)
                # print(download_list)
                downloaded = []
                if len(download_list) >= 1:
                    with console.status(
                        f"[yellow]Downloading {len(download_list)} Items"
                    ) as status:
                        downloaded += await self.here_we_download(download_list)
                    print(f"Downloaded {len(downloaded)} Items✅")
                else:
                    return False, None, []

                if len(downloaded) < 1:
                    return False, None, []
                return "post", CAPTION, downloaded
            else:
                Console.print(f"[red] API Response: [blue]{mydict} [reset]")
                return False, None, []
        except Exception as e:
            print("ig_dlp main Exception" + str(e))
            return False, None, []

