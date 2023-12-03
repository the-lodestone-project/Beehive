import gradio as gr
import lodestone
from lodestone import plugins
import time
from lodestone import logger
from javascript import require
import requests
import threading

global created
created = False
global chat_history
chat_history = []
global plugin_list
plugin_list = []

global bot_list
bot_list = []

global auto_scripts
auto_scripts = {}


def get_bot_status():
    if 'bot' in globals():
        return "Stop Bot"
    else:
        return "Start/Stop Bot"

def change_tab():
    return gr.Tabs.update(selected=1)





def create(email, auth, host, port, version, viewer, plugin, enable_viewer, skip_checks):
    try:
        if 'bot' in globals():
            def stop_bot():
                try:
                    global bot
                    bot.stop()
                    gr.Info("Successfully stopped bot!")
                    del bot
                except Exception as e:
                    print(e)
                    pass
            stop_bot()
            return "Already logged in!", "Already logged in!", "Login/Create Bot"
    except Exception as e:
        print(e)
        pass
    if not host or not email or not version:
        gr.Warning("not all fields are filled in!")
        return "Unknown", "Unknown", "Login/Create Bot"
    
    
    gr.Warning("If its your first time logging in you may need to login using the terminal!")
    
    global bot
    plugin_str = ""
    if plugin:
        plugin_str += "Plugins: "
        for new_plugin in plugin:
            if new_plugin == "Schematic Builder":
                plugin_str += "Schematic Builder, "
                plugin_list.append(plugins.schematic)
            elif new_plugin == "Cactus Farm Builder":
                plugin_str += "Cactus Farm Builder, "
                plugin_list.append(plugins.cactus)
            elif new_plugin == "Discord Rich Presence":
                plugin_str += "Discord Rich Presence, "
                plugin_list.append(plugins.discordrp)
            else:
                pass
    if enable_viewer == False:
        enable_viewer = True
    elif enable_viewer == True:
        enable_viewer = False
    
        
    bot = lodestone.createBot(
        host=host,
        username=email,
        port=port,
        ls_viewer_port=viewer,
        version=version,
        profilesFolder="./cache",
        auth=auth,
        ls_disable_viewer=enable_viewer,
        ls_skip_checks=skip_checks,
        ls_plugin_list=plugin_list
    )
    
    version_check = int(str(bot.bot.version).replace(".",""))
    
    if version_check >= 119:
        gr.Warning(f"Beehive viewer does not currently support {bot.bot.version} this will cause the viewer to not work")
    
    @bot.on('messagestr')
    def chat_history_add(this, message, messagePosition, jsonMsg, sender, *args):
        message = str(message).replace("\n","")
        if str(sender).lower() == "none":
            chat_history.append(f"{message}")
        else:
            chat_history.append(f"{sender}: {message}")
    
    
    if auto_scripts:
        for script in auto_scripts:
            if script["event"] == "Start once spawn":
                for text in script["script"]:
                    if text != "":
                        bot.chat(text)
                        time.sleep(script["delay"])
                gr.Info(f"Successfully ran script {script['name']}")
            elif script["event"] == "Start on time (See Advanced Options)":
                def run_time_script():
                    while True:
                        for text in script["script"]:
                            if text != "":
                                bot.chat(text)
                                time.sleep(script["delay"])
                        time.sleep(script["every"])
                threading.Thread(target=run_time_script).start()
            else:
                pass
    
    
    info =f"""Successfully logged in as {bot.username}"""
    
    
    bot_list.append({f"{email}": bot})
    gr.Info(f"Successfully logged in as {bot.username}\n{plugin_str}")
    return bot.username, info, "Stop Bot"


