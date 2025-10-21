from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, CallbackContext
import logging

# Logging setup
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)
logger = logging.getLogger(__name__)

# Your UPI ID
UPI_ID = "BHARATPE09895529437@yesbankltd"

# Subscription buttons
SUBSCRIPTION_OPTIONS = [
    [
        InlineKeyboardButton("✅ 1 Week – ₹199", callback_data="sub_1w"),
        InlineKeyboardButton("✅ 1 Month – ₹299", callback_data="sub_1m")
    ]
]

# Command to show subscription plans
async def payment_info(update: Update, context: CallbackContext):
    query = update.callback_query
    message = update.ef
