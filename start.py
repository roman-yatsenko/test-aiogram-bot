import config
from aiogram import Bot, Dispatcher, executor, types

bot = Bot(token=config.TOKEN)
dp = Dispatcher(bot)

# Хэндлер на команду /start
@dp.message_handler(commands=["start"])
async def cmd_start(message: types.Message):
    poll_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    poll_keyboard.add(types.KeyboardButton(
        text="Создать тест",
        request_poll=types.KeyboardButtonPollType(type=types.PollType.QUIZ)
    ))
    poll_keyboard.add(types.KeyboardButton(text="Отмена"))
    await message.answer("Нажмите на кнопку и создайте тест!", 
        reply_markup=poll_keyboard)

# Хэндлер на текстовое сообщение "Отмена"
@dp.message_handler(lambda message: message.text == "Отмена")
async def action_cancel(message: types.Message):
    remove_keyboard = types.ReplyKeyboardRemove()
    await message.answer("Действие отменено. Введите /start, чтобы начать заново",
        reply_markup=remove_keyboard)

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
