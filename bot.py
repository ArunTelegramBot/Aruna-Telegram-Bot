import os
import logging
import uvicorn
from quart import Quart, request
from telegram import Update
from telegram.ext import Application, CommandHandler, CallbackQueryHandler

from handlers.verification import get_callback_handlers
from handlers.start import start_command
from handlers.menu import menu_button_handler
from handlers.help import help_command
from handlers.payments import payment_info, handle_payment_selection, handle_payment_method, handle_upload_screenshot

logging.basicConfig(level=logging.INFO)

app = Quart(__name__)

TOKEN = os.getenv("BOT_TOKEN")
WEBHOOK_URL = os.getenv("WEBHOOK_URL")
PORT = int(os.getenv("PORT", 5000))

if not TOKEN or not WEBHOOK_URL:
    logging.error("❌ BOT_TOKEN or WEBHOOK_URL not defined.")
    exit(1)

# --- Initialize Bot Application ---
bot_app = Application.builder().token(TOKEN).build()

# --- Command Handlers ---
bot_app.add_handler(CommandHandler("start", start_command))
bot_app.add_handler(CommandHandler("payment", payment_info))
bot_app.add_handler(CommandHandler("help", help_command))

# --- CallbackQuery Handlers ---
bot_app.add_handler(
    CallbackQueryHandler(menu_button_handler, pattern="^(payment_info|help_info)$")
)
bot_app.add_handler(
    CallbackQueryHandler(handle_payment_selection, pattern="^(sub_1w|sub_1m)$")
)
bot_app.add_handler(
    CallbackQueryHandler(handle_payment_method, pattern="^(pay_qr_|pay_upi_).*")  # FIXED
)
bot_app.add_handler(
    CallbackQueryHandler(handle_upload_screenshot, pattern="^upload_screenshot$")
)

# --- Verification Handlers ---
for handler in get_callback_handlers():
    bot_app.add_handler(handler)

# --- Webhook Routes ---
@app.route("/", methods=["GET"])
async def home():
    return "Bot is running!", 200

@app.route("/webhook", methods=["POST"])
async def webhook():
    update_json = await request.get_json()
    logging.info(f"📩 Received update: {update_json}")
    if update_json:
        update_obj = Update.de_json(update_json, bot_app.bot)
        await bot_app.process_update(update_obj)
    return "OK", 200

# --- Initialize Bot & Set Webhook ---
@app.before_serving
async def startup():
    logging.info("🚀 Initializing bot...")
    await bot_app.initialize()  # Initialize bot
    await bot_app.bot.set_webhook(url=f"{WEBHOOK_URL}/webhook")
    logging.info("✅ Webhook set and bot initialized successfully")

@app.after_serving
async def shutdown():
    logging.info("🛑 Closing bot...")
    await bot_app.shutdown()
    logging.info("✅ Bot shut down cleanly")

# --- Start Quart Server ---
if __name__ == "__main__":
    logging.info("🚀 Starting Quart server...")
    uvicorn.run(app, host="0.0.0.0", port=PORT)
