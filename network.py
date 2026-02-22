import asyncio, json, requests, time, threading
from aiortc import (
    RTCPeerConnection,
    RTCSessionDescription,
    RTCConfiguration,
    RTCIceServer,
)
from random import *
from queue import Queue

import game_logic


# Ajout des paramètres de la base de donnée Firebase
API_KEY = "AIzaSyCYI_3pSmQTPU2YtLcMlPCW0ch8qurqbEs"
PROJECT_ID = "projet-sup-epita"

# Déclaration globale datachannel et boucle réseau pour intercommunication des boucles
channel = None  # Channel à créer
network_loop = None  # Loop réseau

# Event globale pour prevenir que le réseau est près (connexion établie)
network_ready = threading.Event()

# Queue globale pour la reception des messages
incoming_messages = Queue()

# Evenement pour arreter la connexion qd on ferme le jeu et gestion de quand on quitte la partie
stop_event = None
pc_global = None

# Contexte du jeu
game_context = None
local_player = None
distant_player = None

def share_context_multi(fen_context):
    global game_context, local_player, distant_player
    game_context = fen_context

    if not game_context.multiplayer:
        local_player = game_context.host_player
        distant_player = game_context.client_player

def reset_network():
    global network_ready,pc_global,channel,stop_event
    if network_ready:
        network_ready.clear()
    pc_global = None
    channel = None
    # stop_event = None
    print("reseau :",network_ready.is_set())

def start_network(is_host):
    if game_context.multiplayer:
        # Lancement de la boucle de connexion dans un endroit séparé de la boucle principale du jeu
        thread = threading.Thread(target=_network_thread, args=(is_host,), daemon=True)
        thread.start()


def _network_thread(is_host):
    global local_player, distant_player, stop_event, pc_global

    stop_event = threading.Event()

    config = RTCConfiguration(
        iceServers=[RTCIceServer(urls=["stun:stun.l.google.com:19302"])]
    )
    pc = RTCPeerConnection(config)
    pc_global = pc

    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    if is_host:
        local_player = game_context.host_player
        distant_player = game_context.client_player
        loop.run_until_complete(start_host(pc))
    else:
        local_player = game_context.client_player
        distant_player = game_context.host_player
        loop.run_until_complete(start_client(pc))

    loop.close()


async def start_host(pc):
    global channel, network_loop
    channel = pc.createDataChannel("game_chanel")

    @channel.on("open")
    def on_open():
        # À faire quand on ouvre le datachannel
        print("DataChannel ouvert.")
        network_ready.set()

    @channel.on("message")
    def on_message(message):
        # À faire quand on reçois un message
        print("← message reçu du client:", message)
        incoming_messages.put(message)

    offer = await pc.createOffer()
    await pc.setLocalDescription(offer)

    game_code = find_code(generate_game_code())
    game_data = {
        "fields": {
            "offer": {
                "stringValue": json.dumps(
                    {"sdp": pc.localDescription.sdp, "type": pc.localDescription.type}
                )
            },
            "answer": {"nullValue": None},
        }
    }

    create_lobby(game_code, game_data)
    game_context.edit_game_code(game_code)
    print("Code de partie : " + game_code)
    print("\n-----------------------------------\n")

    answer = wait_for_answer(game_code)
    await pc.setRemoteDescription(
        RTCSessionDescription(sdp=answer["sdp"], type=answer["type"])
    )
    network_loop = asyncio.get_running_loop()
    while not stop_event.is_set():
        await asyncio.sleep(0.01)

    print("Fermeture du DataChannel...")
    if channel and channel.readyState == "open":
        channel.close()
    await pc.close()


async def start_client(pc):
    global channel, network_loop

    @pc.on("datachannel")
    def on_datachannel(channelp):
        global channel
        print("DataChannel reçu.")
        channel = channelp
        network_ready.set()
        @channel.on("message")
        def on_message(message):
            print("← message reçu du host:", message)
            incoming_messages.put(message)

    game_code, offer = wait_for_offer(game_context.game_code)

    await pc.setRemoteDescription(
        RTCSessionDescription(sdp=offer["sdp"], type=offer["type"])
    )

    answer = await pc.createAnswer()
    await pc.setLocalDescription(answer)

    add_answer_to_db(pc, game_code)

    print("\n---------------------------------\n")

    network_loop = asyncio.get_running_loop()
    while not stop_event.is_set():
        await asyncio.sleep(0.01)


# ========== Gestion de la création de la partie et de l'envoie des offres / réponses =========


def generate_game_code():
    """Génère aléatoirement un code de partie (5 lettres majuscules)"""
    alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    res = ""
    for _ in range(5):
        res += choice(alphabet)
    return res


