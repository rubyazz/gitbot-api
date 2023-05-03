# gitbot-api
This is a Telegram bot that retrieves information about a GitHub user when the user sends a command with the username of the GitHub user.

When the user sends the `/start` command, the bot sends a welcome message and instructions to enter the username of the GitHub user they want to search for.

When the user sends the `/search` command, the bot prompts them to enter the GitHub username. The username entered by the user is then used to make a request to the GitHub API to retrieve information about the user.

The user information is then formatted into a message and sent back to the user. If the username entered by the user is not found, the bot informs the user that the user was not found.

The bot uses the `aiogram` library to interact with the Telegram API and the `requests` library to interact with the GitHub API. The bot also uses the `aiogram` `FSMContext` to manage the state of the conversation with the user, so that the bot can prompt the user to enter the username of the GitHub user and retrieve the user information in separate steps.
