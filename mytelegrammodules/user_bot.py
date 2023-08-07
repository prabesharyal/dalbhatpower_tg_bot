from telethon import TelegramClient
from utils.loader import Loader

# import asyncio
import os 
# import dotenv
# dotenv.load_dotenv()


api_id = int(os.environ.get('TG_APP_API_ID'))
api_hash = os.environ.get('TG_APP_API_HASH')
session = os.environ.get('TG_APP_SHORT_NAME')
chat_id=int(os.environ.get('TG_APP_CHAT_ID'))

class TelethonModuleByME():
    def callback(current, total):
        # print('Uploaded', current, 'out of', total,
        #       'bytes: {:.2%}'.format(current / total))
        print('  {:.2f}/{:.2f} MB ({:.2%}) '.format((current/1000000),(total/1000000),(current/total)),end='',flush=True)
  
        # Function to send video to chat
    async def send_video_to_chat(video_file_path):
        with Loader("Uploading Large Video : ", "Uploaded Sucessfully"):
            async with TelegramClient(session, api_id, api_hash) as client:
                a= await client.send_file(chat_id, video_file_path, supports_streaming=True, progress_callback=TelethonModuleByME.callback)
                return a
    # Function to send audio to chat
    async def send_audio_to_chat(audio_file_path):
        with Loader("Uploading Large Audio : ", "Uploaded Sucessfully"):
            async with TelegramClient(session, api_id, api_hash) as client:
                a= await client.send_file(chat_id, audio_file_path, progress_callback=TelethonModuleByME.callback, supports_streaming=True)
                return a

# async def main():
#     # Call the functions from telegram_utils with await
#     response = await TelethonModuleByME.send_video_to_chat(chat_id,'')
#     print(response)
#     # await send_audio_to_chat(chat_id, audio_file_path)

# # Create an event loop and run the main coroutine
# if __name__ == "__main__":
#     loop = asyncio.get_event_loop()
#     loop.run_until_complete(main())


# response = await TelethonModuleByME.send_video_to_chat(chat_id,'')
