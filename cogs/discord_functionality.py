import discord
from discord.ext import commands

from utils import output

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
		banned = "\n".join(usr.name for usr in (await self.bot.get_bans(ctx.message.server)))
		if len(banned) == 0:
			banned = 'No current bans.'
		await output.speak(self.bot, banned)

	@commands.command(pass_context=True, aliases=['whom'])
	async def who(self, ctx, *members : discord.Member):
		""" A report of members currently playing games.
			Can also mention specific player(s)"""
		members = members or ctx.message.server.members
		status = "\n".join('{0.name} ({0.game.name})'.format(m) for m in members if m.voice_channel and m.game)
		if len(status) == 0:
			status = 'No one currently playing.'
		await output.speak(self.bot, status)

	@commands.command(pass_context=True, aliases=['del'])
	async def delete(self, ctx, count=1):
		"""Deletes commanders last X messages. 
		Only checks the channels last 500 messages"""
		logs = self.bot.logs_from(ctx.message.channel, limit=500, before=ctx.message)
		msgs = []

		# find the messages
		async for log in logs:
			if log.author == ctx.message.author and count > 0:
				#await self.bot.delete_message(log)
				msgs.append(log)
				count -= 1
			if count == 0:
				break

		# delete the messages in chunks of 100
		while len(msgs) > 100: # limit for client.delete_messages 
			await self.bot.delete_messages(msgs[:100])
			msgs = msgs[100:]

		# clean up any remaing messages: 0 <= msgs <= 100 now
		if len(msgs) > 1:
			await self.bot.delete_messages(msgs)
		elif len(msgs) == 1:
			await self.bot.delete_message(msgs[0])

		await self.bot.delete_message(ctx.message) # delete the command

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
		logs = self.bot.logs_from(ctx.message.channel, limit=500, before=ctx.message)
		msgs = []
		async for log in logs:
			if log.author == member and count > 0:
				msgs.insert(0,'({}) {}'.format(count, log.content))
				count -= 1
			if count == 0:
				break

		if len(msgs) == 0:
			msgs.append('No messages found.')
		await self.bot.say("\n".join(msgs))

	@last.command(name='me', pass_context=True)
	async def _me(self, ctx, count=1):
		""" Retrieves the callers last X commands"""
		await ctx.command.parent.callback(self, ctx, ctx.message.author, count) #calls last() with caller as the member obj

def setup(bot):
	bot.add_cog(Discord_Functionality(bot))