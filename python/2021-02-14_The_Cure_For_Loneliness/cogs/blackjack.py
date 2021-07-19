from discord.ext import commands
import functions
import random

def get_value(hand):
    value = 0
    vs = {}
    for i in range(2, 11):
        vs[str(i)] = i
    vs["J"] = 10
    vs["Q"] = 10
    vs["K"] = 10
    vs["A2"] = 1
    vs["A"] = 11
    has_a = False
    for card in hand:
        c_v = card[1:]
        value += vs[c_v]
    return value

def hit(hand, deck):
    bust = False
    card = random.choice(deck)
    deck.remove(card)
    new = hand + [card]
    v = get_value(new)
    if v <= 21:
        hand = new
    else:
        if card[1] == "A":
            fixed = hand + [card+"2"]
            v = get_value(fixed)
            if v <= 21:
                hand = fixed
            else:
                bust = True
        else:
            index = [hand.index(c) for c in hand if len(c) == 2 and c[1] == "A"]
            if len(index) > 0:
                hand[index[0]] = hand[index[0]][0] + "A2"
                fixed2 = hand + [card]
                v = get_value(fixed2)
                if v <= 21:
                    hand = fixed2
                else:
                    bust = True
            else:
                hand = new
                bust = True
    return hand, deck, bust

                    


