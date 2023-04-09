import discord
from discord import option
from pydactyl import PterodactylClient
from config import *
from lang import *

bot = discord.Bot()
api = PterodactylClient(HOST, api_key=PTERODACTYL_USER_TOKEN)

if SERV_ID == '':
    SERV_ID=api.client.servers.list_servers()[0]['attributes']['identifier']
    

@bot.event
async def on_ready():
    print('-----------------------------')
    print(f'Logged in as: {bot.user}')
    print('-----------------------------')
class ButtonMain(discord.ui.View):
    @discord.ui.button(label=check_server, row=0, style=discord.ButtonStyle.primary)
    async def first_button_callback(self, button, interaction):
        server_utilization = api.client.servers.get_server_utilization(SERV_ID)
        bytes=server_utilization['resources']['disk_bytes']
        disk_usage_mb=bytes/1024/1024
        bytes=server_utilization['resources']['memory_bytes']
        memory_usage_mb=bytes/1024/1024
        
        embed=discord.Embed(title=f"ServerID: {SERV_ID}", color=0x0084ff)
        embed.add_field(name="CPU", value=f"{round(server_utilization['resources']['cpu_absolute'], 2)}%", inline=True)
        embed.add_field(name="DISK", value=f"{round(disk_usage_mb,2)} MB", inline=True)
        embed.add_field(name="RAM", value=f"{round(memory_usage_mb,2)} MB", inline=True)
        embed.add_field(name="Uptime", value=f"{round(server_utilization['resources']['uptime']/1000/60, 2)} MIN", inline=True)
        embed.set_footer(text=f"{server_running if server_utilization['current_state'] == 'running' else server_stopped}")
        await interaction.response.send_message(embed=embed, view=ControllingServer())

    @discord.ui.button(label=check_user, row=1, style=discord.ButtonStyle.primary)
    async def second_button_callback(self, button, interaction):
        user=api.client.account.get_account()
        user_id=user["attributes"]["id"]
        ifadmin=user["attributes"]["admin"]
        username=user["attributes"]["username"]
        email=user["attributes"]["email"]
        name=user["attributes"]["first_name"] + ' ' + user["attributes"]["last_name"]

        embed=discord.Embed(title=f"{l_username}: {username}", color=0x0084ff)
        embed.add_field(name=l_name, value=f"{name}", inline=True)
        embed.add_field(name="Email", value=f"{email}", inline=True)
        embed.add_field(name="Admin", value=f"{'❌' if ifadmin == False else '✔️'}", inline=True)
        embed.set_footer(text=f"UserID: {user_id}")
        await interaction.response.send_message(embed=embed)

    
class ControllingServer(discord.ui.View):
    @discord.ui.button(label=startserver, row=0, style=discord.ButtonStyle.success)
    async def first_button_callback(self, button, interaction):
        api.client.servers.send_power_action(SERV_ID, 'start')
        await interaction.response.send_message(l_started)
    @discord.ui.button(label=restartserver, row=1, style=discord.ButtonStyle.primary)
    async def second_button_callback(self, button, interaction):
        api.client.servers.send_power_action(SERV_ID, 'restart')
        await interaction.response.send_message(l_restarted)
    @discord.ui.button(label=stopserver, row=0, style=discord.ButtonStyle.danger)
    async def three_button_callback(self, button, interaction):
        api.client.servers.send_power_action(SERV_ID, 'stop')
        await interaction.response.send_message(l_stopped)
    """@discord.ui.button(label=killserver, row=1, style=discord.ButtonStyle.primary)
    async def second_button_callback(self, button, interaction):
        api.client.servers.send_power_action(SERV_ID, 'kill')
        await interaction.response.send_message("Server killed!")"""

@bot.slash_command(name = "menu", description = "Menu")
async def say_hello(ctx):
    await ctx.respond(actions, view=ButtonMain())

@bot.slash_command(name = "execute_command", description = l_execute)
@option(
    "command", 
    description=l_command,
    required=True,
    default=''
)
async def execute_command(ctx, command):
    if command == None:
        await ctx.respond(f"{l_typecommand}")
        return
    exec=api.client.servers.send_console_command(SERV_ID, command)
    await ctx.respond(f"{l_executed} - {command}",)
bot.run(BOT_TOKEN_DISCORD)