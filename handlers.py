from aiogram import F, Router, flags
from aiogram.types import Message
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types.callback_query import CallbackQuery

import keyboard
import text
import utils
from states import Gen

router = Router()


@router.message(Command("start"))
async def start_handler(msg: Message):
    await msg.answer(text.greeting.format(name=msg.from_user.full_name), reply_markup=keyboard.menu)


@router.message(F.text == "Меню")
@router.message(F.text == "Выйти в меню")
@router.message(F.text == "◀️ Выйти в меню")
async def menu(msg: Message):
    await msg.answer(text.menu, reply_markup=keyboard.menu)


@router.callback_query(F.data == "generate_text")
async def input_text_prompt(clbck: CallbackQuery, state: FSMContext):
    await state.set_state(Gen.text_prompt)
    await clbck.message.edit_text(text.gen_text)
    await clbck.message.answer(text.gen_exit, reply_markup=keyboard.exit_kb)


@router.message(Gen.text_prompt)
@flags.chat_action("typing")
async def generate_text(msg: Message, state: FSMContext):
    prompt = msg.text
    msg_ans = await msg.answer(text.gen_wait)
    res = await utils.gen_txt(prompt)
    if not res:
        return await msg_ans.edit_text(text.gen_error, reply_markup=keyboard.iexit_kb)
    await msg_ans.edit_text(res[0] + text.watermark, disable_web_page_preview=True)


@router.callback_query(F.data == "generate_image")
async def input_image_prompt(clbck: CallbackQuery, state: FSMContext):
    await state.set_state(Gen.img_prompt)
    await clbck.message.edit_text(text.gen_image)
    await clbck.message.answer(text.gen_exit, reply_markup=keyboard.exit_kb)


@router.message(Gen.img_prompt)
@flags.chat_action("upload_photo")
async def generate_image(msg: Message, state: FSMContext):
    prompt = msg.text
    msg_ans = await msg.answer(text.gen_wait)
    img_res = await utils.gen_img(prompt)
    if len(img_res) == 0:
        return await msg_ans.edit_text(text.gen_error, reply_markup=keyboard.iexit_kb)
    await msg_ans.delete()
    await msg_ans.answer_photo(photo=img_res[0], caption=prompt + text.watermark)
