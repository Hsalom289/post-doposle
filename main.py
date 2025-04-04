import os
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.enums import ParseMode

TOKEN = '7596912191:AAGTup9GbxIe0m8Ex6pJqKZhfnvRK2L1WAY'
MUHAMMAD_ISKANDAROV_ID = 7807493773

bot = Bot(token=TOKEN)
dp = Dispatcher()

class Form(StatesGroup):
    waiting_for_question = State()
    waiting_for_reply = State()

@dp.message(Command("start"))
async def start(message: types.Message):
    user = message.from_user
    
    if user.id == MUHAMMAD_ISKANDAROV_ID:
        await message.answer("Salom, nma gap boshliq?")
        return
    
    inline_keyboard = InlineKeyboardBuilder()
    inline_keyboard.add(InlineKeyboardButton(
        text="Adminga Savol berish", 
        callback_data="ask_question"
    ))
    
    reply_keyboard = ReplyKeyboardBuilder()
    reply_keyboard.add(
        KeyboardButton(text="Narxlar"),
        KeyboardButton(text="Isbot uchun")
    )
    reply_keyboard.adjust(2)
    
    await message.answer(
        f"Salom, {user.first_name}! 😊\n"
        "Adminga savol berish uchun quyidagi knopkani bosing:",
        reply_markup=inline_keyboard.as_markup()
    )
    
    await message.answer(
        "Quyidagi knopkalardan birini tanlang:",
        reply_markup=reply_keyboard.as_markup(resize_keyboard=True)
    )

@dp.message(F.text == "Narxlar")
async def show_prices(message: types.Message):
    await message.answer(
        "Narxlar❕\n\n"
        "1000 ta 50 ming (aralash)👥\n"
        "1000 ta 55 ming (faqat ayollar)👩\n\n"
        "ESLATMA📌\n"
        "BITTA GURUHGA 24 SOAT ICHIDA 5 MINGTA ODAM QO'SHSA BO'LADI\n\n"
        "5MINGTA QUSHTIRGANLAR UCHUN SKITKA BOR✅\n\n"
        "ADMIN 👤@Muhammad_iskandarov"
    )

@dp.message(F.text == "Isbot uchun")
async def show_proof(message: types.Message):
    await message.answer(
        "ISBOT GURUHI! 🤖\n"
        "@Odamqushishhizmatil\n"
        "@Odam_QUSHlSH\n\n"
        "SHAXSIY AKKAUNTIM👇🏻\n"
        "@Muhammad_iskandarov\n\n"
        "TELEFON RAQAMIM\n"
        "+998 93 311 15 29 📱\n\n"
        "BUNDAN BOSHQA AKKAUNT VA NOMERIM YUQ ALDANIB QOLMANG‼️",
        parse_mode=ParseMode.HTML
    )

@dp.callback_query(F.data == "ask_question")
async def ask_question(callback: types.CallbackQuery, state: FSMContext):
    await callback.answer()
    await callback.message.answer("Savolingizni yozing:")
    await state.set_state(Form.waiting_for_question)

@dp.message(Form.waiting_for_question)
async def handle_question(message: types.Message, state: FSMContext):
    user_message = message.text
    if len(user_message.strip()) < 5:
        await message.answer("Savolingizni to'liq va aniq yozing!")
        return
    
    user = message.from_user
    
    try:
        keyboard = InlineKeyboardBuilder()
        keyboard.add(InlineKeyboardButton(
            text="Foydalanuvchiga javob yozish", 
            callback_data=f"reply_to_{user.id}"
        ))
        
        if user.username:
            username_display = f"@{user.username}"
        else:
            username_display = f'<a href="tg://user?id={user.id}">Foydalanuvchi lichkasi</a>'
        
        await bot.send_message(
            chat_id=MUHAMMAD_ISKANDAROV_ID,
            text=f"Yangi savol!\n\nFoydalanuvchi: {user.first_name} (ID: {user.id})\nUsername: {username_display}\n\nXabar:\n{user_message}",
            reply_markup=keyboard.as_markup(),
            parse_mode=ParseMode.HTML
        )
        await message.answer("Savolingiz adminga yuborildi, javobni kuting!")
        await state.clear()
    except Exception as e:
        await message.answer(f"Xatolik: {str(e)}")

@dp.callback_query(F.data.startswith("reply_to_"))
async def handle_reply_button(callback: types.CallbackQuery, state: FSMContext):
    if callback.from_user.id != MUHAMMAD_ISKANDAROV_ID:
        await callback.answer(f"Bu funksiya faqat admin uchun! Sizning ID'ingiz: {callback.from_user.id}")
        return
    
    user_id = int(callback.data.split('_')[-1])
    await state.update_data(reply_to_user_id=user_id)
    
    await callback.answer()
    await callback.message.answer(f"Foydalanuvchi (ID: {user_id}) ga yuboriladigan javobingizni yozing:")
    await state.set_state(Form.waiting_for_reply)

@dp.message(Form.waiting_for_reply)
async def handle_admin_reply(message: types.Message, state: FSMContext):
    if message.from_user.id != MUHAMMAD_ISKANDAROV_ID:
        return
    
    data = await state.get_data()
    if 'reply_to_user_id' not in data:
        await message.answer("Javob yuborish uchun foydalanuvchi tanlanmagan.")
        return
    
    reply_message = message.text
    user_chat_id = data['reply_to_user_id']
    
    try:
        await bot.send_message(
            chat_id=user_chat_id,
            text=f"Admin javobi:\n\n{reply_message}"
        )
        await bot.send_message(
            chat_id=MUHAMMAD_ISKANDAROV_ID,
            text=f"Javob foydalanuvchiga (ID: {user_chat_id}) yuborildi!"
        )
    except Exception as e:
        await message.answer(f"Xatolik: {str(e)}")
        return
    
    await state.clear()

@dp.message()
async def handle_other_messages(message: types.Message):
    await message.answer("Iltimos, adminga savol berish uchun matndagi 'Adminga Savol berish' knopkasini bosing yoki pastdagi knopkalardan birini tanlang!")

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
