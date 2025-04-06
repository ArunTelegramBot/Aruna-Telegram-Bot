from telegram import Update
from telegram.ext import CallbackContext
from handlers.payments import payment_info
from handlers.help import help_command
from telegram.ext import Application, CommandHandler, CallbackQueryHandler

async def menu_button_handler(update: Update, context: CallbackContext):
    query = update.callback_query
    await query.answer()

    if query.data == "payment_info":
        await payment_info(update, context)  

    elif query.data == "help_info":
        await help_command(update, context)

menu_button_callback_handler = CallbackQueryHandler(menu_button_handler, pattern="^(payment_info|help_info)$")
