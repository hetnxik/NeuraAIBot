import disnake
import os
import schedule
import requests
import asyncio
from disnake.ext import commands
from dotenv import load_dotenv

intents = disnake.Intents.all()
client = commands.Bot(command_prefix="*", intents=intents, case_insensitive=True, owner_id=807655087643557919)

load_dotenv()

# test

current_url = ""
url = f"https://newsdata.io/api/1/news?apikey={os.getenv('NEWSAPI')}&country=fr,de,in,gb,us&language=en&category=science,technology"


def get_latest_article():
    response = requests.get(url)
    articles = response.json()['results']
    current_article = articles[0]
    return current_article


async def send_article():
    global current_url
    current_article = get_latest_article()
    if current_article["link"] != current_url:
        channel = await client.fetch_channel(os.getenv("NEWSCHANNEL"))
        articleEmbed = disnake.Embed(title=current_article['title'], url=current_article['link'],
                                     color=disnake.Color.random())
        articleEmbed.add_field(name="Description", value=current_article['description'])
        if current_article['image_url']:
            articleEmbed.set_thumbnail(url=current_article['image_url'])
        articleEmbed.set_footer(text=f"Published Date: {current_article['pubDate']}")
        await channel.send(embed=articleEmbed)
        current_url = current_article['link']


@client.event
async def on_ready():
    print("ready")
    schedule.every(90).minutes.do(send_article)

    while True:
        await send_article()
        await asyncio.sleep(90 * 60)  # wait for 10 minutes before sending the next article


for folder in os.listdir('./commands'):
    if folder != '.DS_Store':  # and folder != 'vc-interactions':
        print(folder)
        for file in os.listdir(f'./commands/{folder}'):
            if file.endswith('.py') and not file.startswith('_') and not file.startswith('.'):
                client.load_extension(f'commands.{folder}.{file[:-3]}')
                print(f'Loaded the category: {file}')

print("=================================")
client.run(os.getenv("TOKEN"))
