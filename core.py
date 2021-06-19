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
import re
print(' + Re')
import asyncio
print(' + AsyncIO')
import requests
print(' + Requests')
import os
print(' + OS')
import io
print(' + IO')
import time
print(' + Time')
import datetime
print(' + DateTime')
import PIL
print(' + Pillow')
import json
print(' + Json')
print('Загрузка YouTubeDL...')
import youtube_dl
print('Успешно!')
print('Инициализация...')

global loops
loops = {}
bot = commands.Bot('!!')
bot.remove_command('help')
print('Регистрация асинхронных команд...')

@bot.command()
@commands.cooldown(1, 10, commands.BucketType.user)
async def help(ctx):
    if ctx.message.author.bot:
        return
    emb = discord.Embed(title='Доступные команды',description='`!!kick <member>` - кикнуть пользователя\n`!!ban <member>` - забанить пользователя\n`!!unban <member>` - разбанить пользователя\n`!!mute <member> <time [in minutes]>` - замутить пользователя\n`!!unmute <member>` - размутить пользователя\n`!!clear <amount>` - удалить последние X сообщений в текущем канале\n`!!avatar <member>` - вывести аватар пользователя\n`!!join` - присоединиться к голосовому каналу\n`!!leave` - покуинуть голосовой канал\n`!!play <query>` - воспроизвести музыку с YouTube\n`!!yt <query>` - найти видео на YouTube\n`!!radio <stream_url>` - проигрывать радио в голосовом канале\n`!!stop` - остановить воспроизведение\n`!!ping <ip>` - выводит информацию о сервере Minecraft\n`!!say <text>` - отправить сообщение от имени бота\n`!!embed <text>` - отправить текст как Embed',color=0x000000)
    emb.set_footer(text = '© 2021 Sweety187 | Все права защищены.',icon_url = 'https://images-ext-1.discordapp.net/external/tr8-aB33nhUsEseYHWn1lDJQAJ8F2X4dC4cKHAk46FU/%3Fsize%3D512/https/cdn.discordapp.com/avatars/811976103673593856/0943ab2a7d403226ee29703f3ce65d11.png')
    await ctx.message.delete()
    await ctx.send(embed = emb)

@bot.command()
@commands.has_permissions(view_audit_log=True)
@commands.cooldown(1, 10, commands.BucketType.user)
async def mute(ctx,member:discord.Member,time:float=0.0):
    if ctx.message.author.bot:
        return
    if not discord.utils.get(ctx.guild.roles,name='Muted'):
        me = bot.user
        guild = ctx.guild
        if ctx.guild.me.guild_permissions.manage_roles:
            perms = discord.Permissions()
            perms.update(send_messages = False, change_nickname=False, send_tts_messages=False, speak=False, request_to_speak=False)
            await guild.create_role(name="Muted")
            muterole = discord.utils.get(ctx.guild.roles,name='Muted')
            pos = ctx.guild.me.top_role.position - 1
            await muterole.edit(permissions=perms,position=pos)
    else:
        muterole = discord.utils.get(ctx.guild.roles,name='Muted')
        emb = discord.Embed(description=f'<:phantom_ok:837302406060179516> {member.mention} замучен на `{time}` мин.',color=0x000000)
        await ctx.message.delete()
        await member.add_roles(muterole)
        if time <= 0:
            emb = discord.Embed(description=f'<:phantom_ok:837302406060179516> {member.mention} замучен навсегда.',color=0x000000)
            await ctx.send(embed = emb)
        else:
            await ctx.send(embed = emb)
            await asyncio.sleep(time * 60)
            await member.remove_roles(muterole)

@bot.command()
@commands.has_permissions(view_audit_log=True)
@commands.cooldown(1, 10, commands.BucketType.user)
async def unmute(ctx,member:discord.Member):
    if ctx.message.author.bot:
        return
    muterole = discord.utils.get(ctx.guild.roles,name='Muted')
    emb = discord.Embed(description='<:phantom_ok:837302406060179516> '+member.mention+' размучен.',color=0x000000)
    await ctx.message.delete()
    await member.remove_roles(muterole)
    await ctx.send(embed = emb)

