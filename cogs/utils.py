import discord
from discord.ext import commands
import re
import requests
import urllib
import json
import datetime
from datetime import timedelta
import asyncio
__skinopts__ = "&width=600&height=300&scale=4&overlay=true&theta=30"
__skinopts__ += "&phi=20&time=90&shadow_color=000&shadow_radius=0"
__skinopts__ += "&shadow_x=0&shadow_y=0&front_and_back=true"


class utils(commands.Cog):
	def __init__(self, bot):
		self.bot = bot

	@commands.command()
	async def avatar(self, ctx, member: discord.Member=None):
		if member == None:
			member = ctx.author
		e = discord.Embed(title=f"Аватар {member}")
		e.set_image(url=member.avatar_url)
		await ctx.send(embed=e)

	@commands.command()
	async def say(self, ctx, *, text):
		if re.search(".*@.*", str(text)):
			if not ctx.author.guild_permissions.mention_everyone:
				return await error(ctx, 'Ваше сообщение содержит упоминание.')
		await ctx.send(text)

	@commands.command()
	async def embed(self, ctx, *, text):
		e = discord.Embed(description=text)
		await ctx.send(embed=e)

	@commands.command(aliases=['youtube', 'video'])
	async def yt(self, ctx, *, query):
		e = discord.Embed(description=f'Выполняется поиск на YouTube:'
									  f'\n```{query}```')
		lastmsg = await ctx.send(embed=e)
		query = urllib.parse.urlencode({'search_query': query})
		async with ctx.typing():
			page = urllib.request.urlopen('http://www.youtube.com/results?' + query)
			results = re.findall(r'/watch\?v=(.{11})', page.read().decode())
		try:
			await ctx.send(f'''
`1.` https://youtu.be/{results[0]}
`2.` https://youtu.be/{results[1]}
`3.` https://youtu.be/{results[2]}''')
			await lastmsg.delete()
		except:
			await lastmsg.delete()
			await error(ctx, 'По вашему запросу ничего не найдено.')

	@commands.command(aliases=['mcserver'])
	async def ping(self, ctx, ip):
		async with ctx.typing():
			e = get_status(ip)
		await ctx.send(embed=e)

	@commands.command(name="2b2t", aliases=['2b'])
	async def _2b2t(self, ctx):
		e = discord.Embed(description='Пожалуйста, подождите...')
		msg = await ctx.send(embed=e)
		queue = requests.get('https://www.2b2t.io/api/queue?last=true')
		queue = int(queue.text.split(',')[1].replace(']', ''))
		prio = requests.get('https://api.2b2t.dev/prioq')
		prio = int(prio.text.split(',')[1].replace(',null]', ''))
		url = f'https://mc.api.srvcontrol.xyz/server/status?ip=2b2t.org'
		data = requests.get(url).text
		status = json.loads(data)
		await msg.delete()
		if not status['online'] or status['error']:
			await msg.delete()
			await error(ctx, 'Не удалось установить соединение с сервером.')
			return
		online = status['players']['now']
		ingame = online - int(queue)
		info = f'''В очереди: {queue}.
				   В приоритетной очереди: {prio}.
				   На сервере: {ingame}.
				   Общий онлайн: {online}.'''
		e = discord.Embed(title='2b2t', description=info)
		e.set_thumbnail(url=f'https://eu.mc-api.net/v3/server/favicon/2b2t.org')
		await ctx.send(embed=e)

	@commands.command()
	async def skin(self, ctx, nick):
		if len(re.findall("[^A-Za-z0-9_]", nick)):
			return await error(ctx, 'Заданный никнейм сдержит недопустимые символы.')
		url = f"https://ru.namemc.com/profile/{nick}.1"
		async with ctx.typing():
			guild = discord.utils.get(self.bot.guilds, id=832662675963510824)
			channel = discord.utils.get(guild.channels, id=859408699985887244)
			await channel.send(url)
			await asyncio.sleep(1)
			message = await channel.send(url)
		if "Поиск" in message.embeds[0].title:
			return await error(ctx, 'Лицензионного аккаунта с таким ником нет.')
		skin = message.embeds[0].thumbnail.url
		name = message.embeds[0].title.split(' | Учётная запись Minecraft')[0]
		skin = skin.split("&width=")[0] + __skinopts__
		e = discord.Embed(title=f"Скин {name}")
		e.set_image(url=skin)
		await ctx.send(embed=e)

	@commands.command(aliases=['guild', 'serverinfo'])
	async def server(self, ctx):
		async with ctx.typing():
			guild = ctx.guild
			name = guild.name
			icon = guild.icon_url
			created = str(guild.created_at).split('.')[0].replace('-', '.')
			owner = self.bot.get_user(guild.owner_id)
			members = guild.member_count
			categories = len(guild.categories)
			tchannels = len(guild.text_channels)
			vchannels = len(guild.voice_channels)
			roles = len(guild.roles)
			blevel = guild.premium_tier
			bcount = guild.premium_subscription_count
			region = str(guild.region).upper()
		e = discord.Embed()
		info = f"""```
ID сервера:			 {guild.id}
Дата создания:		  {created}
Владелец:			   {owner}
Участников:			 {members}
Категорий:			  {categories}
Текстовых каналов:	  {tchannels}
Голосовых каналов:	  {vchannels}
Ролей:				  {roles}
Уровень буста:		  {blevel}
Бустов:				 {bcount}
Регион:				 {region}
```"""
		e.add_field(name=name, value=info)
		e.set_thumbnail(url=icon)
		await ctx.send(embed=e)

	@commands.command(aliases=['userinfo'])
	async def user(self, ctx, user: discord.Member=None):
		if not user:
			user = ctx.author
		status = str(user.status)
		if status == 'dnd':
			status = 'Не беспокоить'
		elif status == 'idle':
			status = 'Неактивен'
		elif status == 'online':
			status = 'В сети'
		elif status == 'offline':
			status = 'Не в сети'
		activity = user.activity
		info = f"""```
Пользователь:		{str(user).replace("`", "")}
ID:				  {user.id}
Статус:			  {status}
Активность:		  {activity if activity else 'Нет'}
Бот:				 {"Да" if user.bot else "Нет"}
Роль:				{str(user.top_role).replace("`", "")}
Ролей:			   {len(user.roles)-1}
Зарегистрирован:	 {user.created_at.strftime("%d.%m.%Y %H:%M:%S")}
Присоединился:	   {user.joined_at.strftime("%d.%m.%Y %H:%M:%S")}
```"""
		e = discord.Embed(title=user, description=info)
		e.set_thumbnail(url=user.avatar_url)
		await ctx.send(embed=e)

	@commands.command()
	async def timer(self, ctx, time):
		try:
			_time = time
			time = cts(time)
		except:
			await error(ctx, f'Некорректный формат времени.'
							 f'\nПример использования: `!!timer 5m`')
			return
		if time <= 0:
			return await error(ctx, 'Некорректный формат времени.')
		if time > 60:
			return await error(ctx, 'Нельзя установить таймер больше чем на 60 минут.')
		_time = ctts(_time)
		await success(ctx, f'Установлен таймер на {_time}.')
		await asyncio.sleep(time)
		msg = await ctx.send(ctx.author.mention)
		await msg.delete()
		await success(ctx, f'Таймер сработал, прошло {_time}.')


