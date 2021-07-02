# coding=UTF-8
print('Импорт библиотек...')
import discord
print(' + Discord')
from discord.ext import commands
print('    + Commands')
import urllib
print(' + URL-Lib')
from urllib import parse
print('    + Parse')
from urllib import request
print('    + Reqest')
import asyncio
print(' + AsyncIO')
import requests
print(' + Requests')
import datetime
print(' + DateTime')
print('Инициализация...')

import json
import re
import os
import io
import time
import psutil
import nekos
import base64

import config

bot = commands.Bot('!!', shard_count = 4)
bot.remove_command('help')

print('Регистрация асинхронных команд...')

@bot.command()
@commands.has_permissions(manage_messages = True)
@commands.cooldown(1, 10, commands.BucketType.user)
async def mute(ctx, member: discord.Member, time = ''):
    if member == ctx.author:
        emb = discord.Embed(description = ':x: Вы не можете наказать самого себя.', color = 0xdd2e44)
        await ctx.send(embed = emb, delete_after = 2)
        return
    try:
        time = cts(time)/60
    except:
        emb = discord.Embed(description = ':x: Некорректный формат времени.\nПример использования: `!!mute @xshadowsexy 15m`', color = 0xdd2e44)
        await ctx.send(embed = emb, delete_after = 2)
        return
    if 0 < time <= 0.005:
        emb = discord.Embed(description = ':x: Некорректный формат времени.', color = 0xdd2e44)
        await ctx.send(embed = emb, delete_after = 2)
        return
    if time > 1440:
        emb = discord.Embed(description = ':x: Нельзя выдать мут больше чем на 24 часа.', color = 0xdd2e44)
        await ctx.send(embed = emb, delete_after = 2)
        return
    if int(time) == time:
        t = round(time)
    else:
        t = round(time, 2)
    if not discord.utils.get(ctx.guild.roles, name = 'Muted'):
        me = bot.user
        guild = ctx.guild
        if ctx.guild.me.guild_permissions.manage_roles:
            perms = discord.Permissions()
            perms.update(send_messages = False, change_nickname = False, send_tts_messages = False, speak = False, request_to_speak = False)
            try:
                await guild.create_role(name = "Muted")
            except:
                await permerror(ctx)
                return
            muterole = discord.utils.get(ctx.guild.roles, name = 'Muted')
            pos = ctx.guild.me.top_role.position - 1
            await muterole.edit(permissions = perms, position = pos)
    muterole = discord.utils.get(ctx.guild.roles, name = 'Muted')
    emb = discord.Embed(description = f'<:phantom_ok:837302406060179516> Пользователь {member.mention} замучен на `{t}` минут.', color = 0x000000)
    try:
        await member.add_roles(muterole)
    except:
        await permerror(ctx)
        return
    if time == None:
        emb = discord.Embed(description = f'<:phantom_ok:837302406060179516> Пользователь {member.mention} замучен навсегда.', color = 0x000000)
        await ctx.send(embed = emb)
    else:
        await ctx.send(embed = emb)
        await asyncio.sleep(time * 60)
        try:
            await member.remove_roles(muterole)
        except:
            pass

@bot.command()
@commands.has_permissions(manage_messages = True)
@commands.cooldown(1, 10, commands.BucketType.user)
async def unmute(ctx, member: discord.Member):
    muterole = discord.utils.get(ctx.guild.roles,name='Muted')
    if not muterole in member.roles:
        emb = discord.Embed(description = ':x: Этот пользователь уже размучен.', color = 0xdd2e44)
        await ctx.send(embed = emb, delete_after = 2)
        return
    emb = discord.Embed(description = f'<:phantom_ok:837302406060179516> Пользователь {member.mention} размучен.',color=0x000000)
    try:
        await member.remove_roles(muterole)
    except:
        await permerror(ctx)
        return
    await ctx.send(embed = emb)

@bot.command()
@commands.has_permissions(kick_members = True)
@commands.cooldown(1, 10, commands.BucketType.user)
async def kick(ctx, member: discord.Member):
    if member == ctx.author:
        emb = discord.Embed(description = ':x: Вы не можете наказать самого себя.', color = 0xdd2e44)
        await ctx.send(embed = emb, delete_after = 2)
        return
    emb = discord.Embed(description = f'<:phantom_ok:837302406060179516> Пользователь {member} кикнут.', color = 0x000000)
    try:
        await member.kick()
    except:
        await permerror(ctx)
        return
    await ctx.send(embed = emb)