@bot.command()
@commands.has_permissions(kick_members=True)
@commands.cooldown(1, 10, commands.BucketType.user)
async def kick(ctx,member:discord.Member):
    if ctx.message.author.bot:
        return
    emb = discord.Embed(description='<:phantom_ok:837302406060179516> '+member.mention+' кикнут.',color=0x000000)
    await ctx.message.delete()
    await member.kick()
    await ctx.send(embed = emb)

@bot.command()
@commands.has_permissions(ban_members=True)
@commands.cooldown(1, 10, commands.BucketType.user)
async def ban(ctx,member:discord.Member):
    if ctx.message.author.bot:
        return
    emb = discord.Embed(description='<:phantom_ok:837302406060179516> '+member.mention+' забанен.',color=0x000000)
    await ctx.message.delete()
    await member.ban()
    await ctx.send(embed = emb)

@bot.command()
@commands.has_permissions(ban_members=True)
@commands.cooldown(1, 10, commands.BucketType.user)
async def unban(ctx,member:discord.Member):
    if ctx.message.author.bot:
        return
    emb = discord.Embed(description='<:phantom_ok:837302406060179516> '+member.mention+' разбанен.',color=0x000000)
    await ctx.message.delete()
    await member.unban()
    await ctx.send(embed = emb)

@bot.command()
@commands.has_permissions(manage_messages=True)
@commands.cooldown(1, 60, commands.BucketType.user)
async def clear(ctx,amount:int):
    if ctx.message.author.bot:
        return
    if amount <= 100:
        deleted = await ctx.message.channel.purge(limit=amount + 1)
        emb = discord.Embed(description=f'<:phantom_ok:837302406060179516> Очищено `{amount}` сообщений.',color=0x000000)
    else:
        emb = discord.Embed(description=f':x: Вы не можете назначить более 100 сообщний для удаления.',color=0xdd2e44)
    await ctx.send(embed = emb)

@bot.command()
@commands.cooldown(1, 10, commands.BucketType.user)
async def avatar(ctx,member:discord.Member=0):
    if ctx.message.author.bot:
        return
    if not member:
        member = ctx.message.author
    emb = discord.Embed(title=f'Аватар {member}',color=0x000000)
    avatar = str(member.avatar_url)[:-10]+'?size=512&width=512&height=512'
    emb.set_image(url = avatar)
    await ctx.message.delete()
    await ctx.send(embed = emb)

@bot.command()
@commands.cooldown(1, 10, commands.BucketType.user)
async def join(ctx):
    if ctx.message.author.bot:
        return
    if ctx.author.voice:
        channel = ctx.author.voice.channel
        voice = discord.utils.get(ctx.bot.voice_clients, guild=ctx.guild)
        emb = discord.Embed(description='<:phantom_ok:837302406060179516> Подключен к голосовому каналу.',color=0x000000)
        if voice:
            await voice.disconnect()
        try:
            await channel.connect(timeout=10)
        except:
            emb = discord.Embed(description=':x: Не удалось подключиться к голосовому каналу.',color=0xdd2e44)
            pass
    else:
        emb = discord.Embed(description=':x: Вы должны находиться в голосовом канале для вызова этой команды.',color=0xdd2e44)
    await ctx.message.delete()
    await ctx.send(embed = emb)

@bot.command()
@commands.cooldown(1, 10, commands.BucketType.user)
async def leave(ctx):
    if ctx.message.author.bot:
        return
    await ctx.message.delete()
    if is_connected(ctx):
        vc = ctx.message.guild.voice_client
        await vc.disconnect()
        emb = discord.Embed(description='<:phantom_ok:837302406060179516> Отключен от голосового канала.',color=0x000000)
        await ctx.send(embed = emb)
    else:
        emb = discord.Embed(description=':x: Я не подключен к голосовому каналу на этом сервере.',color=0xdd2e44)
        await ctx.send(embed = emb)

