import os
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')

bot = commands.Bot(command_prefix="!")
pool = []
votes = {}
vote_threshold = 0

@bot.command(name='add', help='Adds an item to the draft pool. Usage: !add item1 item2 ... item_n')
async def on_add(ctx, *args):
    [pool.append(item) for item in args if item not in pool]
    added_items = ', '.join(args)
    if (len(args) > 1):
        await ctx.send(f'The following items were added to the draft pool:\n{added_items}')
    else:
        await ctx.send(f'Added \"{args[0]}\" to the draft pool.')

@bot.command(name='pool', help='Displays the items currently in the draft pool. Usage: !pool')
async def on_pool(ctx):
    if not pool:
        await ctx.send('The draft pool is currently empty.')
        return
    pool_str = ', '.join(pool)
    await ctx.send(f'The draft pool contains {len(pool)} items.\n{pool_str}')

@bot.command(name='veto', help='Vetoes an item, removing it from the draft pool. Usage: !veto item')
async def on_veto(ctx, item):
    if (item not in pool):
        await ctx.send(f'\"{item}\" isn\'t in the draft pool.')
        return
        
    pool.remove(item)
    await ctx.send(f'{item} was removed from the draft pool.')

@bot.command(name='clear', help='Clears the draft pool. Usage: !clear')
async def on_clear(ctx):
    pool.clear()
    await ctx.send('The draft pool has been cleared.')

@bot.command(name='startvote', help='Launches a vote to select an item. Usage !startvote win_threshold')
async def on_startvote(ctx, threshold: int):
    global vote_threshold, votes
    if threshold is None or not isinstance(threshold, int):
        await ctx.send('Usage: !startvote vote_threshold')
        return
    if threshold < 1:
        await ctx.send('Threshold value must be >=1')
        return
    if not pool or len(pool) == 1:
        await ctx.send('The draft pool must contain >=2 items in order to run a vote.')
        return

    vote_threshold = threshold
    votes = dict.fromkeys(pool, 0)
    await ctx.send(f'Started a poll - first item to {threshold} votes wins.')

@bot.command(name='endvote', help='Preliminarily ends the current vote. Usage: !endvote')
async def on_endvote(ctx):
    global vote_threshold, votes
    if vote_threshold == 0:
        await ctx.send('There is no active vote.')
        return
    vote_threshold = 0
    votes = {}
    await ctx.send('The vote was concluded.')

@bot.command(name='showvotes', help='Shows the current vote counts. Usage: !showvotes')
async def show_votes(ctx):
    if vote_threshold == 0:
        await ctx.send('There is no active vote.')
        return
    sorted_votes = sorted(votes.items(), key = lambda kv: kv[1], reverse=True)
    output = []
    [output.append(f'{kv[0]} - {kv[1]}\n') for kv in sorted_votes]
    output_str = ''.join(output)
    await ctx.send(f'The current vote counts are as follows:\n{output_str}')

@bot.command(name='vote', help='Votes for an item. Usage: !vote item')
async def on_vote(ctx, item):
    global vote_threshold, votes
    if item is None:
        await ctx.send('Usage: !vote item')
        return
    if vote_threshold == 0:
        await ctx.send('There is no active vote.')
        return
    if item not in pool:
        await ctx.send(f'\"{item}\" is not in the pool.')
        return
    
    votes[item] += 1
    item_votes = votes.get(item)
    await ctx.send(f'{ctx.message.author.mention} voted for {item}.')
    if (item_votes == vote_threshold):
        votes = {}
        vote_threshold = 0
        await ctx.send(f'\"{item}" has won the vote!')
        

bot.run(TOKEN)