@bot.command()
@commands.has_permissions(ban_members = True)
@commands.cooldown(1, 10, commands.BucketType.user)
async def ban(ctx, member: discord.Member):
    if member == ctx.author:
        emb = discord.Embed(description = ':x: Вы не можете наказать самого себя.', color = 0xdd2e44)
        await ctx.send(embed = emb, delete_after = 2)
        return
    emb = discord.Embed(description = f'<:phantom_ok:837302406060179516> Пользователь {member} забанен.', color = 0x000000)
    try:
        await member.ban()
    except:
        await permerror(ctx)
        return
    await ctx.send(embed = emb)

@bot.command()
@commands.has_permissions(ban_members = True)
@commands.cooldown(1, 10, commands.BucketType.user)
async def unban(ctx, *, member):
    try:
        banned_users = await ctx.guild.bans()
    except:
        await permerror(ctx)
        return
    try:
        member_name, member_discriminator = member.split('#')
    except:
        emb = discord.Embed(description = ':x: Некорректный аргумент.\nПример использования: `!!unban User#0000`', color = 0xdd2e44)
        await ctx.send(embed = emb, delete_after = 2)
        return
    for ban_entry in banned_users:
        user = ban_entry.user
    try:
        await ctx.guild.unban(user)
    except commands.errors.BotMissingPermissions:
        await permerror(ctx)
        return
    except:
        emb = discord.Embed(description = ':x: Этот пользователь не был забанен.', color = 0xdd2e44)
        await ctx.send(embed = emb, delete_after = 2)
        return
    emb = discord.Embed(description = f'<:phantom_ok:837302406060179516> Пользователь {user} разбанен.', color  = 0x000000)
    await ctx.send(embed = emb)

@bot.command(aliases=['purge'])
@commands.has_permissions(manage_messages = True)
@commands.cooldown(1, 30, commands.BucketType.user)
async def clear(ctx, amount):
    if await is_overloaded(ctx):
        return
    try:
        amount = int(amount)
        if amount < 0:
            emb = discord.Embed(description = f':x: Аргумент не может быть отрицательным числом.', color = 0xdd2e44)
            await ctx.send(embed = emb, delete_after = 2)
            return
    except:
        emb = discord.Embed(description = f':x: Заданный аргумент не является числом.', color = 0xdd2e44)
        await ctx.send(embed = emb, delete_after = 2)
    if amount <= 100:
        try:
            deleted = await ctx.message.channel.purge(limit = amount + 1)
        except:
            await permerror(ctx)
            return
        emb = discord.Embed(description = f'<:phantom_ok:837302406060179516> Удалено `{len(deleted)-1}` сообщений.', color = 0x000000)
    else:
        emb = discord.Embed(description = f':x: Нельзя назначить более 100 сообщний для удаления.', color = 0xdd2e44)
    await ctx.send(embed = emb, delete_after = 2)

@bot.command()
@commands.cooldown(1, 5, commands.BucketType.user)
async def cat(ctx):
    link = nekos.cat()
    emb = discord.Embed(color = 0x00000)
    emb.set_image(url = link)
    await ctx.send(embed = emb)

@bot.command()
@commands.cooldown(1, 5, commands.BucketType.user)
async def neko(ctx):
    link = nekos.img('neko')
    emb = discord.Embed(color = 0x000000)
    emb.set_image(url = link)
    await ctx.send(embed = emb)

@bot.command(aliases = ['ngif'])
@commands.is_nsfw()
@commands.cooldown(1, 5, commands.BucketType.user)
async def nekogif(ctx):
    link = nekos.img('ngif')
    emb = discord.Embed(color = 0x000000)
    emb.set_image(url = link)
    await ctx.send(embed = emb)

