<file-attachment-contents filename="README.md">

<h1 align="center">
  <br>
  <a href="https://github.com/SilkePilon/lodestone/"><img src="assets/9990F441-DB4B-4BE1-AAE6-2E8A3EBC5D12.png" alt="Lodestone" width="560"></a>
  <br>
</h1>

<h4 align="center">🤖 An free and fully open source alternative for paid minecraft bots.</h4>

<p align="center">
    <img alt="Node version" src="https://img.shields.io/static/v1?label=node&message=%20%3E=18.0.0&logo=node.js&color=2334D058" />
      <a href="https://python.org/"><img src="https://img.shields.io/badge/Python-FFD43B?logo=python&logoColor=blue" alt="Python"></a>
  <a href="https://github.com/reworkd/AgentGPT/blob/master/docs/README.zh-HANS.md"><img src="https://img.shields.io/badge/JavaScript-323330?logo=minecraft&logoColor=F7DF1E" alt="javascript"></a>
  <a href="soon!"><img src="https://img.shields.io/badge/Discord-5865F2?logo=discord&logoColor=white" alt="Hungarian"></a>
</p>

<p align="center">
  <a href="#about">About</a> •
  <a href="#key-features">Key Features</a> •
  <a href="#how-to-use">How To Use</a> •
  <a href="#how-to-install">Install</a> •
  <a href="#credits">Credits</a> •
  <a href="#license">License</a>
</p>

<!-- ![screenshot](https://raw.githubusercontent.com/SilkePilon/youdotcom/main/assets/images/YouDotCom.jpg) -->

## About 📬

Project Beehive is an open source Minecraft bot with a goal to provide players access to helpful gameplay features at no cost. Developed with a clean user interface, Project Beehive offers various plugins and options similar to paid alternatives out there. The project is completely free, open source, and welcoming to contributions from the Minecraft community. Check the wiki for information on plugins, setup guides, contributing, and more. We aim to provide Minecraft players with an easy-to-use bot to enhance their gameplay experience without needing to pay. Feel free to open issues for bugs, suggestions, or questions!

## Freature and Plugins 🕹
| Plugin | Description | ✅ / ❌ |
|-|-|-|
| BobTheBotter | Follows the owner and kills anybody that gets close to him. | ❌ |   
| Shield aura | Follows the owner. | ❌ |
| Schematic Builder | WARNING before using this read the settings menu | ✅ |
| Raid alerts | Notifies the user on discord when an explosion occurs/mobs appear... | ❌ |
| Area miner | (BETA) Mines the selected zone. | ❌ |
| HypixelAutocrafting | IMPORTANT!! Read the Description in the bot!! | ❌ |  
| Chat spy | Allows you to see a bots chat | ✅ |
| Sugarcane farmer | Mines the closest sugarcane. Once full it stores the items in the closest empty chest. | ❌ (SOON) |
| Ore miner | Mines ores using xray. | ❌ (SOON) |
| ZerGo0.CactusFarmBuilder | Builds a cactus farm for you. (Thanks to @BobTheBotter) | ✅ |
| Auto AFK | Allows you to automatically AFK your farms | ❌ (SOON) |
| Container Viewer | Allows you to inspect the opened inventories of an individual bot. | ❌ (SOON) |
| Chat2Discord | Sends the players chat to a discord channel. | ✅ |
| KnockBack | Makes your bots able to rechieve knockback, for bypassing anticheats, like = ^ | ✅ |
| Chatbot | a basic chat bot which gets more commands every update | ✅ |
| CaptchaBreaker | Auto solves chat, inventory/chest and book captchas. | ❌ |
| SandPrinter | Places sand in the specified area. | ❌ |  
| Discoli.Wander | Aimlessly moves bots around tricking people into thinking they&apos;re real players. | ✅ |
| Sugarcane farm builder | Automatically builds sugarcane farms. | ❌ |
| AutoFisher | Gets you level 99 in fishing. | ❌ |
| Ban checker | Checks if an account is banned on a server and outputs the result. | ❌ |
| Auto eater | Eats food when hungry, eats gapples when low on hp. | ✅ |
| Crop farmer | Farms carrots, potatoes and wheat | ❌ (SOON) |
| eZ.InventoryManager | Allows you to access a bot&apos;s inventory from a windows form | ❌ |  
| ZerGo0.StationaryMobAura | Attacks all mobs around the bot | ❌ |
| Netherwart farmer | Farms netherwarts. | ❌ |
| ZerGo0.TreeFarmer | Farms Trees in a certain area or infinitely | ❌ |
| Term.WindowCaptchaBreaker | Clicks the correct block in a GUI to bypass a captcha | ❌ |  
| No fall | Allows the player to float in the air. | ✅ |
| Killaura | Moves and attacks the closest players. | ❌ (SOON) |
| Tunneler | Digs tunnels and mines ores that it finds. | ❌ |
| AntiCaptcha | Bypass &quot;Please type &apos;abcd&apos; in chat&quot; Captchas! | ❌ |
| Term.AutoArmor | Automatically puts on the best armor the bot current has in its inventory. | ❌ (SOON) |
| JF.Chat2Discord | Send the chat to discord | ✅ |
| Anti Cheat Compliance | Slows down the bots for aggressive anti cheat plugins. | ❌ |
| eZ.ContainerNav | Allows you to navigate a container-based GUI on Minecraft servers e.g lobby selector | ❌ |


## How To Install 📥

### Docker 🐳 (recommended)
If you have Docker installed, you can easily get Project Beehive up and running. Follow the steps below:

1. Open your terminal.

2. Pull the Docker image from the Docker Hub using the following command:

```bash
docker pull thelodestoneproject/beehive:latest
```

After pulling the image, run the Docker container with the following command:

```bash
docker run -p 8000:8000 thelodestoneproject/beehive:latest
```
This command will start the Project Beehive bot and map it to port 8000 on your local machine.

Open your web browser and navigate to http://localhost:8000 to access the bot.
Please note that Docker must be installed and running on your machine to execute these steps. If you don't have Docker installed, you can download it from [here](https://docs.docker.com/get-docker/).

### Python 🐍
If you dont have Docker installed, you can easily get Project Beehive up and running using python. Follow the steps below:

1. Open your terminal.

2. Clone the latest version of this repository using the following command:

```bash
git clone https://github.com/the-lodestone-project/Beehive.git
```

3. Move to the new directory:
```bash
cd Beehive
```

4. Install all the dependencies using following command:
```bash
pip install -r requirements.txt
```
After cloning the repository and installing all the dependencies, run the python script with the following command:

```bash
python main.py
```
This command will start the Project Beehive bot and map it to port 8000 on your local machine.

Open your web browser and navigate to http://localhost:8000 to access the bot.
Please note that Python and pip must be installed and running on your machine to execute these steps. If you don't have python and pip installed, you can download it from [here](https://www.python.org/downloads/).


## images

![alt text](https://i.imgur.com/RRHOgzp.png)

</file-attachment-contents>
