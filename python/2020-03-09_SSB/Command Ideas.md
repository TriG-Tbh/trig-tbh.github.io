# Command Ideas for Server-Specific Bot (SSB)

## Information

This has ideas for commands that will be implemented into SSB, a bot that will be used for one specific server. The bot will use the Echo token, however will not be available to add to other servers.

Command Prefix: `!`

---

## Syntax

Normal text: not yet implemented

~~Strikethrough text: finished and implemented~~

(raw): Return message is sent in plain text, rather than in an embed

`<argument>`: Required argument

`[argument]`: Optional argument

---

## General

- ~~`echo <message>` (raw): echos message, used primarily for testing that the bot is online~~
- ~~`cascade [-reverse] <message>` (raw): returns a multi-line message, where every line has one more character than the last, so the last line has the given message. Using `-reverse` will reverse the message.~~
- `rate <item>`: rates an item on a scale of 1-10
- `ship <person 1> <person 2>`: ships two given objects, rates their compaitbility on a scale of 1-10
- `tag <name> [value, if tag isn't already set]`: views saved text. If the text is not already set, it can be defined. Once set, it cannot be changed

---

## Utilities

- ~~`bitcoin [amount, default set to 1]`: returns the price for a set amount of Bitcoin~~
- `morse <encode/decode> <message>` (raw): encodes/decodes a given message into Morse code
- ~~`roll [sides, defaults to 6]`: rolls a die with a given number of sides~~
- ~~`tinyurl <url>`: shortens a given URL~~
- ~~`avatar [user mention]`: shows the avatar of the command user, or a mentioned user~~
- ~~`reddit [-image] <subreddit>`: gets a random post from the first 25 posts of any subreddit's Hot page. You can also force it to be an image using the `-image` flag.~~
- ~~`meme`: a shortcut for `reddit -image memes`~~
- ~~`time <location>`: get the time and date in a specified location~~

---

## Fun

- ~~`mastermind`: play a game of Mastermind, where you guess a combination of characters~~
- `hangman`: play a game of Hangman. Two-player games are possible by passing a user mention
- `tictactoe [user mention]`: play a game of Tic-Tac-Toe. Two-player games are possible by passing a user mention
- `connect4 [user mention]`: play a game of Connect 4. Two-player games are possible by passing a user mention
- `8ball <question>`: answers a given yes/no question through the power of a Magic 8 Ball

---

## Administration

- ~~`whois <user mention>`: returns information about a given user~~
- `mute <user mention> <duration> [reason]`: prevents a user from speaking until a given duration
- `warn <user mention> [reason]`: warns a user - 3 warnings = ban
- ~~`kick <user mention> [reason]`: kicks a mentioned user with an optional reason~~
- ~~`ban <user mention> [reason]`: bans a mentioned user with an optional reason~~
- ~~`hackban <user mention> [reason]`: bans a mentioned user with an optional reason - only to be used with users that are not in the server~~
- ~~`unban <user ID> [reason]`: unbans a user from their id with an optional reason~~
- ~~`proxy <user ID> <message>`: sends a message to a user - only to be used if user cannot be contacted otherwise~~
- `purge <message count>`: deletes a specific number of messages in a channel. Will delete the command message plus the specified number of messages

---

## Server Functions

- ~~Starboard: when a message gets 5 star reactions, it will appear in the starboard channel. This is used to circumvent the 50 pin limit per channel.~~
- ~~Verification system: custom command (like `verify`) to gain access to the rest of the server~~
- ~~Audit Log: a channel that has system messages. Examples include:~~
  - member joining
  - member leaving
  - member deleting messages
  - bulk message deletion
  - role given/removed
  - message edited
  - member kicked/banned/hackbanned/unbanned
- Role menus - reacting to a message gives members a role
- Leveling system - 15-25 XP gained per message, XP gained once per minute, rate can be changed through command. Ranks gained when a certain number of XP is achieved, with roles earned at certain levels
- Rules - one command that is able to show all rules, while also able to take a parameter to show a specific rule
- Moderation - all moderating commands that allow a reason to be passed as an argument will output an embed in a specified channel