def create_multiple(email, auth, host, port, version, amount):
    try:
        if 'bot' in globals():
            def stop_bot():
                try:
                    global bot
                    bot.stop()
                    gr.Info("Successfully stopped bot!")
                    del bot
                except Exception as e:
                    print(e)
                    pass
            stop_bot()
            return "Already logged in!", "Already logged in!", "Login/Create Bot"
    except Exception as e:
        print(e)
        pass
    if not host or not email or not version:
        gr.Warning("not all fields are filled in!")
        return "Unknown", "Unknown", "Login/Create Bot"
    
    
    for bots in range(0, amount):
        lodestone.createBot(
            host=host,
            username=email+str(bots),
            port=port,
            ls_disable_viewer=True,
            version=version,
            profilesFolder="./cache",
            auth=auth,
            ls_skip_checks=True,
        )
    
    global bot
    bot = amount
    # @bot.on('messagestr')
    # def chat(this, message, messagePosition, jsonMsg, sender, *args):
    #     message = str(message).replace("\n","")
    #     if str(sender).lower() == "none":
    #         chat_history.append(f"{message}")
    #     else:
    #         chat_history.append(f"{sender}: {message}")
    
    info =f"""Successfully created {amount} bots!"""
    
    
    
    gr.Info(f"Successfully created {amount} bots!")
    return amount, info, "Stop Bot"



def get_username():
    if 'bot' in globals():
        return bot.username
    else:
        return "None"



def get_player_health():
    if 'bot' in globals():
        return bot.health
    else:
        return "Unknown"

def get_player_food():
    if 'bot' in globals():
        return bot.food
    else:
        return "Unknown"
    
def get_player_experience():
    if 'bot' in globals():
        return bot.experience.level
    else:
        return "Unknown"
    
def get_player_difficulty():
    if 'bot' in globals():
        
        if bot.settings.difficulty == 0:
            return "peaceful"
        elif bot.settings.difficulty == 1:
            return "easy"
        elif bot.settings.difficulty == 2:
            return "normal"
        elif bot.settings.difficulty == 3:
            return "hard"
    
    else:
        return "Unknown"
    

def get_all_data():
    if 'bot' in globals():
        return bot.player
    else:
        return "Unknown"




def get_latest_chats():
    if 'bot' in globals():
        if len(chat_history) > 200:
            chat_history.clear()
            return "No chat messages yet!"
        string = ""
        for i in chat_history[-40:]:
            string += i + "\n"
        return string
    else:
        return "No chat messages yet!"



# def upload_file(files):
#     global build_file
#     file_paths = [file.name for file in files]
#     build_file = file_paths
#     print(file_paths)
#     return file_paths


def build_schematic(files, x, z):
    if not x or not z or not files:
        gr.Warning("not all fields are filled in!")
        return
    if 'bot' in globals():
        bot.goto(x=x, y=0, z=z)
        time.sleep(2)
        gr.Info(f"Successfully building schematic at {x}, {z}")
        bot.build_schematic(f'{files.name}')
    else:
        gr.Warning("You need to login first!")
        


