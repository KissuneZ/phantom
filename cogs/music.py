import discord
from discord.ext import commands
from discord import FFmpegPCMAudio
import urllib
from urllib import parse
from urllib import request
from urllib.request import urlopen
import asyncio
from requests import get
import datetime
import requests
import youtube_dl
import re
import json

loops = {}
nowPlaying = {}
__bopts__ = '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 10'
FFMPEG_OPTIONS = {'before_options': __bopts__,
				  'options': '-vn'}
__data__ = requests.get("https://espradio.ru/stream_list.json")
list = __data__.text
ydl_opts = {'format': 'worstaudio'}


class Music(commands.Cog):
	def __init__(self, bot):
		self.bot = bot

	@commands.command(aliases=['summon'])
	async def join(self, ctx, *, channel=None):
		channel = gc(ctx, channel)
		if channel == 1:
			return await error(ctx, 'Канал не найден.')
		elif channel == 2:
			return await error(ctx, 'Вы должны быть в голосовом канале для вызова этой комнды.')
		e = False
		voice = discord.utils.get(ctx.bot.voice_clients, guild=ctx.guild)
		msg = f'Подключен к голосовому каналу.'
		if voice:
			vc = ctx.message.guild.voice_client
			try:
				await vc.move_to(channel)
			except:
				msg = 'Не удалось подключиться к голосовому каналу.'
				e = True
		else:
			try:
				await channel.connect(timeout=1, reconnect=True)
			except:
				msg = 'Не удалось подключиться к голосовому каналу.'
				e = True
		if e:
			return await error(ctx, msg)
		await rts(ctx)
		await success(ctx, msg)

	@commands.command()
	async def leave(self, ctx):
		if await voice_check(ctx):
			return
		voice = get_voice(ctx)
		nowPlaying[ctx.guild.id] = None
		await voice.disconnect()
		await success(ctx, 'Отключен от голосового канала.')

	@commands.command(aliases=['p'])
	async def play(self, ctx, *, query):
		if await voice_check(ctx, ignore_not_connected=True):
			return
		_query = query.replace("`", "`‎")
		e = discord.Embed(description=f"""Выполняется поиск на YouTube:
```{_query}```""")
		msg = await ctx.send(embed=e)
		async with ctx.typing():
			results = ytsearch(query)
		try:
			url = f'https://youtu.be/{results[0]}'
		except:
			await msg.delete()
			return await error(ctx, 'По вашему запросу ничего не найдено.')
		channel = ctx.author.voice.channel
		voice = get_voice(ctx)
		if is_connected(ctx):
			player = voice
		else:
			try:
				player = await channel.connect(timeout=1, reconnect=True)
			except:
				return await error(ctx, f'Не удалось подключиться к голосовому каналу.')
		await rts(ctx)
		async with ctx.typing():
			ydl = youtube_dl.YoutubeDL(ydl_opts)
			ydl.add_default_info_extractors()
			with ydl:
				info = ydl.extract_info(url, download=False)
				source_url = info['formats'][0]['url']
				title = info.get('title', None)
				duration = info.get('duration', None)
			dur = duration
			key = ctx.guild.id
			if nowPlaying.get(key) != url:
				nowPlaying[key] = url
			duration = datetime.timedelta(seconds=duration)
		i = True
		while loops.get(key) or i:
			voicestop(voice)
			player.play(FFmpegPCMAudio(source_url, **FFMPEG_OPTIONS))
			if i:
				title = title.replace("`", "`‎")
				await msg.delete()
				await success(ctx, f'Воспроизведение:\n```{title} ({duration})```\nСсылка на видео: {url}')
				i = False
			await asyncio.sleep(dur + 1)
			if nowPlaying.get(key) != url or not is_connected(ctx):
				break
		nowPlaying[key] = None

	@commands.command(aliases=['skip'])
	async def stop(self, ctx):
		if await voice_check(ctx):
			return
		voice = get_voice(ctx)
		key = ctx.guild.id
		if nowPlaying.get(key):
			voice.stop()
			nowPlaying[key] = None
			await success(ctx, 'Воспроизведение остановлено.')
		else:
			await error(ctx, 'Сейчас ничего не играет.')

	@commands.command()
	async def pause(self, ctx):
		if await voice_check(ctx):
			return
		voice = get_voice(ctx)
		try:
			voice.pause()
			await success(ctx, 'Воспроизведение приостановлено.')
		except:
			await error(ctx, 'Сейчас ничего не играет.')

	@commands.command()
	async def resume(self, ctx):
		if await voice_check(ctx):
			return
		voice = get_voice(ctx)
		try:
			voice.resume()
			await success(ctx, 'Воспроизведение продолжено.')
		except:
			await error(ctx, 'Воспроизведение не было приостановлено.')

	@commands.command(aliases=['repeat'])
	async def loop(self, ctx):
		if await voice_check(ctx):
			return
		key = ctx.guild.id
		state = loops.get(key)
		if state:
			loops[key] = False
			return await success(ctx, 'Стандартный режим воспроизведения.')
		else:
			loops[key] = True
			await success(ctx, 'Воспроизведение зациклено.')

	@commands.command()
	async def radio(self, ctx, url):
		if not re.findall(f"\"url\":\"{url}\"", list):
			return await error(ctx, 'Использование: `!!radio <url>`\nСписок станций: https://espradio.ru/stream_list')
		if await voice_check(ctx, ignore_not_connected=True):
			return
		voice = get_voice(ctx)
		key = ctx.guild.id
		if nowPlaying.get(key) != url:
			nowPlaying[key] = url
		if ctx.message.author.voice:
			channel = ctx.author.voice.channel
			if is_connected(ctx):
				player = voice
				voicestop(player)
			else:
				try:
					player = await channel.connect(timeout=1, reconnect=True) 
				except:
					return await error(ctx, 'Не удалось подключиться к голосовому каналу.')
		await rts(ctx)
		name = re.findall(f"\"name\":\".*\",\"url\":\"{url}\"", list)[0].split(":\"")[1].split('\",')[0]
		await success(ctx, f'Воспроизведение:\n```{name}```\nСсылка на радиостанцию: {url}')
		player.play(FFmpegPCMAudio(url, **FFMPEG_OPTIONS))

	@commands.command(aliases=['np', 'nowplaying'])
	async def now(self, ctx):
		url = nowPlaying.get(ctx.guild.id)
		if not url or not is_connected(ctx):
			return await error(ctx, 'Сейчас ничего не играет.')
		if "youtu.be" not in url:
			async with ctx.typing():
				name = re.findall(f"\"name\":\".*\",\"url\":\"{url}\"", list)[0].split(":\"")[1].split('\",')[0]
				e = discord.Embed(description=f'\📻 Сейчас играет:```{name}```\nСсылка на радиостанцию: {url}')
			return await ctx.send(embed=e)
		async with ctx.typing():
			ydl = youtube_dl.YoutubeDL(ydl_opts)
			ydl.add_default_info_extractors()
			with ydl:
				info = ydl.extract_info(url, download=False)
				title = info.get('title', None)
				duration = info.get('duration', None)
				thumbnail = info.get('thumbnail', None)
				likes = info.get('like_count', None)
				views = info.get('view_count', None)
			duration = datetime.timedelta(seconds=duration)
		e = discord.Embed(description=f'<:youtube:861493156876386324> Сейчас играет:\n```{title.replace("`", "`‎")} ({duration})```\nСсылка на видео: {url}')
		e.set_image(url=thumbnail)
		e.set_footer(text=f"Просмотров: {views}. Лайков: {likes}.")
		await ctx.send(embed=e)


