# coding=UTF-8
print('Импорт библиотек...')
import discord
print(' + Discord')
from discord.ext import commands
print('    + Commands')
from discord import Activity
print('    + Activity')
from discord import ActivityType
print('    + ActivityType')
from discord import FFmpegPCMAudio
print('    + FFmpegPCMAudio')
import urllib
print(' + URL-Lib')
from urllib import parse
print('    + Parse')
from urllib import request
print('    + Request')
import asyncio
print(' + AsyncIO')
import requests
print(' + Requests')
import datetime
print(' + DateTime')

print('Загрузка YouTubeDL...')
import youtube_dl

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

nullTime = time.time()
loops = {}
nowPlaying = {}
FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 10', 'options': '-vn'}

bot = commands.Bot('!!', shard_count = 4, case_insensitive = True, intents = discord.Intents().all())
bot.remove_command('help')

__data__ = requests.get("https://espradio.ru/stream_list.json")
list = __data__.text

print('Регистрация асинхронных команд...')

@bot.command()
@commands.cooldown(1, 5, commands.BucketType.user)
async def help(ctx, page = 0):
    if ctx.message.author.bot:
        return
    if page == 0 or page > 4:
        default = '`1.` Модерация\n`2.` Музыка\n`3.` Утилиты\n`4.` Прочее\n\nИспользуйте `!!help [page]` для просмотра списка команд из этой категории. Что нового: `!!about`. [Сервер поддержки](https://discord.gg/fj4vCdFVw3).'
        emb = discord.Embed(color = 0x000000)
        emb.add_field(name = 'Доступные категории команд', value = default)
        emb.set_footer(text = '© 2021 Sweety187 | Все права защищены.', icon_url = 'https://media.discordapp.net/attachments/832662675963510827/855762014010081300/b5222c5b.jpg')
        #emb.set_thumbnail(url = bot.user.avatar_url)
        await ctx.send(embed = emb)
        return
    mod = '`!!kick <member>` - кикнуть пользователя\n`!!ban <member>` - забанить пользователя\n`!!unban <user#0000>` - разбанить пользователя\n`!!mute <member> [time]` - замутить пользователя\n`!!unmute <member>` - размутить пользователя\n`!!clear <amount>` - удалить последние N сообщений в канале'
    music = '`!!join [channel]` - присоединиться к голосовому каналу\n`!!leave` - покуинуть голосовой канал\n`!!play <query>` - воспроизвести музыку с YouTube\n`!!radio <stream>` - проигрывать радио в голосовом канале\n`!!stop` - остановить воспроизведение\n`!!pause` - приостановить воспроизведение\n`!!resume` - продолжить воспроизведение\n`!!repeat` - зациклить воспроизведение\n`!!now` - узнать, что сейчас играет'
    utils = '`!!avatar [member]` - вывести аватар пользователя\n`!!yt <query>` - найти видео на YouTube\n`!!ping <ip>` - выводит информацию о сервере Minecraft\n`!!2b2t` - выводит данные о сервере 2b2t (очередь и т.п.)\n`!!skin <nick>` - выводит скин игрока Minecraft\n`!!say <text>` - отправить сообщение от имени бота\n`!!embed <text>` - отправить ваш текст внутри ембеда\n`!!timer <time>` - поставить таймер\n`!!user [user]` - информация о пользователе\n`!!server` - информация о сервере'
    misc = '`!!neko` - случайная картинка с неко\n`!!nekogif` - случайная гифка с неко\n`!!cat` - случайная картинка с котом\n`!!nsfw [tag]` - хентай-картинка по тегу («lewd», если тег не указан)\n`!!invite` - добавить меня на свой сервер\n`!!about` - сведения о текущей версии бота\n`!!status` - статистика бота\n`!!bug <report>` - сообщить об ошибке'
    pages = [mod, music, utils, misc]
    titles = ['1. Модерация','2. Музыка','3. Утилиты','4. Прочее']
    emb = discord.Embed(color = 0x000000)
    emb.add_field(name = titles[page - 1], value = pages[page - 1])
    emb.set_footer(text = '© 2021 Sweety187 | Все права защищены.', icon_url = 'https://media.discordapp.net/attachments/832662675963510827/855762014010081300/b5222c5b.jpg')
    await ctx.send(embed = emb)

@bot.command()
@commands.cooldown(1, 15, commands.BucketType.user)
async def status(ctx):
    t = int(time.time() - nullTime)
    t = datetime.timedelta(seconds = t)
    e = discord.Embed(title = "Статистика бота", color = 0x000000)
    e.add_field(name = 'Аптайм', value = t, inline = True)
    e.add_field(name = 'Версия', value = 'b10.2.5', inline = True)
    e.add_field(name = 'Серверов', value = len(bot.guilds), inline = True)
    mc = 0
    for guild in bot.guilds:
        mc = mc + guild.member_count
    e.add_field(name = 'Пользователей',value = mc, inline = True)
    e.add_field(name = 'Нагрузка', value = f'ЦП: {psutil.cpu_percent()}% ОЗУ: {psutil.virtual_memory().percent}%', inline = True)
    e.set_thumbnail(url="https://media.discordapp.net/attachments/832662675963510827/857631236355522650/logo.png")
    e.set_footer(text = '© 2021 Sweety187 | Все права защищены.', icon_url = 'https://media.discordapp.net/attachments/832662675963510827/855762014010081300/b5222c5b.jpg')
    await ctx.send(embed = e)

