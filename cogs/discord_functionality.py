import discord
from discord.ext import commands
from cogs.utils import output

class Discord_Functionality():

	def __init__(self, bot):
		self.bot = bot

	@commands.command(pass_context=True, aliases=['inv', 'i'])
	async def invite(self, ctx, mins = 0):
		""" Creates an invite and returns it """
		await self.bot.say((await self.bot.create_invite(ctx.message.server, **{"max_age":mins})).url)

	@commands.command(pass_context=True)
	async def banned(self, ctx):
		""" Says who is banned on the server """
		banned = ''
		for banned_user in (await self.bot.get_bans(ctx.message.server)):
			banned += '**'+banned_user.name+'**\n'
		if len(banned) > 0:
			await output.speak(self.bot, 'Ban List: \n'+banned)
		else:
			await output.speak(self.bot, 'No _current_ bans. Not yet at least.')

	@commands.command(pass_context=True, aliases=['whom'])
	async def who(self, ctx, *mentioned_members : discord.Member):
		""" A report of members currently playing games.
			Can also mention a specific player and report only their game status."""
		status_str = ''

		### IF NO ARGS SUPPLIED
		if len(mentioned_members) == 0:
			##retrieve all voice channels
			voice_channels = (ch for ch in ctx.message.server.channels if ch.type == discord.ChannelType.voice)
			for ch in voice_channels: ##search all voice_channels in server
				##members who are currently gaming
				gaming_members = (g_mem for g_mem in ch.voice_members if g_mem.game != None)
				for member in gaming_members:
					status_str += '**{}** _({})_\n'.format(member.name, member.game.name)
		###IF ARGS SUPPLIED
		else: 
			for member in (m for m in mentioned_members if m.game != None):
				status_str += '**{}** _({})_\n'.format(member.name, member.game.name)

		if len(status_str) > 0:
			await output.speak(self.bot, status_str)
		else:
			await output.speak(self.bot, 'No one currently playing.')

	@commands.command(pass_context=True, aliases=['del'])
	async def delete(self, ctx, count=1):
		""" Deletes commanders last X messages. 
		Only checks the channels last 500 messages
		"""
		if(count > 99):
			raise commands.BadArgument('Cannot delete more than 99 messages at a time.')

		logs = self.bot.logs_from(ctx.message.channel, limit=500, before=ctx.message)
		remaining = count
		user_logs = []
		async for log in logs:
			if log.author == ctx.message.author and remaining > 0:
				user_logs.append(log)
				remaining -= 1
			if remaining == 0:
				break

		if remaining == count: #no msgs deleted, none found to delete.
			raise commands.CommandError('I couldn\'t find any of your messages to delete.')
		else:
			user_logs.append(ctx.message) ##delete the command too!
			await self.bot.delete_messages(user_logs) #delete the desired logs

	@commands.command(pass_context=True)
	async def msgcount(self, ctx):
		"""Tells you how many of the last 500 messages are yours"""
		logs = self.bot.logs_from(ctx.message.channel, limit=500, before=ctx.message)
		count = 0
		async for log in logs:
			if log.author == ctx.message.author:
				count += 1
		await output.speak(self.bot, '{}/500 of the last channel messages are yours.'.format(count))

	@commands.group(invoke_without_command=True, pass_context=True)
	async def last(self, ctx, member : discord.Member, count=1):
		""" Gets the specified users last X messages"""
		if count > 100:
			raise commands.BadArgument('Cannot display more than 100 messages.')
		logs = self.bot.logs_from(ctx.message.channel, limit=500, before=ctx.message)
		user_logs = []

		async for log in logs:
			if log.author == member and len(user_logs) < count:
				user_logs.append(log)
				
			if len(user_logs) == count:
				break
		
		log_str = ''
		for log in reversed(user_logs):
			log_str += '{}\n'.format(log.content)

		if len(log_str) > 0:
			await self.bot.say(log_str)
		else:
			await self.bot.say('No messages found.')

	@last.command(name='me', pass_context=True)
	async def _me(self, ctx, count=1):
		""" Retrieves the callers last X commands
		Default = 1"""
		await ctx.command.parent.callback(self, ctx, ctx.message.author, count) #calls last() with caller as the member obj

def setup(bot):
	bot.add_cog(Discord_Functionality(bot))