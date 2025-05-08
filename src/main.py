import os
from time import sleep
import traceback
from multiprocessing import Process
from threading import Thread

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


# THIS IS NOT A SETTING. DO NOT CHANGE
EXIT = False


def main():

    server_instances = {}
    checking_thread = Thread(target=check_running_servers, args=(server_instances,))
    checking_thread.start()

    while True:

        print(f"Last known running servers:")
        for running_map_name in server_instances.keys():
            print(f"\t{running_map_name}")

        if not os.path.exists(INSTALL_LOCATION):
            input("Could not find server executable. Check installation directory. Press enter to close.")
            close()

        map_name, selected_map = prompt_for_map()
        if map_name in server_instances.keys():
            print("That map is already running. Restart all servers and the manager if you're having problems.")
            close()

        command = format_map_command(map_name, selected_map)

        print(f"Starting map {map_name}. Startup settings:\n\t{command}")
        server_instance = Process(target=os.system, args=(command,))
        server_instance.start()
        server_instances[map_name] = server_instance


def prompt_for_map():
    server_selection = None
    ark_maps = list(MAPS_AND_PORTS.keys())

    while not server_selection:
        server_selection = None  # Resets the value in case of bad input
        print("Please select the desired map: ")
        for map_number, ark_map in enumerate(ark_maps):
            print(f"\t{map_number + 1}. {ark_map}")
        server_selection = input()

        if not server_selection.isdigit():
            print("You did not select a valid choice")
            continue
        server_selection = int(server_selection)
        if not 0 < server_selection <= len(ark_maps):
            print("You did not select a valid choice")
            continue

        break

    server_selection = ark_maps[server_selection-1]
    return server_selection, MAPS_AND_PORTS[server_selection]


def check_running_servers(server_instances):
    while True:
        if EXIT:
            return
        sleep(1)
        prunes = []
        for map_name, process in server_instances.items():
            process.join(timeout=0)
            if not process.is_alive():
                print(f"Map {map_name} is no longer running")
                prunes.append(map_name)
        for prune in prunes:
            del server_instances[prune]


def format_map_command(map_name, map_config):
    command = f"start {INSTALL_LOCATION} " + \
              f"{map_config['map']}"
    command += f'?SessionName={SERVER_NAME + map_name}?GameServerQueryPort={map_config['ports'][2]}'

    for x in SETTINGS:
        command += f' -{x}'
    command += f' -port={map_config['ports'][0]}'

    if MODS:
        command += " -mods=\"" + ",".join(list(map(str, MODS))) + "\""
    return command


def close():
    global EXIT
    EXIT = True
    exit(1)


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print("".join(traceback.format_exception(e)))
        input()
