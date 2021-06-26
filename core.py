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
print('    + Reqest')
import asyncio
print(' + AsyncIO')
import requests
print(' + Requests')
import datetime
print(' + DateTime')
print('Загрузка YouTubeDL...')
import youtube_dl
print('Успешно!')
print('Инициализация...')

import json
import re
import os
import io
import time
import psutil
import nekos

import config

global loops, nullTime, nowPlaying
nullTime = time.time()
loops = {}
nowPlaying = {}
bot = commands.Bot('!!')
bot.remove_command('help')
print('Регистрация асинхронных команд...')

@bot.command()
@commands.cooldown(1, 5, commands.BucketType.user)
async def help(ctx, page = 0):
    if ctx.message.author.bot:
        return
    if page == 0 or page > 4:
        default = '`1.` Модерация\n`2.` Музыка\n`3.` Утилиты\n`4.` Прочее\n\nИспользуйте `!!help [page]` для просмотра списка команд из этой категории.'
        emb = discord.Embed(color = 0x000000)
        emb.add_field(name = 'Доступные категории команд', value = default)
        emb.set_footer(text = '© 2021 Sweety187 | Все права защищены.', icon_url = 'https://media.discordapp.net/attachments/832662675963510827/855762014010081300/b5222c5b.jpg')
        emb.set_thumbnail(url = "https://media.discordapp.net/attachments/832662675963510827/857632646045499443/bcb453631de553497b809cdc83a0e5ca.png")
        await ctx.send(embed = emb)
        return
    mod = '`!!kick <member>` - кикнуть пользователя\n`!!ban <member>` - забанить пользователя\n`!!unban <member>` - разбанить пользователя\n`!!mute <member> [time]` - замутить пользователя\n`!!unmute <member>` - размутить пользователя\n`!!clear <amount>` - удалить последние N сообщений в канале'
    music = '`!!join [channel]` - присоединиться к голосовому каналу\n`!!leave` - покуинуть голосовой канал\n`!!play <query>` - воспроизвести музыку с YouTube\n`!!radio <stream>` - проигрывать радио в голосовом канале\n`!!stop` - остановить воспроизведение\n`!!pause` - приостановить воспроизведение\n`!!resume` - продолжить воспроизведение\n`!!repeat` - зациклить воспроизведение\n`!!now` - узнать, что сейчас играет'
    utils = '`!!avatar [member]` - вывести аватар пользователя\n`!!yt <query>` - найти видео на YouTube\n`!!ping <ip>` - выводит информацию о сервере Minecraft\n`!!2b2t` - выводит данные о сервере 2b2t (очередь и т.п.)\n`!!say <text>` - отправить сообщение от имени бота\n`!!embed <text>` - отправить ваш текст внутри Embed\'а\n`!!timer <time>` - поставить таймер'
    misc = '`!!status` - статистика бота\n`!!neko` - случайная картинка с неко\n`!!cat` - случайная картинка с котом\n`!!nsfw [tag]` - хентай-картинка с указанным тегом (по умолчанию «lewd»)\n`!!invite` - добавить меня на свой сервер'
    pages = [mod, music, utils, misc]
    titles = ['`1.` Модерация','`2.` Музыка','`3.` Утилиты','`4.` Прочее']
    emb = discord.Embed(color = 0x000000)
    emb.add_field(name = titles[page - 1], value = pages[page - 1])
    emb.set_footer(text = '© 2021 Sweety187 | Все права защищены.', icon_url = 'https://media.discordapp.net/attachments/832662675963510827/855762014010081300/b5222c5b.jpg')
    await ctx.send(embed = emb)

@bot.command()
@commands.cooldown(1, 10, commands.BucketType.user)
async def status(ctx):
    global nullTime
    t = int(time.time() - nullTime)
    t = datetime.timedelta(seconds=t)
    e = discord.Embed(title="Статистика бота", color = 0x000000)
    e.add_field(name = 'Аптайм', value = t, inline = True)
    e.add_field(name = 'Версия', value = 'b_9.9.7', inline = True)
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
    emb = discord.Embed(description = '<:phantom_ii:857628296745320528> Добавить бота на свой сервер: [https://discord.com/api/oauth2/authorize](https://discord.com/api/oauth2/authorize?client_id=837282453654732810&permissions=305491206&scope=bot)', color = 0x000000)
    await ctx.send(embed = emb)

