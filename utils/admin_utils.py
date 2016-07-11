import asyncio
import discord
from discord.ext import commands
from utils import output

async def ban_dispenser(bot, ctx, time, members):
	if time == 0:	# INDEFINITE BAN
		for member in members:
			await bot.send_message(member, 'You have been indefinitely banned from the server. _Jah praise_.')
			await bot.ban(member)
		await bot.say('Indefinitely Banned: \n\t{}'.format(", ".join(m.name for m in members)))

	else:			# TEMP BAN
		banstr = ''
		inv = (await bot.create_invite(ctx.message.server)).url

		# send messages to all the members specified and ban then
		for member in members:
			banstr += '\t{}\n'.format(member.name)
			await bot.send_message(member, 'You have been banned for {} mins.\nYou will be able to use the link below to rejoin the server when your ban is automatically lifted.\n{}'.format(time, inv))
			await bot.ban(member)

		# wait out the duration of the ban
		await bot.say('Banned for {} mins:\n{}'.format(time, banstr))
		await asyncio.sleep(time*60) # `time` minutes
		
		# unban all the members
		for member in members:	
			await bot.unban(ctx.message.server, member)
			await bot.say('{}\'s ban has been lifted.'.format(member.name))

async def ban_hammer(bot, ctx, time, members):
	for member in members:
		await bot.ban(member)

	if time > 0: # temp ban
		await asyncio.sleep(time*60)

		for member in members:
			await bot.unban(member)

async def voice_state_changer(bot, ctx, time, members, mute, deafen):
	names = ", ".join([m.name for m in members])
	for member in members:
		await bot.server_voice_state(member, mute=mute, deafen=deafen)

	if time == 0:
		await output.speak(bot, 'Muted:\n\t {}'.format(names))

	elif time > 0:
		await output.speak(bot, 'Temporarily muted ({} mins):\n\t {}'.format(time, names))
		await asyncio.sleep(time*60)

		for member in members:
			await bot.server_voice_state(member, mute=False, deafen=False)

		await output.speak(bot, 'Mutes lifted:\n\t {}'.format(names))