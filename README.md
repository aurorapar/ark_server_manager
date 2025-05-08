Just a tool to help manage multiple instances of ARK servers via CLI

All options are near the top of `main.py`. Set these to desired settings, and then view options in the below image.

```
INSTALL_LOCATION = r"C:\arksa\ShooterGame\Binaries\Win64\ArkAscendedServer.exe"
CLUSTER_ID = "SpawningPool"
SERVER_NAME = "The Spawning Pool - "
MAPS_AND_PORTS = {
    "The Center": {
        "map": "TheCenter_WP",
        "ports": [7777, 7778, 27015]
    },
    "The Island": {
        "map": "TheIsland_WP",
        "ports": [7779, 7780, 27016]
    },
}
SETTINGS = [
    'NoTransferFromFiltering',
    'ForceAllowCaveFlyers',
    'NoBattlEye'
]
MODS = [
    928603,  # Easy Mutations
    929420   # Super SpyGlass Plus
]
```

![image](https://github.com/user-attachments/assets/80b3ee50-76ea-439b-b54a-4cc0154c805d)