@bot.command()
@commands.has_permissions(manage_messages = True)
@commands.cooldown(1, 10, commands.BucketType.user)
async def mute(ctx, member: discord.Member, time = ''):
    if ctx.message.author.bot:
        return
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
    emb = discord.Embed(description = f'<:phantom_ok:837302406060179516> {member.mention} замучен на `{t}` минут.', color = 0x000000)
    try:
        await member.add_roles(muterole)
    except:
        await permerror(ctx)
        return
    if time == None:
        emb = discord.Embed(description = f'<:phantom_ok:837302406060179516> {member.mention} замучен навсегда.', color = 0x000000)
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
    if ctx.message.author.bot:
        return
    muterole = discord.utils.get(ctx.guild.roles,name='Muted')
    emb = discord.Embed(description = '<:phantom_ok:837302406060179516> '+member.mention+' размучен.',color=0x000000)
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
    if ctx.message.author.bot:
        return
    if member == ctx.author:
        emb = discord.Embed(description = ':x: Вы не можете наказать самого себя.', color = 0xdd2e44)
        await ctx.send(embed = emb, delete_after = 2)
        return
    emb = discord.Embed(description = '<:phantom_ok:837302406060179516> '+member.mention+' кикнут.', color = 0x000000)
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
    if ctx.message.author.bot:
        return
    if member == ctx.author:
        emb = discord.Embed(description = ':x: Вы не можете наказать самого себя.', color = 0xdd2e44)
        await ctx.send(embed = emb, delete_after = 2)
        return
    emb = discord.Embed(description = '<:phantom_ok:837302406060179516> '+member.mention+' забанен.', color = 0x000000)
    try:
        await member.ban()
    except:
        await permerror(ctx)
        return
    await ctx.send(embed = emb)

@bot.command()
@commands.has_permissions(ban_members = True)
@commands.cooldown(1, 10, commands.BucketType.user)
async def unban(ctx, member: discord.Member):
    if ctx.message.author.bot:
        return
    try:
        await member.unban()
    except:
        await permerror(ctx)
        return
    emb = discord.Embed(description = '<:phantom_ok:837302406060179516> '+member.mention+' разбанен.', color  = 0x000000)
    await ctx.send(embed = emb)

@bot.command(aliases=['purge'])
@commands.has_permissions(manage_messages = True)
@commands.cooldown(1, 30, commands.BucketType.user)
async def clear(ctx, amount):
    if ctx.message.author.bot:
        return
    if await is_overloaded(ctx):
        return
    try:
        amount = int(amount)
    except:
        emb = discord.Embed(description = f':x: Заданный аргумент не является числом.', color = 0xdd2e44)
        await ctx.send(embed = emb, delete_after = 2)
    if amount <= 100:
        try:
            deleted = await ctx.message.channel.purge(limit = amount + 1)
        except:
            await permerror(ctx)
            return
        emb = discord.Embed(description = f'<:phantom_ok:837302406060179516> Удалено `{len(deleted)}` сообщений.', color = 0x000000)
    else:
        emb = discord.Embed(description = f':x: Нельзя назначить более 100 сообщний для удаления.', color = 0xdd2e44)
    await ctx.send(embed = emb, delete_after = 2)

@bot.command()
@commands.cooldown(1, 10, commands.BucketType.user)
async def avatar(ctx, member: discord.Member = None):
    if ctx.message.author.bot:
        return
    if not member:
        member = ctx.message.author
    emb = discord.Embed(title = f'Аватар {member}', color = 0x000000)
    avatar = str(member.avatar_url)[:-10]+'?size=512&width=512&height=512'
    emb.set_image(url = avatar)
    await ctx.send(embed = emb)

@bot.command()
@commands.cooldown(1, 10, commands.BucketType.user)
async def join(ctx, channel: discord.VoiceChannel = None):
    e = False
    if ctx.message.author.bot:
        return
    if await is_overloaded(ctx):
        return
    if ctx.author.voice:
        if channel == None:
            channel = ctx.author.voice.channel
        else:
            pass
        voice = discord.utils.get(ctx.bot.voice_clients, guild=ctx.guild)
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
                await channel.connect(timeout = 1)
            except:
                emb = discord.Embed(description = ':x: Не удалось подключиться к голосовому каналу.', color = 0xdd2e44)
                e == True
    else:
        emb = discord.Embed(description = ':x: Вы должны находиться в голосовом канале для вызова этой команды.', color = 0xdd2e44)
        e = True
    m = await ctx.send(embed = emb)
    if e == True:
        await asyncio.sleep(3)
        await m.delete()

