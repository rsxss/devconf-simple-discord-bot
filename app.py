"""FastAPI serving HTTP healthcheck endpoint"""

import os
import asyncio
import aiohttp

from fastapi import FastAPI
from discord.ext import commands
from azure.keyvault.secrets import SecretClient
from azure.identity import DefaultAzureCredential


key_vault_name = os.environ["KEY_VAULT_NAME"]
key_vault_uri = f"https://{key_vault_name}.vault.azure.net"

credential = DefaultAzureCredential()
vault_client = SecretClient(vault_url=key_vault_uri, credential=credential)

cat_apikey = vault_client.get_secret('cat-apikey').value
bot_token = vault_client.get_secret('discord-bot-token').value

cat_api = 'https://api.thecatapi.com/v1/images'

headers = {
    'x-api-key': cat_apikey
}


class DiscordBot(commands.Bot):

    def __init__(self, command_prefix='!', *args, **kwargs):
        super().__init__(command_prefix=command_prefix, *args, **kwargs)

    def default_commands(self):
        @commands.command(name='ping')
        async def _bc_ping(ctx):
            await ctx.send('pong')

        @commands.command(name='cat')
        async def _bc_cat(ctx):
            async with global_session.get(f'{cat_api}/search', headers=headers) as resp:
                await ctx.send((await resp.json(encoding='utf-8'))[0]['url'])

        return [_command for _command in locals().values() if isinstance(_command, commands.Command)]

    def add_command(self, *_commands):
        if not _commands:
            _commands = self.default_commands()

        for _command in _commands:
            print(f'Added command <{_command}>')
            super().add_command(_command)

        return True


api = FastAPI(docs_url=None)

bot = DiscordBot()
bot.add_command()

global_session = aiohttp.ClientSession()


@api.on_event('startup')
async def startup_event():
    asyncio.create_task(bot.start(bot_token))


@api.get('/')
async def health_check():
    return {'status': 'OK'}
