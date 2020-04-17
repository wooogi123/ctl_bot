import os
from discord.ext import commands
from src import ctl

bot = commands.Bot(command_prefix='$')

ctl_bot = ctl.CTL()

@bot.event
async def on_ready():
    print(f'We have logged in as {bot.user.name}')

@bot.command()
async def help(ctx):
    await ctx.send('\
        $login `ID` `PW`\n\
        $show_rooms\n\
        $enter_room `IDX`\n\
        $show_lectures\n\
        $run_lecture `IDX`\
    ')

@bot.command()
async def login(ctx, id: str, pw: str):
    await ctx.send(f'{ctl_bot.login(id, pw)}')

@bot.command()
async def show_rooms(ctx):
    arr = ctl_bot.rooms
    await ctx.send(f'{arr}')

@bot.command()
async def enter_room(ctx, idx: int):
    await ctx.send(f'{ctl_bot.enter_room(idx)}')

@bot.command()
async def show_lectures(ctx):
    arr = ctl_bot.lectures
    await ctx.send(f'{arr}')

@bot.command()
async def run_lecture(ctx, idx: int):
    await ctx.send(f'{int(ctl_bot.lectures[idx]["max_study_time"])}분 뒤에 완료됩니다')
    ctl_bot.run_lecture(idx)

token = os.environ['KDU_ctl_token']

bot.run(token)