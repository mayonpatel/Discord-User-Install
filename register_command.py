import requests

def register_command():
    try:
        APPLICATION_ID = os.environ["DISCORD_APP_ID"]
        BOT_TOKEN = os.environ["DISCORD_BOT_TOKEN"]
        url = f"https://discord.com/api/v10/applications/{APPLICATION_ID}/commands"
        headers = {
            "Authorization": f"Bot {BOT_TOKEN}",
            "Content-Type": "application/json"
        }
        json_data = {
            "name": "whatvaradhan",
            "type": 1,
            "description": "Tell the truth about Varadhan"
        }
        r = requests.post(url, headers=headers, json=json_data)
        print("Command registration status:", r.status_code)
        print(r.json())
    except Exception as e:
        print("Command registration failed:", e)
