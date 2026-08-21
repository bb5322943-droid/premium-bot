# -*- coding: utf-8 -*-
from telegram import Update, LabeledPrice, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, PreCheckoutQueryHandler, CallbackQueryHandler, ContextTypes, filters

BOT_TOKEN = "8991050114:AAEsfYudMCJTFrpKzpZV3Dxko_9pBxowVBM"
ADMIN_ID = 8702674939

async def start(update, context):
    await update.message.reply_text("Assalomu alaykum!\n\nPremium Gift Bot ga xush kelibsiz!\n\nPremium olish uchun /premium buyrug'ini bosing.")

async def premium(update, context):
    keyboard = [
        [InlineKeyboardButton("1 kun - 100 Stars", callback_data="p1")],
        [InlineKeyboardButton("1 hafta - 300 Stars", callback_data="p2")],
        [InlineKeyboardButton("1 oy - 500 Stars", callback_data="p6")],
        [InlineKeyboardButton("3 oy - 1000 Stars", callback_data="p3")],
        [InlineKeyboardButton("6 oy - 1500 Stars", callback_data="p4")],
        [InlineKeyboardButton("12 oy - 2500 Stars", callback_data="p5")],
    ]
    await update.message.reply_text("Tarifni tanlang:", reply_markup=InlineKeyboardMarkup(keyboard))

async def button(update, context):
    q = update.callback_query
    await q.answer()
    t = {"p1":("1 kun",100),"p2":("1 hafta",300),"p6":("1 oy",500),"p3":("3 oy",1000),"p4":("6 oy",1500),"p5":("12 oy",2500)}
    if q.data in t:
        context.user_data["tarif"] = q.data
        await q.message.reply_text("Kimga gift qilmoqchisiz?\n\nUsername yozing. Masalan: @sardor")

async def username(update, context):
    if "tarif" not in context.user_data:
        return
    u = update.message.text
    td = context.user_data.pop("tarif")
    t = {"p1":("1 kun",100),"p2":("1 hafta",300),"p6":("1 oy",500),"p3":("3 oy",1000),"p4":("6 oy",1500),"p5":("12 oy",2500)}
    n, s = t[td]
    context.user_data["username"] = u
    await context.bot.send_invoice(chat_id=update.message.chat_id, title="Premium "+n, description=u+" ga "+n+" Premium", payload=td+"|"+u, currency="XTR", prices=[LabeledPrice(n, s)])

async def precheckout(update, context):
    await update.pre_checkout_query.answer(ok=True)

async def payment(update, context):
    p = update.message.successful_payment.invoice_payload.split("|")
    u = update.message.from_user
    await update.message.reply_text("Tolov qabul qilindi! Premium tez orada yuboriladi. Rahmat "+u.first_name+"!")
    await context.bot.send_message(chat_id=8702674939, text="YANGI TOLOV!\nKimdan: "+str(u.full_name)+"\nKimga: "+(p[1] if len(p)>1 else "?"))

def main():
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("premium", premium))
    app.add_handler(CallbackQueryHandler(button))
    app.add_handler(PreCheckoutQueryHandler(precheckout))
    app.add_handler(MessageHandler(filters.SUCCESSFUL_PAYMENT, payment))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, username))
    print("Bot ishga tushdi...")
    app.run_polling()

if __name__ == "__main__":
    main()