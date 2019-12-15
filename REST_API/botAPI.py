from flask import Flask, request
import json
from telethon import TelegramClient, sync
import asyncio
import os

app = Flask(__name__)

api_id = 1069475
api_hash = '03b85d0fad308c7a26a19b3bacc1a262'


######################## UTILS #####################################
async def make_client(user_id, phone, code=None, hashval=None):
    client = TelegramClient(user_id, api_id, api_hash)
    await client.connect()
    if code is None:
        phone_code_hash = await client.sign_in('+' + phone)
        return f'Code should be sent to user with {user_id}. Your hash value: {phone_code_hash.phone_code_hash}'
    elif hashval is not None:
        await client.sign_in(phone, code, phone_code_hash=hashval)
        return f'Successfully registered user with {user_id}.'


async def send_message_util(user_id, message):
    client = TelegramClient(user_id, api_id, api_hash)
    await client.connect()
    await client.send_message("@Osmiyg", message)
    await client.disconnect()
    return True


async def get_message_util(user_id, limit=1):
    client = TelegramClient(user_id, api_id, api_hash)
    await client.connect()
    entity = await client.get_entity("@Osmiyg")
    messages = await client.get_messages(entity, limit=limit)
    json_list = []
    for i in range(limit):
        json_list.append({"text": messages[i].message, "id": messages[i].id})

    response = json.dumps(json_list)
    await client.disconnect()
    return response


def check_user_util(user_id):
    return os.path.isfile(f'./{user_id}.session')


#####################################################################################

@app.route('/')
def index():
    return 'Hello, I am catBreadBot! You may start the conversation with me by using sendMessage request with ' \
           'chat_id and message as URL parameters. If you are not registered in system, proceed to /register'


@app.route('/sendMessage')
def send_message():
    user_id = request.args.get('user_id')
    message = request.args.get('message')

    response = ""
    if user_id is None:
        response += "User id is empty. "
    elif message is None:
        response += "Message is empty"
    else:
        loop = asyncio.new_event_loop()
        key = loop.run_until_complete(send_message_util(user_id, message))
        if key:
            response = json.dumps({"user_id": user_id, "message": message}, sort_keys=True)
        else:
            response = "Could not deliver a message"
    return response


@app.route('/register/check')
def check():
    user_id = request.args.get('user_id')

    if check_user_util(user_id):
        return f"The user {user_id} is already registered. You may use it)"
    else:
        return f"The user {user_id} is not registered yet. Please, register in /register/register"


@app.route('/register')
def register():
    return 'Register by sending /register/register with two parameters user_id and phone. After you get code via SMS, ' \
           'proceed to /register/register with parameter user_id, phone and code. After that you may ' \
           'use this API. If you want to check the registration use /register/check with parameter user_id'


@app.route('/register/register')
def register_procedure():
    user_id = request.args.get('user_id')
    phone = request.args.get('phone')
    code = request.args.get('code')
    hashval = request.args.get('hash')

    loop = asyncio.new_event_loop()
    response = loop.run_until_complete(make_client(user_id, phone, code, hashval))

    return response


@app.route('/getMessages')
def get_response():
    user_id = request.args.get('user_id')
    limit = request.args.get('limit')
    if limit is None or not limit.isdigit():
        limit = 1
    if user_id is None:
        return "User id is empty"
    elif not check_user_util(user_id):
        return f"The user {user_id} is not registered yet. Please, register in /register/register"

    loop = asyncio.new_event_loop()
    response = loop.run_until_complete(get_message_util(user_id, int(limit)))
    return response


if __name__ == "__main__":
    app.run(host="0.0.0.0")