@bot.command()
@commands.cooldown(1, 15, commands.BucketType.user)
async def invite(ctx):
    emb = discord.Embed(description = '<:phantom_ii:857628296745320528> Добавить бота на свой сервер: [https://discord.com/api/oauth2/authorize](https://discord.com/api/oauth2/authorize?client_id=837282453654732810&permissions=8&scope=bot)', color = 0x000000)
    await ctx.send(embed = emb)

@bot.command()
@commands.cooldown(1, 15, commands.BucketType.user)
async def about(ctx):
    emb = discord.Embed(title = "Бета 10.2.5 от 08.07.2021 11:52 MSK", color = 0x000000)
    fixed = "ㆍИсправления мелких ошибок."
    improved = "ㆍВ команде `!!server` вместо ID теперь отображается ник владельца сервера."
    added = "ㆍВ команде `!!server` отображается ID сервера.\nㆍВ команде `!!user` отображается активность и статус пользователя."
    deleted = "ㆍБот больше не будет автоматически отключаться от голосового канала."
    #emb.add_field(name = 'Исправлено', value = fixed, inline = False)
    emb.add_field(name = 'Изменено', value = improved, inline = False)
    emb.add_field(name = 'Добавлено', value = added, inline = False)
    #emb.add_field(name = 'Удалено', value = deleted, inline = False)
    emb.set_footer(text = '© 2021 Sweety187 | Все права защищены.', icon_url = 'https://media.discordapp.net/attachments/832662675963510827/855762014010081300/b5222c5b.jpg')
    await ctx.send(embed = emb)

@bot.command()
@commands.cooldown(1, 1800, commands.BucketType.user)
async def bug(ctx, *, message):
    guild = discord.utils.get(bot.guilds, id = 859735750555992064)
    channel = discord.utils.get(guild.channels, id = 859838257542201365)
    emb = discord.Embed(title = "Сообщение об ошибке", color = 0x000000)
    emb.add_field(name = "Автор", value = ctx.author, inline = False)
    emb.add_field(name = "Сообщение", value = message, inline = False)
    emb.set_thumbnail(url = "https://www.iconsdb.com/icons/download/white/error-6-64.png")
    await channel.send(embed = emb)
    emb = discord.Embed(description = f'<:phantom_ok:837302406060179516> Ваше сообщение было отправлено на [сервер поддержки](https://discord.gg/fj4vCdFVw3).', color = 0x000000)
    await ctx.send(embed = emb)

@bot.command(aliases = ['userinfo'])
@commands.cooldown(1, 5, commands.BucketType.user)
async def user(ctx, user: discord.Member = None):
    if user is None:
        user = ctx.author
    status = str(user.status)
    if status == 'dnd':
        status = 'Не беспокоить'
    if status == 'dnd':
        status = 'Не активен'
    if status == 'online':
        status = 'В сети'
    if status == 'dnd':
        status = 'Не в сети'
    activity = user.activity
    rows = f"""Пользователь:        {str(user).replace("`", "")}
ID:                  {user.id}
Статус:              {status}
Активность:          {activity if activity else 'Нет'}
Бот:                 {"Да" if user.bot else "Нет"}
Роль:                {str(user.top_role).replace("`", "")}
Ролей:               {len(user.roles)-1}
Зарегистрирован:     {user.created_at.strftime("%d.%m.%Y %H:%M:%S")}
Присоединился:       {user.joined_at.strftime("%d.%m.%Y %H:%M:%S")}"""
    emb = discord.Embed(title = user, description = f"```{rows}```", color = 0x000000)
    emb.set_thumbnail(url = user.avatar_url)
    await ctx.send(embed = emb)

@bot.command()
@commands.cooldown(1, 5, commands.BucketType.user)
async def server(ctx):
    async with ctx.typing():
        guild = ctx.guild
        name = guild.name
        icon = guild.icon_url
        created = str(guild.created_at).split('.')[0].replace('-', '.')
        owner = bot.get_user(guild.owner_id)
        members = guild.member_count
        categories = len(guild.categories)
        tchannels = len(guild.text_channels)
        vchannels = len(guild.voice_channels)
        roles = len(guild.roles)
        blevel = guild.premium_tier
        bcount = guild.premium_subscription_count
        region = str(guild.region).upper()
    emb = discord.Embed(color = 0x000000)
    a = f"""```
ID сервера:             {guild.id}
Дата создания:          {created}
Владелец:               {owner}
Участников:             {members}
Категорий:              {categories}
Текстовых каналов:      {tchannels}
Голосовых каналов:      {vchannels}
Ролей:                  {roles}
Уровень буста:          {blevel}
Бустов:                 {bcount}
Регион:                 {region}
```"""
    emb.add_field(name = name, value = a)
    emb.set_thumbnail(url = icon)
    await ctx.send(embed = emb)