@bot.command()
@commands.cooldown(1, 10, commands.BucketType.user)
async def leave(ctx):
    if ctx.message.author.bot:
        return
    global loops
    if is_connected(ctx):
        vc = ctx.message.guild.voice_client
        if loops.get(ctx.guild.id) == True:
            loops[ctx.guild.id] = False
        await vc.disconnect()
        emb = discord.Embed(description = '<:phantom_ok:837302406060179516> Отключен от голосового канала.', color = 0x000000)
        await ctx.send(embed = emb)
    else:
        emb = discord.Embed(description = ':x: Я не подключен к голосовому каналу на этом сервере.', color = 0xdd2e44)
        await ctx.send(embed = emb, delete_after = 2)

@bot.command()
@commands.cooldown(1, 10, commands.BucketType.user)
async def say(ctx, *, text):
    if ctx.message.author.bot:
        return
    if re.search(".*@.*", str(text)):
        text = re.sub("@everyone", "<...>", text)
        text = re.sub("@here", "<...>", text)
        text = re.sub("<@.*>", "<...>", text)
    await ctx.send(text)

@bot.command()
@commands.cooldown(1, 10, commands.BucketType.user)
async def embed(ctx, *, text):
    if ctx.message.author.bot:
        return
    emb = discord.Embed(description = text, color = 0x000000)
    await ctx.send(embed = emb)

@bot.command()
@commands.cooldown(1, 15, commands.BucketType.user)
async def timer(ctx, time = ''):
    if ctx.message.author.bot:
        return
    try:
        time = cts(time)/60
    except:
        emb = discord.Embed(description = ':x: Некорректный формат времени.\nПример использования: `!!timer 5m`', color = 0xdd2e44)
        await ctx.send(embed = emb, delete_after = 2)
        return
    if time <= 0.005:
        emb = discord.Embed(description = ':x: Некорректный формат времени.', color = 0xdd2e44)
        await ctx.send(embed = emb, delete_after = 2)
        return
    if time > 60:
        emb = discord.Embed(description = ':x: Нельзя установить таймер больше чем на 60 минут.', color = 0xdd2e44)
        await ctx.send(embed = emb, delete_after = 2)
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
@commands.cooldown(1, 25, commands.BucketType.user)
async def radio(ctx, url = ''):
    if ctx.message.author.bot:
        return
    global loops, nowPlaying
    if await is_overloaded(ctx):
        return
    if not url:
        emb = discord.Embed(description = ':x: Использование: `!!radio <url>`\nСписок станций: https://espradio.ru/stream_list', color = 0xdd2e44)
        await ctx.send(embed = emb)
        return
    if not ctx.author.voice:
        emb = discord.Embed(description = ':x: Вы должны находиться в голосовом канале для вызова этой команды.', color = 0xdd2e44)
        await ctx.send(embed = emb, delete_after = 3)
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
                player = await channel.connect(timeout = 1) 
            except:
                emb = discord.Embed(description = ':x: Не удалось подключиться к голосовому каналу.', color = 0xdd2e44)
                await ctx.send(embed = emb, delete_after = 2)
                return
    player.play(FFmpegPCMAudio(url))
    emb = discord.Embed(description = f'<:phantom_ok:837302406060179516> Воспроизведение:\n```{url}```', color = 0x000000)
    await ctx.send(embed = emb)

