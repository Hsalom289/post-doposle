import os
from telegram import Update, InputMediaPhoto
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, CallbackContext
from io import BytesIO

# BOT TOKENINGIZNI BU YERGA YOZING
TOKEN = "5233146018:AAHaX8HrPm0-Pxmhti-OoewN26ZfvlVoZpo"

# Yangi matn (siz ko'rsatgan matn)
CAPTION_TEXT = """
✨ Buyurtmalar qabul qilinmoqda! ✨ ✅✅

📩 Lich : https://t.me/doniyor_rakhimovv

📞 Aloqa uchun: +998507710826 ☎️

🌍 O‘zingiz xohlagan viloyat va kerakli auditoriyani tanlab, guruhingizga faqat maqsadli odamlarni qo‘shib beramiz!😊
"""

# Rasmlarni saqlash uchun vaqtinchalik papka
TEMP_FOLDER = "temp_images"
os.makedirs(TEMP_FOLDER, exist_ok=True)

async def start(update: Update, context: CallbackContext):
    """ /start buyrug‘ini bajarganda ishlaydi """
    await update.message.reply_text("Botga rasmlar yuboring, ularni 2 ta qilib post qiladi!")

async def handle_post(update: Update, context: CallbackContext):
    """ Rasm qabul qilib, har 2 ta bo‘lganda post qiladi """
    # Rasmni yuklab olish
    photo_file = await update.message.photo[-1].get_file()
    file_path = os.path.join(TEMP_FOLDER, f"{update.message.message_id}.jpg")
    await photo_file.download_to_drive(file_path)

    # Rasmlar ro‘yxatini saqlash
    if "photos" not in context.user_data:
        context.user_data["photos"] = []
    context.user_data["photos"].append(file_path)

    # Har 2 ta rasm yig‘ilganda post qilish
    while len(context.user_data["photos"]) >= 2:
        photos_to_send = context.user_data["photos"][:2]  # 2 ta rasm olish
        context.user_data["photos"] = context.user_data["photos"][2:]  # Qolganlarini saqlash

        # Media guruhini yaratish
        media_group = [
            InputMediaPhoto(open(photos_to_send[0], 'rb')),
            InputMediaPhoto(open(photos_to_send[1], 'rb'), caption=CAPTION_TEXT)
        ]

        # Media guruhini yuborish
        await update.message.reply_media_group(media=media_group)

        # Fayllarni tozalash
        for file_path in photos_to_send:
            os.remove(file_path)

def main():
    """ Botni ishga tushirish """
    application = ApplicationBuilder().token(TOKEN).build()

    # Handlerlarni qo'shish
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.PHOTO, handle_post))

    # Botni ishga tushirish
    application.run_polling()

if __name__ == '__main__':
    main()