@bot.command()
@commands.cooldown(1, 30, commands.BucketType.user)
async def skin(ctx, nick):
    if await is_overloaded(ctx):
        return
    if len(re.findall("[^A-Za-z0-9_]", nick)) > 0:
        emb = discord.Embed(description = ':x: Недопустимые символы.', color = 0xdd2e44)
        await ctx.message.reply(embed = emb, delete_after = 2, mention_author = False)
        return
    url = f"https://ru.namemc.com/profile/{nick}.1"
    async with ctx.typing():
        guild = discord.utils.get(bot.guilds, id = 832662675963510824)
        channel = discord.utils.get(guild.channels, name = "skins")
        await channel.send(url, delete_after = 5)
        await asyncio.sleep(1)
        message = await channel.send(url, delete_after = 5)
    if "Поиск" in message.embeds[0].title:
        emb = discord.Embed(description = ':x: Лицензионного аккаунта с таким ником нет.', color = 0xdd2e44)
        await ctx.message.reply(embed = emb, delete_after = 2, mention_author = False)
        return
    skin = message.embeds[0].thumbnail.url
    name = message.embeds[0].title.split(' | Учётная запись Minecraft')[0]
    emb = discord.Embed(title = f"Скин {name}", color = 0x000000)
    skin = skin.split("&width=")[0] + "&width=600&height=300&scale=4&overlay=true&theta=30&phi=20&time=90&shadow_color=000&shadow_radius=0&shadow_x=0&shadow_y=0&front_and_back=true"
    emb.set_image(url = skin)
    await ctx.send(embed = emb)

@bot.command()
@commands.has_permissions(manage_messages = True)
@commands.cooldown(1, 10, commands.BucketType.user)
async def mute(ctx, member: discord.Member, time = ''):
    if member == ctx.author:
        emb = discord.Embed(description = ':x: Вы не можете наказать самого себя.', color = 0xdd2e44)
        await ctx.message.reply(embed = emb, delete_after = 2, mention_author = False)
        return
    try:
        time = cts(time)/60
    except:
        emb = discord.Embed(description = ':x: Некорректный формат времени.\nПример использования: `!!mute @xshadowsexy 15m`', color = 0xdd2e44)
        await ctx.message.reply(embed = emb, delete_after = 2, mention_author = False)
        return
    if 0 < time <= 0.005:
        emb = discord.Embed(description = ':x: Некорректный формат времени.', color = 0xdd2e44)
        await ctx.message.reply(embed = emb, delete_after = 2, mention_author = False)
        return
    if time > 1440:
        emb = discord.Embed(description = ':x: Нельзя выдать мут больше чем на 24 часа.', color = 0xdd2e44)
        await ctx.message.reply(embed = emb, delete_after = 2, mention_author = False)
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
    if t == None or t <= 0:
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
@commands.cooldown(1, 5, commands.BucketType.user)
async def unmute(ctx, member: discord.Member):
    muterole = discord.utils.get(ctx.guild.roles,name='Muted')
    if not muterole in member.roles:
        emb = discord.Embed(description = ':x: Этот пользователь уже размучен.', color = 0xdd2e44)
        await ctx.message.reply(embed = emb, delete_after = 2, mention_author = False)
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
@commands.cooldown(1, 5, commands.BucketType.user)
async def kick(ctx, member: discord.Member):
    if member == ctx.author:
        emb = discord.Embed(description = ':x: Вы не можете наказать самого себя.', color = 0xdd2e44)
        await ctx.message.reply(embed = emb, delete_after = 2, mention_author = False)
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
@commands.cooldown(1, 5, commands.BucketType.user)
async def ban(ctx, member: discord.Member):
    if member == ctx.author:
        emb = discord.Embed(description = ':x: Вы не можете наказать самого себя.', color = 0xdd2e44)
        await ctx.message.reply(embed = emb, delete_after = 2, mention_author = False)
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
@commands.cooldown(1, 5, commands.BucketType.user)
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
        await ctx.message.reply(embed = emb, delete_after = 3, mention_author = False)
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
        await ctx.message.reply(embed = emb, delete_after = 3, mention_author = False)
        return
    emb = discord.Embed(description = f'<:phantom_ok:837302406060179516> Пользователь {user} разбанен.', color  = 0x000000)
    await ctx.send(embed = emb)

@bot.command(aliases = ['purge'])
@commands.has_permissions(manage_messages = True)
@commands.cooldown(1, 5, commands.BucketType.user)
async def clear(ctx, amount):
    if await is_overloaded(ctx):
        return
    try:
        amount = int(amount)
        if amount <= 0:
            emb = discord.Embed(description = f':x: Некорректный аргумент.', color = 0xdd2e44)
            await ctx.message.reply(embed = emb, delete_after = 2, mention_author = False)
            return
    except:
        emb = discord.Embed(description = f':x: Заданный аргумент не является числом.', color = 0xdd2e44)
        await ctx.message.reply(embed = emb, delete_after = 2, mention_author = False)
        return
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
async def avatar(ctx, member: discord.Member = None):
    if not member:
        member = ctx.message.author
    emb = discord.Embed(title = f'Аватар {member}', color = 0x000000)
    avatar = str(member.avatar_url)[:-10]+'?size=512&width=512&height=512'
    emb.set_image(url = avatar)
    await ctx.send(embed = emb)

