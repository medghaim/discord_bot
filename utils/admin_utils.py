import asyncio
import discord
from discord.ext import commands

""" Keep in mind that any administrative function written here, 
	and added to do_dispatcher and undo_dispatcher, 
	CAN be called from both admin_do and admin_undo.
	ie, unban can be called by from admin_undo (ie, !unban x)
	or it can be called in admin_do, after a temp ban (ie, !ban 5 x <-- will call unban)
"""
# helpers
def voice_kwarg_converter(**kwargs):
	""" When a usr is temp muted, admin_do is called with kwargs={mute:True}.
	This calls do_dispatcher (ie, bot.server_voice_status(member, **kwargs)) and mutes the member (since mute:True)
	After temp mute lapses, admin_do ALSO calls undo_dispatcher w/ same kwargs. (ie, bot.server_voice_status(member, **kwargs))
	Problem is, our **kwargs say that {mute:True} in this case. So we want to reverse ONLY the voice option kwargs
	func def: bot.server_voice_state(member, *, mute=None, deafen=None) -- only kwarg options are 'mute' & 'deafen'
	"""
	t_kwargs = {}
	for key, value in kwargs.items():
		if key == 'mute' or key == 'deafen':
			value = not value # flip the value
		t_kwargs[key] = value # add to new kwargs
	return t_kwargs

# "private" administrative utilities - don't call these directly, use admin_do, and admin_undo
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

async def unban(bot, ctx, members):
	bans = await bot.get_bans(ctx.message.server)
	output = 'Unbanned:\n\t'
	for member in members:
		if isinstance(member, str): # member is str, unban was called from admin_undo, thus we must find member from bans list
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
	"""Only True kwargs should be passed to this function
		 - the things we want to DO (mute, deafen, silence, etc)
	"""
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


async def enable_voice_state(bot, ctx, members, **kwargs):
	"""Only False kwargs should be passed to this function
		 - the things we want to UNDO (unmute, undeafen, unsilence, etc)
	"""
	is_mute = kwargs.get('mute', True)
	is_deaf = kwargs.get('deafen', True)

	if not is_mute and not is_deaf:
		output = 'Unsilenced:\n\t'
	elif not is_mute:
		output = 'Unmuted:\n\t'
	elif not is_deaf:
		output = 'Undeafened:\n\t'

	for member in members:
		await bot.server_voice_state(member, **kwargs)
		output += '{}\n\t'.format(member.name)
	await bot.say_block(output.strip())



# ADMINISTRATIVE FUNCTION DISPATCHERS (dict of value->function)
do_dispatcher = {
	'ban' : ban,
	'voice_state' : disable_voice_state, #mute/deafen/silence
	'chatmute' : None,
}

undo_dispatcher = {
	'ban' : unban,
	'voice_state' : enable_voice_state, #unmute/undeafen/unsilence
	'chatmute' : None,
}


# "public" administrative utilities

#Only functions that have the option of specifying time SHOULD call this
async def admin_do(func_key, bot, ctx, members, time, **kwargs):
	""" Parse arguments (check for optional int, convert to member as necessary)
	and use the admin_dispatcher dict to call the appropriate administrative function 

	Allows us to check for option time arg, which is common procedure for ban/mute/deafen
	"""
	# parsing arguments, determining if time was supplied argument or not
	try:
		time = int(time)
	except ValueError:
		converter = commands.MemberConverter(ctx, time)
		members = list(members)
		members.insert(0, converter.convert())
		time = 0

	if len(members) == 0:
		raise commands.MissingRequiredArgument('Must specify member(s) to {}.'.format(func_key))
	
	# the administration / temp administration (ie, ban / temp ban)
	await do_dispatcher[func_key](bot, ctx, members, time, **kwargs)
	if time > 0: # temp ban
		await asyncio.sleep(time)#*60)
		await undo_dispatcher[func_key](bot, ctx, members, **voice_kwarg_converter(**kwargs))

#Only functions that DON'T have the option to specify a time SHOULD call this
async def admin_undo(func_key, bot, ctx, members, **kwargs):
	if len(members) == 0:
		raise commands.MissingRequiredArgument('Must specifiy member(s) to {}.'.format(func_key))
	await undo_dispatcher[func_key](bot, ctx, members, **kwargs)
