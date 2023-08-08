# Import the instaloader module
import instaloader
import os

def convert_html(string):
    string= string.replace('&', '&amp')
    string= string.replace('"', '&quot')
    string= string.replace("'", "&#039")
    string= string.replace('<', '&lt')
    string= string.replace('>', '&gt')
    return string


    
    
def download_from_shortcode(shortcode):
    # Create an instance of instaloader with only_download option
    loader = instaloader.Instaloader(download_video_thumbnails=False, save_metadata=False, post_metadata_txt_pattern='',sanitize_paths=True)
    # try:
    #     loader.load_session_from_file(username = os.getenv('ig_session_USER'),filename = os.getenv('ig_session_USER_file'))
    #     print("Insta Login Success")
    # except Exception as e:
    #     print("Instagarm Login Failed")   
    # Check if the link is valid
    try:
        post = instaloader.Post.from_shortcode(loader.context, shortcode)
        CAPTION = post.caption
        CAPTION= "✨" if CAPTION=='' else CAPTION   
        CAPTION = convert_html(CAPTION)
        # Download the post or reel
        loader.download_post(post, target='downloads')
        filenames = [os.path.join(os.getcwd(),'downloads',post) for post in os.listdir('downloads')]
        return CAPTION, filenames, True
    except Exception as e:
        print(e)
        return None, None, False
    
# print(download_from_link('https://www.instagram.com/p/CvpnA3Et9Nt/?utm_source=ig_web_copy_link&igshid=MzRlODBiNWFlZA=='))
# print(download_from_link('https://www.instagram.com/reel/CubZ5FMIwTh/?utm_source=ig_web_copy_link'))
# print(download_from_link('https://www.instagram.com/reel/CubZ5FMIwTh/?utm_source=ig_web_copy_link'))