@bot.command(aliases=['p'])
@commands.cooldown(1, 20, commands.BucketType.user)
async def play(ctx, *, query = ''):
    if ctx.message.author.bot:
        return
    if await is_overloaded(ctx):
        return
    global loops, nowPlaying
    if not query:
        emb = discord.Embed(description = ':x: Использование: `!!play <query>`', color = 0xdd2e44)
        m = await ctx.send(embed = emb, delete_after = 2)
        return
    if not ctx.author.voice:
        emb = discord.Embed(description = ':x: Вы должны находиться в голосовом канале для вызова этой команды.', color = 0xdd2e44)
        await ctx.send(embed = emb, delete_after = 2)
        return
    channel = ctx.author.voice.channel
    voice = get_voice(ctx)
    emb = discord.Embed(description = f'<:phantom_sr:851443028979613716> Выполняется поиск на YouTube:\n```{query}```', color = 0x000000)
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
        await ctx.send(embed = emb, delete_after = 2)
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
            player = await channel.connect(timeout = 1, reconnect = True)
        except:
            await lastmsg.delete()
            emb = discord.Embed(description = ':x: Не удалось подключиться к голосовому каналу.', color = 0xdd2e44)
            await ctx.send(embed = emb, delete_after = 2)
            return
    async with ctx.typing():
        ydl_opts = {'format': 'worstaudio'}
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            URL = info['formats'][0]['url']
            title = info.get('title', None)
            duration = info.get('duration', None)
        FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 10', 'options': '-vn'}
        d = duration
        if nowPlaying.get(ctx.guild.id) == None or nowPlaying.get(ctx.guild.id) != url:
            nowPlaying[ctx.guild.id] = url
        duration = datetime.timedelta(seconds = duration)
    await lastmsg.delete()
    emb = discord.Embed(description = f'<:phantom_ok:837302406060179516> Воспроизведение:\n```{title} ({duration})```\nСсылка на видео: {url}', color = 0x000000)
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
            await ctx.send(embed = emb)
        i = 0
        await asyncio.sleep(d+1)
        if nowPlaying.get(ctx.guild.id) != url:
            break
        player.stop()

@bot.command(aliases=['np', 'nowplaying'])
@commands.cooldown(1, 15, commands.BucketType.user)
async def now(ctx):
    if ctx.message.author.bot:
        return
    if await is_overloaded(ctx):
        return
    global nowPlaying
    url = nowPlaying.get(ctx.guild.id)
    if not url:
        emb = discord.Embed(description = ':x: Сейчас ничего не играет.', color = 0xdd2e44)
        await ctx.send(embed = emb, delete_after = 2)
        return
    if "youtu.be" not in url:
        async with ctx.typing():
            emb = discord.Embed(description = f'<:phantom_ii:857628296745320528> Сейчас играет:\n```{url}```', color = 0x000000)
            await ctx.send(embed = emb)
            return
    async with ctx.typing():
        ydl_opts = {'format': 'worstaudio'}
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            title = info.get('title', None)
            duration = info.get('duration', None)
        duration = datetime.timedelta(seconds = duration)
    emb = discord.Embed(description = f'<:phantom_ii:857628296745320528> Сейчас играет:\n```{title} ({duration})```\nСсылка на видео: {url}', color = 0x000000)
    await ctx.send(embed = emb)

@bot.command()
@commands.cooldown(1, 5, commands.BucketType.user)
async def pause(ctx):
    if ctx.message.author.bot:
        return
    if not ctx.author.voice:
        emb = discord.Embed(description = ':x: Вы должны находиться в голосовом канале для вызова этой команды.', color = 0xdd2e44)
        await ctx.send(embed = emb, delete_after = 2)
        return
    voice = discord.utils.get(ctx.bot.voice_clients, guild=ctx.guild)
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
    if ctx.message.author.bot:
        return
    if not ctx.author.voice:
        emb = discord.Embed(description = ':x: Вы должны находиться в голосовом канале для вызова этой команды.', color = 0xdd2e44)
        await ctx.send(embed = emb,delete_after = 2)
        return
    voice = discord.utils.get(ctx.bot.voice_clients, guild=ctx.guild)
    if await is_overloaded(ctx) and voice:
        voice.stop()
        return
    if voice.is_paused():
        voice.resume()
        emb = discord.Embed(color = 0x000000, description = '<:phantom_ok:837302406060179516> Воспроизведение продолжено.')
        await ctx.send(embed = emb)
    else:
        emb = discord.Embed(color = 0xdd2e44, description = ':x: Воспроизведение не было приостановлено.')
        await ctx.send(embed = emb, delete_after = 2)

@bot.command(aliases = ['youtube'])
@commands.cooldown(1, 20, commands.BucketType.user)
async def yt(ctx, *, query=''):
    if ctx.message.author.bot:
        return
    if await is_overloaded(ctx):
        return
    if not query:
        emb = discord.Embed(description = ':x: Использование: `!!yt <query>`', color = 0xdd2e44)
        await ctx.send(embed = emb,delete_after = 2)
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
        await ctx.send(embed = emb, delete_after = 2)

