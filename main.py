import os

from aiogram import Bot, Dispatcher, executor, types
from dotenv import load_dotenv

import helper

load_dotenv()
bot = Bot(token=os.getenv('TG_TOKEN'))
dp = Dispatcher(bot)
owner_tg_id = int(os.getenv('OWNER_TG_ID'))


@dp.message_handler(lambda message: message.from_user.id == owner_tg_id)
async def answer_owner(message: types.Message):
    my_jira = helper.Jira()
    issues = my_jira.get_issues()
    issues = list(filter(lambda issue: issue.get_status_name() == 'To Do', issues))
    biggest_priority = min([issue.get_priority() for issue in issues])
    issues = list(filter(lambda issue: issue.get_priority() == biggest_priority, issues))
    issues_with_due_date = list(filter(lambda issue: issue.get_due_date(), issues))
    if issues_with_due_date:
        issues = list(sorted(issues_with_due_date, key=lambda issue: issue.get_due_date()))
    else:
        issues = list(sorted(issues, key=lambda issue: issue.get_key()))
    issue = issues[0]
    text = f"[{issue.get_key()}] {issue.get_summary()}\n\n"
    text += f"{issue.get_description()}\n\n" if issue.get_description() else ''
    text += f"{issue.get_due_date().strftime('%d.%m.%Y')}\n" if issue.get_due_date() else ''
    text += f"{issue.get_url()}\n"
    await message.answer(text)


@dp.message_handler()
async def answer_other(message: types.Message):
    await message.answer('This bot is not ready yet, but I will notify the creator of your interest!')
    first_name = message.from_user.first_name
    last_name = message.from_user.last_name if 'last_name' in message.from_user else ''
    username = message.from_user.username if 'username' in message.from_user else ''
    user_id = message.from_user.id
    about_user = f"{first_name} {last_name}\n{username}\n{user_id}"
    await bot.send_message(os.getenv('OWNER_TG_ID'), about_user)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
