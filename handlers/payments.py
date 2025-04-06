from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import CallbackContext

SUBSCRIPTION_OPTIONS = [
    [InlineKeyboardButton("✅ 1 Week – ₹259", callback_data="sub_1w")],
    [InlineKeyboardButton("✅ 1 Month – ₹369", callback_data="sub_1m")]
]

PAYMENT_METHODS = [
    [InlineKeyboardButton("📸 Pay via QR Code", callback_data="pay_qr")],
    [InlineKeyboardButton("🏦 Pay via UPI ID", callback_data="pay_upi")]
]

async def payment_info(update: Update, context: CallbackContext):
    """Mostra os planos de assinatura disponíveis."""
    query = update.callback_query
    if query:
        await query.answer()

    text = "📜 *Choose your subscription plan:*\n\n"
    text += "✅ 1 Week – ₹259\n✅ 1 Month – ₹369\n\n"
    text += "Please select an option below:"

    await update.effective_message.reply_text(
        text,
        parse_mode="Markdown",
        reply_markup=InlineKeyboardMarkup(SUBSCRIPTION_OPTIONS)
    )

async def handle_payment_selection(update: Update, context: CallbackContext):
    """Mostra os métodos de pagamento depois que o usuário escolhe um plano."""
    query = update.callback_query
    if query:
        await query.answer()

    plan_text = "✅ *Selected Plan:* 1 Week – ₹259" if query.data == "sub_1w" else "✅ *Selected Plan:* 1 Month – ₹369"

    text = f"{plan_text}\n\nChoose your preferred payment method:"

    await update.effective_message.reply_text(
        text,
        parse_mode="Markdown",
        reply_markup=InlineKeyboardMarkup(PAYMENT_METHODS)
    )

async def handle_payment_method(update: Update, context: CallbackContext):
    """Executa a ação do pagamento com base na escolha do usuário."""
    query = update.callback_query
    if query:
        await query.answer()

    if query.data == "pay_qr":
        await update.effective_message.reply_photo(
            photo=open("assets/QR_Code.jpg", "rb"),
            caption="📸 *Scan this QR Code to make the payment.*\n\n"
                    "After payment, send a screenshot for verification.",
            parse_mode="Markdown"
        )
    elif query.data == "pay_upi":
        await update.effective_message.reply_text(
            "🏦 *Manual Payment via UPI*\n\n"
            "Send your payment to the following UPI ID:\n"
            "`fansclub9@axl`\n\n"
            "After payment, send a screenshot for verification.",
            parse_mode="Markdown"
        )
    
    if query.message: 
        try:
            await query.edit_message_text("✅ Payment method selected successfully.")
        except Exception as e:
            print(f"Erro ao editar mensagem: {e}")  
