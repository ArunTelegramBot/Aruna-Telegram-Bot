from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CallbackContext, MessageHandler, CallbackQueryHandler, filters
from .payments import pending_transactions

ADMIN_GROUP_ID = -1002594045216
GROUP_LINK = "https://t.me/+kbMWRA7RG0FiZTM1"

async def verify_payment(update: Update, context: CallbackContext):
    user = update.message.from_user
    user_id = user.id
    username = user.username if user.username else "No Username"

    if user_id not in pending_transactions:
        await update.message.reply_text("❌ No pending payment.")
        return

    plan_info = pending_transactions[user_id]

    keyboard = [
        [InlineKeyboardButton("✅ Approve", callback_data=f"approve_{user_id}"),
         InlineKeyboardButton("❌ Reject", callback_data=f"reject_{user_id}")]
    ]

    if update.message.photo:
        photo = update.message.photo[-1]
        file = await photo.get_file()

        await context.bot.send_photo(
            chat_id=ADMIN_GROUP_ID,
            photo=file.file_id,
            caption=f"👤 @{username}\n💰 {plan_info['plan']} – ₹{plan_info['amount']}",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )

async def handle_approval(update: Update, context: CallbackContext):
    query = update.callback_query
    action, user_id = query.data.split("_")
    user_id = int(user_id)

    if action == "approve":
        await context.bot.send_message(user_id, f"✅ Approved!\n{GROUP_LINK}")
    else:
        await context.bot.send_message(user_id, "❌ Rejected.")

    pending_transactions.pop(user_id, None)
    await query.answer()

verification_handler = MessageHandler(filters.PHOTO, verify_payment)
approval_handler = CallbackQueryHandler(handle_approval, pattern="^(approve|reject)_")

def get_callback_handlers():
    return [verification_handler, approval_handler]
