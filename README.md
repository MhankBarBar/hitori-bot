<p align="center">
  <img src="https://i.ibb.co/TKfNh1r/bocchi.png" height="200px" alt="bocchi"/>
  <h3 align="center">Hitori Bot is Multipurpose WhatsApp Bot Written in Python</h3>
</p>

# Requirements
- [Python 3.9+](https://www.python.org/downloads/) (Recommended)
- [Node.js](https://nodejs.org/en/download/)
- [FFmpeg](https://ffmpeg.org/download.html)

# Installation

### Clone this project
```cmd
> git clone https://github.com/MhankBarBar/hitori-bot
> cd hitori-bot
```
### Install the dependencies:
```cmd
> pip3 install -r requirements.txt
```
### Usage
replace the `secure_api_key` with whatever you want
```cmd
> npx @open-wa/wa-automate --socket -p 8085 -k secure_api_key --use-chrome
> python3 main.py
```
also don't forget to replace this part with your own secure_api_key in `main.py` on line 6
```python
KEY = 'your secure api key here'
```
#### Cli usage
For advanced users, you can use cli to run the bot, this command will automatically restart program when file changed/modified
```cmd
> python3 -m cli run --debug
```
### Configuration
open `config.json` and change this part with whatever you want
```json
{
    "authorSticker": "MhankBarBar",
    "chatGPT": "",
    "owner": "62xxxxxx@c.us",
    "packSticker": "Hitori Bot",
    "prefix": "!"
}
```
### How to get chatGPT api-key?
1. Create account on OpenAI
2. Go to https://platform.openai.com/account/api-keys
3. Copy API key and paste it on `config.json`


# Features
|     Feature     | Status |
|:---------------:|:------:|
| Sticker Creator |   ✅    |
|   Downloader    |   ✅    |
|  Group Manager  |   ✅    |
| Image Converter |   ✅    |
| Genshin Impact  |   ✅    |
|  Owner Command  | `Todo` |
