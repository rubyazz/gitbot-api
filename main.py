import os
import requests
from aiogram import Bot, Dispatcher, types, executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from config import TOKEN_API


class SearchUser(StatesGroup):
    waiting_for_username = State()
    waiting_for_id = State()

bot = Bot(TOKEN_API)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)

repositories_button = KeyboardButton('Repositories')

repositories_markup = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
repositories_markup.add(repositories_button)


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

        repositories_list_button = KeyboardButton('List Repositories')


        repositories_list_markup = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        repositories_list_markup.add(repositories_list_button)
        
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
        await message.answer(output_message, reply_markup=repositories_list_markup)
        #update data
        await state.update_data(user_data=user_data) # Store user_data in the state context
    else:
        await message.answer(f"User {username} not found. Please try again.")
    await state.finish()



@dp.message_handler(lambda message: message.text == 'List Repositories', state='*')
async def process_list_repositories(message: types.Message, state: FSMContext):
    # Get the user's data from the FSM context
    data = await state.get_data()
    user_data = data.get('user_data')  # get user_data from the context, return None if it doesn't exist
    print(user_data)
    if user_data:
        username = user_data['login']
        repos_url = user_data['repos_url']

        # Send a message with the list of repositories
        response = requests.get(repos_url)
        if response.status_code == 200:
            repositories_data = response.json()
            repositories_list = []
            for repository_data in repositories_data:
                repositories_list.append(repository_data['full_name'])

            await message.answer(f"Repositories for {username}:\n\n" + "\n".join(repositories_list))
        else:
            await message.answer(f"Error retrieving repositories for {username}. Please try again.")
    else:
        await message.answer("User data not found. Please start the conversation again.")

    # End the conversation
    await state.finish()


if __name__ == '__main__':
    print("alright")
    executor.start_polling(dp)
    
