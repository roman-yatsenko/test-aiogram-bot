import config
from aiogram import Bot, Dispatcher, executor, types
from quiz import *

bot = Bot(token=config.TOKEN)
dp = Dispatcher(bot)

quiz_db = {} # quiz info
quiz_owners = {} # quiz owners info

# Хэндлер на команду /start
@dp.message_handler(commands=["start"])
async def cmd_start(message: types.Message):
    poll_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    poll_keyboard.add(types.KeyboardButton(
        text="Create quiz",
        request_poll=types.KeyboardButtonPollType(type=types.PollType.QUIZ)
    ))
    poll_keyboard.add(types.KeyboardButton(text="Cancel"))
    await message.answer("Push the button and create quiz!", 
        reply_markup=poll_keyboard)

# Хэндлер на текстовое сообщение "Отмена"
@dp.message_handler(lambda message: message.text == "Cancel")
async def action_cancel(message: types.Message):
    remove_keyboard = types.ReplyKeyboardRemove()
    await message.answer("The action canceled. Type /start to launch again",
        reply_markup=remove_keyboard)

@dp.message_handler(content_types=["poll"])
async def msg_with_poll(message: types.Message):
    user_id = str(message.from_user.id)
    # if user is unknown
    if not quiz_db.get(user_id):
        quiz_db[user_id] = []

    # quiz type check
    if message.poll.type != "quiz":
        await message.reply("Sorry, I can get only quizes!")
        return

    # quiz saving
    quiz_db[user_id].append(Quiz(
        quiz_id=message.poll.id,
        question=message.poll.question,
        options=[o.text for o in message.poll.options],
        correct_option_id=message.poll.correct_option_id,
        owner_id=user_id
    ))
    quiz_owners[message.poll.id] = user_id

    await message.reply(
        f"Quiz saved. Total quiz count: {len(quiz_db[user_id])}"
    )


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