@bot.command(aliases = ['summon'])
@commands.cooldown(1, 5, commands.BucketType.user)
async def join(ctx, *, channel=None):
    if await is_overloaded(ctx):
        return
    e = False
    if ctx.author.voice or channel:
        if channel == None:
            channel = ctx.author.voice.channel
        else:
            channel = get_channel(ctx, channel)
            if not channel:
                emb = discord.Embed(description = ':x: Канал не найден.', color = 0xdd2e44)
                await ctx.message.reply(embed = emb, delete_after = 2, mention_author = False)
                return
        voice = discord.utils.get(ctx.bot.voice_clients, guild = ctx.guild)
        emb = discord.Embed(description = '<:phantom_ok:837302406060179516> Подключен к голосовому каналу.', color = 0x000000)
        if voice:
            vc = ctx.message.guild.voice_client
            try:
                await vc.move_to(channel)
            except:
                emb = discord.Embed(description = ':x: Не удалось подключиться к голосовому каналу.', color = 0xdd2e44)
                e == True
        else:
            try:
                await channel.connect(timeout = 5, reconnect = True)
            except:
                emb = discord.Embed(description = ':x: Не удалось подключиться к голосовому каналу.', color = 0xdd2e44)
                e == True
    else:
        emb = discord.Embed(description = ':x: Вы должны находиться в голосовом канале для вызова этой команды.', color = 0xdd2e44)
        e = True
    if e == True:
        await ctx.message.reply(embed = emb, delete_after = 2, mention_author = False)
        return
    await ctx.send(embed = emb)

@bot.command(aliases = ['disconnect'])
@commands.cooldown(1, 5, commands.BucketType.user)
async def leave(ctx):
    if is_connected(ctx):
        vc = ctx.message.guild.voice_client
        await vc.disconnect()
        emb = discord.Embed(description = '<:phantom_ok:837302406060179516> Отключен от голосового канала.', color = 0x000000)
        await ctx.send(embed = emb)
    else:
        emb = discord.Embed(description = ':x: Я не подключен к голосовому каналу на этом сервере.', color = 0xdd2e44)
        await ctx.message.reply(embed = emb, delete_after = 2, mention_author = False)

@bot.command()
@commands.cooldown(1, 5, commands.BucketType.user)
async def say(ctx, *, text):
    if re.search(".*@.*", str(text)):
        if not ctx.author.guild_permissions.mention_everyone:
            emb = discord.Embed(description = ':x: У вас нет прав для отправки сообщений с упоминаниями.', color = 0xdd2e44)
            await ctx.message.reply(embed = emb, delete_after = 2, mention_author = False)
            return
    await ctx.send(text)

@bot.command()
@commands.cooldown(1, 5, commands.BucketType.user)
async def embed(ctx, *, text):
    emb = discord.Embed(description = text, color = 0x000000)
    await ctx.send(embed = emb)

@bot.command()
@commands.cooldown(1, 15, commands.BucketType.user)
async def timer(ctx, time = ''):
    try:
        time = cts(time)/60
    except:
        emb = discord.Embed(description = ':x: Некорректный формат времени.\nПример использования: `!!timer 5m`', color = 0xdd2e44)
        await ctx.message.reply(embed = emb, delete_after = 2, mention_author = False)
        return
    if time <= 0.005:
        emb = discord.Embed(description = ':x: Некорректный формат времени.', color = 0xdd2e44)
        await ctx.message.reply(embed = emb, delete_after = 2, mention_author = False)
        return
    if time > 60:
        emb = discord.Embed(description = ':x: Нельзя установить таймер больше чем на 60 минут.', color = 0xdd2e44)
        await ctx.message.reply(embed = emb, delete_after = 3, mention_author = False)
        return
    if int(time) == time:
        t = round(time)
    else:
        t = round(time, 2)
    emb = discord.Embed(description = f'<:phantom_ok:837302406060179516> Установлен таймер на `{t}` минут.', color = 0x000000)
    await ctx.send(embed = emb)
    await asyncio.sleep(time * 60)
    m = await ctx.send(ctx.author.mention)
    await m.delete()
    emb = discord.Embed(description = f'<:phantom_wr:857262088068792350> Таймер сработал, прошло `{t}` минут!', color = 0x000000)
    await ctx.send(embed = emb)

@bot.command()
@commands.cooldown(1, 20, commands.BucketType.user)
async def radio(ctx, url = ''):
    if await is_overloaded(ctx):
        return
    if not url or not re.findall(f"\"url\":\"{url}\"", list):
        emb = discord.Embed(description = ':x: Использование: `!!radio <url>`\nСписок станций: https://espradio.ru/stream_list', color = 0xdd2e44)
        await ctx.message.reply(embed = emb, delete_after = 8, mention_author = False)
        return
    if not ctx.author.voice:
        emb = discord.Embed(description = ':x: Вы должны находиться в голосовом канале для вызова этой команды.', color = 0xdd2e44)
        await ctx.message.reply(embed = emb, delete_after = 2, mention_author = False)
        return
    voice = get_voice(ctx)
    if nowPlaying.get(ctx.guild.id) != url:
        nowPlaying[ctx.guild.id] = url
    if ctx.message.author.voice:
        channel = ctx.author.voice.channel
        if is_connected(ctx):
            player = voice
            try:
                voice.stop()
            except:
                pass
        else:
            try:
                player = await channel.connect(timeout = 5, reconnect = True) 
            except:
                emb = discord.Embed(description = ':x: Не удалось подключиться к голосовому каналу.', color = 0xdd2e44)
                await ctx.message.reply(embed = emb, delete_after = 2, mention_author = False)
                return
    try:
        await ctx.guild.me.edit(suppress=False)
    except:
        pass
    async with ctx.typing():
        name = re.findall(f"\"name\":\".*\",\"url\":\"{url}\"", list)[0].split(":\"")[1].split('\",')[0]
        emb = discord.Embed(description = f'<:phantom_ok:837302406060179516> Воспроизведение:\n```{name}```\nСсылка на радиостанцию: {url}', color = 0x000000)
    player.play(FFmpegPCMAudio(url))
    await ctx.send(embed = emb)

