# coding=UTF-8
import discord
from discord.ext import commands
from discord import Activity
from discord import ActivityType
import asyncio
import datetime
import re
import os
import time
import psutil
import config

intents = discord.Intents().all()
bot = commands.Bot('!!', shard_count=1, case_insensitive=True, intents=intents)
bot.remove_command('help')


def do_load():
    bot.load_extension("cogs.mod")
    bot.load_extension("cogs.utils")
    bot.load_extension("cogs.music")
    bot.load_extension("cogs.misc")


def do_unload():
    bot.unload_extension("cogs.mod")
    bot.unload_extension("cogs.utils")
    bot.unload_extension("cogs.music")
    bot.unload_extension("cogs.misc")


do_load()




@bot.command()
@commands.is_owner()
async def load(ctx, extension):
    bot.load_extension(f'cogs.{extension}')
    await success(ctx, f"Модуль `{extension}` загружен.")


@bot.command()
@commands.is_owner()
async def unload(ctx, extension):
    bot.unload_extension(f'cogs.{extension}')
    await success(ctx, f"Модуль `{extension}` отключен.")


@bot.command(aliases=['rl'])
@commands.is_owner()
async def reload(ctx, extension):
    bot.unload_extension(f'cogs.{extension}')
    bot.load_extension(f'cogs.{extension}')
    await success(ctx, f"Модуль `{extension}` перезагружен.")


@bot.command(aliases=['rl_all', 'reloadall'])
@commands.is_owner()
async def fullreload(ctx):
    do_unload()
    do_load()
    await success(ctx, f"Все модули перезагружены.")


@bot.command()
@commands.is_owner()
async def shutdown(ctx):
    await ctx.message.add_reaction('✅')
    exit()


@bot.command()
@commands.is_owner()
async def restart(ctx):
    await ctx.message.add_reaction('✅')
    os.system('python core.py')
    exit()




print('Регистрация ивентов...')


@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        return
    print(error)
    msg = None
    if isinstance(error, commands.MissingPermissions):
        msg = f'У вас нет права {str(error).split("missing ")[1].split(" permission")[0]}!'
    if isinstance(error, commands.MissingRequiredArgument):
        msg = 'Вы не задали необходимый аргумент.'
    if isinstance(error, commands.CommandOnCooldown):
        cooldown = round(error.retry_after)
        msg = f'Вы сможете использовать эту команду через {cooldown} секунд.'
    if isinstance(error, commands.errors.NSFWChannelRequired):
        msg = 'Эта команда доступна только в NSFW канале.'
    if isinstance(error, commands.errors.MemberNotFound):
        msg = 'Пользователь не найден.'
    if isinstance(error, commands.errors.CommandInvokeError):
        msg = f'Произошла ошибка. ```{error.original}```'
    if isinstance(error, commands.errors.ChannelNotFound):
        msg = 'Канал не найден.'
    if msg != None:
        e = discord.Embed(description='<a:error:862306041546407936> ' + msg)
        await ctx.send(embed=e)
    return


@bot.event
async def on_message(message):
    if not message.author.bot:
        await bot.process_commands(message)


@bot.event
async def on_ready():
    print('Загрузка завершена!')
    while True:
        s = f'!!help | [{len(bot.guilds)}]'
        await bot.change_presence(activity=discord.Streaming(name=s, url="https://www.youtube.com/watch?v=wq0OaK6dMEo"))
        time = re.sub("\.[0-9][0-9][0-9].*", "", str(datetime.datetime.now().time()))
        print(f'[{time}] Я на {len(bot.guilds)} серверах. CPU: {psutil.cpu_percent()}% RAM: {psutil.virtual_memory().percent}%')
        await asyncio.sleep(300)


async def success(ctx, message, delete_after=None, image=None):
    e = discord.Embed(description='<a:success:860037468279406592> ' + message)
    if image:
        e.set_thumbnail(url=image)
    await ctx.send(embed=e, delete_after=delete_after)


print('Выполняется вход...')
bot.run(config.token())