@bot.command()
@commands.cooldown(1, 10, commands.BucketType.user)
async def say(ctx,*,text):
    if ctx.message.author.bot:
        return
    await ctx.message.delete()
    await ctx.send(text)

@bot.command()
@commands.cooldown(1, 10, commands.BucketType.user)
async def embed(ctx,*,text):
    if ctx.message.author.bot:
        return
    emb = discord.Embed(description=text,color=0x000000)
    await ctx.message.delete()
    await ctx.send(embed = emb)

@bot.command()
@commands.cooldown(1, 15, commands.BucketType.user)
async def radio(ctx, url=''):
    if ctx.message.author.bot:
        return
    await ctx.message.delete()
    if not url:
        emb = discord.Embed(description=':x: Использование: `!!radio <stream_url>`\nСписок станций: https://espradio.ru/stream_list',color=0xdd2e44)
        await ctx.send(embed = emb)
        return
    if not ctx.author.voice:
        emb = discord.Embed(description=':x: Вы должны находиться в голосовом канале для вызова этой команды.',color=0xdd2e44)
        await ctx.send(embed = emb)
        return
    if ctx.message.author.voice:
        channel = ctx.author.voice.channel
        if is_connected(ctx):
            voice = discord.utils.get(ctx.bot.voice_clients, guild=ctx.guild)
            await voice.disconnect()
            try:
                player = await channel.connect(timeout=100)
            except:
                emb = discord.Embed(description=':x: Не удалось подключиться к голосовому каналу.',color=0xdd2e44)
                await ctx.send(embed = emb)
                return
        else:
            try:
                player = await channel.connect(timeout=100) 
            except:
                emb = discord.Embed(description=':x: Не удалось подключиться к голосовому каналу.',color=0xdd2e44)
                await ctx.send(embed = emb)
                return
    player.play(FFmpegPCMAudio(url))
    emb = discord.Embed(description=f'<:phantom_ok:837302406060179516> Воспроизведение:\n```{url}```',color=0x000000)
    await ctx.send(embed = emb)

@bot.command(pass_context=True, aliases=['p'])
@commands.cooldown(1, 30, commands.BucketType.user)
async def play(ctx, *, query=''):
    global loops
    if ctx.message.author.bot:
        return
    await ctx.message.delete()
    if not query:
        emb = discord.Embed(description=':x: Использование: `!!play <query>`',color=0xdd2e44)
        await ctx.send(embed = emb)
        return
    if not ctx.author.voice:
        emb = discord.Embed(description=':x: Вы должны находиться в голосовом канале для вызова этой команды.',color=0xdd2e44)
        await ctx.send(embed = emb)
        return
    channel = ctx.message.author.voice.channel
    if is_connected(ctx):
        await ctx.message.guild.voice_client.disconnect()
        await asyncio.sleep(1)
    try:
        player = await channel.connect(timeout=100) 
    except:
        print(e)
        emb = discord.Embed(description=':x: Не удалось подключиться к голосовому каналу.',color=0xdd2e44)
        await ctx.send(embed = emb)
        return
    emb = discord.Embed(description=f'<:phantom_sr:851443028979613716> Выполняется поиск на YouTube:\n```{query}```',color=0x000000)
    lastmsg = await ctx.send(embed = emb)
    query_string = urllib.parse.urlencode({'search_query': query})
    htm_content = urllib.request.urlopen('http://www.youtube.com/results?' + query_string)
    try:
        search_results = re.findall(r'/watch\?v=(.{11})', htm_content.read().decode())
        url = f'https://youtu.be/{search_results[0]}'
    except:
        pass
        emb = discord.Embed(description=':x: По вашему запросу ничего не найдено.',color=0xdd2e44)
        await ctx.send(embed = emb)
        return
    await lastmsg.add_reaction('✅')
    async with ctx.typing():
        ydl_opts = {'format': 'bestaudio'}
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            URL = info['formats'][0]['url']
            title = info.get('title', None)
            duration = info.get('duration', None)
            d = duration
            duration = datetime.timedelta(seconds=duration)
        FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}
    audio = discord.FFmpegPCMAudio(URL, **FFMPEG_OPTIONS)
    if loops.get(ctx.guild.id) == True:
        await rplay(ctx,audio,player,d)
        return
    player.play(discord.FFmpegPCMAudio(URL, **FFMPEG_OPTIONS)) 
    await lastmsg.delete()
    emb = discord.Embed(description=f'<:phantom_ok:837302406060179516> Воспроизведение:\n```{title} ({duration})```\nСсылка на видео: {url}',color=0x000000)
    await ctx.send(embed = emb) 
    
