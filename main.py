import telebot
from telebot import types
import json
import os
import sys

home = os.path.dirname(os.path.abspath(__file__))

def clear_buffer():
    with open(os.path.join(home, 'buffer'), 'w') as f:
        f.write("")

def load_config():
    with open(os.path.join(home, "config.json"), 'r') as f:
        config = json.load(f)
    return config

config = load_config()
allowed_users = config["allowed_users"]
services = config["services"]

bot = telebot.TeleBot(config["bot_token"])

def get_answer(answer_code, lang = config["app"]["lang"]):
    with open(os.path.join(home, 'answs.json'), "r") as f:
        answers = json.load(f)
    return answers[answer_code][lang]

@bot.message_handler(commands=['start'])
def start(message):
    if message.id == 1:
        print("abcd")
        bot.send_message(message.chat.id, get_answer("registration_greet").format(id=message.from_user.id), parse_mode='HTML')
    else:
        if message.from_user.id in allowed_users:
            bot.send_message(message.chat.id, get_answer("greet_accept").format(username=message.from_user.first_name))
        else:
            bot.send_message(message.chat.id, get_answer("denied_error"))


@bot.message_handler(commands=['help'])
def help(message):
    if message.from_user.id in allowed_users:
        bot.send_message(message.chat.id, get_answer("help"))
    else:
        bot.send_message(message.chat.id, get_answer("denied_error"))
        
@bot.message_handler(commands=['reboot'])
def reboot(message):
    if message.from_user.id in allowed_users:
        button_reboot = types.InlineKeyboardButton('Reboot', callback_data='reboot')
        kb=types.InlineKeyboardMarkup([[button_reboot]])
        bot.send_message(message.chat.id, 'REBOOT', reply_markup=kb)

@bot.callback_query_handler(func=lambda call: call.data == 'reboot')
def reboot_handler(call):
    if call.from_user.id in allowed_users:
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text='REBOOTING...')
        os.system('reboot')

@bot.message_handler(commands=['systemctl'])
def services_(message):
    if message.from_user.id in allowed_users:
        markup = types.InlineKeyboardMarkup()
        for service in services:
            button = types.InlineKeyboardButton(service, callback_data=service)
            markup.add(button)
        bot.send_message(message.chat.id, get_answer("systemctl_greet"), reply_markup=markup)
    else:
        bot.send_message(message.chat.id, get_answer("denied_error"))

@bot.callback_query_handler(func=lambda call: call.data in services)
def service_handler(call):
    if call.from_user.id in allowed_users:
        service = call.data
        buffer = os.path.join(home, "buffer")
        req=os.system(f'sudo systemctl status {service}>"{buffer}"')
        print(req)
        with open(os.path.join(home, 'buffer'), 'r') as f:
            status = f.read()
        clear_buffer()
        if status:
            markup = types.InlineKeyboardMarkup()
            markup.add(types.InlineKeyboardButton("start", callback_data=f"?{service}?start"))
            markup.add(types.InlineKeyboardButton("stop", callback_data=f"?{service}?stop"))
            markup.add(types.InlineKeyboardButton("restart", callback_data=f"?{service}?restart"))
            markup.add(types.InlineKeyboardButton("enable", callback_data=f"?{service}?enable"))
            markup.add(types.InlineKeyboardButton("disable", callback_data=f"?{service}?disable"))
            bot.edit_message_text(text=get_answer("service_status").format(service=service, status=status), chat_id=call.message.chat.id, message_id=call.message.message_id)
            bot.edit_message_reply_markup(chat_id=call.message.chat.id, message_id=call.message.message_id, reply_markup=markup)
        if req ==1024:
            bot.send_message(call.message.chat.id, get_answer("service_not_found"))
    else:
        bot.send_message(call.message.chat.id, get_answer("denied_error"))

@bot.callback_query_handler(func=lambda call: call.data.startswith("?"))
def service_action_handler(call):
    if call.from_user.id in allowed_users:
        service, action = call.data[1:].split("?")
        req=os.system(f"sudo systemctl {action} {service}")
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton(get_answer("come_back"), callback_data="come_back"))
        bot.edit_message_text(text=get_answer(f"service_{action}"), chat_id=call.message.chat.id, message_id=call.message.message_id)
        bot.edit_message_reply_markup(chat_id=call.message.chat.id, message_id=call.message.message_id, reply_markup=markup)
    else:
        bot.send_message(call.message.chat.id, get_answer("denied_error"))
@bot.callback_query_handler(func=lambda call: call.data == "come_back")
def come_back_handler(call):
    if call.from_user.id in allowed_users:
        markup = types.InlineKeyboardMarkup()
        for service in services:
            button = types.InlineKeyboardButton(service, callback_data=service)
            markup.add(button)
        bot.edit_message_text(chat_id=call.message.chat.id, text=get_answer("systemctl_greet"), message_id=call.message.message_id)
        bot.edit_message_reply_markup(chat_id=call.message.chat.id, message_id=call.message.message_id, reply_markup=markup)
    else:
        bot.edit_message_text(chat_id=call.message.chat.id, text=get_answer("denied_error"), message_id=call.message.message_id)

bot.set_my_commands(commands=[
    types.BotCommand(command="start", description="start"),
    types.BotCommand(command="reboot", description="reboot server"),
    types.BotCommand(command="systemctl", description="services control"),
    ])

bot.polling(non_stop=True)
