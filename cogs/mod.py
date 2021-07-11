import discord
from discord.ext import commands
from datetime import timedelta
import asyncio
import re


class Moderation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=['purge'])
    @commands.has_permissions(manage_messages=True)
    async def clear(self, ctx, amount):
        """Очистить сообщения в этом канале"""
        try:
            amount = int(amount)
            if amount <= 0:
                await error(ctx, 'Некорректный аргумент.')
                return
        except:
            await error(ctx, 'Аргумент должен быть числом.')
            return
        if amount <= 100:
            try:
                deleted = await ctx.message.channel.purge(limit=amount + 1)
            except:
                await error(ctx, 'У меня нет прав для выполнения этой команды.')
                return
            await success(ctx, f'Удалено {len(deleted) - 1} сообщений.', 5)
        else:
            await error(ctx, 'Нельзя удалить больше 100 сообщений.')

    @commands.command()
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx, member: discord.Member, *, reason=""):
        """Кикнуть пользователя"""
        if member == ctx.author:
            await error(ctx, 'Вы не можете кикнуть самого себя.')
            return
        try:
            await member.kick()
        except:
            await error(ctx, 'У меня нет прав для выполнения этой команды.')
            return
        await success(ctx, f'''Пользователь {member} кикнут.
        Причина: {reason}''' if reason else f'Пользователь {member} кикнут.')

    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, member: discord.Member, *, reason=None):
        """Забанить пользователя"""
        if member == ctx.author:
            await error(ctx, 'Вы не можете забанить самого себя.')
            return
        try:
            await member.ban()
        except Forbidden:
            await error(ctx, 'У меня нет прав для выполнения этой команды.')
            return
        await success(ctx, f"""Пользователь {member} забанен.
        					   Причина: """ + reason if reason else f"Пользователь {member} забанен.")

    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def unban(self, ctx, *, member):
        """Разбанить пользователя"""
        try:
            banned_users = await ctx.guild.bans()
        except:
            await error(ctx, 'У меня нет прав для выполнения этой команды.')
            return
        for member in banned_users:
            user = member.user
        if not user:
            await error(ctx, 'Этот пользователь не был забанен.')
            return
        await ctx.guild.unban(user)
        await success(ctx, f'Пользователь {user} разбанен.')

    @commands.command()
    @commands.has_permissions(manage_messages=True)
    async def mute(self, ctx, member: discord.Member,
                   time=None, *, reason=None):
        """Замутить пользователя"""
        if member == ctx.author:
            await error(ctx, 'Вы не можете замутить самого себя.')
            return
        muterole = get_muterole(ctx)
        if muterole in member.roles:
        	await error(ctx, 'Этот пользователь уже замучен.')
        me = ctx.guild.me
        _time = time
        time, timestring = get_time(time)
        t = tround(time)
        if not t and _time:
            reason = str(reason) if reason else ''
            reason = str(_time) + ' ' + reason
        if not get_muterole(ctx):
            guild = ctx.guild
            permsissions = muteperms()
            try:
                muterole = await guild.create_role(name="Muted")
            except:
                await error(ctx, 'У меня нет прав для выполнения этой команды.')
                return
            position = me.top_role.position - 1
            await muterole.edit(permissions=permsissions, position=position)
        try:
            await member.add_roles(muterole)
        except:
            await error(ctx, 'У меня нет прав для выполнения этой команды.')
            return
        r = "\nПричина: " + reason if reason else ""
        user = member.mention
        if time <= 0:
            await success(ctx, f'Пользователь {user} замучен навсегда. {r}')
            return
        await success(ctx, f'Пользователь {user} замучен на {timestring}. {r}')
        await asyncio.sleep(time)
        await _unmute(member, muterole)

    @commands.command()
    @commands.has_permissions(manage_messages=True)
    async def unmute(self, ctx, member: discord.Member):
        """Размутить пользователя"""
        muterole = get_muterole(ctx)
        if not muterole in member.roles:
        	await error(ctx, 'Этот пользователь уже размучен.')
        	return
        try:
            await member.remove_roles(muterole)
        except:
            await error(ctx, 'У меня нет прав для выполнения этой команды.')
            return
        await success(ctx, f'Пользователь {member.mention} размучен.')


def setup(bot):
    bot.add_cog(Moderation(bot))


async def success(ctx, message, delete_after=None):
    e = discord.Embed(description='<a:success:860037468279406592> ' + message)
    await ctx.send(embed=e, delete_after=delete_after)


async def error(ctx, message):
    e = discord.Embed(description='<a:error:862306041546407936> ' + message)
    await ctx.send(embed=e)


def tround(time):
    try:
        if int(time) == time:
            if time > 0:
                t = round(time)
            else:
                t = 0
        else:
            t = round(time, 2)
    except:
        t = 0
    return t


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
    return time


async def _unmute(member, muterole):
    try:
        await member.remove_roles(muterole)
    except:
        pass


def muteperms():
    permissions = discord.Permissions()
    permsissions.update(send_messages=False,
                        change_nickname=False,
                        speak=False,
                        request_to_speak=False,
                        manage_messages=False)
    return permissions


def get_time(time):
    timestring = None
    try:
        if not time:
            time = 0
            raise Exception
        timestring = ctts(time)
        time = cts(time)
    except:
        time = 0
    return time, timestring


def get_muterole(ctx):
    return discord.utils.get(ctx.guild.roles, name='Muted')