@bot.command(aliases=['p'])
@commands.cooldown(1, 20, commands.BucketType.user)
async def play(ctx, *, query = ''):
    if await is_overloaded(ctx):
        return
    if not query:
        emb = discord.Embed(description = ':x: Использование: `!!play <query>`', color = 0xdd2e44)
        await ctx.message.reply(embed = emb, delete_after = 2, mention_author = False)
        return
    if not ctx.author.voice:
        emb = discord.Embed(description = ':x: Вы должны находиться в голосовом канале для вызова этой команды.', color = 0xdd2e44)
        await ctx.message.reply(embed = emb, delete_after = 2, mention_author = False)
        return
    channel = ctx.author.voice.channel
    voice = get_voice(ctx)
    emb = discord.Embed(description = f'<:phantom_sr:851443028979613716> Выполняется поиск на YouTube:\n```{query.replace("`", "")}```', color = 0x000000)
    lastmsg = await ctx.send(embed = emb)
    query_string = urllib.parse.urlencode({'search_query': query})
    htm_content = urllib.request.urlopen('http://www.youtube.com/results?' + query_string)
    try:
        search_results = re.findall(r'/watch\?v=(.{11})', htm_content.read().decode())
        url = f'https://youtu.be/{search_results[0]}'
    except:
        pass
        await lastmsg.delete()
        emb = discord.Embed(description = ':x: По вашему запросу ничего не найдено.', color = 0xdd2e44)
        await ctx.message.reply(embed = emb, delete_after = 2, mention_author = False)
        return
    if is_connected(ctx) and voice.is_playing():
        try:
            voice.stop()
        except:
            pass
    await lastmsg.add_reaction('✅')
    if get_voice(ctx) != None:
        player = get_voice(ctx)
    else:
        try:
            player = await channel.connect(timeout = 5, reconnect = True)
        except:
            await lastmsg.delete()
            emb = discord.Embed(description = ':x: Не удалось подключиться к голосовому каналу.', color = 0xdd2e44)
            await ctx.message.reply(embed = emb, delete_after = 2, mention_author = False)
            return
    try:
        await ctx.guild.me.edit(suppress=False)
    except:
        pass
    async with ctx.typing():
        ydl_opts = {'format': 'worstaudio'}
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download = False)
            URL = info['formats'][0]['url']
            title = info.get('title', None)
            duration = info.get('duration', None)
        d = duration
        if nowPlaying.get(ctx.guild.id) == None or nowPlaying.get(ctx.guild.id) != url:
            nowPlaying[ctx.guild.id] = url
        duration = datetime.timedelta(seconds = duration)
    emb = discord.Embed(description = f'<:phantom_ok:837302406060179516> Воспроизведение:\n```{title.replace("`", "")} ({duration})```\nСсылка на видео: {url}', color = 0x000000)
    i = 1
    while loops.get(ctx.guild.id) == True or i == 1:
        if nowPlaying.get(ctx.guild.id) != url:
            break
        voice = get_voice(ctx)
        try:
            if voice.is_playing():
                voice.stop()
        except:
            pass
        player.play(discord.FFmpegPCMAudio(URL, **FFMPEG_OPTIONS))
        if i == 1:
            await lastmsg.delete()
            await ctx.send(embed = emb)
        i = 0
        await asyncio.sleep(d + 1)
        if nowPlaying.get(ctx.guild.id) != url:
            break
        if not is_connected(ctx):
            break
        if not loops.get(ctx.guild.id):
            nowPlaying[ctx.guild.id] = None
        player.stop()

@bot.command(aliases=['np', 'nowplaying'])
@commands.cooldown(1, 15, commands.BucketType.user)
async def now(ctx):
    if await is_overloaded(ctx):
        return
    url = nowPlaying.get(ctx.guild.id)
    if not url:
        emb = discord.Embed(description = ':x: Сейчас ничего не играет.', color = 0xdd2e44)
        await ctx.message.reply(embed = emb, delete_after = 2, mention_author = False)
        return
    if "youtu.be" not in url:
        async with ctx.typing():
            name = re.findall(f"\"name\":\".*\",\"url\":\"{url}\"", list)[0].split(":\"")[1].split('\",')[0]
            emb = discord.Embed(description = f'<:phantom_ii:857628296745320528> Сейчас играет:\n```{name}```\nСсылка на радиостанцию: {url}', color = 0x000000)
            await ctx.send(embed = emb)
            return
    async with ctx.typing():
        ydl_opts = {'format': 'worstaudio'}
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            title = info.get('title', None)
            duration = info.get('duration', None)
        duration = datetime.timedelta(seconds = duration)
    emb = discord.Embed(description = f'<:phantom_ii:857628296745320528> Сейчас играет:\n```{title.replace("`", "")} ({duration})```\nСсылка на видео: {url}', color = 0x000000)
    await ctx.send(embed = emb)

