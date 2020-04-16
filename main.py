from discord.ext import commands
from src import ctl

bot = commands.Bot(command_prefix='$')

ctl_bot = ctl.CTL()

@bot.event
async def on_ready():
    print(f'We have logged in as {bot.user.name}')

@bot.command()
async def hello(ctx):
    await ctx.send('Hello!')

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

token = 'NzAwMjQwNDYyODQxMzgwOTI2.XpgD7A.Y4jxNrxAp5_sZJ3ycgOKOXJwwT4'

bot.run(token)