@bot.command(aliases = ['s','skip'])
@commands.cooldown(1, 5, commands.BucketType.user)
async def stop(ctx):
    if ctx.message.author.bot:
        return
    if not ctx.author.voice:
        emb = discord.Embed(description = ':x: Вы должны находиться в голосовом канале для вызова этой команды.', color = 0xdd2e44)
        await ctx.send(embed = emb, delete_after = 2)
        return
    voice = discord.utils.get(ctx.bot.voice_clients, guild=ctx.guild)
    if is_connected(ctx) and voice.is_playing():
        voice.stop()
        global loops, nowPlaying
        if loops.get(ctx.guild.id) == True and nowPlaying.get(ctx.guild.id) != None:
            nowPlaying[ctx.guild.id] = None
        emb = discord.Embed(description = f'<:phantom_ok:837302406060179516> Воспроизведение остановлено.', color = 0x000000)
        await ctx.send(embed = emb)
    else:
        emb = discord.Embed(description = ':x: Сейчас ничего не играет.', color = 0xdd2e44)
        await ctx.send(embed = emb, delete_after = 2)

@bot.command(aliases = ['loop','l'])
@commands.cooldown(1, 5, commands.BucketType.user)
async def repeat(ctx):
    if ctx.message.author.bot:
        return
    global loops
    if not ctx.author.voice:
        emb = discord.Embed(description = ':x: Вы должны находиться в голосовом канале для вызова этой команды.', color = 0xdd2e44)
        await ctx.send(embed = emb, delete_after = 2)
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
    if ctx.message.author.bot:
        return
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
    await ctx.send(embed = emb,delete_after = 4)
    while True:
        emb = get_status(ctx,ip)
        await asyncio.sleep(360)
        try:
            await lastmsg.edit(embed = emb)
        except:
            break
            
@bot.command(aliases = ['2b2t', '2b'])
@commands.cooldown(1, 20, commands.BucketType.user)
async def twobuilderstwotools(ctx):
    if ctx.message.author.bot:
        return
    if await is_overloaded(ctx):
        return
    e = discord.Embed(description = '<:phantom_dl:851384026719322122> Получние данных из [API-1](https://2b2t.io)...', color = 0x000000)
    msg = await ctx.send(embed = e)
    x = requests.get('https://www.2b2t.io/api/queue?last=true')
    q = int(x.text.split(',')[1].replace(']',''))
    await msg.delete()
    e = discord.Embed(description = '<:phantom_dl:851384026719322122> Получние данных из [API-2](https://2b2t.dev)...', color = 0x000000)
    msg1 = await ctx.send(embed = e)
    p = requests.get('https://api.2b2t.dev/prioq')
    await msg1.delete()
    e = discord.Embed(description = '<:phantom_dl:851384026719322122> Получние данных из [API-3](https://mc.api.srvcontrol.xyz)...', color = 0x000000)
    msg2 = await ctx.send(embed = e)
    pq = int(p.text.split(',')[1].replace(',null]',''))
    url = f'https://mc.api.srvcontrol.xyz/server/status?ip=2b2t.org'
    with urllib.request.urlopen(url) as data:
        status = json.loads(data.read().decode())
        await msg2.delete()
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
    if ctx.message.author.bot:
        return
    link = nekos.cat()
    emb = discord.Embed(color = 0x00000)
    emb.set_image(url = link)
    await ctx.send(embed = emb)

@bot.command()
@commands.cooldown(1, 5, commands.BucketType.user)
async def neko(ctx):
    if ctx.message.author.bot:
        return
    link = nekos.img('neko')
    emb = discord.Embed(color=0x000000)
    emb.set_image(url = link)
    await ctx.send(embed = emb)

@bot.command()
@commands.is_nsfw()
@commands.cooldown(1, 5, commands.BucketType.user)
async def nsfw(ctx, req='lewd'):
    if ctx.message.author.bot:
        return
    try:
        if req == 'neko':
            req = 'lewd'
        link = nekos.img(req)
    except:
        tags = '`anal` `bj` `blowjob` `boobs` `classic` `cum` `eroyuri` `feet` `femdom` `futanari` `haloero` `hentai` `hentaigif` `keta` `kuni` `lewd` `ngif` `pussy` `pwankg` `sex` `solo` `spank` `tits` `trap` `waifu` `yuri`'
        emb = discord.Embed(description=f':x: Использование: `!!nsfw [tag]`\nДоступные теги: {tags}',color=0xdd2e44)
        await ctx.send(embed = emb, delete_after = 8)
        return
    emb = discord.Embed(color=0x000000)
    emb.set_image(url = link)
    await ctx.send(embed = emb)

print('Регистрация ивентов...')

