"""/rasifal — Nepali horoscope handler."""
from telegram import Update, ReplyKeyboardRemove
from telegram.ext import ContextTypes

from bot.services import rasifal_service as r

# Hardcoded zodiac sticker IDs (one per rashi index, 0-11).
STICKERS = [
    "CAACAgUAAxkBAAJ74WXWKWOVywjGrjc9iz7YUIxnGNh0AAKeDwACtWuxVssBRvxLCox_NAQ",
    "CAACAgUAAxkBAAJ742XWKWhOlMB8m-OTkXR5OP-v6m95AALtEAACE46xVuvFXw7YBgYJNAQ",
    "CAACAgUAAxkBAAJ75WXWKWxMQeaIDwsW2YJi8Vj2UP8bAAKaDQAC2NmxVlj2VYEDp4W0NAQ",
    "CAACAgUAAxkBAAJ752XWKXCE083Zn3Kt9wu9iK8RWRi2AAKrDQACM4C4Vk290tsPyqcdNAQ",
    "CAACAgUAAxkBAAJ76WXWKXWs4YPL_euiyfdLb-7yfTkfAAKuDQACPXmxVidbu3IWF3MGNAQ",
    "CAACAgUAAxkBAAJ762XWKXlmI5DuiZdUozNcoG_UrVQSAAIKDQAC68OxVhPxyJHgufnzNAQ",
    "CAACAgUAAxkBAAJ77WXWKX2st3eXnLWdbaPsu6dcNL7nAAL3DgACqUm5VoxgyitRWEJrNAQ",
    "CAACAgUAAxkBAAJ772XWKYAxGexGUmiD6cnR0SA5P4H6AAI5DwACjJuwVnNLLoVNlbLdNAQ",
    "CAACAgUAAxkBAAJ78WXWKYXaegfmbdQooLicbtH9T8qrAAJKDgACxCmxVo2-1j7flB7lNAQ",
    "CAACAgUAAxkBAAJ782XWKYnotppVQgKggw2os5fSjb-BAALDDwACpBKwVnDN-DU80cD2NAQ",
    "CAACAgUAAxkBAAJ79WXWKZKdc8v_0MZBlG3EqBroZ2_YAAK_DgACBdGwViMLCU3hJk8tNAQ",
    "CAACAgUAAxkBAAJ792XWKZYQx8id9r8nagnYNWQ_o6S4AAInDgACPtixVl5KXpz40gyJNAQ",
]


async def rasifal(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    parts = update.message.text.split()
    if len(parts) == 1:
        text = r.all_horoscopes()
        await update.message.reply_markdown(text, reply_markup=ReplyKeyboardRemove(selective=True))
        return
    text, idx = r.horoscope(" ".join(parts[1:]))
    if 0 <= idx <= 11:
        try:
            await update.message.reply_sticker(sticker=STICKERS[idx])
        except Exception:
            pass
    await update.message.reply_markdown(text, reply_markup=ReplyKeyboardRemove(selective=True))
