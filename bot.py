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
from handlers.payments import payment_info, handle_payment_selection, handle_payment_method

logging.basicConfig(level=logging.INFO)

app = Quart(__name__)

TOKEN = os.getenv("BOT_TOKEN")
WEBHOOK_URL = os.getenv("WEBHOOK_URL")
PORT = int(os.getenv("PORT", 5000))

if not TOKEN or not WEBHOOK_URL:
    logging.error("❌ BOT_TOKEN or WEBHOOK_URL not defined."
