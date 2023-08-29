import disnake
from disnake.ext import commands


class Ban(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client

    @commands.slash_command(name="ban", description="ban member")
    @commands.has_permissions(ban_members=True)
    async def ban(self, inter: disnake.ApplicationCommandInteraction, member: disnake.Member, *, reason=None):
        await inter.response.defer()
        member_top_role = member.top_role
        author_top_role = inter.author.top_role

        if member_top_role < author_top_role:
            await member.ban(reason=reason)
            ban_embed = disnake.Embed(title=f"Command - ban: Success", description=f"{member} was baned by {inter.author.display_name}", color=disnake.Colour.green())
        else:
            ban_embed = disnake.Embed(title=f"Command - ban: Fail", description=f"{member} was not baned because he has higher role than {inter.author.display_name}", color=disnake.Colour.red())

        await inter.edit_original_message(embed=ban_embed)

    @ban.error
    async def ban_error(self, inter: disnake.ApplicationCommandInteraction, error):
        if isinstance(error, commands.MissingPermissions):
            error_embed = disnake.Embed(title="Command - ban: Fail", description=f"You do not have permissions to ban members.", color=disnake.Colour.red())
        elif isinstance(error, commands.MemberNotFound):
            error_embed = disnake.Embed(title="Command - ban: Fail", description=f"No such member was found.", color=disnake.Colour.red())
        elif isinstance(error, commands.BotMissingPermissions):
            error_embed = disnake.Embed(title="Command - ban: Fail", description=f"The bot does not have permissions to ban this member.", color=disnake.Colour.red())
        else:
            error_embed = disnake.Embed(title="Command - ban: Fail", description=f"An unknown error occurred.", color=disnake.Colour.red())

        await inter.response.send_message(embed=error_embed)


def setup(client: commands.Bot):
    client.add_cog(Ban(client))