def setup(bot):
	bot.add_cog(Music(bot))


def voicestop(voice):
	try:
		if voice.is_playing():
			voice.stop()
	except:
		pass


async def success(ctx, message, delete_after=None, image=None):
	e = discord.Embed(description='<a:success:860037468279406592> ' + message)
	if image:
		e.set_thumbnail(url=image)
	await ctx.send(embed=e, delete_after=delete_after)


async def error(ctx, message):
	e = discord.Embed(description='<a:error:862306041546407936> ' + message)
	return await ctx.send(embed=e)


def is_connected(ctx):
	voice_client = discord.utils.get(ctx.bot.voice_clients, guild=ctx.guild)
	return voice_client and voice_client.is_connected()


def get_voice(ctx):
	voice = discord.utils.get(ctx.bot.voice_clients, guild=ctx.guild)
	return voice


def gc(ctx, channel):
	if channel:
		channel = get_channel(ctx, channel)
		if channel:
			return channel
		channel = 1
	else:
		channel = ctx.author.voice.channel
		if channel:
			return channel
		channel = 2
	return channel


async def rts(ctx):
	try:
		await ctx.guild.me.edit(suppress=False)
	except:
		pass


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


def ytsearch(query):
	q = urllib.parse.urlencode({'search_query': query})
	html = urlopen(f'https://www.youtube.com/results?{q}')
	return re.findall(r'/watch\?v=(.{11})', html.read().decode())


async def voice_check(ctx, ignore_not_connected=False):
	if not ctx.author.voice:
		return await error(ctx, 'Вы должны быть в голосовом канале для вызова этой команды.')
	if not ctx.guild.me.voice and not ignore_not_connected:
		return await error(ctx, 'Я не подключен к голосовому каналу на этом сервере.')
	if not is_connected(ctx):
		return
	if ctx.author.voice.channel != ctx.guild.me.voice.channel:
		return await error(ctx, 'Вы должны находиться в том же голосовом канале, что и бот.')
