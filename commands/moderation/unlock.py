import disnake
from disnake.ext import commands


class unlock(commands.Cog, name='unlock', description="Unlocks a channel"):

    def __init__(self, client: commands.Bot):
        self.client = client

    @commands.slash_command(name="unlock", description="unlock a channel.")
    @commands.cooldown(1, 5, commands.BucketType.user)
    @commands.has_permissions(manage_channels=True)
    async def Unlock(self, inter: disnake.ApplicationCommandInteraction, channel: disnake.TextChannel = None):
        channel = channel or inter.channel
        overwrite = channel.overwrites_for(inter.guild.default_role)
        if overwrite.send_messages:
            unlock_embed = disnake.Embed(title="Command `unlock` => unaffected", color=disnake.Color.yellow())
            unlock_embed.add_field(name="The command probably didn't work because:", value="1. Channel is already unlocked")
            await inter.response.send_message(embed=unlock_embed, delete_after=5)
            await channel.send(embed=unlock_embed, delete_after=5)
        else:
            await channel.set_permissions(inter.guild.default_role, send_messages=True)
            unlock_embed = disnake.Embed(title="Command `unlock` => Success", color=disnake.Color.green())
            unlock_embed.add_field(name="The command executed", value="The channel is now unlocked")
            await inter.response.send_message(embed=unlock_embed, delete_after=5)
            await channel.send(embed=unlock_embed, delete_after=5)

    @Unlock.error
    async def unlock_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            errorEmbed = disnake.Embed(title="Command => `*unlock` => Fail",
                                       description="You dont have permissions to manage channels")
            await ctx.send(embed=errorEmbed)
        elif isinstance(error, commands.BotMissingPermissions):
            errorEmbed = disnake.Embed(title="Command => `*unlock` => Fail",
                                       description="The bot doesnt have permissions to manage channels")
            await ctx.send(embed=errorEmbed)
        else:
            errorEmbed = disnake.Embed(title="Command `*unlock` => Fail", description="Some error occurred")
            await ctx.channel.send(embed=errorEmbed)


def setup(client: commands.Bot):
    client.add_cog(unlock(client))
