"""
Blancos Uz — Birinchi Komment Boti (Tugmalar bilan)
Railway.app uchun tayyor versiya
"""

import os
import logging
from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import Application, MessageHandler, filters, ContextTypes

# ─── SOZLAMALAR ───
BOT_TOKEN  = os.environ.get("BOT_TOKEN", "")
CHANNEL_ID = os.environ.get("CHANNEL_ID", "")

# ─── XABAR MATNI ───
XABAR_MATNI = "🤍 Blancos Uz — Bizni kuzatib boring!"

# ─── TUGMALAR (inline keyboard) ───
TUGMALAR = InlineKeyboardMarkup([
    [
        InlineKeyboardButton("📢 Telegram",    url="https://t.me/blancosuzdirect"),
        InlineKeyboardButton("🎬 Media",       url="https://t.me/blancosuztv"),
    ],
    [
        InlineKeyboardButton("😎 Emoji packs", url="https://t.me/c/2362531843/24834"),
        InlineKeyboardButton("🚀 Boost",       url="https://t.me/boost?c=2362531843"),
    ],
    [
        InlineKeyboardButton("📣 Reklama uchun joy", url="https://t.me/Manager_ABUCHANNELS"),
    ],
])

# ─── LOGGING ───
logging.basicConfig(
    format="%(asctime)s | %(levelname)s | %(message)s",
    level=logging.INFO
)
log = logging.getLogger(__name__)


async def yangi_post(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Kanalga yangi post kelganda tugmali xabar yuboradi."""
    msg = update.channel_post
    if msg is None:
        return

    chat_username = f"@{msg.chat.username}" if msg.chat.username else str(msg.chat.id)
    if chat_username != CHANNEL_ID and str(msg.chat.id) != str(CHANNEL_ID):
        return

    log.info(f"📢 Yangi post: #{msg.message_id}")

    try:
        await context.bot.send_message(
            chat_id=msg.chat.id,
            text=XABAR_MATNI,
            reply_to_message_id=msg.message_id,
            reply_markup=TUGMALAR
        )
        log.info("✅ Tugmali xabar yuborildi!")
    except Exception as e:
        log.error(f"❌ Xato: {e}")


def main():
    if not BOT_TOKEN:
        raise ValueError("❌ BOT_TOKEN o'rnatilmagan!")
    if not CHANNEL_ID:
        raise ValueError("❌ CHANNEL_ID o'rnatilmagan!")

    log.info("🤖 Bot ishga tushmoqda...")
    log.info(f"📡 Kanal: {CHANNEL_ID}")

    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(MessageHandler(filters.ChatType.CHANNEL, yangi_post))
    app.run_polling(drop_pending_updates=True)


if __name__ == "__main__":
    main()
