import disnake
from disnake.ext import commands


class Kick(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client

    @commands.slash_command(name="kick", description="Kick member")
    @commands.has_permissions(kick_members=True)
    async def kick(self, inter: disnake.ApplicationCommandInteraction, member: disnake.Member, *, reason=None):
        await inter.response.defer()
        member_top_role = member.top_role
        author_top_role = inter.author.top_role

        if member_top_role < author_top_role:
            await member.kick(reason=reason)
            kick_embed = disnake.Embed(title=f"Command - Kick: Success", description=f"{member} was kicked by {inter.author.display_name}", color=disnake.Colour.green())
        else:
            kick_embed = disnake.Embed(title=f"Command - Kick: Fail", description=f"{member} was not kicked because he has higher role than {inter.author.display_name}", color=disnake.Colour.red())

        await inter.edit_original_message(embed=kick_embed)

    @kick.error
    async def kick_error(self, inter: disnake.ApplicationCommandInteraction, error):
        if isinstance(error, commands.MissingPermissions):
            error_embed = disnake.Embed(title="Command - Kick: Fail", description=f"You do not have permissions to kick members.", color=disnake.Colour.red())
        elif isinstance(error, commands.MemberNotFound):
            error_embed = disnake.Embed(title="Command - Kick: Fail", description=f"No such member was found.", color=disnake.Colour.red())
        elif isinstance(error, commands.BotMissingPermissions):
            error_embed = disnake.Embed(title="Command - Kick: Fail", description=f"The bot does not have permissions to kick this member.", color=disnake.Colour.red())
        else:
            error_embed = disnake.Embed(title="Command - Kick: Fail", description=f"An unknown error occurred.", color=disnake.Colour.red())

        await inter.response.send_message(embed=error_embed)


def setup(client: commands.Bot):
    client.add_cog(Kick(client))
