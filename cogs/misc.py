import discord
from discord.ext import commands
import nekos
import time
import datetime
import psutil
bot_invite_link = "https://discord.com/api/oauth2/authorize?client_id=837282453654732810&permissions=8&scope=bot"
nullTime = time.time()

class misc(commands.Cog):
	def __init__(self, bot):
		self.bot = bot

	@commands.command()
	async def help(self, ctx, page=0):
		if not page or page > 4:
			default = '`1.` Модерация\n`2.` Музыка\n`3.` Утилиты\n`4.` Прочее\n\nИспользуйте `!!help [page]` для просмотра списка команд из этой категории.'
			e = discord.Embed()
			e.add_field(name='Доступные категории команд', value=default)
			e.set_footer(text='© 2021 Sweety187 | Все права защищены.',
				     icon_url='https://media.discordapp.net/attachments/832662675963510827/855762014010081300/b5222c5b.jpg')
			await ctx.send(embed=e)
			return
		mod = '`!!kick <member> [reason]` - кикнуть пользователя\n`!!ban <member> [reason]` - забанить пользователя\n`!!unban <user>` - разбанить пользователя\n`!!mute <member> [time] [reason]` - замутить пользователя\n`!!unmute <member>` - размутить пользователя\n`!!clear <amount>` - удалить последние N сообщений в канале'
		music = '`!!join [channel]` - присоединиться к голосовому каналу\n`!!leave` - покуинуть голосовой канал\n`!!play <query>` - воспроизвести музыку с YouTube\n`!!radio <stream>` - проигрывать радио в голосовом канале\n`!!stop` - остановить воспроизведение\n`!!pause` - приостановить воспроизведение\n`!!resume` - продолжить воспроизведение\n`!!repeat` - зациклить воспроизведение\n`!!now` - узнать, что сейчас играет'
		utils = '`!!avatar [member]` - вывести аватар пользователя\n`!!yt <query>` - найти видео на YouTube\n`!!ping <ip>` - выводит информацию о сервере Minecraft\n`!!2b2t` - выводит данные о сервере 2b2t (очередь и т.п.)\n`!!skin <nick>` - выводит скин игрока Minecraft\n`!!say <text>` - отправить сообщение от имени бота\n`!!embed <text>` - отправить ваш текст внутри ембеда\n`!!timer <time>` - поставить таймер\n`!!user [user]` - информация о пользователе\n`!!server` - информация о сервере'
		misc = '`!!neko` - случайная картинка с неко\n`!!nekogif` - случайная гифка с неко\n`!!cat` - случайная картинка с котом\n`!!nsfw [tag]` - хентай-картинка по тегу («lewd», если тег не указан)\n`!!invite` - добавить меня на свой сервер\n`!!about` - сведения о текущей версии бота\n`!!status` - статистика бота'
		pages = [mod, music, utils, misc]
		titles = ['1. Модерация', '2. Музыка', '3. Утилиты', '4. Прочее']
		e = discord.Embed()
		e.add_field(name=titles[page - 1], value=pages[page - 1])
		e.set_footer(text='© 2021 Sweety187 | Все права защищены.',
			     icon_url='https://media.discordapp.net/attachments/832662675963510827/855762014010081300/b5222c5b.jpg')
		await ctx.send(embed=e)

	@commands.command()
	async def status(self, ctx):
		uptime = int(time.time() - nullTime)
		uptime = datetime.timedelta(seconds=uptime)
		e = discord.Embed(title="Статистика бота")
		e.add_field(name='Аптайм', value=uptime, inline=True)
		e.add_field(name='Версия', value='s1.0.1', inline=True)
		e.add_field(name='Серверов', value=len(self.bot.guilds), inline=True)
		users = 0
		for guild in self.bot.guilds:
			users = users + guild.member_count
		e.add_field(name='Пользователей', value=users, inline=True)
		e.add_field(name='Нагрузка',
					value=f'ЦП: {psutil.cpu_percent()}% ОЗУ: {psutil.virtual_memory().percent}%',
					inline=True)
		e.set_thumbnail(url="https://media.discordapp.net/attachments/832662675963510827/857631236355522650/logo.png")
		e.set_footer(text='© 2021 Sweety187 | Все права защищены.',
			     icon_url='https://media.discordapp.net/attachments/832662675963510827/855762014010081300/b5222c5b.jpg')
		await ctx.send(embed=e)

	@commands.command()
	async def about(self, ctx):
		e=discord.Embed(title="Стабильная 1.0.1 от 23.07.2021 16:04 MSK")
		fixed="ㆍИсправления мелких ошибок."
		improved="ㆍИзменен интерфейс бота."
		added="ㆍДобавлена возможность указывать причину для бана, кика, мута."
		deleted="ㆍКоманда `!!bug`, вместе с сервером поддержки."
		e.add_field(name='Исправлено', value=fixed, inline=False)
		#e.add_field(name='Изменено', value=improved, inline=False)
		#e.add_field(name='Добавлено', value=added, inline=False)
		emb.add_field(name='Удалено', value=deleted, inline=False)
		e.set_footer(text='© 2021 Sweety187 | Все права защищены.',
			     icon_url='https://media.discordapp.net/attachments/832662675963510827/855762014010081300/b5222c5b.jpg')
		await ctx.send(embed=e)

	@commands.command()
	@commands.is_nsfw()
	async def nsfw(self, ctx, req='lewd'):
		possible = ['feet', 'yuri', 'trap', 'futanari', 'hololewd', 'lewdkemo', 'solog',
					'feetg', 'cum', 'erokemo', 'les', 'lewdk', 'ngif', 'lewd', 'gecg',
					'eroyuri', 'eron', 'cum_jpg', 'bj', 'nsfw_neko_gif', 'solo', 'anal',
			    		'hentai', 'erofeet', 'keta', 'blowjob', 'pussy', 'tits', 'holoero',
					'pussy_jpg', 'pwankg', 'classic', 'kuni', 'femdom', 'spank', 'erok', 'boobs',
					'random_hentai_gif', 'smallboobs', 'ero']
		if req not in possible:
			tags = str(possible).replace('[\'', '`').replace('\', \'', '` `').replace('\']', '`')
			await error(ctx, f'Использование: `!!nsfw [tag]`'
							 f'\nДоступные теги: {tags}')
			return
		link = nekos.img(req)
		e = discord.Embed()
		e.set_image(url=link)
		await ctx.send(embed=e)

	@commands.command()
	async def cat(self, ctx):
		link = nekos.cat()
		e = discord.Embed()
		e.set_image(url=link)
		await ctx.send(embed=e)

	@commands.command()
	async def neko(self, ctx):
		link = nekos.img('neko')
		e = discord.Embed()
		e.set_image(url=link)
		await ctx.send(embed=e)

	@commands.command(aliases = ['ngif'])
	@commands.is_nsfw()
	async def nekogif(self, ctx):
		link = nekos.img('ngif')
		e = discord.Embed()
		e.set_image(url=link)
		await ctx.send(embed=e)

	@commands.command()
	async def invite(self, ctx):
		e = discord.Embed(description=f'<:info:863711569975967745> Добавить бота на свой сервер: '
									  f'[[Нажми]]({bot_invite_link})')
		await ctx.send(embed=e)


def setup(bot):
	bot.add_cog(misc(bot))


async def success(ctx, message, delete_after=None, image=None):
	e = discord.Embed(description='<a:success:860037468279406592> ' + message)
	if image:
		e.set_thumbnail(url=image)
	await ctx.send(embed=e, delete_after=delete_after)


async def error(ctx, message):
	e = discord.Embed(description='<a:error:862306041546407936> ' + message)
	await ctx.send(embed=e)
