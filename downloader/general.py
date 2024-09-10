import os
from downloader_cli.download import Download

class FileDownloader:
    def __init__(self, download_path= os.path.join(os.getcwd(), 'downloads','general')):
        self.download_path = download_path
        os.makedirs(self.download_path, exist_ok=True)

    def download_file(self, link):
        try:
            # Download the file to the specified path
            start = Download(URL=link, des=self.download_path, continue_download=True, overwrite=True)
            start.download()

            # Get the list of downloaded files
            file_list = [os.path.join(self.download_path,f) for f in os.listdir(self.download_path) if os.path.isfile(os.path.join(self.download_path, f))]


            # Check if download is successful
            download_successful = True

            # Prepare the file metadata information
            file_metadata = ""
            if len(file_list) == 1 :
                file_name = file_list[0]
                file_path = os.path.join(self.download_path, file_name)
                file_size = os.path.getsize(file_path) / (1024 * 1024)  # Convert to MB
                file_extension = os.path.splitext(file_name)[1]

                # Append metadata information in Markdown format
                file_metadata += f"***File Name:*** `{os.path.basename(file_name)}`\n" \
                                 f"***Size:*** {file_size:.2f} MB\n" \
                                 f"***File Type:*** {file_extension}\n\n"
            else:
                return False, None, []

            # Return a summary including check (download_successful), caption, and file metadata
            return download_successful, file_metadata, file_list[0]

        except Exception as e:
            # Handle any exceptions that may occur during download
            print(f"Failed to download {link}: {str(e)}")
            return False, None, []