with gr.Blocks(theme=gr.themes.Soft(), title="The Lodestone Project") as ui:
    with gr.Tab("Bot Settings"):
        # gr.Markdown(requests.get('https://raw.githubusercontent.com/the-lodestone-project/Lodestone/main/README.md').text)
        # gr.Image("https://github.com/the-lodestone-project/Lodestone/blob/main/assets/logo.png?raw=true", min_width=2000)
        with gr.Tab("Signle Bot"):
            email = gr.Textbox(placeholder="Notch", label="Username",info="Username to login with")
            auth = gr.Dropdown(["microsoft", "offline"], value="microsoft", label="Authentication Method",info="Authentication method to login with")
            host = gr.Textbox(placeholder="2b2t.org", label="Server Ip",info="Server ip to connect to")
            port = gr.Number(value=25565, label="Sever Port", info="Server port to connect to. Most servers use 25565",precision=0)
            version = gr.Dropdown(["auto","1.20", "1.19", "1.18", "1.17", "1.16.4", "1.16", "1.15", "1.14", "1.13", "1.12", "1.11", "1.10", "1.9", "1.8"], value="auto", label="Version",info="Version to connect with. Use auto to automatically detect the version of the server")
            with gr.Accordion("Optional Settings", open=False):
                enable_viewer = gr.Checkbox(value=True, label="Enable Viewer", info="Enable the viewer to see the bot's view",interactive=True)
                skip_checks = gr.Checkbox(value=True, label="Skip Checks/Updates", info="Skip checks to speed up the bot",interactive=True)
                viewer = gr.Number(value=5001, label="Viewer Port", info="Viewer port to display the bot's view",precision=0)
                plugin = gr.Dropdown(["Schematic Builder", "Cactus Farm Builder", "Discord Rich Presence"],multiselect=True, label="Plugins",info="Plugins to load on startup")
            btn = gr.Button(value=get_bot_status,variant='primary')
            
            
            
            
            out_username = gr.Textbox(value="", label="Logged in as")
            info = gr.Textbox(value="", label="Info")
            
            btn.click(create, inputs=[email, auth, host, port, version, viewer, plugin, enable_viewer, skip_checks], outputs=[out_username, info, btn], show_progress="minimal")
        with gr.Tab("Multiple Bots"):
            email = gr.Textbox(placeholder="Notch", label="Username Prefix",info="Username prefix. The bot will login with this prefix and a number after it")
            auth = gr.Dropdown(["offline"], value="offline", label="Authentication Method",info="Authentication method to login with")
            host = gr.Textbox(placeholder="2b2t.org", label="Server Ip",info="Server ip to connect to")
            port = gr.Number(value=25565, label="Sever Port", info="Server port to connect to. Most servers use 25565",precision=0)
            version = gr.Dropdown(["auto","1.20", "1.19", "1.18", "1.17", "1.16.4", "1.16", "1.15", "1.14", "1.13", "1.12", "1.11", "1.10", "1.9", "1.8"], value="auto", label="Version",info="Version to connect with. Use auto to automatically detect the version of the server")
            amount = gr.Slider(minimum=1, maximum=50, step=1, label="Amount", info="Amount of bots to create", interactive=True)
            with gr.Accordion("Optional Settings", open=False):
                enable_viewer = gr.Checkbox(value=False, label="Enable Viewer", info="Enable the viewer to see the bot's view",interactive=False)
                viewer = gr.Number(value=5001, label="Viewer Port", info="Viewer port to display the bot's view",precision=0, interactive=False)
                # plugin = gr.Dropdown(["Schematic Builder", "Cactus Farm Builder", "Discord Rich Presence"],multiselect=True, label="Plugins",info="Plugins to load on startup")
            btn = gr.Button(value=get_bot_status,variant='primary')
            
            
            
            
            out_username = gr.Textbox(value="", label="Bot count")
            info = gr.Textbox(value="", label="Info")
            
            btn.click(create_multiple, inputs=[email, auth, host, port, version, amount], outputs=[out_username, info, btn], show_progress="minimal")
        
        # with gr.Tab("EasyMC"):
        #     email = gr.Textbox(placeholder="********************", label="Token",info="Token to login with")
        #     host = gr.Textbox(placeholder="2b2t.org", label="Server Ip",info="Server ip to connect to")
        #     port = gr.Number(value=25565, label="Sever Port", info="Server port to connect to. Most servers use 25565",precision=0)
        #     version = gr.Dropdown(["auto","1.20", "1.19", "1.18", "1.17", "1.16.4", "1.16", "1.15", "1.14", "1.13", "1.12", "1.11", "1.10", "1.9", "1.8"], value="auto", label="Version",info="Version to connect with. Use auto to automatically detect the version of the server")
        #     with gr.Accordion("Optional Settings", open=False):
        #         enable_viewer = gr.Checkbox(value=True, label="Enable Viewer", info="Enable the viewer to see the bot's view",interactive=True)
        #         skip_checks = gr.Checkbox(value=True, label="Skip Checks/Updates", info="Skip checks to speed up the bot",interactive=True)
        #         viewer = gr.Number(value=5001, label="Viewer Port", info="Viewer port to display the bot's view",precision=0)
        #         plugin = gr.Dropdown(["Schematic Builder", "Cactus Farm Builder", "Discord Rich Presence"],multiselect=True, label="Plugins",info="Plugins to load on startup")
                
            
            
        #     btn = gr.Button(value=get_bot_status,variant='primary')
            
            
            
            
        #     out_username = gr.Textbox(value="", label="Logged in as")
        #     info = gr.Textbox(value="", label="Info")
            
        #     btn.click(create, inputs=[email, auth, host, port, version, viewer, plugin, enable_viewer, skip_checks], outputs=[out_username, info, btn], show_progress="minimal")
        
        # with gr.Tab("The Altening"):
        #     email = gr.Textbox(placeholder="*******@alt.com", label="Token",info="Token to login with")
        #     host = gr.Textbox(placeholder="2b2t.org", label="Server Ip",info="Server ip to connect to")
        #     port = gr.Number(value=25565, label="Sever Port", info="Server port to connect to. Most servers use 25565",precision=0)
        #     version = gr.Dropdown(["auto","1.20", "1.19", "1.18", "1.17", "1.16.4", "1.16", "1.15", "1.14", "1.13", "1.12", "1.11", "1.10", "1.9", "1.8"], value="auto", label="Version",info="Version to connect with. Use auto to automatically detect the version of the server")
        #     with gr.Accordion("Optional Settings", open=False):
        #         enable_viewer = gr.Checkbox(value=True, label="Enable Viewer", info="Enable the viewer to see the bot's view",interactive=True)
        #         skip_checks = gr.Checkbox(value=True, label="Skip Checks/Updates", info="Skip checks to speed up the bot",interactive=True)
        #         viewer = gr.Number(value=5001, label="Viewer Port", info="Viewer port to display the bot's view",precision=0)
        #         plugin = gr.Dropdown(["Schematic Builder", "Cactus Farm Builder", "Discord Rich Presence"],multiselect=True, label="Plugins",info="Plugins to load on startup")
        #     btn = gr.Button(value=get_bot_status,variant='primary')
            
            
            
            
        #     out_username = gr.Textbox(value="", label="Logged in as")
        #     info = gr.Textbox(value="", label="Info")
            
        
        #     btn.click(create, inputs=[email, auth, host, port, version, viewer, plugin, enable_viewer, skip_checks], outputs=[out_username, info, btn], show_progress="minimal")
    
    
    
    
    
    
    with gr.Tab("Chat"):
        chat = gr.Textbox(value=get_latest_chats,every=2,label="Chat History (Updated every 2 seconds)",lines=20, max_lines=20, min_width=100, autoscroll=True, autofocus=False)
        with gr.Accordion("Advanced Options", open=False):
            with gr.Column(scale=1):
                whisper = gr.Checkbox(value=False, label="Whisper", info="Whisper the message to the player",interactive=True)
                whisper_player = gr.Dropdown([],show_label=False, info="The player to whisper to (Updated every 20 seconds)",interactive=True)
            # get_players = gr.Button("Get Players", variant='primary')
            
            
            with gr.Column(scale=1):
                prefix = gr.Textbox(value="", show_label=False, info="Prefix to add to the start of the message",interactive=True)
                suffix = gr.Textbox(value="", show_label=False, info="Suffix to add to the end of the message",interactive=True)
                
                
                
                
            def get_players_def():
                if 'bot' in globals():
                    global players
                    players = []
                    for player in bot.bot.players.valueOf():
                        players.append(player)
                    players.remove(bot.username)
                    return gr.Dropdown(choices=players)
                else:
                    return gr.Dropdown([])
            
            def just_some_random_update():
                return time.time()
            
            updates = gr.Textbox(value=just_some_random_update, every=20, show_label=False, visible=False)
            
            
            updates.change(get_players_def, outputs=[whisper_player])
            
        with gr.Row():
                with gr.Column(scale=2, ):
                    msg = gr.Textbox(show_label=False, container=False, placeholder="Type an message...", autofocus=True)
                with gr.Column(scale=1, ):
                    send_message = gr.Button("Send Message", variant='primary')
        clear = gr.ClearButton([msg, chat],value="Clear Chat History")

        def respond(message, whisper, whisper_player, prefix, suffix):
            if 'bot' in globals():
                if message != "":
                    if whisper and whisper_player != None or "":
                        bot.whisper(whisper_player, f"{prefix}{message}{suffix}")
                    if not whisper:
                        bot.chat(f"{prefix}{message}{suffix}")
                return ""
            else:
                gr.Warning("You need to create a bot first!")
                return ""
        
        def delete():
            chat_history.clear()
        
        clear.click(delete)
        send_message.click(respond, inputs=[msg, whisper, whisper_player, prefix, suffix],outputs=[msg])
        msg.submit(respond, inputs=[msg, whisper, whisper_player, prefix, suffix],outputs=[msg])
        
    with gr.Tab("Plugins"):
        with gr.Accordion("Schematic Builder", open=False):
            # with gr.Row():
            #     with gr.Column(scale=1, ):
            file_output = gr.File(file_types=[".schematic", ".nbt", ".schem"], label="Schematic File (.schematic .nbt .schem)",file_count="single")
            with gr.Row():
                with gr.Column(scale=1, ):
                    x = gr.Number(label="X Coordinate",info="The X coord to build at", precision=0)
                with gr.Column(scale=1, ):
                    z = gr.Number(label="Z Coordinate",info="The Z coord to build at", precision=0)
            # upload_button = gr.UploadButton("Click to Upload a schematic", file_count="single")
            # upload_button.upload(upload_file, upload_button, file_output)
            build = gr.Button("Build schematic", variant='primary')
            build.click(build_schematic, inputs=[file_output, x, z])
            
            
        with gr.Accordion("Build Cactus Farm", open=False):
            gr.Markdown("")
            
        with gr.Accordion("Auto Farm", open=False):
            with gr.Row():
                with gr.Column(scale=1, ):
                    crop_type = gr.Dropdown(["wheat_seeds", "wheat", "beetroot_seeds", "beetroot", "carrot", "potato", "poisonous_potato", "melon", "melon_slice", "melon_seeds", "melon_stem", "attached_melon_stem", "pumpkin", "carved_pumpkin", "pumpkin_seeds", "pumpkin_stem", "attached_pumpkin_stem", "torchflower_seeds", "torchflower_crop", "torchflower", "pitcher_pod", "pitcher_crop", "pitcher_plant", "farmland", "bamboo", "cocoa_beans", "sugar_cane", "sweet_berries", "cactus", "mushrooms", "kelp", "sea_pickle", "nether_wart", "chorus_fruit", "fungus", "glow_berries"], label="Crop Type",info="The Crop type to farm", interactive=True)
                with gr.Column(scale=1, ):
                    seed_name = gr.Dropdown(["wheat_seeds", "wheat", "beetroot_seeds", "beetroot", "carrot", "potato", "poisonous_potato", "melon", "melon_slice", "melon_seeds", "melon_stem", "attached_melon_stem", "pumpkin", "carved_pumpkin", "pumpkin_seeds", "pumpkin_stem", "attached_pumpkin_stem", "torchflower_seeds", "torchflower_crop", "torchflower", "pitcher_pod", "pitcher_crop", "pitcher_plant", "farmland", "bamboo", "cocoa_beans", "sugar_cane", "sweet_berries", "cactus", "mushrooms", "kelp", "sea_pickle", "nether_wart", "chorus_fruit", "fungus", "glow_berries"], label="Seed Name",info="The Seed name to plant back", interactive=True)
                with gr.Column(scale=1, ):
                    harvest_name = gr.Dropdown(["wheat_seeds", "wheat", "beetroot_seeds", "beetroot", "carrot", "potato", "poisonous_potato", "melon", "melon_slice", "melon_seeds", "melon_stem", "attached_melon_stem", "pumpkin", "carved_pumpkin", "pumpkin_seeds", "pumpkin_stem", "attached_pumpkin_stem", "torchflower_seeds", "torchflower_crop", "torchflower", "pitcher_pod", "pitcher_crop", "pitcher_plant", "farmland", "bamboo", "cocoa_beans", "sugar_cane", "sweet_berries", "cactus", "mushrooms", "kelp", "sea_pickle", "nether_wart", "chorus_fruit", "fungus", "glow_berries"], label="Harvest Name",info="The block name to harvest", interactive=True)
                
            with gr.Row():
                with gr.Column(scale=1, ):
                    x = gr.Number(label="X Coordinate",info="The X coord to build at", precision=0)
                with gr.Column(scale=1, ):
                    z = gr.Number(label="Z Coordinate",info="The Z coord to build at", precision=0)
            
            with gr.Row():
                with gr.Column(scale=1, ):
                    x = gr.Number(label="X Coordinate",info="The X coord to build at", precision=0)
                with gr.Column(scale=1, ):
                    z = gr.Number(label="Z Coordinate",info="The Z coord to build at", precision=0)
            with gr.Accordion("Optional Settings", open=False):
                gr.Markdown("Optional Settings")
            start_farm = gr.Button("Start auto Farming", variant='primary')
            
        with gr.Accordion("Discord Rich Presence", open=False):        
            with gr.Row():
                with gr.Column(scale=1, ):
                    state = gr.Textbox(label="State",info="The state to display")
                with gr.Column(scale=1, ):
                    details = gr.Textbox(label="Details",info="The details to display")
                with gr.Column(scale=1, ):
                    large_image = gr.Textbox(label="Large Image (url)",info="The large image to display")
                with gr.Column(scale=1, ):
                    large_text = gr.Textbox(label="Large Text",info="The large text to display")
                with gr.Column(scale=1, ):
                    small_image = gr.Textbox(label="Small Image (url)",info="The small image to display")
                with gr.Column(scale=1, ):
                    small_text = gr.Textbox(label="Small Text",info="The small text to display")
            
            def update_presence_def(state="No state provided", details="No details Provided", large_image=None, large_text=None, small_image=None, small_text=None):
                print(details)
                if 'bot' in globals():
                    bot.discordrp(state=state, details=details, start=time.time())
                    gr.Info("Successfully updated presence!")
                else:
                    pass
            
            update_presence = gr.Button("Update Presence", variant='primary')
            update_presence.click(update_presence_def, inputs=[state, details, large_image, large_text, small_image, small_text])
            
    
    with gr.Tab("Movements"):
        with gr.Tab("Basic Movements"):
            with gr.Row():
                with gr.Column(scale=1, ):
                    jump = gr.Button("Start Jumping")
                    jump = gr.Button("Stop Jumping")
                with gr.Column(scale=1, ):
                    jump = gr.Button("Start walking forward")
                    jump = gr.Button("Stop walking forward")
        with gr.Tab("Follow Player/Entity"):
            gr.Markdown("")
            
    
    with gr.Tab("Automation"):
        with gr.Tab("Script Scheduler"):
            with gr.Row():
                with gr.Column(scale=2, ):
                    new_script = gr.Textbox(placeholder="Enter your chat commands here.",every=2,label="Automated Script",lines=20, max_lines=20, min_width=100, autoscroll=True, autofocus=False)
                with gr.Column(scale=1, ):
                    with gr.Accordion("Active Scripts", open=True):
                        def get_active_scripts():
                            # string = ""
                            # for script_name, script_data in auto_scripts.items():
                            #     string += f"""### {script_data['name']}\nCommands:\n"""
                            #     scripts = [text for text in str(script_data["script"]).split("\n")]
                            #     for text in scripts:
                            #         if text != "":
                            #             string += f"""* {text}\n"""
                            #     string += f"""\n"""
                            #     string += f"""Every {script_data['every']} seconds\n\n"""
                            #     string += f"""Delay: {script_data['delay']} seconds\n\n"""
                            #     string += """---\n"""
                            # return string
                            return auto_scripts
                        
                        gr.JSON(value=get_active_scripts, label="Active Scripts (Updated every 5 seconds)", every=5)
            with gr.Accordion("Advanced Script Options", open=False):
                every_time = gr.Number(value=100, label="Every (seconds)",info="How often to run the script (in seconds)",interactive=True)
                script_delay = gr.Slider(minimum=1, maximum=50, step=1, label="Delay (seconds)",info="Delay between chat commands (in seconds)",interactive=True)

            with gr.Row():
                    with gr.Column(scale=2, ):
                        script_name = gr.Textbox(show_label=False, container=False, placeholder="Script Name", autofocus=True)
                    with gr.Column(scale=1, ):
                        script_start_on = gr.Dropdown(choices=["Start once spawn", "Start on time (See Advanced Options)"], value="Start once spawn", show_label=False, container=False, )
                    with gr.Column(scale=1, ):
                        add_script_to = gr.Button("Add Script", variant='primary')
            clear = gr.ClearButton([script_name],value="Remove All Scripts")
            
            def delete():
                auto_scripts.clear()
                gr.Info("Successfully removed all scripts!")
                
            
            def add_script(new_script, every_time, script_name, script_start_on, script_delay):
                global auto_scripts
                if not new_script or not every_time or not script_name or not script_start_on:
                    gr.Warning("not all fields are filled in!")
                    return new_script, script_name
                else:   
                    commands = [text for text in str(new_script).split("\n")]
                    auto_scripts[script_name] = {"script": commands, "every": every_time, "name": script_name, "event": script_start_on, "delay": script_delay}
                    gr.Info(f"Successfully added script {script_name} to the scheduler!")
                    return "", ""
            
            clear.click(delete)
            add_script_to.click(add_script, inputs=[new_script, every_time, script_name, script_start_on, script_delay], outputs=[new_script, script_name])
                
            

    with gr.Tab("Player Info"):
        # refresh_button = gr.Button("Refresh")
        with gr.Accordion("Bot Info", open=False):
            with gr.Row():
                with gr.Column(scale=1):
                    health = gr.Textbox(value=get_player_health, label=f"Health", every=5)
                with gr.Column(scale=1):
                    food = gr.Textbox(value=get_player_food, label=f"Food", every=5)
                with gr.Column(scale=1):
                    experience = gr.Textbox(value=get_player_experience, label=f"Experience Level", every=5)
                with gr.Column(scale=1):
                    difficulty = gr.Textbox(value=get_player_difficulty, label=f"Difficulty", every=5)
                with gr.Column(scale=1):
                    all_data = gr.Textbox(value=get_all_data, label=f"All Data", every=5)
        with gr.Accordion("Online Player Info", open=False):
            pass
        # refresh_button.click(get_player_info, outputs=[health, food, experience])

    with gr.Tab("System Resources"):
        # refresh_button = gr.Button("Refresh")
        import psutil
        import platform
        
        def cpu():
            return psutil.cpu_percent(interval=5)
        
        def ram_used():
            return psutil.virtual_memory().percent
        
        def ram_available():
            
            ram=  psutil.virtual_memory().available / (1024.0 ** 3)
            return "{:.1f}".format(ram)
        
        
        with gr.Row():
            with gr.Column(scale=1):
                health = gr.Textbox(value=ram_used, label=f"Ram Used (%)", every=5)
            with gr.Column(scale=1):
                food = gr.Textbox(value=ram_available, label=f"Available Ram (GB)", every=5)
            with gr.Column(scale=1):
                experience = gr.Textbox(value=cpu, label=f"CPU usage (%)", every=5)
            with gr.Column(scale=1):
                difficulty = gr.Textbox(value=platform.system, label=f"System Type")
        # refresh_button.click(get_player_info, outputs=[health, food, experience])
    
# import os
# from dotenv import load_dotenv
# import socket
# import requests
# s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
# s.connect(("8.8.8.8", 80))
# host = s.getsockname()[0]
# s.close()
    
# load_dotenv()

username = "lodestone"
password = "lodestone"

# if not os.path.isfile("/favicon.ico"):
#     img_data = requests.get("https://github.com/the-lodestone-project/Lodestone/raw/main/assets/favicon.png").content
#     with open('/favicon.png', 'wb') as handler:
#         handler.write(img_data)


try:
    logger.info("Running!\nURL: http://localhost:8000\nUsername: lodestone\nPassword: lodestone\n")
    ui.queue().launch(inbrowser=True,ssl_verify=False, server_name="0.0.0.0",server_port=8000, show_api=False, auth=(f'{username}', f'{password}'), share=False, quiet=True, auth_message="Please login with your set username and password. These are not your Minecraft credentials.")
except OSError:
    raise OSError(f"Port 8000 is already in use!")
    