@bot.command()
@commands.cooldown(1, 5, commands.BucketType.user)
async def pause(ctx):
    if not ctx.author.voice:
        emb = discord.Embed(description = ':x: Вы должны находиться в голосовом канале для вызова этой команды.', color = 0xdd2e44)
        await ctx.message.reply(embed = emb, delete_after = 2, mention_author = False)
        return
    voice = get_voice(ctx)
    if voice.is_playing():
        voice.pause()
        emb = discord.Embed(color = 0x000000, description = '<:phantom_ok:837302406060179516> Воспроизведение приостановлено.')
        await ctx.send(embed = emb)
    else:
        emb = discord.Embed(color = 0xdd2e44, description = ':x: Сейчас ничего не играет.')
        await ctx.send(embed = emb, delete_after = 2)

@bot.command(aliases = ['re'])
@commands.cooldown(1, 5, commands.BucketType.user)
async def resume(ctx):
    if not ctx.author.voice:
        emb = discord.Embed(description = ':x: Вы должны находиться в голосовом канале для вызова этой команды.', color = 0xdd2e44)
        await ctx.message.reply(embed = emb, delete_after = 2, mention_author = False)
        return
    voice = get_voice(ctx)
    if await is_overloaded(ctx) and voice:
        voice.stop()
        return
    if voice.is_paused():
        voice.resume()
        emb = discord.Embed(color = 0x000000, description = '<:phantom_ok:837302406060179516> Воспроизведение продолжено.')
        await ctx.send(embed = emb)
    else:
        emb = discord.Embed(color = 0xdd2e44, description = ':x: Воспроизведение не было приостановлено.')
        await ctx.message.reply(embed = emb, delete_after = 2, mention_author = False)

@bot.command(aliases = ['youtube'])
@commands.cooldown(1, 15, commands.BucketType.user)
async def yt(ctx, *, query = ''):
    if await is_overloaded(ctx):
        return
    if not query:
        emb = discord.Embed(description = ':x: Использование: `!!yt <query>`', color = 0xdd2e44)
        await ctx.message.reply(embed = emb, delete_after = 3, mention_author = False)
        return
    emb = discord.Embed(description=f'<:phantom_sr:851443028979613716> Выполняется поиск на YouTube:\n```{query}```', color = 0x000000)
    lastmsg = await ctx.send(embed = emb)
    query_string = urllib.parse.urlencode({'search_query': query})
    async with ctx.typing():
        htm_content = urllib.request.urlopen('http://www.youtube.com/results?' + query_string)
        search_results = re.findall(r'/watch\?v=(.{11})', htm_content.read().decode())
    try:
        msg = description=f'`1.` https://youtu.be/{search_results[0]}\n`2.` https://youtu.be/{search_results[1]}\n`3.` https://youtu.be/{search_results[2]}'
        await lastmsg.delete()
        await ctx.send(msg)
    except:
        await lastmsg.delete()
        emb = discord.Embed(description=':x: По вашему запросу ничего не найдено.', color = 0xdd2e44)
        await ctx.message.reply(embed = emb, delete_after = 3, mention_author = False)

@bot.command(aliases = ['s', 'skip'])
@commands.cooldown(1, 5, commands.BucketType.user)
async def stop(ctx):
    if not ctx.author.voice:
        emb = discord.Embed(description = ':x: Вы должны находиться в голосовом канале для вызова этой команды.', color = 0xdd2e44)
        await ctx.message.reply(embed = emb, delete_after = 3, mention_author = False)
        return
    voice = get_voice(ctx)
    if is_connected(ctx) and voice.is_playing():
        voice.stop()
        if loops.get(ctx.guild.id) == True and nowPlaying.get(ctx.guild.id) != None:
            nowPlaying[ctx.guild.id] = None
        emb = discord.Embed(description = f'<:phantom_ok:837302406060179516> Воспроизведение остановлено.', color = 0x000000)
        await ctx.send(embed = emb)
    else:
        emb = discord.Embed(description = ':x: Сейчас ничего не играет.', color = 0xdd2e44)
        await ctx.message.reply(embed = emb, delete_after = 2, mention_author = False)

@bot.command(aliases = ['loop', 'l'])
@commands.cooldown(1, 5, commands.BucketType.user)
async def repeat(ctx):
    if not ctx.author.voice:
        emb = discord.Embed(description = ':x: Вы должны находиться в голосовом канале для вызова этой команды.', color = 0xdd2e44)
        await ctx.message.reply(embed = emb, delete_after = 2, mention_author = False)
        return
    key = ctx.guild.id
    loops[key] = loops.get(key)
    if loops[key] == None:
        loops[key] = False
    if loops[key] == False:
        loops[key] = True
        emb = discord.Embed(description = '<:phantom_ok:837302406060179516> Воспроизведение зациклено.', color = 0x000000)
        await ctx.send(embed = emb)
        return
    if loops[key] == True:
        loops[key] = False
        emb = discord.Embed(description = '<:phantom_ok:837302406060179516> Стандартный режим воспроизведения.', color = 0x000000)
        await ctx.send(embed = emb)