async def rplay(ctx,audio,player,duration):
    FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}
    while True:
        print(f'Repeating ({audio})')
        player.play(audio)
        await asyncio.sleep(duration)

@bot.command()
@commands.cooldown(1, 30, commands.BucketType.user)
async def yt(ctx, *, query=''):
    if ctx.message.author.bot:
        return
    await ctx.message.delete()
    if not query:
        emb = discord.Embed(description=':x: Использование: `!!yt <query>`',color=0xdd2e44)
        await ctx.send(embed = emb)
        return
    emb = discord.Embed(description=f'<:phantom_sr:851443028979613716> Выполняется поиск на YouTube:\n```{query}```',color=0x000000)
    lastmsg = await ctx.send(embed = emb)
    query_string = urllib.parse.urlencode({'search_query': query})
    async with ctx.typing():
        htm_content = urllib.request.urlopen('http://www.youtube.com/results?' + query_string)
        search_results = re.findall(r'/watch\?v=(.{11})', htm_content.read().decode())
    try:
        emb = f'`1.` https://youtu.be/{search_results[0]}\n`2.` https://youtu.be/{search_results[1]}\n`3.` https://youtu.be/{search_results[2]}'
        await lastmsg.delete()
        await ctx.send(embed = emb)
    except:
        emb = discord.Embed(description=':x: По вашему запросу ничего не найдено.',color=0xdd2e44)
        await ctx.send(embed = emb)

@bot.command()
@commands.cooldown(1, 10, commands.BucketType.user)
async def stop(ctx):
    if ctx.message.author.bot:
        return
    await ctx.message.delete()
    if not ctx.author.voice:
        emb = discord.Embed(description=':x: Вы должны находиться в голосовом канале для вызова этой команды.',color=0xdd2e44)
        await ctx.send(embed = emb)
        return
    channel = ctx.message.guild.voice_client.channel
    if is_connected(ctx):
        if channel == ctx.author.voice.channel:
            await ctx.message.guild.voice_client.disconnect()
            await asyncio.sleep(1)
            await channel.connect(reconnect=True,timeout=100)
            emb = discord.Embed(description=f'<:phantom_ok:837302406060179516> Воспроизведение остановлено.',color=0x000000)
            await ctx.send(embed = emb)
        else:
            emb = discord.Embed(description=':x: Вы должны находиться в том же голосовом канале, что и бот.',color=0xdd2e44)
            await ctx.send(embed = emb)

@bot.command()
@commands.cooldown(1, 10, commands.BucketType.user)
async def repeat(ctx):
    if ctx.message.author.bot:
        return
    global loops
    key = ctx.guild.id
    loops[key] = loops.get(key)
    if loops[key] == None:
        loops[key] = False
    if loops[key] == False:
        loops[key] = True
        await ctx.send(':x: Эта функция на данный момент в разработке')
        return
    if loops[key] == True:
        loops[key] = False
        await ctx.send(':x: Эта функция на данный момент в разработке')

