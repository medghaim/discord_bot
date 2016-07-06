import discord
import asyncio

async def speak(bot, msg):
	await bot.say('```py\n{}\n```'.format(msg))