import os
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')

bot = commands.Bot(command_prefix="!")
pool = []

@bot.command(name='add', help='Adds an item to the draft pool.')
async def on_add(ctx, *args):
    [pool.append(item) for item in args if item not in pool]
    added_items = ', '.join(args)
    await ctx.send(f'The following items were added to the draft pool:\n{added_items}')

@bot.command(name='pool', help='Displays the items currently in the draft pool.')
async def on_pool(ctx):
    pool_str = ', '.join(pool)
    await ctx.send(f'The draft pool contains {len(pool)} items.\n{pool_str}')

@bot.command(name='veto', help='Vetoes an item, removing it from the draft pool.')
async def on_veto(ctx, item):
    if (item not in pool):
        await ctx.send(f'{item} isn\'t in the draft pool.')
        return
        
    pool.remove(item)
    await ctx.send(f'{item} was removed from the draft pool.')

@bot.command(name='clear', help='Clears the draft pool.')
async def on_clear(ctx):
    pool.clear()
    await ctx.send('The draft pool has been cleared.')

bot.run(TOKEN)