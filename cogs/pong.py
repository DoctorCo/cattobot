import discord
from discord.ext import commands, tasks
import random
import asyncio


class PongCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.boards = {}
        self.balls = {}
        self.points = {}  # {123456789: [{123456789876: 4}, {987654321234: 3}]
        self.messages2 = {}
        self.messages1 = {}

    @commands.command()
    async def pong(self, ctx):

        await ctx.send(f"Player 2, send any message in this channel")

        def check(m):
            return m.channel == ctx.channel and m.author != m.guild.me and m.author != ctx.author
        newMessage = await self.bot.wait_for("message", check=check, timeout=60)
        message = await ctx.send(embed=discord.Embed(description=self.displayboard([[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                             [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                             [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                             [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                             [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                             [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2],
                             [0, 0, 0, 0, 0, 0, 0, 0, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2],
                             [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2],
                             [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2],
                             [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]])))
        self.boards[str(message.id)] = [[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                             [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                             [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                             [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                             [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                             [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2],
                             [0, 0, 0, 0, 0, 0, 0, 0, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2],
                             [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2],
                             [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2],
                             [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]
        self.balls[str(message.id)] = [1, 1]
        self.points[str(message.id)] = [{"name": str(ctx.author), "points": 0}, {"name": str(newMessage.author), "points": 0}]
        self.messages2[str(newMessage.author.id)] = message.id
        await message.add_reaction("⬆")
        await message.add_reaction("⬇")
        await message.add_reaction("⏹")
        self.messages1[str(ctx.author.id)] = message.id
        self.game.start(message.id, ctx)

    @tasks.loop()
    async def game(self, id, ctx):
        self.move_ball(str(id))
        message = await ctx.message.channel.fetch_message(int(self.messages1[str(ctx.author.id)]))
        await message.edit(
            embed=discord.Embed(
                title=f"{self.points[str(message.id)][0]['name']}: {self.points[str(message.id)][0]['points']}           {self.points[str(message.id)][1]['name']}: {self.points[str(message.id)][1]['points']}",
                description=self.displayboard(self.boards[str(message.id)])))
        await asyncio.sleep(.25)

    def move_ball(self, id):
        ball = self.balls[id]
        board = self.boards[id]
        points = self.points[id]
        ball_pos = []
        for x in range(len(board)):
            if 3 in board[x]:
                ball_pos.append(x)
                for i in range(len(board[x])):
                    if board[x][i] == 3:
                        board[x][i] = 0
                        if 9 >= x+ball[1] >= 0:
                            if i + ball[0] >= 19:
                                points[0]["points"] += 1
                                board[5][9] = 3
                            elif i + ball[0] <= -1:
                                points[1]["points"] += 1
                                board[5][9] = 3
                            elif board[x + ball[1]][i + ball[0]] == 1 or board[x + ball[1]][i + ball[0]] == 2:
                                ball[0] *= -1
                                board[x + ball[1]][i + ball[0]] = 3
                            elif 18 >= i+ball[0] >= 0:
                                if board[x + ball[1]][i + ball[0]] == 1 or board[x + ball[1]][i + ball[0]] == 2:
                                    ball[0] *= -1
                                else:
                                    board[x + ball[1]][i + ball[0]] = 3
                        else:
                            ball[1] *= -1
                            board[x + ball[1]][i + ball[0]] = 3
                        ball_pos.append(i)
                        break
                break
        self.balls[id] = ball
        self.points[id] = points
        self.boards[id] = board


    @commands.Cog.listener()
    async def on_reaction_add(self, reaction, user):
        if str(user.id) in self.messages1.keys():
            if str(reaction) == '<a:up:785562023256915978>':
                self.boards[str(reaction.message.id)] = self.getpos(str(reaction.message.id), "player1", "up")
                message = await reaction.message.channel.fetch_message(int(self.messages1[str(user.id)]))
                await message.remove_reaction(reaction, user)
                await message.edit(embed=discord.Embed(title=f"{self.points[str(message.id)][0]['name']}: {self.points[str(message.id)][0]['points']}           {self.points[str(message.id)][1]['name']}: {self.points[str(message.id)][1]['points']}",
                                                       description=self.displayboard(self.boards[str(reaction.message.id)])))
            elif str(reaction) == '<a:down:785574282171645972>':
                self.boards[str(reaction.message.id)] = self.getpos(str(reaction.message.id), "player1", "down")
                message = await reaction.message.channel.fetch_message(int(self.messages1[str(user.id)]))
                await message.remove_reaction(reaction, user)
                await message.edit(embed=discord.Embed(title=f"{self.points[str(message.id)][0]['name']}: {self.points[str(message.id)][0]['points']}           {self.points[str(message.id)][1]['name']}: {self.points[str(message.id)][1]['points']}",
                                                       description=self.displayboard(self.boards[str(reaction.message.id)])))
            elif str(reaction) == "<:stop:785636300178325554>":
                self.game.stop()
                self.boards[str(reaction.message.id)] = self.getpos(str(reaction.message.id), "player2", "down")
                message = await reaction.message.channel.fetch_message(int(self.messages2[str(user.id)]))
                await message.remove_reaction(reaction, user)
                embed = discord.Embed(
                    title=f"{self.points[str(message.id)][0]['name']}: {self.points[str(message.id)][0]['points']}           {self.points[str(message.id)][1]['name']}: {self.points[str(message.id)][1]['points']}",
                    description=self.displayboard(self.boards[str(reaction.message.id)]))
                embed.set_footer(
                    text=f"This game has ended. Winner: {self.points[str(message.id)][0]['name'] if self.points[str(message.id)][0]['points'] > self.points[str(message.id)][1]['points'] else self.points[str(message.id)][1]['name']}")
                await message.edit(embed=embed)
        elif str(user.id) in self.messages2.keys():
            if str(reaction) == '<a:up:785562023256915978>':
                self.boards[str(reaction.message.id)] = self.getpos(str(reaction.message.id), "player2", "up")
                message = await reaction.message.channel.fetch_message(int(self.messages2[str(user.id)]))
                await message.remove_reaction(reaction, user)
                await message.edit(embed=discord.Embed(title=f"{self.points[str(message.id)][0]['name']}: {self.points[str(message.id)][0]['points']}           {self.points[str(message.id)][1]['name']}: {self.points[str(message.id)][1]['points']}",
                                                       description=self.displayboard(self.boards[str(reaction.message.id)])))
            elif str(reaction) == '<a:down:785574282171645972>':
                self.boards[str(reaction.message.id)] = self.getpos(str(reaction.message.id), "player2", "down")
                message = await reaction.message.channel.fetch_message(int(self.messages2[str(user.id)]))
                await message.remove_reaction(reaction, user)
                await message.edit(embed=discord.Embed(title=f"{self.points[str(message.id)][0]['name']}: {self.points[str(message.id)][0]['points']}           {self.points[str(message.id)][1]['name']}: {self.points[str(message.id)][1]['points']}",
                                                       description=self.displayboard(self.boards[str(reaction.message.id)])))
            elif str(reaction) == "<:stop:785636300178325554>":
                self.game.stop()
                self.boards[str(reaction.message.id)] = self.getpos(str(reaction.message.id), "player2", "down")
                message = await reaction.message.channel.fetch_message(int(self.messages2[str(user.id)]))
                await message.remove_reaction(reaction, user)
                embed = discord.Embed(
                    title=f"{self.points[str(message.id)][0]['name']}: {self.points[str(message.id)][0]['points']}           {self.points[str(message.id)][1]['name']}: {self.points[str(message.id)][1]['points']}",
                    description=self.displayboard(self.boards[str(reaction.message.id)]))
                embed.set_footer(text=f"This game has ended. Winner: {self.points[str(message.id)][0]['name'] if self.points[str(message.id)][0]['points'] > self.points[str(message.id)][1]['points'] else self.points[str(message.id)][1]['name']}")
                await message.edit(embed=embed)

    def getpos(self, id, player, direction):
        board = self.boards[str(id)]
        top = 0
        if player == "player1":
            for x in range(len(board)):
                if 1 in board[x]:
                    top = x
                    break
            if direction == "up":
                if top != 0:
                    board[top-1][0] = 1
                    board[top+3][0] = 0
            elif direction == "down":
                if top != 6:
                    board[top][0] = 0
                    board[top+4][0] = 1
        elif player == "player2":
            for x in range(len(board)):
                if 2 in board[x]:
                    top = x
                    break
            if direction == "up":
                if top != 0:
                    board[top-1][-1] = 2
                    board[top+3][-1] = 0
            elif direction == "down":
                if top != 6:
                    board[top][-1] = 0
                    board[top+4][-1] = 2

        return board


    def displayboard(self, board):
        description = ''
        for i in board:
            for j in i:
                if j == 1:
                    description += '🟩'
                elif j == 2:
                    description += '🟦'
                elif j == 0:
                    description += '⬛'
                elif j == 3:
                    description += '🟥'
            description += '\n'
        return description

    @commands.command()
    async def pongboard(self, ctx):
        embed = discord.Embed(title=f"PONG!!!", description=f'''
⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛
⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛
⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛
⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛
⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛
⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛
⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛
⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛
⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛
⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛
''')
        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(PongCog(bot))