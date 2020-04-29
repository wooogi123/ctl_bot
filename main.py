import os
from discord.ext import commands
from src import ctl

bot = commands.Bot(command_prefix='$')

ctl_bot = ctl.CTL()

@bot.event
async def on_ready():
    print(f'We have logged in as {bot.user.name}')

@bot.event
async def help(ctx):
    await ctx.send('\
        $login `ID` `PW`\n\
        $enter_room `IDX`\n\
        $run_lecture `IDX`\
    ')

@bot.command()
async def login(ctx, id: str, pw: str):
    s = '```'
    flag = ctl_bot.login(id, pw)
    if flag == '로그인 성공':
        s += f'{flag}\n'
        for idx, room in enumerate(ctl_bot.rooms):
            s += f'{str(idx)}: {room[0]}\n'
        s += '```'
    else:
        s += f'{flag}\n```'
    await ctx.send(f'{s}')

@bot.command()
async def enter_room(ctx, idx: int):
    s = '```'
    if ctl_bot.enter_room(idx):
        lectures = ctl_bot.lectures
        for idx, lec in enumerate(lectures):
            s += f'{str(idx)}: {lec["max_study_time"]:.3f}분 / {lec["basic_time"]}분\n'
        s += '```'
    await ctx.send(f'{s}')

@bot.command()
async def run_lecture(ctx, idx: int):
    await ctx.send(f'```{ctl_bot.lectures[idx]["max_study_time"]:.3f}분 뒤에 완료됩니다```')
    ctl_bot.run_lecture(idx)

token = os.environ['KDU_ctl_token']

bot.run(token)