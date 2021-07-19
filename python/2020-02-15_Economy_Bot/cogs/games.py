import discord
from discord.ext import commands

import random
import json
import os
import asyncio

currentpath = os.path.dirname(os.path.realpath(__file__))

def join(name):
    return os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), name)

def botembed(title):
    embed = discord.Embed(color=random.randint(0, 0xffffff))
    embed.set_author(name=title)
    return embed

def helpembed(prefix):
    embed = botembed("Help (Games)")
    embed.add_field(name="{}mastermind".format(prefix), value="Play a game of Mastermind. You have 10 attempts to guess a 5-character code.")
    embed.add_field(name="{}hangman".format(prefix), value="Play a game of Hangman. You have 7 attempts to correctly guess a word, one letter at a time.")
    embed.add_field(name="{}tictactoe [user mention] [bet]".format(prefix), value="Play a game of Tic-Tac-Toe. Select grid cells to get 3 in a row. You can also play with a second player, and bet a specific amount of coins.")
    embed.add_field(name="{}connect4 [user mention] [bet]".format(prefix), value="Play a game of Connect 4. Select columns to get 4 in a row. You can also play with a second player, and bet a specific amount of coins.")
    return embed

def read_coins(id):
    id = str(id)
    with open(join("economy.json")) as f:
        values = json.load(f)
        if id not in values.keys():
            return None
        else:
            return values[id]
        
def add_coins(id, amount):
    id = str(id)
    with open(join("economy.json")) as f:
        values = json.load(f)
        if id not in values.keys():
            values[id] = 0
        values[id] += amount
        with open(join("economy.json"), "w") as nf:
            json.dump(values, nf)