async def is_overloaded(ctx):
    if psutil.cpu_percent() >= 89 or psutil.virtual_memory().percent >= 89:
        emb = discord.Embed(description = ':x: Эта команда недоступна, так как бот в данный момент перегружен.', color = 0xdd2e44)
        await ctx.send(embed = emb, delete_after = 4)
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
            cc = ['§1','§2','§3','§4','§5','§6','§7','§8','§9','§0','§a','§b','§c','§d','§e','§f','§m','§n','§l','§k','§r']
            for i in cc:
                motd = motd.replace(i,'')
                core = core.replace(i,'')
            emb = discord.Embed(title=f'Информация о сервере {ip}',description=f'```{motd}```', color = 0x000000)
            emb.add_field(name='Игроков онлайн', value=f'{online}/{max}', inline=True)
            emb.add_field(name='Ядро', value=core, inline=True)
            emb.set_thumbnail(url=f'https://eu.mc-api.net/v3/server/favicon/{ip}')
            return emb
        else:
            emb = discord.Embed(description = ':x: Не удалось установить соединение с сервером.', color = 0xdd2e44)
            return emb

def is_connected(ctx):
    voice_client = discord.utils.get(ctx.bot.voice_clients, guild=ctx.guild)
    return voice_client and voice_client.is_connected()

async def permerror(ctx):
    emb = discord.Embed(description = ':x: У меня нет прав для выполнения этой команды.', color = 0xdd2e44)
    await ctx.send(embed = emb, delete_after = 2)

@bot.event
async def on_command_error(ctx,error):
    print(error)
    if isinstance(error, commands.CommandNotFound):
        pass
    if isinstance(error, commands.MissingPermissions):
        emb = discord.Embed(description = ':x: У вас нет прав для вызова этой команды.', color = 0xdd2e44)
        await ctx.send(embed = emb ,delete_after = 2)
        return
    if isinstance(error, commands.MissingRequiredArgument):
        emb = discord.Embed(description = ':x: Неправильный синтаксис команды.', color = 0xdd2e44)
        await ctx.send(embed = emb, delete_after = 2)
        return
    if isinstance(error, commands.CommandInvokeError):
        emb = discord.Embed(description = f':x: Произошла ошибка.\n```{error}```', color = 0xdd2e44)
        await ctx.send(embed = emb, delete_after = 2)
        return
    if isinstance(error, commands.CommandOnCooldown):
        cooldown = round(error.retry_after)
        emb = discord.Embed(description = f':x: Вы сможете использовать эту команду через {cooldown} секунд.', color = 0xdd2e44)
        await ctx.send(embed = emb, delete_after = 2)
        return
    if isinstance(error, commands.errors.NSFWChannelRequired):
        emb = discord.Embed(description = ':x: Эта команда может быть выполнена только в NSFW канале.', color = 0xdd2e44)
        await ctx.send(embed=emb, delete_after = 2)
        return
    if isinstance(error, commands.errors.MemberNotFound):
        emb = discord.Embed(description = ':x: Пользователь не найден.', color = 0xdd2e44)
        await ctx.send(embed=emb, delete_after = 2)
        return

def cts(s):
    seconds_per_unit = {"s": 1, "m": 60, "h": 3600, "d": 86400, "w": 604800}
    return int(s[:-1]) * seconds_per_unit[s[-1]]
    UNITS = {"s":"seconds", "m":"minutes", "h":"hours", "d":"days", "w":"weeks"}
    count = int(s[:-1])
    unit = UNITS[ s[-1] ]
    td = timedelta(**{unit: count})
    return td.seconds + 60 * 60 * 24 * td.days

@bot.event
async def on_message(message):
    if message.author.bot:
        return
    emb_content = f'{message.author.mention}, используйте `!!help` для вывода списка команд.'
    emb = discord.Embed(description=emb_content, color = 0x000000)
    if message.content == f'<@!{bot.user.id}>':
        await message.channel.send(embed=emb, delete_after = 2)
    await bot.process_commands(message)

@bot.event
async def on_ready():
    print('Загрузка завершена!')
    while True:
        s = f'!!help | [{len(bot.guilds)}]'
        await bot.change_presence(activity=discord.Streaming(name = s, url = "https://www.youtube.com/watch?v=wq0OaK6dMEo"))
        await asyncio.sleep(360)
        print(f'[HerokuAntiSleep] {time.time()}')

print('Выполняется вход...')
intents = discord.Intents.default()
intents.members = True
bot.run(config.token())