@bot.command()
@commands.is_nsfw()
@commands.cooldown(1, 5, commands.BucketType.user)
async def nsfw(ctx, req = 'lewd'):
    possible = ['feet', 'yuri', 'trap', 'futanari', 'hololewd', 'lewdkemo', 'solog', 'feetg', 'cum', 'erokemo', 'les', 'lewdk', 'ngif', 'lewd', 'gecg', 'eroyuri', 'eron', 'cum_jpg', 'bj', 'nsfw_neko_gif', 'solo', 'kemonomimi', 'anal', 'hentai', 'erofeet', 'keta', 'blowjob', 'pussy', 'tits', 'holoero', 'pussy_jpg', 'pwankg', 'classic', 'kuni', 'femdom', 'spank', 'erok', 'boobs', 'random_hentai_gif', 'smallboobs', 'ero']
    a = False
    if req in possible:
        a = True
    if not a:
        tags = str(possible).replace('[\'', '`').replace('\', \'', '` `').replace('\']', '`')
        emb = discord.Embed(description=f':x: Использование: `!!nsfw [tag]`\nДоступные теги: {tags}',color=0xdd2e44)
        await ctx.send(embed = emb, delete_after = 8)
        return
    link = nekos.img(req)
    emb = discord.Embed(color = 0x000000)
    emb.set_image(url = link)
    await ctx.send(embed = emb)

@bot.event
async def on_ready():
    print('Загрузка завершена!')

def cts(s):
    seconds_per_unit = {"s": 1, "m": 60, "h": 3600, "d": 86400, "w": 604800}
    return int(s[:-1]) * seconds_per_unit[s[-1]]
    UNITS = {"s":"seconds", "m":"minutes", "h":"hours", "d":"days", "w":"weeks"}
    count = int(s[:-1])
    unit = UNITS[ s[-1] ]
    td = timedelta(**{unit: count})
    return td.seconds + 60 * 60 * 24 * td.days

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        return
    if isinstance(ctx.channel, discord.DMChannel):
        emb = discord.Embed(description = ':x: Выполение этой команды в личных сообщениях невозможно.', color = 0xdd2e44)
        await ctx.send(embed = emb ,delete_after = 2)
        return
    print(f"{ctx.author}: {error}")
    if isinstance(error, commands.MissingPermissions):
        emb = discord.Embed(description = ':x: У вас нет прав для вызова этой команды.', color = 0xdd2e44)
        await ctx.send(embed = emb ,delete_after = 2)
        return
    if isinstance(error, commands.MissingRequiredArgument):
        emb = discord.Embed(description = ':x: Неправильный синтаксис команды.', color = 0xdd2e44)
        await ctx.send(embed = emb, delete_after = 2)
        return
    if isinstance(error, commands.CommandInvokeError):
        emb = discord.Embed(description = f':x: Произошла ошибка.\n```{str(error).split("exception: ")[1]}```', color = 0xdd2e44)
        await ctx.send(embed = emb)
        return
    if isinstance(error, commands.CommandOnCooldown):
        cooldown = round(error.retry_after)
        emb = discord.Embed(description = f':x: Вы сможете использовать эту команду через {cooldown} секунд.', color = 0xdd2e44)
        await ctx.send(embed = emb, delete_after = 2)
        return
    if isinstance(error, commands.errors.NSFWChannelRequired):
        emb = discord.Embed(description = ':x: Эта команда может быть выполнена только в NSFW канале.', color = 0xdd2e44)
        await ctx.send(embed = emb, delete_after = 2)
        return
    if isinstance(error, commands.errors.MemberNotFound):
        emb = discord.Embed(description = ':x: Пользователь не найден.', color = 0xdd2e44)
        await ctx.send(embed = emb, delete_after = 2)
        return
    if isinstance(error, commands.errors.ChannelNotFound):
        emb = discord.Embed(description = ':x: Канал не найден.', color = 0xdd2e44)
        await ctx.send(embed = emb, delete_after = 2)
        return

async def permerror(ctx):
    emb = discord.Embed(description = ':x: У меня нет прав для выполнения этой команды.', color = 0xdd2e44)
    await ctx.send(embed = emb, delete_after = 2)

async def is_overloaded(ctx):
    if ctx.author.id == 811976103673593856:
        return False
    if psutil.cpu_percent() >= 98.4 or psutil.virtual_memory().percent >= 89:
        raise InternalException('Эта команда не доступна во время перегрузки (Проверьте !!status).')
        return True
    else:
        return False

class InternalException(Exception):
    def __init__(self, message):
        super().__init__(message)
        self.message = message

print('Выполняется вход...')
bot.run(config.token())
