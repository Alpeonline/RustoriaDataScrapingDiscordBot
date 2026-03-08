import interactions
from interactions import Button, ButtonStyle, SelectOption, ActionRow
import requests
from bs4 import BeautifulSoup
from datetime import datetime
import pytz
from pytz import timezone
# Set timezone
tz = timezone("US/Eastern")
# Date with timezone

def get_time():
    date = datetime.now(tz)
    format_date = date.strftime("%I:%M %p")
    return format_date
token = 'discord token'
def get_main(username):
    try:

        rustoria_main = requests.get('https://api.rustoria.co/statistics/leaderboards/vanilla_main_us/kdr?from=0&sortBy=total&orderBy=asc&username='+username)
        rustoria_main = rustoria_main.json()['leaderboard'][0]['data']
    except IndexError:
        return "Data not found"
    kills_ma, deaths_ma = rustoria_main["kill_player"], rustoria_main["deaths"] - rustoria_main["death_suicide"]
    if deaths_ma == 0:
      deaths_ma= 1
    #kill stats
    main_kill_stats = "Kills: " + str(kills_ma) + " | Player Deaths: " + str(deaths_ma) + "| KD: " + str(round(kills_ma/deaths_ma,2))
    #mine starts
    rustoria_main = requests.get('https://api.rustoria.co/statistics/leaderboards/vanilla_main_us/resources?from=0&sortBy=total&orderBy=asc&username='+username)
    rustoria_main =  rustoria_main = rustoria_main.json()['leaderboard'][0]['data']
    wood_ma , stone_ma, metal_ma , sulfur_ma = rustoria_main["harvest.wood"], rustoria_main["harvest.stones"], rustoria_main["harvest.metal.ore"], rustoria_main["harvest.sulfur.ore"]
    main_farm_stats = (" Wood Farmed: " + str(wood_ma) + " | Stone Farmed: " + str(stone_ma) +" | Metal Farmed: " + str(metal_ma) + " | Sulfur Farmed: " + str(sulfur_ma))
    main_stats = f""" {main_kill_stats}
{main_farm_stats}"""
    return main_stats
    
#med
def get_medium(username):
    try:

        rustoria_med = requests.get('https://api.rustoria.co/statistics/leaderboards/vanilla_medium_us/kdr?from=0&sortBy=total&orderBy=asc&username='+username)
        rustoria_med = rustoria_med.json()['leaderboard'][0]['data']
        kills_m, deaths_m = rustoria_med["kill_player"], rustoria_med["deaths"] - rustoria_med["death_suicide"]
        #kill stats
        medium_kill_stats = "Kills: " + str(kills_m) + " | Player Deaths: " + str(deaths_m) + " | KD: " + str(round(kills_m/deaths_m,2))
        #mine starts
        rustoria_med = requests.get('https://api.rustoria.co/statistics/leaderboards/vanilla_medium_us/resources?from=0&sortBy=total&orderBy=asc&username='+username)
        rustoria_med =  rustoria_med = rustoria_med.json()['leaderboard'][0]['data']
        wood_m , stone_m, metal_m , sulfur_m = rustoria_med["harvest.wood"], rustoria_med["harvest.stones"], rustoria_med["harvest.metal.ore"], rustoria_med["harvest.sulfur.ore"]
        medium_farm_stats = (" Wood Farmed: " + str(wood_m) + " | Stone Farmed: " + str(stone_m) +" | Metal Farmed: " + str(metal_m) + " | Sulfur Farmed: " + str(sulfur_m))
        medium_stats = f""" {medium_kill_stats}
{medium_farm_stats}"""
        return medium_stats
    except (KeyError, IndexError) as error:
        return "Data not found"
#long
def get_long(username):
  try:
      rustoria_lo = requests.get('https://api.rustoria.co/statistics/leaderboards/vanilla_long_us/kdr?from=0&sortBy=total&orderBy=asc&username='+username)
      rustoria_lo = rustoria_lo.json()['leaderboard'][0]['data']
      kills_l, deaths_l = rustoria_lo["kill_player"], rustoria_lo["deaths"] - rustoria_lo["death_suicide"]
      #kill stats
      lo_kill_stats = "Kills: " + str(kills_l) + " | Player Deaths: "  + str(deaths_l) + " | KD: " + str(round(kills_l/deaths_l,2))
      #mine starts
      rustoria_lo = requests.get('https://api.rustoria.co/statistics/leaderboards/vanilla_long_us/resources?from=0&sortBy=total&orderBy=asc&username='+username)
      rustoria_lo = rustoria_lo.json()['leaderboard'][0]['data']
      wood_m , stone_m, metal_m , sulfur_m = rustoria_lo["harvest.wood"], rustoria_lo["harvest.stones"], rustoria_lo["harvest.metal.ore"], rustoria_lo["harvest.sulfur.ore"]
      lo_farm_stats = (" Wood Farmed: " + str(wood_m) + " | Stone Farmed: " + str(stone_m) +" | Metal Farmed: " + str(metal_m) + " | Sulfur Farmed: " + str(sulfur_m))
      lo_stats = f""" {lo_kill_stats}
  {lo_farm_stats}"""
      return lo_stats
  except (KeyError,IndexError) as error:
    return "Data not found"
