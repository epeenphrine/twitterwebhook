import config
import requests


def message(url):
## webhooking
                discord_webhook_url = config.discord_webhook_url
                # Post the message to the Discord webhook
                data = {
                    "content": f"{url}"
                }
                data2 = {
                    "content": "!c2 spy"
                }
                requests.post(discord_webhook_url, data=data)