import json

from steam import Steam as MySteam

from decouple import config


KEY = config("STEAM_API_KEY")

terraria_app_id = 105600
steam = MySteam(KEY)

# arguments: app_id
user = steam.apps.get_app_details(terraria_app_id)
print(user)