@bot.command()
@commands.cooldown(1, 30, commands.BucketType.user)
async def ping(ctx,ip = None):
    def check(reaction,user):
        if reaction.message.id == lastmsg.id and reaction.emoji == '📌':
            return reaction
        else:
            return False
    if ctx.message.author.bot:
        return
    await ctx.message.delete()
    if ip == None:
        emb = discord.Embed(description=':x: Использование: `!!ping <ip>`',color=0xdd2e44)
        await ctx.send(embed = emb)
        return
    async with ctx.typing():
        emb = get_status(ctx,ip)
    lastmsg = await ctx.send(embed = emb)
    await lastmsg.add_reaction('📌')
    try:
        await asyncio.sleep(1)
        reaction = await bot.wait_for('reaction_add', timeout=30.0, check=check)
    except asyncio.TimeoutError as error:
        pass
        return
    emb = discord.Embed(description = '<:phantom_ok:837302406060179516> Закреплено! Каждые 5 минут информация о сервере будет обновляться.',color=0x000000)
    msg = await ctx.send(embed = emb)
    await asyncio.sleep(5)
    await msg.delete()
    while True:
        emb = get_status(ctx,ip)
        await asyncio.sleep(360)
        try:
            await lastmsg.edit(embed = emb)
        except:
            break

print('Регистрация ивентов...')

def get_status(ctx,ip):
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
            emb = discord.Embed(title=f'Информация о сервере {ip}',description=f'```{motd}```',color=0x000000)
            emb.add_field(name='Игроков онлайн', value=f'{online}/{max}', inline=True)
            emb.add_field(name='Ядро', value=core, inline=True)
            emb.set_thumbnail(url=f'https://eu.mc-api.net/v3/server/favicon/{ip}')
            return emb
        else:
            emb = discord.Embed(description=':x: Не удалось установить соединение с сервером.',color=0xdd2e44)
            return emb

def is_connected(ctx):
    voice_client = discord.utils.get(ctx.bot.voice_clients, guild=ctx.guild)
    return voice_client and voice_client.is_connected()
    
@bot.event
async def on_command_error(ctx,error):
    print(error)
    if isinstance(error,commands.CommandNotFound):
        pass
    if isinstance(error,commands.MissingPermissions):
        emb = discord.Embed(description=':x: У вас нет прав для вызова этой команды.',color=0xdd2e44)
        m = await ctx.send(embed = emb)
        await asyncio.sleep(3)
        await m.delete()
    if isinstance(error,commands.MissingRequiredArgument):
        emb = discord.Embed(description=':x: Неправильный синтаксис команды.',color=0xdd2e44)
        m = await ctx.send(embed = emb)
        await asyncio.sleep(3)
        await m.delete()
    if isinstance(error,commands.CommandInvokeError):
        emb = discord.Embed(description=f':x: Произошла ошибка:\n```{error}```',color=0xdd2e44)
        await ctx.send(embed = emb)
    if isinstance(error, commands.CommandOnCooldown):
        cooldown = round(error.retry_after)
        emb = discord.Embed(description=f':x: Вы сможете использовать эту команду через {cooldown} секунд.',color=0xdd2e44)
        m = await ctx.send(embed = emb)
        await asyncio.sleep(3)
        await m.delete()

@bot.event
async def on_message(message):
    emb_content = f'{message.author.mention}, используйте `!!help` для вывода списка команд.'
    emb = discord.Embed(description=emb_content,color=0x000000)
    if message.content == f'<@!{bot.user.id}>':
        await message.channel.send(embed=emb)
    await bot.process_commands(message)

@bot.event
async def on_ready():
    print('Загрузка завершена!')
    await bot.change_presence(status=discord.Status.dnd,activity=Activity(name='!!help',type=ActivityType.watching))
    while True:
        await asyncio.sleep(360)
        print(f'[AntiAFK] {time.time()}')

print('Выполняется вход...')
bot.run('ODM3MjgyNDUzNjU0NzMyODEw.YIqSDA.X_0k2aENwjIXWCssOPTKjwuCdHI')
