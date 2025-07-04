import os
from time import sleep
import traceback
import subprocess
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
            close(server_instances)

        user_selections = {
            "Start Server": start_server,
            "Stop Server": stop_server,
            "Exit": close
        }

        selection_names = list(user_selections.keys())

        user_selection = None
        while not user_selection:
            user_selection = None  # Resets the value in case of bad input
            print("Please select the desired option: ")
            for selection_number, selection_name in enumerate(selection_names):
                print(f"\t{selection_number + 1}. {selection_name}")
            user_selection = input().strip().lower()

            if not user_selection.isdigit():
                print("You did not select a valid choice")
                continue
            user_selection = int(user_selection)
            if not 0 < user_selection <= len(selection_names):
                print("You did not select a valid choice")
                continue

            user_selections[selection_names[user_selection - 1]](server_instances)


def start_server(server_instances):
    map_name, selected_map = prompt_for_map(server_instances)
    if map_name in server_instances.keys():
        print("That map is already running. Restart all servers and the manager if you're having problems.")
        return

    command = format_map_command(map_name, selected_map)

    print(f"Starting map {map_name}. Startup settings:\n\t{" ".join(command)}")

    thread = Thread(target=start_server_instance, args=(map_name, command, server_instances))
    thread.start()
    thread.join()


def stop_server(server_instances):
    selection_names = list(server_instances.keys())
    user_selection = None  # Resets the value in case of bad input
    print("Please select the desired option: ")
    for selection_number, selection_name in enumerate(selection_names):
        print(f"\t{selection_number + 1}. {selection_name}")
    user_selection = input().strip().lower()

    if not user_selection.isdigit():
        print("You did not select a valid choice")
        return
    user_selection = int(user_selection)
    if not 0 < user_selection <= len(selection_names):
        print("You did not select a valid choice")
        return

    server_instances[selection_names[user_selection - 1]].terminate()


def prompt_for_map(server_instances):
    server_selection = None
    ark_maps = list(MAPS_AND_PORTS.keys())

    print("Please select the desired map: ")
    for map_number, ark_map in enumerate(ark_maps):
        print(f"\t{map_number + 1}. {ark_map}")
    server_selection = input().strip().lower()

    if server_selection in ['exit', 'close', 'quit']:
        close(server_instances)

    if not server_selection.isdigit():
        print("You did not select a valid choice")
        return
    server_selection = int(server_selection)
    if not 0 < server_selection <= len(ark_maps):
        print("You did not select a valid choice")
        return

    server_selection = ark_maps[server_selection-1]
    return server_selection, MAPS_AND_PORTS[server_selection]


def check_running_servers(server_instances):
    while True:
        if EXIT:
            return
        sleep(1)
        prunes = []
        for map_name, process in server_instances.items():
            status = process.poll()
            if status:
                print(f"Map {map_name} is no longer running")
                prunes.append(map_name)
        if prunes:
            for prune in prunes:
                del server_instances[prune]
            print(f"Last known running servers:")
            for running_map_name in server_instances.keys():
                print(f"\t{running_map_name}")


def format_map_command(map_name, map_config):
    command = [
        f'{INSTALL_LOCATION}',
        f'{map_config['map']}' +
        f'?SessionName={SERVER_NAME + map_name}' +
        f'?GameServerQueryPort={map_config['ports'][2]}'
    ]
    for x in SETTINGS:
        command.append(f'-{x}')
    command.append(f'-port={map_config['ports'][0]}')

    if MODS:
        command.append("-mods=\"" + ",".join(list(map(str, MODS))) + "\"")
    return command


def start_server_instance(map_name, command, server_instances):
    server_instance = subprocess.Popen(command)
    server_instances[map_name] = server_instance


def close(server_instances):
    print("Exiting...")
    for map_name, server_instance in server_instances.items():
        server_instance.terminate()
    global EXIT
    EXIT = True
    exit(1)


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print("".join(traceback.format_exception(e)))
        input()