def get_stock(server):
  if server == 'long':
    website_use = 'https://donate.rustoria.co/packages.php?game=3&server=25'
  elif server == 'main':
    website_use = 'https://donate.rustoria.co/packages.php?game=3&server=15'
  elif server == 'medium':
    website_use = 'https://donate.rustoria.co/packages.php?game=3&server=24'
  elif server == 'small':
    website_use = 'https://donate.rustoria.co/packages.php?game=3&server=26'
  else:
    return "Wrong"

  website = requests.get(website_use)
  soup = BeautifulSoup(website.content, "html.parser")
  soup_elements = soup.find("div", class_="package-stock-info")
  if "OUT OF STOCk" in soup_elements:
    return "OUT OF STOCK"
  else:
    return "IN STOCK"

#main https://donate.rustoria.co/packages.php?game=3&server=15
#long https://donate.rustoria.co/packages.php?game=3&server=25
#small https://donate.rustoria.co/packages.php?game=3&server=26
#medium https://donate.rustoria.co/packages.php?game=3&server=24

client = interactions.Client(token)

@client.event
async def on_ready():
  print("BOT READY")
""""
@client.command(
  name = "say",
  description= "test",
  options=[
    interactions.Option(
      type = interactions.OptionType.STRING,
      name="server",
      description = "test",
    ),
  ],
)
"""
#4
@client.command(name="rustoria-servers",description="Lists all rustoria servers",scope=[])#enter scopes here
async def send_buttons(ctx:interactions.CommandContext):
  button = Button(
    style= ButtonStyle.PRIMARY,
    custom_id = "Long",
    label = "US LONG",
  )
  button2 = Button(style= ButtonStyle.PRIMARY,
    custom_id = "Medium",
    label = "US MEDIUM",
  )
  button3 = Button(style= ButtonStyle.DANGER,
    custom_id = "Main",
    label = "US MAIN",
  )
  button4 = Button(style= ButtonStyle.DANGER,
    custom_id = "Small",
    label = "US SMALL",
  )
  action_row = ActionRow(components=[button,button2,button3,button4])
  await ctx.send("Here are the servers you can check for VIP:",components=[[button,button2],[button3,button4]])

@client.component("Main")
async def main_server(ctx:interactions.ComponentContext):
  time = str(get_time())
  website = requests.get('https://donate.rustoria.co/packages.php?game=3&server=15')
  soup = BeautifulSoup(website.content, "html.parser")
  soup_elements = soup.find("div", class_="package-stock-info")
  if "OUT OF STOCk" in soup_elements:
    await ctx.send(":x: US Main is currently out of stock, Time:" + time+" EST")
  else:
    await ctx.send(":white_check_mark: Us Main is currently in stock, Time: "+time +" EST ")

@client.component("Medium")
async def medium_server(ctx:interactions.ComponentContext):
  time = str(get_time())
  website = requests.get('https://donate.rustoria.co/packages.php?game=3&server=24')
  soup = BeautifulSoup(website.content, "html.parser")
  soup_elements = soup.find("div", class_="package-stock-info")
  if "OUT OF STOCk" in soup_elements:
    await ctx.send(":x: US Medium is currently out of stock, Time:" + time +" EST")
  else:
    await ctx.send(":white_check_mark: Us Medium is currently in stock, Time: "+time +" EST ")

@client.component("Long")
async def Long_server(ctx:interactions.ComponentContext):
  time = str(get_time())
  website = requests.get('https://donate.rustoria.co/packages.php?game=3&server=25')
  soup = BeautifulSoup(website.content, "html.parser")
  soup_elements = soup.find("div", class_="package-stock-info")
  if "OUT OF STOCk" in soup_elements:
    await ctx.send(":x: US Long is currently out of stock, Time:" + time +" EST")
  else:
    await ctx.send(":white_check_mark: Us Long is currently in stock, Time: "+time+" EST ")

@client.component("Small")
async def small_server(ctx:interactions.ComponentContext):
  time = str(get_time())
  website = requests.get('https://donate.rustoria.co/packages.php?game=3&server=26')
  soup = BeautifulSoup(website.content, "html.parser")
  soup_elements = soup.find("div", class_="package-stock-info")
  if "OUT OF STOCk" in soup_elements:
    await ctx.send(":x: US Small is currently out of stock, Time:" + time +" EST")
  else:
    await ctx.send(":white_check_mark: Us Small is currently in stock, Time: "+time  +" EST ")


@client.command(
  name ="statsrustoria",
  description="stats", scope=[],
  
  options=[
    interactions.Option(
      type=interactions.OptionType.STRING,
      name="user",
      description="player name",
      required = True,
    ),
  ],
)
async def statsrustoria(ctx: interactions.CommandContext, user:str):
  button = Button(
    style= ButtonStyle.PRIMARY,
    custom_id = "Long_stat",
    label = "US LONG",
  )
  button2 = Button(style= ButtonStyle.DANGER,
    custom_id = "Medium_stat",
    label = "US MEDIUM",
  )
  button3 = Button(style= ButtonStyle.PRIMARY,
    custom_id = "Main_stat",
    label = "US MAIN",
  )
  action_row = ActionRow(components=[button,button2,button3])
  global user_f
  user_F = ""
  user_f = user
  await ctx.send(f"Here are the servers you can check the stats of {user_f}: (This only works with one player at a time)",components=[[button,button2,button3]])
@client.component("Main_stat")
async def main_server(ctx:interactions.ComponentContext):
  await ctx.send(get_main(user_f))

@client.component("Medium_stat")
async def main_server(ctx:interactions.ComponentContext):
  await ctx.send(get_medium(user_f))

@client.component("Long_stat")
async def main_server(ctx:interactions.ComponentContext):
  await ctx.send(get_long(user_f))

  
client.start()
  
