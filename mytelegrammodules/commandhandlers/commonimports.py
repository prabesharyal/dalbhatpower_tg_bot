
# ---------------------------------------------------------------- #
#                    Import System modules
# ---------------------------------------------------------------- #

import os, re, sys,json,ast
import requests
import time, datetime,nepali_datetime

# ---------------------------------------------------------------- #
# **************************************************************** #
# ---------------------------------------------------------------- #


# ---------------------------------------------------------------- #
#                   Import official packages
# ---------------------------------------------------------------- #

#Import Telegram Features
from telegram import InputMediaAudio, InputMediaVideo, Update, ReplyKeyboardRemove,InlineQueryResultArticle, InputTextMessageContent
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters, Updater, InlineQueryHandler


# import loader
import contextlib
from utils.loader import Loader

# Multiprocess
# ---------------------------------------------------------------- #
# **************************************************************** #
# ---------------------------------------------------------------- #




# ---------------------------------------------------------------- #
#                    Import self made modules
# ---------------------------------------------------------------- #

from NEPAL.dict.nepali_dict import NepaliDictionary
from NEPAL.calendar.rasifal import NepaliRashiFal
from NEPAL.calendar.nepali_calendar import nepalSpecialTimes
from mytelegrammodules.database.databasemanager import DBMSSimple
from NEPAL.NEPSE.nepse import NepalStock

from downloader.audio_video_downloader import theOPDownloader



# ---------------------------------------------------------------- #
# **************************************************************** #
# ---------------------------------------------------------------- #


# ---------------------------------------------------------------- #
#                    Import Telegarm Command Functions
# ---------------------------------------------------------------- #
# Defined in Bot.py

# ---------------------------------------------------------------- #
# **************************************************************** #
# ---------------------------------------------------------------- #