import asyncio, json, requests,time, threading
from aiortc import RTCPeerConnection, RTCSessionDescription, RTCConfiguration, RTCIceServer
from random import *
from queue import Queue

import game_logic

# Ajout des paramètres de la base de donnée Firebase
API_KEY = "AIzaSyCYI_3pSmQTPU2YtLcMlPCW0ch8qurqbEs"
PROJECT_ID = "projet-sup-epita"

# Déclaration globale datachannel et boucle réseau pour intercommunication des boucles
channel = None # Chanel à créer
network_loop = None # Loop réseau

# Queue globale pour les messages
incoming_messages = Queue() 

# evenement pour arrèter la connexion
stop_event = None

# Contexte du jeu 
game_context = None
local_player = None 
distant_player = None 

def start_network(is_host,fen_context):
    global stop_event, game_context, local_player, distant_player
    # Creation d'un event pour arreter la connexion
    stop_event = asyncio.Event()
    # Enregistrement du contexte de la fenetre pygame
    game_context = fen_context

    # Configuration de la connection P2P
    config = RTCConfiguration(
        iceServers=[RTCIceServer(urls=["stun:stun.l.google.com:19302"])]
    )
    pc = RTCPeerConnection(config)

    if is_host:
        local_player = game_context.host_player
        distant_player = game_context.client_player
        asyncio.run(start_host(pc))
    else:
        local_player = game_context.client_player
        distant_player = game_context.host_player
        asyncio.run(start_client(pc))

async def start_host(pc):
    global channel, network_loop
    channel = pc.createDataChannel("game_chanel")

    @channel.on("open")
    def on_open():
        # À faire quand on ouvre le datachannel
        print("🔔 DataChannel ouvert (offer).")
        # Lancement du jeu dans un environnement à part
        threading.Thread(target=initiate_game, daemon=True).start()

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
            "offer": {"stringValue": json.dumps({"sdp": pc.localDescription.sdp, "type": pc.localDescription.type})},
            "answer": {"nullValue": None}
        }
    }

    create_lobby(game_code,game_data)
    print("Code de partie : "+ game_code)
    print("\n-----------------------------------\n")

    answer = wait_for_answer(game_code)
    await pc.setRemoteDescription(RTCSessionDescription(sdp=answer["sdp"], type=answer["type"]))
    network_loop = asyncio.get_running_loop()
    await stop_event.wait()

async def start_client(pc):
    global channel, network_loop

    @pc.on("datachannel")
    def on_datachannel(channel):
        print("🔔 DataChannel reçu (answer).")
        # Lancement du jeu dans un environnement à part
        threading.Thread(target=initiate_game, daemon=True).start()
        @channel.on("open")
        def on_open():
            # À faire quand on ouvre le datachannel
            pass
            
        @channel.on("message")
        def on_message(message):
            print("← message reçu du host:", message)
            incoming_messages.put(message)
            channel.send(json.dumps(local_player.get_pos()))
            
    game_code = input("Code de la game : ")
    game_code,offer = wait_for_offer(game_code)

    await pc.setRemoteDescription(RTCSessionDescription(sdp=offer["sdp"], type=offer["type"]))

    answer = await pc.createAnswer()
    await pc.setLocalDescription(answer)

    add_answer_to_db(pc,game_code)
    
    print("\n---------------------------------\n")

    network_loop = asyncio.get_running_loop()
    await stop_event.wait()

# ========== Gestion de la création de la partie et de l'envoie des offres / réponses =========

def generate_game_code():
    """ Génère aléatoirement un code de partie (5 lettres majuscules)"""
    alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    res = ""
    for _ in range(5):
        res += choice(alphabet)
    return res