@bot.command()
@commands.cooldown(1, 20, commands.BucketType.user)
async def ping(ctx, ip = None):
    def check(reaction,user):
        if reaction.message.id == lastmsg.id and reaction.emoji == '📌':
            return reaction
        else:
            return False
    if await is_overloaded(ctx):
        return
    if ip == None:
        emb = discord.Embed(description = ':x: Использование: `!!ping <ip>`', color = 0xdd2e44)
        await ctx.send(embed = emb)
        return
    async with ctx.typing():
        emb = get_status(ctx,ip)
    lastmsg = await ctx.send(embed = emb)
    await lastmsg.add_reaction('📌')
    try:
        await asyncio.sleep(1)
        reaction = await bot.wait_for('reaction_add', timeout = 30.0, check = check)
    except asyncio.TimeoutError as error:
        await lastmsg.remove_reaction('📌', bot.user)
        pass
        return
    emb = discord.Embed(description = '<:phantom_ok:837302406060179516> Закреплено! Каждые 5 минут информация о сервере будет обновляться.', color = 0x000000)
    await ctx.send(embed = emb, delete_after = 4)
    while True:
        emb = get_status(ctx,ip)
        await asyncio.sleep(300)
        try:
            await lastmsg.edit(embed = emb)
        except:
            break

@bot.command(aliases = ['2b2t', '2b'])
@commands.cooldown(1, 20, commands.BucketType.user)
async def twobuilderstwotools(ctx):
    if await is_overloaded(ctx):
        return
    e = discord.Embed(description = '<:phantom_dl:851384026719322122> Получние данных из [API-1](https://2b2t.io)...', color = 0x000000)
    msg = await ctx.send(embed = e)
    x = requests.get('https://www.2b2t.io/api/queue?last=true')
    q = int(x.text.split(',')[1].replace(']',''))
    e = discord.Embed(description = '<:phantom_dl:851384026719322122> Получние данных из [API-2](https://2b2t.dev)...', color = 0x000000)
    await msg.edit(embed = e)
    p = requests.get('https://api.2b2t.dev/prioq')
    e = discord.Embed(description = '<:phantom_dl:851384026719322122> Получние данных из [API-3](https://mc.api.srvcontrol.xyz)...', color = 0x000000)
    await msg.edit(embed = e)
    pq = int(p.text.split(',')[1].replace(',null]',''))
    url = f'https://mc.api.srvcontrol.xyz/server/status?ip=2b2t.org'
    with urllib.request.urlopen(url) as data:
        status = json.loads(data.read().decode())
        await msg.delete()
    if status['online'] == False or status['error']:
        e = discord.Embed(description = ':x: Не удалось установить соединение с сервером.', color = 0xdd2e44)
        await ctx.send(embed = e, delete_after=3)
    online = status['players']['now']
    ingame = online - int(q)
    m = f'В очереди: {q}.\nВ приоритетной очереди: {pq}.\nНа сервере: {ingame}.\nОбщий онлайн: {online}.'
    e = discord.Embed(title='2b2t', description=m, color = 0x000000)
    e.set_thumbnail(url = f'https://eu.mc-api.net/v3/server/favicon/2b2t.org')
    await ctx.send(embed = e)

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
        emb = discord.Embed(description = f':x: Использование: `!!nsfw [tag]`\nДоступные теги: {tags}', color = 0xdd2e44)
        await ctx.message.reply(embed = emb, delete_after = 8, mention_author = False)
        return
    link = nekos.img(req)
    emb = discord.Embed(color = 0x000000)
    emb.set_image(url = link)
    await ctx.send(embed = emb)

@bot.command()
@commands.is_owner()
async def shutdown(ctx):
    await ctx.message.add_reaction('✅')
    exit()
    
@bot.command(aliases = ['restart', 'reload'])
@commands.is_owner()
@commands.cooldown(1, 15, commands.BucketType.user)
async def do_restart(ctx):
    await ctx.message.add_reaction('✅')
    os.system('python core.py')
    exit()

print('Регистрация ивентов...')

async def is_overloaded(ctx):
    if ctx.author.id == 811976103673593856:
        return False
    if psutil.cpu_percent() >= 98 or psutil.virtual_memory().percent >= 89:
        emb = discord.Embed(description = ':x: Эта команда недоступна, так как бот в данный момент перегружен.', color = 0xdd2e44)
        await ctx.message.reply(embed = emb, delete_after = 4, mention_author = False)
        return True
    else:
        return False

def get_voice(ctx):
    voice = discord.utils.get(ctx.bot.voice_clients, guild = ctx.guild)
    return voice

