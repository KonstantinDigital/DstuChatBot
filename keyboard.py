from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, KeyboardButton, ReplyKeyboardMarkup


menu = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="💬 Генерировать текст", callback_data="generate_text")],
    [InlineKeyboardButton(text="🎨 Генерировать изображение", callback_data="generate_image")],
])
exit_kb = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text="🏡 Выйти в меню")]],
                              resize_keyboard=True)
iexit_kb = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="🏡 Выйти в меню", callback_data="menu")],
])
