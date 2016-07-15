import asyncio
import discord
from discord.ext import commands

# helpers
def voice_kwarg_converter(**kwargs):
	"""Converts voice kwargs ('mute' or 'deafen') to false, if it exists and is true"""
	t_kwargs = {}
	for key, value in kwargs.items():
		if (key == 'mute' or key == 'deafen') and value == True:
			value = False # flip the value
		t_kwargs[key] = value # add to new kwargs
	return t_kwargs

#"private" ban functions - not to be called directly
async def ban(bot, ctx, members, time):
	inv = (await bot.create_invite(ctx.message.channel)).url
	msg = 'You have been banned for {} mins.\n. You will be able to use the following invite when your ban is lifted.\n{}'.format(time, inv)
	output = 'Temporarily banned ({} mins):\n\t'.format(time)

	if time == 0:
		msg = 'You have been indefinitely banned from {}. _Jah praise_'.format(ctx.message.server)
		output = 'Banned:\n\t'

	for member in members:
		await bot.send_message(member, msg)
		output += '{}\n\t'.format(member.name)
		await bot.ban(member)

	await bot.say_block(output.strip())

async def unban(bot, ctx, members, time):
	bans = await bot.get_bans(ctx.message.server)
	output = 'Unbanned:\n\t'

	for member in members:
		if isinstance(member, str): # member is str, !unban called directly (we dont have access to member objs -- banned, not on our server)
			candidates = [m for m in bans if m.name.lower() == member.lower()]
			if len(candidates) <= 0:
				raise commands.BadArgument('"{}" member not found.'.format(member))
			elif len(candidates) > 1:
				raise commands.BadArgument('"{}" refers to more than one person. Please ban manually.'.format(member))
			member = candidates[0] # len(candidates) == 1

		await bot.unban(ctx.message.server, member)
		output += '{}\n\t'.format(member.name)

	await bot.say_block(output.strip())

async def disable_voice_state(bot, ctx, members, time, **kwargs):
	is_mute = kwargs.get('mute', None)
	is_deaf = kwargs.get('deafen', None)

	if is_mute and is_deaf:
		verb = 'Silenced'
	elif is_mute:
		verb = 'Muted'
	elif is_deaf:
		verb = 'Deafened'

	output = '{}:\n\t'.format(verb)
	if time > 0:
		output = 'Temporarily {} ({} mins):\n\t'.format(verb.lower(), time)

	for member in members:
		await bot.server_voice_state(member, **kwargs)
		output += '{}\n\t'.format(member.name)
	await bot.say_block(output.strip())


async def enable_voice_state(bot, ctx, members, time, **kwargs):
	is_mute = kwargs.get('mute', None)
	is_deaf = kwargs.get('deafen', None)

	if is_mute == False and is_deaf == False:
		output = 'Unsilenced:\n\t'
	elif is_mute == False:
		output = 'Unmuted:\n\t'
	elif is_deaf == False:
		output = 'Undeafened:\n\t'

	for member in members:
		await bot.server_voice_state(member, **kwargs)
		output += '{}\n\t'.format(member.name)
	await bot.say_block(output.strip())


# administrative function dispatchers - (dict of value->function)
# must follow mute/unmute, ban/unban, deafen/undeafen, etc, naming convention
admin_dispatcher = {
	'ban' : ban,
	'mute' : disable_voice_state,
	'deafen' : disable_voice_state,
	'silence' : disable_voice_state,
	'chatmute' : None,

	#un<func> - naming convention! IMPORTANT!
	'unban' : unban,
	'unmute' : enable_voice_state,
	'undeafen' : enable_voice_state,
	'unsilence' : enable_voice_state,
	'unchatmute' : None,
}

async def administrator(func_key, bot, ctx, members, time=0, **kwargs):
	#time can be member, or it can be the time specified to admin someone for
	#or it can be 0 (not passed - ie, unimportant for unban/unmute/undeafen etc)
	try:
		time = int(time)
	except ValueError:
		converter = commands.MemberConverter(ctx, time)
		members = list(members)
		members.insert(0, converter.convert())
		time = 0

	if len(members) == 0:
		raise commands.MissingRequiredArgument('Must specify member(s) to {}.'.format(func_key))

	# administration / temp administration (ie, ban / temp ban)
	await admin_dispatcher[func_key](bot, ctx, members, time, **kwargs) #could be a mute, could be an unmute
	if time > 0: # temp ban
		await asyncio.sleep(time)#*60)
		await admin_dispatcher['un'+func_key](bot, ctx, members, 0, **voice_kwarg_converter(**kwargs)) #the 'un' functions don't use time, pass 0

