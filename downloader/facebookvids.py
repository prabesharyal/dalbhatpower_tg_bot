import re, requests, os
from utils.loader import Loader
from bs4 import BeautifulSoup




def fb_to_cdn(link):
    url = 'http://164.92.77.99:5000'
    params = {'url': link}
    response = requests.get(url, params=params)
    return response.json()

def get_caption(url):
    response = requests.get(url)

    # Check if the request was successful
    if response.status_code == 200:
        # Parse the HTML content of the page
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Find the meta description tag
        meta_description_tag = soup.find('meta', attrs={'name': 'description'})
        
        # Extract the content attribute of the meta description tag
        meta_description = meta_description_tag['content'] if meta_description_tag else None

        # Print the meta description
        return meta_description
    else:
        return None


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
        return False


def main_fb_dl(url):
    try:
        with Loader("Running : ", "Done !"):
            print(" Getting Caption ", end='', flush=True)
            CAPTION = "✨" if get_caption(url)==None else get_caption(url)
            print(" Getting Video Link ", end='', flush=True)
            dict_resp = fb_to_cdn(url)
            if dict_resp['success']==True:
                file=download_video(dict_resp['result'])
                if file != False:
                    return True, CAPTION, [file]
                else:
                    return False, None, []
            else:
                return False, None, []
    except BaseException as e:
        print(e)
        return False, None, []
    