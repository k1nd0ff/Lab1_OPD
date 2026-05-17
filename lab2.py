import asyncio
import logging
from datetime import datetime, timedelta

from aiogram import Bot, Dispatcher, F
from aiogram.filters import CommandStart
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s") #настройка logging
token = "8304957959:AAFeVdM8RetJDCPZhPx1SVewUwzWG9fv87Q"

bot = Bot(token=token)
dp = Dispatcher()

doctor = ["Д-р Лобанов", "Д-р Романенко", "Д-р Купитман"]
data = [(datetime.now() + timedelta(days=i)).strftime("%d.%m.%Y") for i in range(1, 8)] # создает список из 7 дат
time = ["09:00", "11:00", "13:00", "15:00", "17:00"]

state = {} # словарь, чтобы не использовать глобальные переменные

def kb(options: list[str]) -> ReplyKeyboardMarkup: #создает кнопки в боте
    rows = []
    for opt in options:
        rows.append([KeyboardButton(text=opt)])
    return ReplyKeyboardMarkup(
        keyboard=rows,
        resize_keyboard=True,
        one_time_keyboard=True,
    )
@dp.message(CommandStart())
async def start(message: Message):
    chat = message.chat.id
    state[chat] = {"step": 1, "data": {}}
    await message.answer(
        "Запись в поликлинику\nВведите ФИО пациента:",
        reply_markup=ReplyKeyboardRemove(),
    )
@dp.message(F.text)
async def dialog(message: Message):
    chat = message.chat.id
    if chat not in state:
        await message.answer("Для запуска: /start.")
        return
    cur = state[chat]
    step = cur["step"]
    txt = message.text.strip()
    if step == 1:
        cur["data"]["fio"] = txt
        cur["step"] = 2
        await message.answer("Выберите врача:", reply_markup=kb(doctor))
        return
    if step == 2:
        if txt not in doctor:
            await message.answer("Выберите врача из списка.")
            return
        cur["data"]["doctor"] = txt
        cur["step"] = 3
        await message.answer("Выберите дату приёма:", reply_markup=kb(data))
        return
    if step == 3:
        if txt not in data:
            await message.answer("Выберите дату.")
            return
        cur["data"]["date"] = txt
        cur["step"] = 4
        await message.answer("Выберите время приёма:", reply_markup=kb(time))
        return
    if step == 4:
        if txt not in time:
            await message.answer("Выберите время из списка.")
            return
        cur["data"]["time"] = txt
        d = cur["data"]
        summary = (
                "Пациент — " + d["fio"] + "\n"
                "Врач — " + d["doctor"] + "\n"
                "Дата — " + d["date"] + "\n"
                "Время — " + d["time"]
        )
        await message.answer(summary, reply_markup=ReplyKeyboardRemove())
        state.pop(chat, None)
async def main() -> None:
    await dp.start_polling(bot)
if __name__ == "__main__":
    asyncio.run(main())