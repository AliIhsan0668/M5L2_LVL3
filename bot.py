from logic import *
import discord
from discord.ext import commands
from config import TOKEN

# Veri tabanı yöneticisini başlatma
manager = DB_Map("database.db")

bot = commands.Bot(command_prefix="!", intents=discord.Intents.all())

@bot.event
async def on_ready():
    print("Bot başlatıldı!")

@bot.command()
async def start(ctx: commands.Context):
    await ctx.send(f"Merhaba, {ctx.author.name}. Mevcut komutların listesini keşfetmek için !help_me yazın.")

@bot.command()
async def help_me(ctx: commands.Context):
    await ctx.send(
        "!show_city <şehir adı> <renk (opsiyonel)> → Belirtilen şehri haritada gösterir\n"
        "!show_my_cities <renk (opsiyonel)> → Kayıtlı şehirlerini listeler ve haritada gösterir\n"
        "!remember_city <şehir adı> → Şehri kaydeder"
    )

@bot.command()
async def show_city(ctx: commands.Context, city_name: str, marker_color: str = "red"):
    manager.create_graph(f"{ctx.author.id}.png", [city_name], marker_color=marker_color)
    await ctx.send(file=discord.File(f"{ctx.author.id}.png"))

@bot.command()
async def show_my_cities(ctx: commands.Context, marker_color: str = "red"):
    cities = manager.select_cities(ctx.author.id)
    if not cities:
        await ctx.send("Hiç şehir kaydetmedin.")
        return
    manager.create_graph(f"{ctx.author.id}.png", cities, marker_color=marker_color)
    await ctx.send(file=discord.File(f"{ctx.author.id}.png"))

@bot.command()
async def remember_city(ctx: commands.Context, *, city_name=""):
    if manager.add_city(ctx.author.id, city_name):
        await ctx.send(f'{city_name} şehri başarıyla kaydedildi!')
    else:
        await ctx.send("Şehir bulunamadı. Lütfen şehir adını İngilizce olarak girin.")

if __name__ == "__main__":
    bot.run(TOKEN)
