import asyncio
import discord
from discord.ext import commands

async def ban_dispenser(bot, ctx, time, members):
	if time == 0:
		for member in members:
			await bot.send_message(member, 'You have been indefinitely banned from the server. _Jah praise_.')
			await bot.ban(member)
		await bot.say('Indefinitely Banned: \n\t{}'.format(", ".join(m.name for m in members)))
	else:
		# send messages to all the members specified and ban then
		banstr = 'Banned for {} mins:\n'.format(time)
		for member in members:
			inv = (await bot.create_invite(ctx.message.server)).url
			banstr += '\t{}\n'.format(member.name)
			await bot.send_message(member, 'You have been banned for {} mins.\nYou will be able to use the link below to rejoin the server when your ban is automatically lifted.\n{}'.format(time, inv))
			await bot.ban(member)
		await bot.say(banstr)

		# wait for `time` minutes
		await asyncio.sleep(time*60)
		
		# unban all the members
		for member in members:	
			await bot.unban(ctx.message.server, member)
			await bot.say('{}\'s ban has been lifted.'.format(member.name))
