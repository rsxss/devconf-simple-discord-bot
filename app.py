"""FastAPI serving HTTP healthcheck endpoint"""

import os
import asyncio
import threading

import discord
import requests

from fastapi import FastAPI
from azure.keyvault.secrets import SecretClient
from azure.identity import DefaultAzureCredential

key_vault_name = os.environ["KEY_VAULT_NAME"]
key_vault_uri = f"https://{key_vault_name}.vault.azure.net"

credential = DefaultAzureCredential()
client = SecretClient(vault_url=key_vault_uri, credential=credential)

cat_apikey = client.get_secret('cat-apikey')
bot_token = client.get_secret('discord-bot-token')

api = FastAPI(docs_url=None)


@api.get('/')
async def health_check():
    return {'status': 'OK'}


def bot_thread(token):
    _loop = asyncio.new_event_loop()
    asyncio.set_event_loop(_loop)

    headers = {
        'x-api-key': cat_apikey
    }

    class DiscordClient(discord.Client):

        async def on_ready(self):
            print('Logged on as', self.user)

        async def on_message(self, message):
            # don't respond to ourselves
            if message.author == self.user:
                return

            if message.content == 'ping':
                await message.channel.send('pong')

            if message.content == 'cat':
                resp = requests.get('https://api.thecatapi.com/v1/images/search', headers=headers).json()
                await message.channel.send(resp[0])

    bot_client = DiscordClient()
    bot_client.run(token)


bot = threading.Thread(target=bot_thread, args=(bot_token,))
bot.start()