def get_probability(hand, opponents):
    deck = []
    for suit in ("D", "C", "H", "S"):
        for value in ("A", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K"):
            deck.append(suit + value)
    
    for opp in opponents:
        for card in opp:
            if not card.startswith("?"):
                try:
                    if card[-1] == "2":
                        to_remove = card[:2]
                    else:
                        to_remove = card
                    deck.remove(to_remove)
                except:
                    deck.remove(to_remove)
    
    for c in hand:
        try:
            if c[-1] == "2":
                to_remove = c[:2]
            else:
                to_remove = c
            deck.remove(to_remove)
        except:
            deck.remove(c)

    
    
    value = get_value(hand)

    if value == 21:
        return -1
        
    win = 0
    total = 0

    
    for card in deck:
        new = hand + [card]
        v = get_value(new)
        if v <= 21:
            win += 1
        else:
            if card[1] == "A":
                fixed = hand + [card+"2"]
                v = get_value(fixed)
                if v <= 21:
                    win += 1
            else:
                if "A" in [c[1] for c in new]:

                    index = [hand.index(c) for c in hand if len(c) == 2 and c[1] == "A"]
                    if len(index) > 0:
                        hand[index[0]] = hand[index[0]][0] + "A2"
                        fixed2 = hand + [card]
                        v = get_value(fixed2)
                        if v <= 21:
                            win + 1
                        
        total += 1
    return win / total

rounds = 5
ante = 5
starting = 150
threshold = 0.4

def process_hand(hand, mask=False):
    h = []
    for c in hand:
        if len(c) == 3:
            if c[-1] == "2":
                c = c[:2]
    
        h.append(c.replace("S", "♠").replace("D", "♦").replace("C", "♣").replace("H", "♥"))
    if mask:
        h = [h[0]] + (["??"] * (len(h) - 1))
    return h


def botembed(title):
    embed = functions.embed("Blackjack - " + title, color=0x8f0000)
    return embed

def error(errormsg):
    embed = functions.error("Blackjack", errormsg)
    return embed

class BlackjackGame(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.playing = False
        self.config = None

    @commands.command(aliases=["bj"])
    async def blackjack(self, ctx, players=4):
        
        if self.playing:
            embed = error("🚫 " + self.bot.response(2) + " we're already playing a game of Blackjack right now!")
            return await ctx.send(embed=embed)
        self.playing = True
        
        players = min(max(players, 2), 7) # (Wikipedia says max players is typically 7)

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
        embed.description = "🃏 " + self.bot.response(1) + " I started a game of Blackjack for us.\n{}Type `start` to start the game.".format(fstring)
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
            playing = can_play.copy()
            waiting = []
            pot = 0
            for suit in ("D", "C", "H", "S"):
                for value in ("A", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K"):
                    deck.append(suit + value)

            random.shuffle(deck)
            actions = []

            for character in playing:
                hands[character] = deck[:2]
                del deck[:2]

            

            for character in playing:
                aces = [c for c in hands[character] if c[1] == "A"]
                if len(aces) == 2:
                    hands[character][1] = aces[1][0] + "A2"
            
            #hands["You"] = ["HA", "DJ"]

            turn = 0

            for c in hands:
                h = hands[c]
                value = get_value(h)
                
            probs = []

            async with ctx.typing():
                for c in playing[:-1]:
                    others = [hands[char] for char in playing]
                    others.remove(hands[c])
                    #others = [["?" + card[1:] for card in cards] for cards in others]
                    others = [[h[0]] + ["??" * (len(h) - 1)] for h in others]
                    hand = hands[c]
                   
                    bet = min(max(random.randint(ante, ante * 5), ante), wallets[c])
                    actions.append([c, "bet", bet])
                    wallets[c] -= bet
                    pot += bet
                    probs.append(bet)
                    

            
            embed = botembed("Started")
            desc = "```Round {} // Pregame Betting```\n__Actions__\n".format(current_r)
            for a in actions:
                name, action, amount = a
                if name == "Me":
                    name = "I"
                
                if action == "fold":
                    action = "folded."
                desc = desc + "**{}** {}".format(name, action)
                if action != "folded.":
                    desc = desc + " `${}`.".format(amount)
                desc = desc + "\n"
            desc = desc + "\n__Wallets__\n"
            for person in wallets:
                x = person
                y = wallets[person]
                desc = desc + f"**{x}**: `${y}`\n"
            desc = desc + "\n__Game Info__\n"
            desc = desc + "There is `${}` in the pot.\n\n__Available Moves__\n`bet {}-{}`\n`fold`\n\nEnter your next move.".format(pot, ante, wallets["You"] if wallets["You"] < ante*5 else ante*5)
            embed.description = desc

            await ctx.send(embed=embed)
            ceil = min(wallets["You"], ante*5)

            def check(message):
                if message.author == ctx.message.author:
                    if message.channel == ctx.channel:
                        content = message.content.strip().lstrip().lower()
                        if len(content.split(" ")) == 2:
                            if content.split(" ")[0] == "bet":
                                if content.split(" ")[1].isdigit():
                                    amount = int(content.split(" ")[1])
                                    if ante <= amount and amount <= ceil:
                                        return True
                        elif content == "fold":
                            return True
                return False

            message = await self.bot.wait_for("message", check=check)
            if message.content != "fold":
                content = message.content
                amount = int(content.split(" ")[1])
                wallets["You"] -= amount
                pot += amount
            else:
                playing.remove("You")
            #return # TEMPORARY

            bj = False
            winners = []
            for c in playing:
                if get_value(hands[c]) == 21:
                    bj = True
                    winners.append(c)
            if bj:
                embed = botembed("Round Over")
                desc = "```Round {}```".format(current_r)
                desc = desc + "\n__Hands__\n"
                if "You" in playing:
                    goahead = playing[:-1]
                else:
                    goahead = playing
                for c in goahead:
                    hand = hands[c]
                    desc = desc + "**{}**: `{}` ({})\n".format(c, ", ".join(process_hand(hand)), get_value(hand))

                desc = desc + "\n__Wallets__\n"
                for person in wallets:
                    x = person
                    y = wallets[person]
                    desc = desc + f"**{x}**: `${y}`\n"

                desc = desc + "\n__Game Info__\n"
                desc = desc + "There is `${}` in the pot.\nYour hand: `{}`\n\nType `continue` to continue.".format(pot, ", ".join(process_hand(hands["You"])))
                embed.description = desc
                await ctx.send(embed=embed)
                await self.bot.wait_for("message", check=lambda m: m.channel == ctx.channel 
                and m.author == ctx.message.author 
                and m.content.lower().strip().lstrip() == "continue")

                embed = botembed("Round Over")
                desc = "```Round {}```\n".format(current_r)
                winning = winners

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
                    if winning[0].title() != "You":
                        if winning[0] != "I":
                            aoran = characters[winning[0]][0]
                        else:
                            aoran = "I"
                    else:
                        aoran = "You"
                    desc = desc + "🃏 All hands have been tallied up.\nWith a blackjack, {} won! {}\n{} won the pot of `${}`.".format(winning[0], self.bot.response(5) if "i" not in [w.lower() for w in winners] else "", aoran, pot)
                elif len(winning) == 2:
                    desc = desc + "🃏 All hands have been tallied up.\nWith a blackjack, {} and {} have tied! {}\n{} won an equal share of the pot of `${}`, recieving `${}` each.".format(winning[0], winning[1], self.bot.response(5) if "i" not in [w.lower() for w in winners] else "", "We've" if "i" in [w.lower() for w in winners] else "You guys have" if "you" in [w.lower() for w in winners] else "They've", pot, pot // len(winners))
                elif len(winning) > 2:
                    desc = desc + "🃏 All hands have been tallied up.\nWith a blackjack, {} and {} have tied! {}\n{} won an equal share of the pot of `${}`, recieving `${}` each.".format(", ".join(winning[:-1]), winning[-1], self.bot.response(5) if "i" not in [w.lower() for w in winners] else "", "We've" if "i" in [w.lower() for w in winners] else "You guys have" if "you" in [w.lower() for w in winners] else "They've", pot, pot // len(winners))

                for index in range(len(winners)):
                    if winners[index] == "you":
                        winners[index] = "You"
                    if winners[index] == "I":
                        winners[index] = "Me"

                for c in [c for c in wallets if wallets[c] <= 0]:
                    can_play.remove(c)

                desc = desc + "\nType `continue` to continue."
                embed.description = desc
                for winner in winners:
                    wallets[winner] += pot // len(winners)
                pot = 0
                await ctx.send(embed=embed)
                await self.bot.wait_for("message", check=lambda m: m.channel == ctx.channel 
                and m.author == ctx.message.author 
                and m.content.lower().strip().lstrip() == "continue")
                continue

            turn = 0
            while True:
                turn += 1
                actions = []
                if len(waiting) > 0 and len(playing) == 0:
                    embed = botembed("Round Over")
                    desc = "```Round {}```".format(current_r, turn)
                    desc = desc + "\n__Hands__\n"
                    for c in can_play:
                        hand = hands[c]
                        desc = desc + "**{}**: `{}` ({})\n".format(c, ", ".join(process_hand(hand)), get_value(hand))
                    desc = desc + "\n__Wallets__\n"
                    for person in wallets:
                        x = person
                        y = wallets[person]
                        desc = desc + f"**{x}**: `${y}`\n"
                    desc = desc + "\n__Game Info__\n"
                    desc = desc + "There is `${}` in the pot.\nYour hand: `{}`\n\nType `continue` to continue.".format(pot, ", ".join(process_hand(hands["You"])), ante, wallets["You"])
                    embed.description = desc

                    await ctx.send(embed=embed)
                    await self.bot.wait_for("message", check=lambda m: m.channel == ctx.channel 
                    and m.author == ctx.message.author 
                    and m.content.lower().strip().lstrip() == "continue")

                    char = waiting[0]
                    hand = hands[char].copy()
                    scores = []
                    s = get_value(hand)

                    highest_scoring = s
                    winning = [char]
                    scores.append(s)
                    for p in waiting[1:]:
                        hand = hands[p].copy()
                        s = get_value(hand)
                        scores.append(s)
                        if s > highest_scoring:
                            highest_scoring = s
                            winning = [p]
                        elif s == highest_scoring:
                            winning.append(p)

                    embed = botembed("Round Over")
                    desc = "```Round {}```\n".format(current_r)
                    winners = winning
                    winning = winners
                    
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
                    if len(winners) == 1:
                        if winning[0].title() != "You":
                            if winning[0] != "I":
                                aoran = characters[winning[0]][0]
                            else:
                                aoran = "I"
                        else:
                            aoran = "You"
                        desc = desc + "🃏 All hands have been tallied up.\nWith a score of {}, {} won! {}\n{} won the pot of `${}`.".format(highest_scoring, winning[0], self.bot.response(5) if "i" not in [w.lower() for w in winners] else "", aoran, pot)
                    elif len(winners) == 2:
                        desc = desc + "🃏 All hands have been tallied up.\nWith a score of {}, {} and {} have tied! {}\n{} won an equal share of the pot of `${}`, recieving `${}` each.".format(highest_scoring, winning[0], winning[1], self.bot.response(5) if "i" not in [w.lower() for w in winners] else "", "We've" if "i" in [w.lower() for w in winners] else "You guys have" if "you" in [w.lower() for w in winners] else "They've", pot, pot // len(winners))
                    elif len(winners) > 2:
                        desc = desc + "🃏 All hands have been tallied up.\nWith a score of {}, {} and {} have tied! {}\n{} won an equal share of the pot of `${}`, recieving `${}` each.".format(highest_scoring, ", ".join(winning[:-1]), winning[-1], self.bot.response(5) if "i" not in [w.lower() for w in winners] else "", "We've" if "i" in [w.lower() for w in winners] else "You guys have" if "you" in [w.lower() for w in winners] else "They've", pot, pot // len(winners))

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

                    desc = desc + "\nType `continue` to continue."
                    embed.description = desc
                    await ctx.send(embed=embed)
                    await self.bot.wait_for("message", check=lambda m: m.channel == ctx.channel 
                    and m.author == ctx.message.author 
                    and m.content.lower().strip().lstrip() == "continue")
                    break
                

                if "You" in playing:    
                    goahead = playing.copy()[:-1]
                else:
                    goahead = playing.copy()


                endearly = False
                index = 0
                for c in goahead:
                    index += 1
                    others = [hands[char] for char in (playing + waiting)]
                    others.remove(hands[c])
                    others = [[h[0]] + ["??" * (len(h) - 1)] for h in others]
                    hand = hands[c]
                    prob = get_probability(hand, others)
                    if prob > 0.4:
                        hand, deck, bust = hit(hand, deck)
                        if bust:
                            hands[c] = hand
                            actions.append([c, "bust"])
                            playing.remove(c)
                        else:
                            hands[c] = hand
                            actions.append([c, "hit"])
                    else:
                        actions.append([c, "stand"])
                        playing.remove(c)
                        waiting.append(c)
                    still = playing + waiting
                    if len(still) == 1:
                        embed = botembed("Round Over")
                        desc = "```Round {}```\n__Actions__\n".format(current_r)
                        for a in actions:
                            name, action = a
                            if name == "Me":
                                name = "I"
                            
                            if action == "fold":
                                action = "folded."
                            if action == "bust":
                                action = "decided to hit, and busted."
                            if action == "hit":
                                action = "decided to hit."
                            if action == "stand":
                                action = "decided to stand."
                            desc = desc + "**{}** {}".format(name, action)
                            desc = desc + "\n"

                        desc = desc + "\n__Hands__\n"
                        if "You" in still:
                            still.remove("You")
                        for c in still:
                            hand = hands[c]
                            desc = desc + "**{}**: `{}`\n".format(c, ", ".join(process_hand(hand, mask=True)))
                        desc = desc + "\n__Wallets__\n"
                        for person in wallets:
                            x = person
                            y = wallets[person]
                            desc = desc + f"**{x}**: `${y}`\n"

                        desc = desc + "\n__Game Info__\n"
                        desc = desc + "There is `${}` in the pot.\nYour hand: `{}`\n\nType `continue` to continue.".format(pot, ", ".join(process_hand(hands["You"])))
                        embed.description = desc
                        await ctx.send(embed=embed)
                        await self.bot.wait_for("message", check=lambda m: m.channel == ctx.channel 
                        and m.author == ctx.message.author 
                        and m.content.lower().strip().lstrip() == "continue")
                        endearly = True
                        break
                    else:
                        continue
                if endearly:
                    embed = botembed("Round Over")
                    desc = "```Round {}```\n".format(current_r)
                    still = playing + waiting
                    aoran = characters[still[0]][0]
                    embed.description = desc + "🃏 All but one of us has busted.\n{} won the round! {}\n{} won the pot of `${}`. Type `continue` to continue.".format("I" if still[0] == "Me" else still[0], self.bot.response(5) if still[0] != "Me" else "", aoran, pot)
                    await ctx.send(embed=embed)
                    wallets[still[0]] += pot
                    pot = 0
                    await self.bot.wait_for("message", check=lambda m: m.channel == ctx.channel 
                    and m.author == ctx.message.author 
                    and m.content.lower().strip().lstrip() == "continue")
                    break
                
                if "You" in playing:
                    embed = botembed("Your Turn")
                    desc = "```Round {} // Turn {}```\n__Actions__\n".format(current_r, turn)
                    for a in actions:
                        name, action = a
                        if name == "Me":
                            name = "I"
                        
                        if action == "fold":
                            action = "folded."
                        if action == "bust":
                            action = "decided to hit, and busted."
                        if action == "hit":
                            action = "decided to hit."
                        if action == "stand":
                            action = "decided to stand."
                        desc = desc + "**{}** {}".format(name, action)
                        desc = desc + "\n"
                    desc = desc + "\n__Hands__\n"
                    for c in (playing[:-1] + waiting):
                        hand = hands[c]
                        desc = desc + "**{}**: `{}`\n".format(c, ", ".join(process_hand(hand, mask=True)))
                    desc = desc + "\n__Wallets__\n"
                    for person in wallets:
                        x = person
                        y = wallets[person]
                        desc = desc + f"**{x}**: `${y}`\n"
                    desc = desc + "\n__Game Info__\n"
                    desc = desc + "There is `${}` in the pot.\nYour hand: `{}`\n\n__Available Moves__\n`hit`\n`stand`\n\nEnter your next move.".format(pot, ", ".join(process_hand(hands["You"])), ante, wallets["You"])
                    embed.description = desc

                    await ctx.send(embed=embed)
                    def check(message):
                        if message.author == ctx.message.author:
                            if message.channel == ctx.channel:
                                content = message.content.strip().lstrip().lower()
                                if content == "hit" or content == "stand":
                                    return True
                    message = await self.bot.wait_for("message", check=check)
                    content = message.content.strip().lstrip().lower()
                    if content == "hit":
                        hand, deck, bust = hit(hands["You"], deck)
                        hands["You"] = hand
                        embed = botembed("Turn Over")
                        desc = "```Round {} // Turn {}```\nHere is your new hand: `{}`\n".format(current_r, turn, ", ".join(process_hand(hand)))
                        if bust:
                            desc = desc + "Unfortunately, you busted.\nType `continue` to continue."
                            playing.remove("You")
                        else:
                            desc = desc + "You didn't bust! {}\nType `continue` to continue.".format(self.bot.response(5))
                            

                        embed.description = desc
                        await ctx.send(embed=embed)
                        await self.bot.wait_for("message", check=lambda m: m.channel == ctx.channel 
                        and m.author == ctx.message.author 
                        and m.content.lower().strip().lstrip() == "continue")
                    else:
                        playing.remove("You")
                        waiting.append("You")
                else:
                    embed = botembed("Turn Over")
                    desc = "```Round {} // Turn {}```\n__Actions__\n".format(current_r, turn)
                    for a in actions:
                        name, action = a
                        if name == "Me":
                            name = "I"
                        
                        if action == "fold":
                            action = "folded."
                        if action == "bust":
                            action = "decided to hit, and busted."
                        if action == "hit":
                            action = "decided to hit."
                        if action == "stand":
                            action = "decided to stand."
                        desc = desc + "**{}** {}".format(name, action)
                        desc = desc + "\n"
                    desc = desc + "\n__Hands__\n"
                    still = playing + waiting
                    if "You" in still:
                        still.remove("You")
                    for c in still:
                        hand = hands[c]
                        desc = desc + "**{}**: `{}`\n".format(c, ", ".join(process_hand(hand, mask=True)))
                    desc = desc + "\n__Wallets__\n"
                    for person in wallets:
                        x = person
                        y = wallets[person]
                        desc = desc + f"**{x}**: `${y}`\n"
                    desc = desc + "\n__Game Info__\n"
                    desc = desc + "There is `${}` in the pot.\nYour hand: `{}`\n\nType `continue` to continue.".format(pot, ", ".join(process_hand(hands["You"])), ante, wallets["You"])
                    embed.description = desc
                    await ctx.send(embed=embed)
                    await self.bot.wait_for("message", check=lambda m: m.channel == ctx.channel 
                    and m.author == ctx.message.author 
                    and m.content.lower().strip().lstrip() == "continue")
                
                still = waiting + playing
                if len(still) == 1:
                    embed = botembed("Round Over")
                    desc = "```Round {}```\n".format(current_r)
                
                    aoran = characters[still[0]][0]
                    embed.description = desc + "🃏 All but one of us has busted.\n{} won the round! {}\n{} won the pot of `${}`. Type `continue` to continue.".format("I" if still[0] == "Me" else still[0], self.bot.response(5) if still[0] != "Me" else "", aoran, pot)
                    await ctx.send(embed=embed)
                    wallets[still[0]] += pot
                    pot = 0
                    await self.bot.wait_for("message", check=lambda m: m.channel == ctx.channel 
                    and m.author == ctx.message.author 
                    and m.content.lower().strip().lstrip() == "continue")
                    break



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
    bot.add_cog(BlackjackGame(bot))