class Games(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def confirmation(self, ctx):
        values = [c for c in "0123456789"]
        code = ""
        for _ in range(4):
            code += random.choice(values)
        def check(message):
            return message.content == code and message.channel == ctx.message.channel and message.author == ctx.message.author
        embed = botembed("Economy")
        embed.add_field(name="Confirmation", value="Are you sure you want to proceed? Type `{}` to proceed.".format(code))
        message = await ctx.send(embed=embed)
        try:
            _ = await self.bot.wait_for("message", check=check, timeout=60.0)
        except asyncio.TimeoutError:
            return False, message
        else:
            return True, message

    @commands.command()
    async def mastermind(self, ctx):
        characters = ["A", "B", "C", "D"]
        code = ""
        for _ in range(5):
            code += random.choice(characters)
        attempts = 10
        embed = botembed("Game")
        embed.add_field(name="Mastermind", value="Enter a 5-character combination, using the characters `A`, `B`, `C` and `D`.")
        await ctx.send(embed=embed)
        def check(message):
            if message.author == ctx.message.author:
                if len(message.content) == len(code):
                    for character in message.content.upper().strip():
                        if character not in characters:
                            return False
                    return True
            else:
                return False
        while True:
            if attempts < 1:
                break
            message = await self.bot.wait_for("message", check=check)
            correct = 0
            for pos in range(len(code)):
                if code[pos] == message.content.upper()[pos]:
                    correct += 1
            if correct == len(code):
                embed = botembed("Game")
                embed.add_field(name="Outcome: WIN", value="The correct code was `{}`. <@{}> won **100 coins**!".format(code, message.author.id))
                add_coins(message.author.id, 100)
                await ctx.send(embed=embed)
                return
            else:
                attempts -= 1
                if attempts >= 1:
                    embed = botembed("Game")
                    embed.add_field(name="Incorrect code", value="{} character{} {} correct. \nYou have {} guess{} remaining.".format(correct, ("s" if correct != 1 else ""), ("were" if correct != 1 else "was"), attempts, ("es" if attempts > 1 else "")))
                    await ctx.send(embed=embed)
        embed = botembed("Game")
        embed.add_field(name="Outcome: LOSE", value="You lose! The correct code was `{}`".format(code))
        await ctx.send(embed=embed)

    @commands.command()
    async def hangman(self, ctx):
        with open(os.path.join(currentpath, "words.txt")) as f:
            wordlist = f.read().strip()
        wordlist = [w.strip().lower() for w in wordlist.split("\n")]
        alphabet = "abcdefghijklmnopqrstuvwxyz0123456789"
        masked = ""
        word = random.choice(wordlist)
        word = word.lower()
        for letter in word:
            if letter not in alphabet:
                masked += letter + " "
            else:
                masked += "_ "
        
        masked = masked.strip()
        attempts = 7
        guessed = []
        embed = botembed("Game")
        embed.set_footer(text="Guessed: " + ", ".join(guessed))
        embed.add_field(name="Hangman", value="Use the letters `A-Z` and numbers `0-9` to spell the word, or guess the word. \nCurrent word: `{}`".format(masked))
        await ctx.send(embed=embed)
        def check(message):
            content = message.content.lower()
            if word.strip().lower() == content.strip():
                return True
            if len(content) == 1:
                if message.author == ctx.message.author:
                    if content in alphabet:
                        return True
            return False
        while True:
            if attempts < 1:
                break
            message = await self.bot.wait_for("message", check=check)
            if message.content.strip().lower() == word:
                embed = botembed("Game")
                embed.add_field(name="Outcome: WIN", value="The correct word was `{}`. <@{}> won **{} coins**!".format(word, message.author.id, len(word) * 2))
                add_coins(message.author.id, len(word) * 2)
                await ctx.send(embed=embed)
                return
            if message.content.lower().strip() in guessed:
                embed = botembed("Game")
                embed.set_footer(text="Guessed: " + ", ".join(guessed))
                embed.add_field(name="Character already guessed", value="`{}` has already been guessed. \nYou have {} guess{} left. \nCurrent word: `{}`".format(message.content.strip().lower(), attempts, ("es" if attempts != 1 else ""), masked))
                await ctx.send(embed=embed)
                continue
            guessed.append(message.content.strip().lower())
            if message.content.strip().lower() not in word:
                attempts -= 1
                if attempts >= 1:
                    embed = botembed("Game")
                    embed.set_footer(text="Guessed: " + ", ".join(guessed))
                    embed.add_field(name="Incorrect character", value="`{}` is not in the word. \nYou have {} guess{} left. \nCurrent word: `{}`".format(message.content.strip().lower(), attempts, ("es" if attempts != 1 else ""), masked))
                    await ctx.send(embed=embed)
                
            else:
                temp = [c for c in masked if c != " "]
                for i in range(len(word)):
                    if word[i] == message.content.lower().strip():
                        temp[i] = message.content.lower().strip()              
                if masked.strip() == word:
                    embed = botembed("Game")
                    embed.add_field(name="Outcome: WIN", value="The correct word was `{}`. <@{}> won **{} coins**!".format(word, message.author.id, len(word) * 2))
                    add_coins(message.author.id, len(word) * 2)
                    await ctx.send(embed=embed)
                    return
                else:
                    masked = " ".join(temp)
                    embed = botembed("Game")
                    embed.set_footer(text="Guessed: " + ", ".join(guessed))
                    embed.add_field(name="Correct character", value="`{}` is in the word. \nYou have {} guess{} left. \nCurrent word: `{}`".format(message.content.strip().lower(), attempts, ("es" if attempts != 1 else ""), masked))
                    await ctx.send(embed=embed)
        embed = botembed("Game")
        embed.add_field(name="Outcome: LOSE", value="You lose! The correct word was `{}`".format(word))
        await ctx.send(embed=embed)

    @commands.command()
    async def tictactoe(self, ctx, p2=None, bet=None):
        players = 1
        if p2 is not None:
            if len(ctx.message.mentions) == 0:
                embed = botembed("Game")
                embed.add_field(name="Error", value="Invalid parameter - mention a user to play against them!")
                return await ctx.send(embed=embed)
            p2 = ctx.message.mentions[0]
            if p2.id == ctx.message.author.id:
                embed = botembed("Game")
                embed.add_field(name="Error", value="Invalid parameter - you can't play against yourself!")
                return await ctx.send(embed=embed)
            p1 = ctx.message.author

            if bet is None:
                bet = 0
            else:
                try:
                    bet = int(bet)
                except:
                    embed = botembed("Game")
                    embed.add_field(name="Error", value="Invalid parameter - amount of coins cannot be converted to integer.")
                    return await ctx.send(embed=embed)
            if bet < 0:
                embed = botembed("Game")
                embed.add_field(name="Error", value="Invalid parameter - you can't bet negative coins.")
                return await ctx.send(embed=embed)

            if read_coins(p2.id) is None and bet > 0:
                embed = botembed("Game")
                embed.add_field(name="Error", value="That user cannot afford this bet!")
                return await ctx.send(embed=embed)
            elif read_coins(p2.id) is None:
                add_coins(p2.id, 0)
            if read_coins(p2.id) < bet:
                embed = botembed("Game")
                embed.add_field(name="Error", value="That user cannot afford this bet!")
                return await ctx.send(embed=embed)

            
            embed = botembed("Game Request")
            embed.add_field(name="{}#{} has sent a game invite!".format(p1.name, p1.discriminator), value="{}#{} has sent you an invite to play `Tic-Tac-Toe`. \nIf you want to play, respond with `yes`. \nIf you do not want to play, ignore this message. \nThis invite will expire in 10 minutes.".format(p1.name, p1.discriminator))
            if bet != 0:
                embed.add_field(name="Bet", value="The game has a bet of **{} coin{}** attached. If you win, you get your coins and the opponent's coins.".format(bet, "s" if bet != 1 else ""))
            try:
                invite = await p2.send(embed=embed)
            except:
                embed = botembed("Game Request")
                embed.add_field(name="Error", value="The game request could not be sent. Most likely the user has disabled DMs.")
                return await ctx.send(embed=embed)
            
            embed = botembed("Game Request")
            embed.add_field(name="Game Request Sent", value="A request has been sent to <@{}>. Wait for a reply to start playing!".format(p2.id))
            await ctx.send(embed=embed)
            
            
            def invitecheck(message):
                if message.author.id == p2.id and message.channel.id == invite.channel.id:
                    return True
                return False 
            while True:
                try:
                    reply = await self.bot.wait_for("message", check=invitecheck, timeout=600.0)
                except asyncio.TimeoutError:
                    embed = botembed("Game Request")
                    embed.add_field(name="Expired", value="Game invite expired.")
                    await invite.edit(embed=embed)
                    embed = botembed("Game Request")
                    embed.add_field(name="Game Request Ignored", value="<@{}> has ignored your game request.".format(p2.id))
                    return await ctx.send(embed=embed)
                else:
                    if reply.content.strip().lower() == "yes":
                        break
            players = 2
            add_coins(p1.id, 0-bet)
            add_coins(p2.id, 0-bet)
        


        board = [
            [3, 3, 3],
            [3, 3, 3],
            [3, 3, 3]
        ]

        showboard = [
            ["`1`", "`2`", "`3`"],
            ["`4`", "`5`", "`6`"],
            ["`7`", "`8`", "`9`"]
        ]
        
        def getboard(board):
            printable = ""
            for line in board:
                newline = ""
                for item in line:
                    newline += item + " "
                printable += newline + "\n"
            return printable

        def isvalid(position, board):
            position -= 1
            flattened = []
            for line in board:
                for item in line:
                    flattened.append(item)
            if flattened[position] == 3:
                return True
            return False

        def chunks(l, n):
            for i in range(0, len(l), n):
                yield l[i:i+n]

        def place(self, turn, position, board, showboard):
            position = position - 1
            piece = ""
            if turn == 0:
                piece = "`X`"
            else:
                piece = "`O`"
            flattened = []
            for line in board:
                for item in line:
                    flattened.append(item)
            flattened[position] = turn
            board = list(chunks(flattened, 3))

            flattened = []
            for line in showboard:
                for item in line:
                    flattened.append(item)
            flattened[position] = piece
            showboard = list(chunks(flattened, 3))
            
            return board, showboard
            
        def win(turn, board):
            for line in board:
                if len(set(line)) == 1 and line[0] == turn:
                    return True
            for i in range(3):
                line = [l[i] for l in board]
                if len(set(line)) == 1 and line[0] == turn:
                    return True
            line = []
            for i in range(3):
                line.append(board[i][i])
            if len(set(line)) == 1 and line[0] == turn:
                return True
            line = []
            
            for i in range(3):
                line.append(board[2-i][i])
            if len(set(line)) == 1 and line[0] == turn:
                return True
            return False

        if players == 1:

            embed = botembed("Game")
            turn = random.randint(0, 1)
            aoran = ""
            if turn == 0:
                aoran = "You"
            else:
                aoran = "I"
                move = random.randint(1, 9)
                if isvalid(move, board):
                    board, showboard = place(self, turn, move, board, showboard)
            
            embed.add_field(name="Tic Tac Toe", value="Select grid cells using the numbers `1-9` to get three in a row. {} will go first.".format(aoran))
            if turn == 1:
                embed.add_field(name="Move", value="I will place a piece at position {}. It is now your turn.".format(move))
                turn = 0

            embed.add_field(name="Board", value="\n{}".format(getboard(showboard)))
            await ctx.send(embed=embed)
        
            def check(message):
                if message.author == ctx.message.author:
                    content = message.content
                    if len(content.strip()) == 1:
                        try:
                            content = int(content)
                        except:
                            return False
                        else:
                            if content > 9 or content < 1:
                                return False
                            if not isvalid(content, board):
                                return False
                            else:
                                return True
                return False

        else:
            order = [p1, p2]
            random.shuffle(order)

            currentplayer = ""

            def check(message):
                if message.author.id == currentplayer.id:
                    content = message.content
                    if content.strip().lower() == "quit":
                        return True
                    if len(content.strip()) == 1:
                        try:
                            content = int(content)
                        except:
                            return False
                        else:
                            if content > 9 or content < 1:
                                return False
                            if not isvalid(content, board):
                                return False
                            else:
                                return True
            


        def tie(board):
            flattened = []
            for line in board:
                for item in line:
                    flattened.append(item)
            for i in range(2):
                if win(i, board):
                    return False
            for item in flattened:
                if item == 3:
                    return False
            return True
        

        while True:
            if players == 1:
                message = await self.bot.wait_for("message", check=check)
                move = int(message.content.strip())
                board, showboard = place(self, turn, move, board, showboard)
                embed = botembed("Game")
                if win(turn, board):
                    embed.add_field(name="Outcome: WIN", value="You won! You recieved **50 coins**!")
                    add_coins(ctx.message.author.id, 50)
                    embed.add_field(name="Board", value=getboard(showboard))
                    return await ctx.send(embed=embed)
                elif tie(board):
                    embed.add_field(name="Outcome: TIE", value="We tied! There is no winner.")
                    embed.add_field(name="Board", value=getboard(showboard))
                    return await ctx.send(embed=embed)
                turn = 1
                embed.add_field(name="Move", value="It is now my turn...")
                embed.add_field(name="Board", value=getboard(showboard))
                message = await ctx.send(embed=embed)
                await asyncio.sleep(3)
                while True:
                    position = random.randint(1, 9)
                    if isvalid(position, board):
                        break
                board, showboard = place(self, turn, position, board, showboard)
                if win(turn, board):
                    embed.add_field(name="Outcome: LOSE", value="You lost!")
                    embed.add_field(name="Board", value=getboard(showboard))
                    return await ctx.send(embed=embed)
                elif tie(board):
                    embed.add_field(name="Outcome: TIE", value="We tied! There is no winner.")
                    embed.add_field(name="Board", value=getboard(showboard))
                    return await ctx.send(embed=embed)
                embed = botembed("Game")
                embed.add_field(name="Move", value="I will place a piece at position {}. It is now your turn.".format(position))
                embed.add_field(name="Board", value=getboard(showboard))
                await message.edit(embed=embed)
                turn = 0
            else:
                for i in range(2):
                    currentplayer = order[i]
                    embed = botembed("Game")
                    embed.add_field(name="Move", value="It is now your turn. Use numbers `1-9` to place a piece on the board, or type `quit` to forfeit. If you forfeit, you lose all betted coins.")
                    embed.add_field(name="Board", value=getboard(showboard))
                    await ctx.send("<@{}>".format(currentplayer.id), embed=embed)
                    message = await self.bot.wait_for("message", check=check)
                    if message.content.strip().lower() == "quit":
                        forfeit, message = await self.confirmation(ctx)
                        if forfeit:
                            await message.delete()
                            embed = botembed("Game")
                            embed.add_field(name="Outcome: WIN", value="<@{}> won!".format(order[(i + 1) % 2].id))
                            embed.add_field(name="Board", value=getboard(showboard))
                            add_coins(order[(i + 1) % 2].id, 2 * bet)
                            return await ctx.send(embed=embed)
                        embed.add_field(name="Outcome: WIN", value="<@{}> won!".format(currentplayer.id))
                        embed.add_field(name="Board", value=getboard(showboard))
                        add_coins(currentplayer.id, 2 * bet)
                        return await ctx.send(embed=embed)
                    move = int(message.content.strip())
                    board, showboard = place(self, i, move, board, showboard)
                    embed = botembed("Game")
                    if win(i, board):
                        embed.add_field(name="Outcome: WIN", value="<@{}> won!".format(currentplayer.id))
                        embed.add_field(name="Board", value=getboard(showboard))
                        add_coins(currentplayer.id, 2 * bet)
                        return await ctx.send(embed=embed)
                    elif tie(board):
                        embed.add_field(name="Outcome: TIE", value="Both players tied! There is no winner.")
                        embed.add_field(name="Board", value=getboard(showboard))
                        for player in order:
                            add_coins(player.id, bet)
                        return await ctx.send(embed=embed)


    @commands.command()
    async def connect4(self, ctx, p2=None, bet=None):
        players = 1
        if p2 is not None:
            if len(ctx.message.mentions) == 0:
                embed = botembed("Game")
                embed.add_field(name="Error", value="Invalid parameter - mention a user to play against them!")
                return await ctx.send(embed=embed)
            p2 = ctx.message.mentions[0]
            if p2.id == ctx.message.author.id:
                embed = botembed("Game")
                embed.add_field(name="Error", value="Invalid parameter - you can't play against yourself!")
                return await ctx.send(embed=embed)
            p1 = ctx.message.author

            if bet is None:
                bet = 0
            else:
                try:
                    bet = int(bet)
                except:
                    embed = botembed("Game")
                    embed.add_field(name="Error", value="Invalid parameter - amount of coins cannot be converted to integer.")
                    return await ctx.send(embed=embed)
            if bet < 0:
                embed = botembed("Game")
                embed.add_field(name="Error", value="Invalid parameter - you can't bet negative coins.")
                return await ctx.send(embed=embed)

            if read_coins(p2.id) is None and bet > 0:
                embed = botembed("Game")
                embed.add_field(name="Error", value="That user cannot afford this bet!")
                return await ctx.send(embed=embed)
            elif read_coins(p2.id) is None:
                add_coins(p2.id, 0)
            if read_coins(p2.id) < bet:
                embed = botembed("Game")
                embed.add_field(name="Error", value="That user cannot afford this bet!")
                return await ctx.send(embed=embed)


            
            embed = botembed("Game Request")
            embed.add_field(name="{}#{} has sent a game invite!".format(p1.name, p1.discriminator), value="{}#{} has sent you an invite to play `Connect 4`. \nIf you want to play, respond with `yes`. \nIf you do not want to play, ignore this message. \nThis invite will expire in 10 minutes.".format(p1.name, p1.discriminator))
            if bet != 0:
                embed.add_field(name="Bet", value="The game has a bet of **{} coin{}** attached. If you win, you get your coins and the opponent's coins.".format(bet, "s" if bet != 1 else ""))
            try:
                invite = await p2.send(embed=embed)
            except:
                embed = botembed("Game Request")
                embed.add_field(name="Error", value="The game request could not be sent. Most likely the user has disabled DMs.")
                return await ctx.send(embed=embed)
            
            embed = botembed("Game Request")
            embed.add_field(name="Game Request Sent", value="A request has been sent to <@{}>. Wait for a reply to start playing!".format(p2.id))
            await ctx.send(embed=embed)
            
            
            def invitecheck(message):
                if message.author.id == p2.id and message.channel.id == invite.channel.id:
                    return True
                return False 
            while True:
                try:
                    reply = await self.bot.wait_for("message", check=invitecheck, timeout=600.0)
                except asyncio.TimeoutError:
                    embed = botembed("Game Request")
                    embed.add_field(name="Expired", value="Game invite expired.")
                    await invite.edit(embed=embed)
                    embed = botembed("Game Request")
                    embed.add_field(name="Game Request Ignored", value="<@{}> has ignored your game request.".format(p2.id))
                    return await ctx.send(embed=embed)
                else:
                    if reply.content.strip().lower() == "yes":
                        break
            players = 2
            add_coins(p1.id, 0-bet)
            add_coins(p2.id, 0-bet)
        


        board = [
            [3, 3, 3, 3, 3, 3, 3],
            [3, 3, 3, 3, 3, 3, 3],
            [3, 3, 3, 3, 3, 3, 3],
            [3, 3, 3, 3, 3, 3, 3],
            [3, 3, 3, 3, 3, 3, 3],
            [3, 3, 3, 3, 3, 3, 3]
        ]

        showboard = [
            ["`■`", "`■`", "`■`", "`■`", "`■`", "`■`", "`■`"], 
            ["`■`", "`■`", "`■`", "`■`", "`■`", "`■`", "`■`"], 
            ["`■`", "`■`", "`■`", "`■`", "`■`", "`■`", "`■`"], 
            ["`■`", "`■`", "`■`", "`■`", "`■`", "`■`", "`■`"], 
            ["`■`", "`■`", "`■`", "`■`", "`■`", "`■`", "`■`"], 
            ["`■`", "`■`", "`■`", "`■`", "`■`", "`■`", "`■`"]
        ]
        
        def getboard(board):
            printable = ""
            for line in board:
                newline = ""
                for item in line:
                    newline += item + " "
                printable += newline + "\n"
            return printable

        def isvalid(position, board):
            position -= 1
            if board[0][position] == 3:
                return True
            return False

        def place(self, turn, position, board, showboard):
            position = position - 1
            piece = ""
            if turn == 0:
                piece = "`X`"
            else:
                piece = "`O`"
            
            column = [line[position] for line in board].copy()[::-1]
            row = 5 - column.index(3)

            board[row][position] = turn
            showboard[row][position] = piece

            return board, showboard
            
        def win(turn, board):
            ROW_COUNT = 6
            COLUMN_COUNT = 7
            WINDOW_COUNT = 4
            for r in range(ROW_COUNT):
                row_array = [i for i in list(board[r][:])]
                for c in range(COLUMN_COUNT - (WINDOW_COUNT - 1)):
                    window = row_array[c:c+WINDOW_COUNT]
                    if window.count(turn) == 4:
                        return True

            for c in range(COLUMN_COUNT):
                col_array = []
                for row in board:
                    col_array.append(row[c])
                for r in range(ROW_COUNT - (WINDOW_COUNT - 1)):
                    window = col_array[r:r+WINDOW_COUNT]
                    if window.count(turn) == 4:
                        return True

            for r in range(ROW_COUNT - 3):
                for c in range(COLUMN_COUNT - 3):
                    window = [board[r+i][c+i] for i in range(WINDOW_COUNT)]
                    if window.count(turn) == 4:
                        return True

            for r in range(len(board) - 3):
                for c in range(len(board[0]) - 3):
                    window = [board[r+3-i][c+i] for i in range(WINDOW_COUNT)]
                    if window.count(turn) == 4:
                        return True
            return False

        if players == 1:

            embed = botembed("Game")
            turn = random.randint(0, 1)
            aoran = ""
            if turn == 0:
                aoran = "You"
            else:
                aoran = "I"
                move = random.randint(1, 7)
                if isvalid(move, board):
                    board, showboard = place(self, turn, move, board, showboard)
            
            embed.add_field(name="Tic Tac Toe", value="Select columns using the numbers `1-7` to get 4 in a row. {} will go first.".format(aoran))
            if turn == 1:
                embed.add_field(name="Move", value="I will place a piece in column {}. It is now your turn.".format(move))
                turn = 0

            embed.add_field(name="Board", value="\n{}".format(getboard(showboard)))
            await ctx.send(embed=embed)
        
            def check(message):
                if message.author == ctx.message.author:
                    content = message.content
                    if len(content.strip()) == 1:
                        try:
                            content = int(content)
                        except:
                            return False
                        else:
                            if content > 7 or content < 1:
                                return False
                            if not isvalid(content, board):
                                return False
                            else:
                                return True
                return False

        else:
            order = [p1, p2]
            random.shuffle(order)

            currentplayer = ""

            def check(message):
                if message.author.id == currentplayer.id:
                    content = message.content
                    if content.strip().lower() == "quit":
                        return True
                    if len(content.strip()) == 1:
                        try:
                            content = int(content)
                        except:
                            return False
                        else:
                            if content > 7 or content < 1:
                                return False
                            if not isvalid(content, board):
                                return False
                            else:
                                return True
            


        def tie(board):
            for i in range(7):
                if board[0][i] == 3:
                    return False
            return True
        

        while True:
            if players == 1:
                message = await self.bot.wait_for("message", check=check)
                move = int(message.content.strip())
                board, showboard = place(self, turn, move, board, showboard)
                embed = botembed("Game")
                if win(turn, board):
                    embed.add_field(name="Outcome: WIN", value="You won! You recieved **50 coins**!")
                    add_coins(ctx.message.author.id, 50)
                    embed.add_field(name="Board", value=getboard(showboard))
                    return await ctx.send(embed=embed)
                elif tie(board):
                    embed.add_field(name="Outcome: TIE", value="We tied! There is no winner.")
                    embed.add_field(name="Board", value=getboard(showboard))
                    return await ctx.send(embed=embed)
                turn = 1
                embed.add_field(name="Move", value="It is now my turn...")
                embed.add_field(name="Board", value=getboard(showboard))
                message = await ctx.send(embed=embed)
                await asyncio.sleep(3)
                while True:
                    position = random.randint(1, 7)
                    if isvalid(position, board):
                        break
                board, showboard = place(self, turn, position, board, showboard)
                if win(turn, board):
                    embed.add_field(name="Outcome: LOSE", value="You lost!")
                    embed.add_field(name="Board", value=getboard(showboard))
                    return await ctx.send(embed=embed)
                elif tie(board):
                    embed.add_field(name="Outcome: TIE", value="We tied! There is no winner.")
                    embed.add_field(name="Board", value=getboard(showboard))
                    return await ctx.send(embed=embed)
                embed = botembed("Game")
                embed.add_field(name="Move", value="I will place a piece in column {}. It is now your turn.".format(position))
                embed.add_field(name="Board", value=getboard(showboard))
                await message.edit(embed=embed)
                turn = 0
            else:
                for i in range(2):
                    currentplayer = order[i]
                    embed = botembed("Game")
                    embed.add_field(name="Move", value="It is now your turn. Use numbers `1-7` to place a piece in a column on the board, or type `quit` to forfeit. If you forfeit, you lose all betted coins.")
                    embed.add_field(name="Board", value=getboard(showboard))
                    await ctx.send("<@{}>".format(currentplayer.id), embed=embed)
                    message = await self.bot.wait_for("message", check=check)
                    if message.content.strip().lower() == "quit":
                        forfeit, message = await self.confirmation(ctx)
                        if forfeit:
                            await message.delete()
                            embed = botembed("Game")
                            embed.add_field(name="Outcome: WIN", value="<@{}> won!".format(order[(i + 1) % 2].id))
                            embed.add_field(name="Board", value=getboard(showboard))
                            add_coins(order[(i + 1) % 2].id, 2 * bet)
                            return await ctx.send(embed=embed)
                        embed.add_field(name="Outcome: WIN", value="<@{}> won!".format(currentplayer.id))
                        embed.add_field(name="Board", value=getboard(showboard))
                        add_coins(currentplayer.id, 2 * bet)
                        return await ctx.send(embed=embed)
                    move = int(message.content.strip())
                    board, showboard = place(self, i, move, board, showboard)
                    embed = botembed("Game")
                    if win(i, board):
                        embed.add_field(name="Outcome: WIN", value="<@{}> won!".format(currentplayer.id))
                        embed.add_field(name="Board", value=getboard(showboard))
                        add_coins(currentplayer.id, 2 * bet)
                        return await ctx.send(embed=embed)
                    elif tie(board):
                        embed.add_field(name="Outcome: TIE", value="Both players tied! There is no winner.")
                        embed.add_field(name="Board", value=getboard(showboard))
                        for player in order:
                            add_coins(player.id, bet)
                        return await ctx.send(embed=embed)




def setup(bot):
    bot.add_cog(Games(bot))