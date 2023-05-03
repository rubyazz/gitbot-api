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
    waiting_for_id = State()

bot = Bot(TOKEN_API)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)



@dp.message_handler(Command('start'))
async def start_command_handler(message: types.Message):
    await message.answer("Welcome to the GitHub user information bot!")

@dp.message_handler(Command('search'))
async def search_command_handler(message: types.Message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button_username = types.KeyboardButton('Search by username')
    button_id = types.KeyboardButton('Search by ID')
    keyboard.add(button_username, button_id)

    await message.answer("How do you want to search for the GitHub user?", reply_markup=keyboard)

@dp.message_handler(lambda message: message.text == 'Search by username')
async def search_by_username(message: types.Message):
    await message.answer("Enter the username of the GitHub user you want to search for:")
    await SearchUser.waiting_for_username.set()

@dp.message_handler(lambda message: message.text == 'Search by ID')
async def search_by_id(message: types.Message):
    await message.answer("Enter the ID of the GitHub user you want to search for:")
    await SearchUser.waiting_for_id.set()

@dp.message_handler(state=SearchUser.waiting_for_id)
async def process_id(message: types.Message, state: FSMContext):
    user_id = message.text
    response = requests.get(f"https://api.github.com/user/{user_id}")

    if response.status_code == 200:
        user_data = response.json()
        
        output_message = f"GitHub user information for {user_id}:\n\n" \
                        f"Name: {user_data['name']}\n" \
                        f"Avatar: {user_data['avatar_url']}\n" \
                        f"Repositories: {user_data['repos_url']}\n" \
                        f"Bio: {user_data['bio']}\n" \
                        f"Location: {user_data['location']}\n" \
                        f"Followers: {user_data['followers']}\n" \
                        f"Following: {user_data['following']}\n"\
                        f"Twitter: {user_data['twitter_username']}\n"\
                        f"Number of public repos: {user_data['public_repos']}\n"\
                        f"created account at: {user_data['created_at']}\n"
        await message.answer(output_message)
    else:
        await message.answer(f"User with ID {user_id} not found. Please try again.")
    await state.finish()


@dp.message_handler(state=SearchUser.waiting_for_username)
async def process_username(message: types.Message, state: FSMContext):
    username = message.text
    response = requests.get(f"https://api.github.com/users/{username}")

    if response.status_code == 200:
        user_data = response.json()
        
        output_message = f"GitHub user information for {username}:\n\n" \
                        f"Name: {user_data['name']}\n" \
                        f"Avatar: {user_data['avatar_url']}\n" \
                        f"Repositories: {user_data['repos_url']}\n" \
                        f"Bio: {user_data['bio']}\n" \
                        f"Location: {user_data['location']}\n" \
                        f"Followers: {user_data['followers']}\n" \
                        f"Following: {user_data['following']}\n"\
                        f"Twitter: {user_data['twitter_username']}\n"\
                        f"Number of public repos: {user_data['public_repos']}\n"\
                        f"created account at: {user_data['created_at']}\n"
        await message.answer(output_message)
    else:
        await message.answer(f"User {username} not found. Please try again.")
    await state.finish()


if __name__ == '__main__':
    print("alright")
    executor.start_polling(dp)
    
