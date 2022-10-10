from util import get_maaldar_user, match_url_regex

import discord

import aiohttp

class Icon:
	async def icon(interaction: discord.Interaction, url: str = None) -> None:
		await interaction.response.defer()
		maaldar_user = get_maaldar_user(interaction.user.id)
		role: discord.Role = interaction.guild.get_role(int(maaldar_user[1]))

		if not url:
			await role.edit(display_icon=None)
			await interaction.followup.send("Role icon removed 🗑️")
			return

		if not match_url_regex(url):
			await interaction.followup.send("Enter a valid URL path!\n> It must end in .png or .jpg")
			return

		async with aiohttp.ClientSession() as session:
			async with session.get(url) as response:
				if response.status == 200:
					try:
						await role.edit(display_icon=await response.read())
						await interaction.followup.send("Role icon set ✨")
						return

					except Exception as error:
						await interaction.followup.send(error)
						return

				await interaction.followup.send("Something is wrong with the website. Try a different one 👉")