def setup(bot):
	bot.add_cog(utils(bot))


async def success(ctx, message, delete_after=None, image=None):
	e = discord.Embed(description='<a:success:860037468279406592> ' + message)
	if image:
		e.set_thumbnail(url=image)
	await ctx.send(embed=e, delete_after=delete_after)


async def error(ctx, message):
	e = discord.Embed(description='<a:error:862306041546407936> ' + message)
	await ctx.send(embed=e)


def get_status(ip):
	url = f'https://mc.api.srvcontrol.xyz/server/status?ip={ip}'
	data = requests.get(url).text
	status = json.loads(data)
	if status['online'] and not status['error']:
		online = status['players']['now']
		max = status['players']['max']
		status['players']['now']
		core = status['server']['name']
		motd = status['motd']
		color_codes = ['§1', '§2', '§3', '§4', '§5', '§6', '§7', '§8',
					   '§9', '§0', '§a', '§b', '§c', '§d', '§e', '§f',
					   '§m', '§n', '§l', '§k', '§r', '§o']
		for i in color_codes:
			motd = motd.replace(i, '')
			core = core.replace(i, '')
		e = discord.Embed(title=f'Информация о сервере {ip}', description=f'```{motd}```')
		e.add_field(name='Игроков онлайн', value=f'{online}/{max}', inline=True)
		e.add_field(name='Ядро', value=core, inline=True)
		e.set_thumbnail(url=f'https://eu.mc-api.net/v3/server/favicon/{ip}')
		return e
	else:
		e = discord.Embed(description='<a:error:862306041546407936> Не удалось установить соединение с сервером.')
		return e

def ctts(time):
	try:
		time = str(int(time)) + ' секунд'
	except:
		pass
	if isinstance(time, str):
		time = time.replace('s', ' секунд ')
		time = time.replace('m', ' минут ')
		time = time.replace('h', ' часов ')
		time = time.replace('d', ' дней ')
		if time[-1:] == ' ':
			time = time[:-1]
	return time.replace('-', '')

def cts(s):
    UNITS = {'s': 'seconds', 'm': 'minutes', 'h': 'hours', 'd': 'days'}
    try:
        s = int(s)
        return s
    except:
        pass
    seconds = int(timedelta(**{
                  UNITS.get(m.group('unit').lower(), 'seconds'): int(m.group('val'))
                  for m in re.finditer(r'(?P<val>\d+)(?P<unit>[smhd]?)', s, flags=re.I)
                  }).total_seconds())
    if not seconds:
        try:
            seconds = int(s)
        except:
            return 0
    return seconds
