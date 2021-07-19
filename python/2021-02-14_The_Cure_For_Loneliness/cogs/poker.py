import discord
from pypokerengine.players import BasePokerPlayer
from pypokerengine.utils.card_utils import gen_cards, estimate_hole_card_win_rate
from discord.ext import commands
import functions
import random

NB_SIMULATION = 1000

rounds = 5
ante = 10
starting = 150

def process_hand(hand):
    hand = [c.replace("S", "♠").replace("D", "♦").replace("C", "♣").replace("H", "♥") for c in hand]
    return hand


def botembed(title):
    embed = functions.embed("Poker - " + title, color=0x8f0000)
    return embed

def error(errormsg):
    embed = functions.error("Poker", errormsg)
    return embed

class PokerGame(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.playing = False
        self.config = None

    @commands.command()
    async def poker(self, ctx, players=4):
        
        if self.playing:
            embed = error("🚫 " + self.bot.response(2) + " we're already playing a game of Poker right now!")
            return await ctx.send(embed=embed)
        self.playing = True
        
        players = min(max(players, 2), 23) # (23 players * 2 cards per hand) + 5 cards in the center at most = 51 cards, the highest number possible for a 52 card deck 

        players -= 2
        if players > 0:
            characters = self.bot.get_characters(players)
        else:
            characters = {}
        opponents = characters.copy()
        #self.manual = Manual(self.bot, ctx, characters.copy())
        characters["Me"] = ["I", "Me", "My"]
        characters["You"] = ["You", "You", "Your"]
        
        embed = botembed("Game Started")
        fstring = ""
        ops = list(opponents.keys())
        if len(ops) > 2:
            fstring = ", ".join(ops[:-1]) + ", and " + ops[-1]
        elif len(ops) == 2:
            fstring = ops[0] + " and " + ops[1]
        elif len(ops) == 1:
            fstring = ops[0]
        if len(ops) > 0:
            fstring = fstring + " also decided to play!\n"
        embed.description = "🃏 " + self.bot.response(1) + " I started a game of Poker for us.\n{}Type `start` to start the game.".format(fstring)
        await ctx.send(embed=embed)
        
        m = await self.bot.wait_for("message", check=lambda m: m.channel == ctx.channel and m.author == ctx.message.author and m.content.strip().lstrip().lower() == "start")

        
        wallets = {}
        for c in characters:
            wallets[c] = starting

        can_play = list(characters.keys())

        for r in range(rounds):
            current_r = r + 1
            deck = []
            hands = {}
            community = []
            playing = can_play.copy()
            pot = 0
            for suit in ("D", "C", "H", "S"):
                for value in ("A", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K"):
                    deck.append(suit + value)

            random.shuffle(deck)


            for character in playing:
                hands[character] = deck[:2]
                del deck[:2]
            
            for c in playing:
                wallets[c] -= ante
                pot += ante
            turn = 0
            
            while True:
                
                actions = []
                calls = []
                
                turn += 1
                if turn == 1:
                    actions.append("ante")
                if turn == 2:
                    community = deck[:3]
                elif turn == 3:
                    community = deck[:4]
                elif turn == 4:
                    community = deck[:5]
                    embed = botembed("Turn Over")
                    desc = "```Round {} // Turn {}```".format(current_r, turn)
                    
                    for play in actions:
                        if play == "ante":
                            desc = desc + "\n**All of us** paid the ante of `${}`.".format(ante)
                            continue
                        name = play[0]
                        action = play[1]
                        amount = play[2]
                        name = play[0]
                        if name == "Me":
                            name = "I"
                        if action == "fold":
                            action = " folded."
                        
                        if action == "call":
                            action = " called"
                        if action == "raise":
                            action = " raised"
                        string = f"**{name}** {action}"
                        if action != " folded.":
                            string = string + f" `${amount}`."

                        desc = desc + "\n" + string

                    desc = desc + "\n__Wallets__\n"

                    for person in wallets:
                        x = person
                        y = wallets[person]
                        desc = desc + f"**{x}**: `${y}`\n"

                        
                    if len(community) > 0:
                        cstring = "Community card: `" + ', '.join(process_hand(community)) + "`\n"
                    else:
                        cstring = ""    

                    desc = desc + "\n__Hands__\n"
                    for c in hands:
                        if c != "You":
                            desc = desc + "**{}**: `{}`\n".format(c, ", ".join(process_hand(hands[c])))
                    
                    hole_card = hands["You"].copy()
                    desc = desc + f"\n__Game Info__\nThere is `${pot}` in the pot.\n{cstring}Your hand: `{', '.join(process_hand(hole_card))}`\n\nType `continue` to continue."

                    embed.description = desc

                    await ctx.send(embed=embed)

                    await self.bot.wait_for("message", check=lambda m: m.channel == ctx.channel 
                    and m.author == ctx.message.author 
                    and m.content.lower().strip().lstrip() == "continue")

                    import score_hand
                    
                    char = playing[0]
                    hand = hands[char].copy()
                    hand = [c[::-1] for c in hand]
                    c = community.copy()
                    c = [card[::-1] for card in c]
                    s = score_hand.evaluate_hand(score_hand.get_best_hand(hand + c))

                    highest_scoring = s
                    winning = [char]
                    scores = []
                    scores.append(s)
                    highest = ["High card", "One pair", "Two pair", "Three of a kind", "Full house", "Four of a kind", "Flush", "Straight", "Straight flush", "Royal flush"]
                    for p in playing[1:]:
                        hand = hands[p].copy()
                        hand = [c[::-1] for c in hand]
                        c = community.copy()
                        c = [card[::-1] for card in c]
                        s = score_hand.evaluate_hand(score_hand.get_best_hand(hand + c))
                        scores.append(s)
                        if highest.index(s) > highest.index(highest_scoring):
                            highest_scoring = s
                            winning = [p]
                        elif highest.index(s) == highest.index(highest_scoring):
                            winning.append(p)
                    embed = botembed("Round Over")
                    desc = "```Round {}```\n".format(current_r)
                    winners = winning
                    for index in range(len(winners)):
                        if winners[index] == "You":
                            winners[index] = "you"
                        if winners[index] == "Me":
                            winners[index] = "I"
                    if "I" in winners:
                        copy1 = winners.index("I")
                        copy2 = winners[-1]
                        winners[copy1] = copy2
                        winners[-1] = "I"
                    if len(winning) == 1:
                        if winning[0] != "You":
                            if winning[0] != "I":
                                aoran = characters[winning[0]][0]
                            else:
                                aoran = "I"
                        else:
                            aoran = "You"
                        desc = desc + "🃏 All hands have been tallied up.\nWith a {}, {} won! {}\n{} won the pot of `${}`.".format(highest_scoring.lower(), winning[0], self.bot.response(5) if playing[0] != "Me" else "", aoran, pot)
                    elif len(winning) == 2:
                        desc = desc + "🃏 All hands have been tallied up.\nWith a {}, {} and {} have tied! {}\n{} won an equal share of the pot of `${}`, recieving `${}` each.".format(highest_scoring.lower(), winning[0], winning[1], self.bot.response(5) if playing[0] != "Me" else "", "We've" if "i" in [w.lower() for w in winners] else "You guys have" if "you" in [w.lower() for w in winners] else "They've", pot, pot // len(winners))
                    elif len(winning) > 2:
                        desc = desc + "🃏 All hands have been tallied up.\nWith a {}, {} and {} have tied! {}\n{} won an equal share of the pot of `${}`, recieving `${}` each.".format(highest_scoring.lower(), ", ".join(winning[:-1]), winning[-1], self.bot.response(5) if playing[0] != "Me" else "", "We've" if "i" in [w.lower() for w in winners] else "You guys have" if "you" in [w.lower() for w in winners] else "They've", pot, pot // len(winners))

                    for index in range(len(winners)):
                        if winners[index] == "you":
                            winners[index] = "You"
                        if winners[index] == "I":
                            winners[index] = "Me"
                    for winner in winners:
                        wallets[winner] += pot // len(winners)
                    pot = 0

                    for c in [c for c in list(wallets.keys()) if wallets[c] <= 0]:
                        can_play.remove(c)
                    
                    desc = desc + "\n\nType `continue` to continue."
                    embed.description = desc
                    
                    await ctx.send(embed=embed)
                    await self.bot.wait_for("message", check=lambda m: m.channel == ctx.channel 
                    and m.author == ctx.message.author 
                    and m.content.lower().strip().lstrip() == "continue")
                    break


                if len(playing) == 1:
                    embed = botembed("Turn Over")
                    desc = "```Round {} // Turn {}```\n".format(current_r, turn)
                    desc = desc + "__Actions__"
                    #input()
                    for play in actions:
                        if play == "ante":
                            desc = desc + "\n**All of us** paid the ante of `${}`.".format(ante)
                            continue
                        name = play[0]
                        action = play[1]
                        amount = play[2]
                        name = play[0]
                        if name == "Me":
                            name = "I"
                        if action == "fold":
                            action = " folded."
                        
                        if action == "call":
                            action = " called"
                        if action == "raise":
                            action = " raised"
                        string = f"**{name}** {action}"
                        if action != " folded.":
                            string = string + f" `${amount}`."

                        desc = desc + "\n" + string

                    desc = desc + "\n\n__Wallets__\n"

                    for person in wallets:
                        x = person
                        y = wallets[person]
                        desc = desc + f"**{x}**: `${y}`\n"

                        
                    if len(community) > 0:
                        cstring = "Community card: `" + ', '.join(process_hand(community)) + "`\n"
                    else:
                        cstring = ""    
                    
                    hole_card = hands["You"].copy()
                    desc = desc + f"\n__Game Info__\nThere is `${pot}` in the pot.\n{cstring}Your hand: `{', '.join(process_hand(hole_card))}`\n\nType `continue` to continue."

                    embed.description = desc

                    await ctx.send(embed=embed)

                    await self.bot.wait_for("message", check=lambda m: m.channel == ctx.channel 
                    and m.author == ctx.message.author 
                    and m.content.lower().strip().lstrip() == "continue")

                    embed = botembed("Round Over")
                    desc = "```Round {}```\n".format(current_r)
                    aoran = characters[playing[0]][0]
                    embed.description = desc + "🃏 All but one of us has folded.\n{} won the round! {}\n{} won the pot of `${}`. \n\nType `continue` to continue.".format("I" if playing[0] == "Me" else playing[0], self.bot.response(5) if playing[0] != "Me" else "", aoran, pot)
                    await ctx.send(embed=embed)
                    wallets[playing[0]] += pot
                    pot = 0
                    await self.bot.wait_for("message", check=lambda m: m.channel == ctx.channel 
                    and m.author == ctx.message.author 
                    and m.content.lower().strip().lstrip() == "continue")
                    break
                end_early = False
                async with ctx.channel.typing():
                    if "You" in playing:
                        goahead = playing[:-1]
                    else:
                        goahead = playing
                    for c in goahead:
                        if len(playing) == 1:
                            embed = botembed("Turn Over")
                            desc = "```Round {} // Turn {}```\n".format(current_r, turn)
                            desc = desc + "__Actions__"
                            #input()
                            for play in actions:
                                name = play[0]
                                action = play[1]
                                amount = play[2]
                                name = play[0]
                                if name == "Me":
                                    name = "I"
                                if action == "fold":
                                    action = " folded."
                                
                                if action == "call":
                                    action = " called"
                                if action == "raise":
                                    action = " raised"
                                string = f"**{name}** {action}"
                                if action != " folded.":
                                    string = string + f" `${amount}`."

                                desc = desc + "\n" + string

                            desc = desc + "\n\n__Wallets__\n"

                            for person in wallets:
                                x = person
                                y = wallets[person]
                                desc = desc + f"**{x}**: `${y}`\n"

                                
                            if len(community) > 0:
                                cstring = "Community card: `" + ', '.join(process_hand(community)) + "`\n"
                            else:
                                cstring = ""    
                            
                            hole_card = hands["You"].copy()
                            desc = desc + f"\n__Game Info__\nThere is `${pot}` in the pot.\n{cstring}Your hand: `{', '.join(process_hand(hole_card))}`\n\nType `continue` to continue."

                            embed.description = desc

                            await ctx.send(embed=embed)


                            await self.bot.wait_for("message", check=lambda m: m.channel == ctx.channel 
                            and m.author == ctx.message.author 
                            and m.content.lower().strip().lstrip() == "continue")
                            embed = botembed("Round Over")
                            desc = "```Round {}```\n".format(current_r)
                            aoran = characters[playing[0]][0]
                            embed.description = desc + "🃏 All but one of us has folded.\n{} won the round! {}\n{} won the pot of `${}`. \n\nType `continue` to continue.".format("I" if playing[0] == "Me" else playing[0], self.bot.response(5) if playing[0] != "Me" else "", aoran, pot)
                            await ctx.send(embed=embed)
                            wallets[playing[0]] += pot
                            pot = 0
                            await self.bot.wait_for("message", check=lambda m: m.channel == ctx.channel 
                            and m.author == ctx.message.author 
                            and m.content.lower().strip().lstrip() == "continue")
                            end_early = True
                            break
                        generated_hand = [card.replace("10", "T") for card in hands[c]]
                        generated_community = [card.replace("10", "T") for card in community]
                        win_rate = estimate_hole_card_win_rate(
                                nb_simulation=NB_SIMULATION,
                                nb_player=len(characters),
                                hole_card=gen_cards(generated_hand),
                                community_card=gen_cards(generated_community)
                                ) 
                        amount = int(win_rate / (1.0 / len(characters)) * ante)
                        a = "call"
                        if len(calls) > 0:
                            go = amount >= min(calls)
                            if amount > min(calls): 
                                a = "raise"
                        else:
                            #amount = ante
                            go = True
                        if win_rate >= 1.0 / len(characters) and wallets[c] >= amount and go:
                            amount = min(amount, wallets[c])
                            actions.append([c, a, amount])
                            calls.append(amount)
                            wallets[c] -= amount
                            pot += amount
                        else:
                            actions.append([c, "fold", 0])
                            playing.remove(c)
                if end_early:
                    
                    break

                if len(playing) == 1:
                    embed = botembed("Turn Over")
                    desc = "```Round {} // Turn {}```\n".format(current_r, turn)
                    desc = desc + "__Actions__"
                    #input()
                    for play in actions:
                        if play == "ante":
                            desc = desc + "\n**All of us** paid the ante of `${}`.".format(ante)
                            continue
                        name = play[0]
                        action = play[1]
                        amount = play[2]
                        name = play[0]
                        if name == "Me":
                            name = "I"
                        if action == "fold":
                            action = " folded."
                        
                        if action == "call":
                            action = " called"
                        if action == "raise":
                            action = " raised"
                        string = f"**{name}** {action}"
                        if action != " folded.":
                            string = string + f" `${amount}`."

                        desc = desc + "\n" + string

                    desc = desc + "\n\n__Wallets__\n"

                    for person in wallets:
                        x = person
                        y = wallets[person]
                        desc = desc + f"**{x}**: `${y}`\n"

                        
                    if len(community) > 0:
                        cstring = "Community card: `" + ', '.join(process_hand(community)) + "`\n"
                    else:
                        cstring = ""    
                    
                    hole_card = hands["You"].copy()
                    desc = desc + f"\n__Game Info__\nThere is `${pot}` in the pot.\n{cstring}Your hand: `{', '.join(process_hand(hole_card))}`\n\nType `continue` to continue."

                    embed.description = desc

                    await ctx.send(embed=embed)

                    await self.bot.wait_for("message", check=lambda m: m.channel == ctx.channel 
                    and m.author == ctx.message.author 
                    and m.content.lower().strip().lstrip() == "continue")
                    embed = botembed("Round Over")
                    desc = "```Round {}```\n".format(current_r)
                
                    aoran = characters[playing[0]][0]
                    embed.description = desc + "🃏 All but one of us has folded.\n{} won the round! {}\n{} won the pot of `${}`. \n\nType `continue` to continue.".format("I" if playing[0] == "Me" else playing[0], self.bot.response(5) if playing[0] != "Me" else "", aoran, pot)
                    await ctx.send(embed=embed)
                    wallets[playing[0]] += pot
                    pot = 0
                    await self.bot.wait_for("message", check=lambda m: m.channel == ctx.channel 
                    and m.author == ctx.message.author 
                    and m.content.lower().strip().lstrip() == "continue")
                    break

                if "You" in playing:

                    if len(playing) == 1:

                        embed = botembed("Turn Over")
                        desc = "```Round {} // Turn {}```\n".format(current_r, turn)
                        desc = desc + "__Actions__"
                        #input()
                        for play in actions:
                            if play == "ante":
                                desc = desc + "\n**All of us** paid the ante of `${}`.".format(ante)
                                continue
                            name = play[0]
                            action = play[1]
                            amount = play[2]
                            name = play[0]
                            if name == "Me":
                                name = "I"
                            if action == "fold":
                                action = " folded."
                            
                            if action == "call":
                                action = " called"
                            if action == "raise":
                                action = " raised"
                            string = f"**{name}** {action}"
                            if action != " folded.":
                                string = string + f" `${amount}`."

                            desc = desc + "\n" + string

                        desc = desc + "\n\n__Wallets__\n"

                        for person in wallets:
                            x = person
                            y = wallets[person]
                            desc = desc + f"**{x}**: `${y}`\n"

                            
                        if len(community) > 0:
                            cstring = "Community card: `" + ', '.join(process_hand(community)) + "`\n"
                        else:
                            cstring = ""    
                        
                        hole_card = hands["You"].copy()
                        desc = desc + f"\n__Game Info__\nThere is `${pot}` in the pot.\n{cstring}\nYour hand: `{', '.join(process_hand(hole_card))}`\n\nType `continue` to continue."

                        embed.description = desc

                        await ctx.send(embed=embed)

                        await self.bot.wait_for("message", check=lambda m: m.channel == ctx.channel 
                            and m.author == ctx.message.author 
                            and m.content.lower().strip().lstrip() == "continue")
                            

                        embed = botembed("Round Over")
                        desc = "```Round {}```\n".format(current_r)
                    
                        aoran = characters[playing[0]][0]
                        embed.description = desc + "🃏 All but one of us has folded.\n{} won the round! {}\n{} won the pot of `${}`. Type `continue` to continue.".format("I" if playing[0] == "Me" else playing[0], self.bot.response(5) if playing[0] != "Me" else "", aoran, pot)
                        await ctx.send(embed=embed)
                        wallets[playing[0]] += pot
                        pot = 0
                        await self.bot.wait_for("message", check=lambda m: m.channel == ctx.channel 
                        and m.author == ctx.message.author 
                        and m.content.lower().strip().lstrip() == "continue")
                        break

                    embed = botembed("Your Turn")
                    desc = "```Round {} // Turn {} (Betting Phase)```\n".format(current_r, turn)
                    desc = desc + "__Actions__"
                    #input()
                    for play in actions:
                        if play == "ante":
                            desc = desc + "\n**All of us** paid the ante of `${}`.".format(ante)
                            continue
                        name = play[0]
                        action = play[1]
                        amount = play[2]
                        name = play[0]
                        if name == "Me":
                            name = "I"
                        if action == "fold":
                            action = " folded."
                        
                        if action == "call":
                            action = " called"
                        if action == "raise":
                            action = " raised"
                        string = f"**{name}** {action}"
                        if action != " folded.":
                            string = string + f" `${amount}`."

                        desc = desc + "\n" + string

                    desc = desc + "\n\n__Wallets__\n"

                    for person in wallets:
                        x = person
                        y = wallets[person]
                        desc = desc + f"**{x}**: `${y}`\n"

                    moves = ""
                    valid_actions = ["fold", "call", "raise"]
                    for a in valid_actions:
                        amount = max(calls)
                        if a == "fold":
                            moves = moves + "`fold`\n"
                        if a == "call":
                            moves = moves + f"`call {amount}`\n"
                        if a == "raise":
                            minimum = max(calls)
                            maximum = wallets["You"]
                            moves = moves + f"`raise {min(minimum+1, maximum)}-{maximum}`\n"
                        
                    if len(community) > 0:
                        cstring = "Community card: `" + ', '.join(process_hand(community)) + "`\n"
                    else:
                        cstring = ""

                    hole_card = hands["You"].copy()
                    desc = desc + f"\n__Game Info__\nThere is `${pot}` in the pot.\n{cstring}Your hand: `{', '.join(process_hand(hole_card))}`\n\n__Available Moves__\n{moves}\nEnter your next move."

                    embed.description = desc

                    await ctx.send(embed=embed)

                    def check(m):
                        if m.channel == ctx.channel:
                            if m.author == ctx.message.author:
                                if m.content.lower().strip().lstrip().startswith("fold"):
                                    return True
                                elif len(m.content.lower().strip().lstrip().split(" ")) == 2:
                                    if m.content.lower().strip().lstrip().split(" ")[1].isdigit():
                                        if m.content.lower().strip().lstrip().startswith("raise ") or (m.content.lower().strip().lstrip().startswith("call ") and int(m.content.lower().strip().lstrip().split(" ")[1]) == max(calls)):
                                            return True

                    message = await self.bot.wait_for("message", check=check)

                    self.plays = []
                    
                    tokens = message.content.split(" ")
                    action = tokens[0]
                    
                    if action == "fold":
                        playing.remove("You")
                        if len(playing) == 1:
                            embed = botembed("Round Over")
                            desc = "```Round {}```\n".format(current_r)
                            aoran = characters[playing[0]][0]
                            embed.description = desc + "🃏 All but one of us has folded.\n{} won the round! {}\n{} won the pot of `${}`. Type `continue` to continue.".format("I" if playing[0] == "Me" else playing[0], self.bot.response(5) if playing[0] != "Me" else "", aoran, pot)
                            await ctx.send(embed=embed)
                            wallets[playing[0]] += pot
                            pot = 0
                            await self.bot.wait_for("message", check=lambda m: m.channel == ctx.channel 
                            and m.author == ctx.message.author 
                            and m.content.lower().strip().lstrip() == "continue")
                            break
                    else:
                        if action == "call":
                            amount = int(tokens[1])
                        else:
                            amount = min(max(int(tokens[1]), minimum+1), maximum)
                        wallets["You"] -= amount
                        pot += amount

                else:
                    embed = botembed("Turn Over")
                    desc = "```Round {} // Turn {}```\n".format(current_r, turn)
                    desc = desc + "__Actions__"
                    #input()
                    for play in actions:
                        name = play[0]
                        action = play[1]
                        amount = play[2]
                        name = play[0]
                        if name == "Me":
                            name = "I"
                        if action == "fold":
                            action = " folded."
                        
                        if action == "call":
                            action = " called"
                        if action == "raise":
                            action = " raised"
                        string = f"**{name}** {action}"
                        if action != " folded.":
                            string = string + f" `${amount}`."

                        desc = desc + "\n" + string

                    desc = desc + "\n\n__Wallets__\n"

                    for person in wallets:
                        x = person
                        y = wallets[person]
                        desc = desc + f"**{x}**: `${y}`\n"

                        
                    if len(community) > 0:
                        cstring = "Community card: `" + ', '.join(process_hand(community)) + "`\n"
                    else:
                        cstring = ""    
                    
                    desc = desc + f"\n__Game Info__\nThere is `${pot}` in the pot.\n{cstring}\nType `continue` to continue."

                    embed.description = desc

                    await ctx.send(embed=embed)

                    await self.bot.wait_for("message", check=lambda m: m.channel == ctx.channel 
                    and m.author == ctx.message.author 
                    and m.content.lower().strip().lstrip() == "continue")
        
        embed = botembed("Game Over")
        desc = "🃏 The game has ended! Here are the final totals:\n"
        sortedplayers = sorted(wallets.items(), key=lambda x: x[1], reverse=True)
        for i, pair in enumerate(sortedplayers):
            val = pair[1]
            c = pair[0]
            desc = desc + f"{i + 1}: **{c}**, with `${val}`\n"
        desc = desc + "Good game! I hope I can play with you again!"
        embed.description = desc
        self.playing = False
        return await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(PokerGame(bot))