def find_code(code):
    """ S"assure que le code de partie mis en paramètre n'existe pas encore, sinon, en génère un nouveau."""
    url = f"https://firestore.googleapis.com/v1/projects/{PROJECT_ID}/databases/(default)/documents/lobbies/{code}?key={API_KEY}"
    res = requests.get(url)
    if res.status_code == 404: # N'existe pas
        return code
    elif res.status_code == 200:
        find_code(generate_game_code())
    else:
        return res.text

def create_lobby(code,data):
    """ Ajoute à la base de donnée la partie avec l'offre sdp."""
    url = f"https://firestore.googleapis.com/v1/projects/{PROJECT_ID}/databases/(default)/documents/lobbies?documentId={code}&key={API_KEY}"
    res = requests.post(url, json=data)
    if res.status_code == 200:
        print(f"Lobby créé avec succès !")
    else:
        print("Erreur:", res.text)

def add_answer_to_db(pc,code):
    """ Modifie la base de donnée pour mettre la réponse du client. """
    url = f"https://firestore.googleapis.com/v1/projects/{PROJECT_ID}/databases/(default)/documents/lobbies/{code}?key={API_KEY}"
    res = requests.patch(
        url,
        params={"updateMask.fieldPaths": "answer"},
        json={ "fields": {
            "answer": {"stringValue": json.dumps({"sdp": pc.localDescription.sdp, "type": pc.localDescription.type})}
        }}
    )
    if res.status_code == 200:
        print("✅ Réponse envoyée")
    else:
        print("Erreur:", res.text)

# ===== Récupération des offres et réponses sdp

def wait_for_answer(code):
    """ Check en continue si la réponse a été rempli dans la db """
    print("En attente de la réponse de l'autre joueur")
    searching_answer = True
    url = f"https://firestore.googleapis.com/v1/projects/{PROJECT_ID}/databases/(default)/documents/lobbies/{code}?key={API_KEY}"
    while searching_answer:
        res = requests.get(url)
        if res.status_code == 200:
            doc = res.json()
            if doc["fields"]["answer"] != {"nullValue": None}:
                print("✅ reponse reçu")
                answer = json.loads(doc["fields"]["answer"]["stringValue"])
                searching_answer = False
            else:
                time.sleep(5)
        else:
            print("Erreur:", res.text)
    return answer

def wait_for_offer(code):
    """ Check en continue si l'offre sdp est prsente / si la partie a été créée dans la db """
    url = f"https://firestore.googleapis.com/v1/projects/{PROJECT_ID}/databases/(default)/documents/lobbies/{code}?key={API_KEY}"
    wait_for_offer = True
    while wait_for_offer:
        # récupération de l'offre
        res = requests.get(url)
        if res.status_code == 200:
            doc = res.json()
            offer = json.loads(doc["fields"]["offer"]["stringValue"])
            wait_for_offer = False
        else:
            print("Mauvais code de partie : vous devez utiliser un code de partie valide ou créer une nouvelle partie.")
            code = input("Code de la game : ")
    return (code, offer)

# Envoie de data via le datachannel
def send_data(data):
    global channel,network_loop
    if (channel == None) or (channel.readyState != "open"):
        print("Channel pas prêt, impossible d'envoyer :", data)
    else:
        network_loop.call_soon_threadsafe(channel.send, data)


# ===== Gestion globale du jeu =====

def initiate_game():
        network_interval = 16   # 1000 ms -> 1 FPS réseau
        last_network_send = game_logic.now()

        while game_context.running: # Boucle du jeu
            # Update des coordonnées
            while not incoming_messages.empty():
                msg = incoming_messages.get()
                data = json.loads(msg)
                distant_player.x = data[0]
                distant_player.y = data[1]

            game_logic.update_game(game_context,local_player,distant_player)

            # Gestion boucle réseau :
            now = game_logic.now()
            
            if local_player.host and now - last_network_send >= network_interval:
                send_data(json.dumps(local_player.get_pos()))
                last_network_send = now

        game_logic.end_game() # Fermeture de pygame
        stop_event.set() # Fermeture du channel