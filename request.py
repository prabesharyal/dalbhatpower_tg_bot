# import requests
"""
The `get_page_title` function takes a TikTok video URL as input, follows any redirects, and extracts
the title of the page from the HTML content.

:param url: The `url` parameter is the URL of the TikTok video page from which you want to extract
the title
:return: The function `get_page_title` returns the title of the web page specified by the given URL.
If the URL matches the expected TikTok video pattern and the title tag is found in the HTML content,
the function returns the extracted title as a string. If the URL does not match the expected pattern
or the title tag is not found, the function returns `None`.
"""
# import re


# def get_page_title(url):
#     try:
#         # Initial request to get redirected URL
#         r = requests.head(url, allow_redirects=False)
#         redirected_url = r.headers["Location"]
#         print("Redirected URL:", redirected_url)

#         # Pattern to match TikTok video URL
#         pattern = r"((https)\:\/\/(www\.tiktok\.com)\/@([\w\.]+)\/(video)\/[\d]+)"
#         match = re.search(pattern, redirected_url)

#         if match:
#             # Follow the actual redirection
#             response = requests.get(match.group(0), allow_redirects=True)
#             print(response.text)

#             # Extract title from the HTML content
#             title_start = response.text.find("<title>")
#             title_end = response.text.find("</title>")

#             if title_start != -1 and title_end != -1:
#                 title_start += len("<title>")
#                 title = response.text[title_start:title_end].strip()
#                 return title
#             else:
#                 return None  # No title tag found
#         else:
#             print("URL does not match the expected TikTok pattern.")
#             return None

#     except requests.exceptions.RequestException as e:
#         print(f"Error: {e}")
#         return None


# # Example usage:
# url = "https://vt.tiktok.com/ZSNsaAATp/"
# title = get_page_title(url)
# print("Page Title:", title)


