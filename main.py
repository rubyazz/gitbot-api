import os
import requests
from aiogram import Bot, Dispatcher, types, executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command
from aiogram.dispatcher.filters.state import State, StatesGroup
from config import TOKEN_API


class SearchUser(StatesGroup):
    waiting_for_username = State()

bot = Bot(TOKEN_API)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)



@dp.message_handler(Command('start'))
async def start_command_handler(message: types.Message):
    await message.answer("Welcome to the GitHub user information bot!")

@dp.message_handler(Command('search'))
async def search_command_handler(message: types.Message):
    await message.answer("Enter the username of the GitHub user you want to search for:")
    await SearchUser.waiting_for_username.set()

@dp.message_handler(state=SearchUser.waiting_for_username)
async def process_username(message: types.Message, state: FSMContext):
    username = message.text
    response = requests.get(f"https://api.github.com/users/{username}")

    if response.status_code == 200:
        user_data = response.json()
        
        output_message = f"GitHub user information for {username}:\n\n" \
                        f"Name: {user_data['name']}\n" \
                        f"Bio: {user_data['bio']}\n" \
                        f"Location: {user_data['location']}\n" \
                        f"Followers: {user_data['followers']}\n" \
                        f"Following: {user_data['following']}"
        await message.answer(output_message)
    else:
        await message.answer(f"User {username} not found. Please try again.")
    await state.finish()


if __name__ == '__main__':
    print("alright")
    executor.start_polling(dp)
    