def get_status(ctx, ip):
    url = f'https://mc.api.srvcontrol.xyz/server/status?ip={ip}'
    with urllib.request.urlopen(url) as data:
        status = json.loads(data.read().decode())
        if status['online'] == True and not status['error']:
            online = status['players']['now']
            max = status['players']['max']
            status['players']['now']
            core = status['server']['name']
            motd = status['motd']
            cc = ['§1', '§2', '§3', '§4', '§5', '§6', '§7', '§8', '§9', '§0', '§a', '§b', '§c', '§d', '§e', '§f', '§m', '§n', '§l', '§k', '§r', '§o']
            for i in cc:
                motd = motd.replace(i, '')
                core = core.replace(i, '')
            emb = discord.Embed(title = f'Информация о сервере {ip}', description = f'```{motd}```', color = 0x000000)
            emb.add_field(name = 'Игроков онлайн', value = f'{online}/{max}', inline = True)
            emb.add_field(name = 'Ядро', value = core, inline = True)
            emb.set_thumbnail(url = f'https://eu.mc-api.net/v3/server/favicon/{ip}')
            return emb
        else:
            emb = discord.Embed(description = ':x: Не удалось установить соединение с сервером.', color = 0xdd2e44)
            return emb

def is_connected(ctx):
    voice_client = discord.utils.get(ctx.bot.voice_clients, guild=ctx.guild)
    return voice_client and voice_client.is_connected()

async def permerror(ctx):
    emb = discord.Embed(description = ':x: У меня нет прав для выполнения этой команды.', color = 0xdd2e44)
    await ctx.message.reply(embed = emb, delete_after = 3, mention_author = False)

def get_channel(ctx, channel):
    if isinstance(channel, discord.VoiceChannel):
        return channel
    if isinstance(channel, discord.StageChannel):
        return channel
    _channel = discord.utils.get(ctx.guild.voice_channels, name=channel)
    if _channel:
        return _channel
    _channel = discord.utils.get(ctx.guild.voice_channels, id=channel)
    if _channel:
        return _channel
    _channel = discord.utils.get(ctx.guild.stage_channels, name=channel)
    if _channel:
        return _channel
    _channel = discord.utils.get(ctx.guild.stage_channels, id=channel)
    if _channel:
        return _channel
    try:
        _channel = str(channel).split('<#')[1].split('>')[0]
    except:
        return False
    _channel = discord.utils.get(ctx.guild.voice_channels, id=_channel)
    if _channel:
        return _channel
    return False

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        return
    print(error)
    if isinstance(error, commands.MissingPermissions):
        emb = discord.Embed(description = ':x: У вас нет прав для вызова этой команды.', color = 0xdd2e44)
        await ctx.message.reply(embed = emb, delete_after = 2, mention_author = False)
        return
    if isinstance(error, commands.MissingRequiredArgument):
        emb = discord.Embed(description = ':x: Неправильный синтаксис команды.', color = 0xdd2e44)
        await ctx.message.reply(embed = emb, delete_after = 2, mention_author = False)
        return
    if isinstance(error, commands.CommandOnCooldown):
        cooldown = round(error.retry_after)
        emb = discord.Embed(description = f':x: Вы сможете использовать эту команду через {cooldown} секунд.', color = 0xdd2e44)
        await ctx.message.reply(embed = emb, delete_after = 2, mention_author = False)
        return
    if isinstance(error, commands.errors.NSFWChannelRequired):
        emb = discord.Embed(description = ':x: Эта команда может быть выполнена только в NSFW канале.', color = 0xdd2e44)
        await ctx.message.reply(embed = emb, delete_after = 3, mention_author = False)
        return
    if isinstance(error, commands.errors.MemberNotFound):
        emb = discord.Embed(description = ':x: Пользователь не найден.', color = 0xdd2e44)
        await ctx.message.reply(embed = emb, delete_after = 2, mention_author = False)
        return
    if isinstance(error, commands.errors.ChannelNotFound):
        emb = discord.Embed(description = ':x: Канал не найден.', color = 0xdd2e44)
        await ctx.message.reply(embed = emb, delete_after = 2, mention_author = False)
        return
    if isinstance(ctx.channel, discord.DMChannel):
        emb = discord.Embed(description = ':x: Выполение этой команды в личных сообщениях невозможно.', color = 0xdd2e44)
        await ctx.message.reply(embed = emb, delete_after = 2, mention_author = False)
        return
    if isinstance(error, commands.CommandInvokeError):
        emb = discord.Embed(description = f':x: Произошла ошибка.\n```{str(error).split("exception: ")[1]}```', color = 0xdd2e44)
        await ctx.message.reply(embed = emb, delete_after = 8, mention_author = False)
        return

def cts(s):
    UNITS = {'s':'seconds', 'm':'minutes', 'h':'hours', 'd':'days'}
    return int(datetime.timedelta(**{
        UNITS.get(m.group('unit').lower(), 'seconds'): int(m.group('val'))
        for m in re.finditer(r'(?P<val>\d+)(?P<unit>[smhd]?)', s, flags=re.I)
        }).total_seconds())

@bot.event
async def on_message(message):
    if not message.author.bot:
        await bot.process_commands(message)

@bot.event
async def on_ready():
    print('Загрузка завершена!')
    while True:
        s = f'!!help | [{len(bot.guilds)}]'
        await bot.change_presence(activity = discord.Streaming(name = s, url = "https://www.youtube.com/watch?v=wq0OaK6dMEo"))
        time = re.sub("\.[0-9][0-9][0-9].*", "", str(datetime.datetime.now().time()))
        print(f'[{time}] Я на {len(bot.guilds)} серверах. CPU: {psutil.cpu_percent()}% RAM: {psutil.virtual_memory().percent}%')
        await asyncio.sleep(300)

print('Выполняется вход...')
bot.run(config.token())