def find_code(code):
    """S"assure que le code de partie mis en paramètre n'existe pas encore, sinon, en génère un nouveau."""
    url = f"https://firestore.googleapis.com/v1/projects/{PROJECT_ID}/databases/(default)/documents/lobbies/{code}?key={API_KEY}"
    res = requests.get(url)
    if res.status_code == 404:  # N'existe pas
        return code
    elif res.status_code == 200:
        find_code(generate_game_code())
    else:
        return res.text


def create_lobby(code, data):
    """Ajoute à la base de donnée la partie avec l'offre sdp."""
    url = f"https://firestore.googleapis.com/v1/projects/{PROJECT_ID}/databases/(default)/documents/lobbies?documentId={code}&key={API_KEY}"
    res = requests.post(url, json=data)
    if res.status_code == 200:
        print(f"Lobby créé.")
    else:
        print("Erreur:", res.text)


def add_answer_to_db(pc, code):
    """Modifie la base de donnée pour mettre la réponse du client."""
    url = f"https://firestore.googleapis.com/v1/projects/{PROJECT_ID}/databases/(default)/documents/lobbies/{code}?key={API_KEY}"
    res = requests.patch(
        url,
        params={"updateMask.fieldPaths": "answer"},
        json={
            "fields": {
                "answer": {
                    "stringValue": json.dumps(
                        {
                            "sdp": pc.localDescription.sdp,
                            "type": pc.localDescription.type,
                        }
                    )
                }
            }
        },
    )
    if res.status_code == 200:
        print("Réponse envoyée")
    else:
        print("Erreur:", res.text)


# ===== Récupération des offres et réponses sdp


def wait_for_answer(code):
    """Check en continue si la réponse a été rempli dans la db"""
    print("En attente de la réponse de l'autre joueur")
    searching_answer = True
    url = f"https://firestore.googleapis.com/v1/projects/{PROJECT_ID}/databases/(default)/documents/lobbies/{code}?key={API_KEY}"
    while searching_answer:
        res = requests.get(url)
        if res.status_code == 200:
            doc = res.json()
            if doc["fields"]["answer"] != {"nullValue": None}:
                print("Réponse reçu.")
                answer = json.loads(doc["fields"]["answer"]["stringValue"])
                searching_answer = False
            else:
                time.sleep(5)
        else:
            print("Erreur:", res.text)
    return answer


def wait_for_offer(code):
    """Check en continue si l'offre sdp est prsente / si la partie a été créée dans la db"""
    wait_for_offer = True
    while wait_for_offer:
        code = game_context.game_code
        if code not in ("","wrong_code"):
            # récupération de l'offre
            url = f"https://firestore.googleapis.com/v1/projects/{PROJECT_ID}/databases/(default)/documents/lobbies/{code}?key={API_KEY}"
            res = requests.get(url)
            if res.status_code == 200:
                doc = res.json()
                offer = json.loads(doc["fields"]["offer"]["stringValue"])
                wait_for_offer = False
            else:
                print("Mauvais code de partie, demande d'un nouveau code")
                game_context.edit_game_code("wrong_code")
        time.sleep(0.5)
    return (code, offer)


# Envoie de data via le datachannel
def send_data(data):
    global channel, network_loop
    if network_loop and not network_loop.is_closed():
        if (channel == None) or (channel.readyState != "open"):
            print(channel,"Channel pas prêt, impossible d'envoyer :", data)
        else:
            network_loop.call_soon_threadsafe(channel.send, data)
    else:
        print(channel,"Channel pas prêt, impossible d'envoyer :", data)


# ===== Gestion globale du jeu =====

def initiate_game():
    """Cette fonction permet de lancer la partie en elle-même : c'est elle qui contient la boucle principale"""
    global has_sent_quit
    network_interval = 16  # 1000 ms -> 1 FPS réseau
    last_network_send = game_logic.now()
    multi_activated = game_context.multiplayer
    game_context.running = True
    distant_player_quitting = False
    while game_context.running:  # Boucle du jeu
        # Reception des messages et update des coordonnées
        if multi_activated:
            while not incoming_messages.empty() and game_context.running:
                msg = incoming_messages.get()
                data = json.loads(msg)
                if data["msg"] == "player_quitting":
                    game_context.running = False
                    distant_player_quitting = True
                    print("L'autre joueur a quitté la partie")
                else:
                    distant_player.x = data["player_coords"][0]
                    distant_player.y = data["player_coords"][1]
        # Gestion boucle réseau :
        if (
            multi_activated
            and game_context.running
            and not stop_event.is_set()
        ):
            #print(game_context.running)
            now = game_logic.now()
            if now - last_network_send >= network_interval:
                send_data(json.dumps({
                    "msg":"",
                    "player_coords": local_player.get_pos()
                }))
                last_network_send = now

        game_logic.update_game(game_context, local_player, distant_player)

    if multi_activated:
        if not distant_player_quitting:
            send_data(json.dumps({
                "msg": "player_quitting",
                "player_coords": (0,0)
            }))
        time.sleep(0.5)
        stop_event.set()