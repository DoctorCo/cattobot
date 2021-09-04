import discord
from discord.ext import commands
import os


class AdminCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # Kick Command
    @commands.command(brief="Admin Command!")
    async def kick(self, ctx, member: discord.Member, *, reason=None):
        """Kick a User (Only for Admin)"""
        if ctx.message.author.guild_permissions.administrator:
            await member.kick(reason=reason)
            await ctx.send(f"{member.mention} has been kicked from the server. Reason: **{reason}**")
        else:
            await ctx.send("You don't have permission to use that command!")

    # Ban Command
    @commands.command(brief="Admin Command!")
    async def ban(self, ctx, member: discord.Member = None, *, reason=None):
        if member == ctx.author:
            await ctx.send("You can't ban yourself! Don't leave us alone, I'm there for you :heart:")
        else:
            embed = discord.Embed(
                title="Banned", description=f"{member.mention} has been banned for\n```{reason}```", color=discord.Color.red())
            await member.ban(reason=reason)
            await ctx.send(embed=embed)

    # Unban Command

    @commands.command(brief="Admin Command!")
    async def unban(self, ctx, *, member):
        """Unban a User (Only for Admin)"""
        if ctx.message.author.guild_permissions.administrator:
            banned_users = await ctx.guild.bans()
            member_name, member_discriminator = member.split("#")

            for ban_entry in banned_users:
                user = ban_entry.user

                if (user.name, user.discriminator) == (member_name, member_discriminator):
                    await ctx.guild.unban(user)
                    await ctx.send(f'{user.mention} has been unbanned!')
        else:
            await ctx.send("You don't have permission to use that command!")

    @commands.command(brief="Admin Command!")
    async def mute(self, ctx, member: discord.Member, *, reason):
        """Mutes a User (Only for Admin)"""
        if ctx.message.author.guild_permissions.administrator:
            guild = ctx.guild
            var1 = 0
            for role in guild.roles:
                if role.name == "Muted":
                    var2 = var1
                    continue
                else:
                    var1 += 1
            for channel in guild.channels:
                await channel.set_permissions(guild.roles[var2], send_messages=False)
            for rol in guild.roles:
                if rol.name == "Muted":
                    await member.add_roles(rol)
                    await ctx.send(f"{member.mention} has been muted, reason : {reason}")
        else:
            await ctx.send("You don't have permission to use that command!")


def setup(bot):
    bot.add_cog(AdminCommands(bot))
