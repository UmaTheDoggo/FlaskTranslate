import sys # sys.exittiä varten
import time # time.sleeppiä varten
from weapons import Weapon # ase luokka
from monsters import Monster # monsteri luokka
from room import Room # huone luokka
from PlayerInfo import Player # pelaaja luokka
import json # pelin tallennusta varten

# Asetetaan aseiden nimi, vahinko ja osumismahdollisuus.  
sword = Weapon("Sword", 6, 4)
weapon_choice = None

# Tehdään sanakirja asekoodia varten, jotta tiedetään mikä ase ladataan nimen perusteella
weapon_directory = {
    "Sword": sword,
}

# Luodaan monstereille nimi, elämäpisteet ja paljon tekee vahinkoa pelaajaan
Goblin = Monster("Goblin", 20, 5)
GGoblin = Monster("Giant Goblin", 50, 10)
MGoblin = Monster("Goblin Master", 100, 30)

#luodaan kartta Room luokan avulla, huoneen sijainti ja kuvaus
level0Start = Room("Fields", "A peaceful spot under a tree") # pelaajan aloitushuone ennen dungeoniin menemistä
level0End = Room("Fields", "You see Gratos waving at you...")
level1Center = Room("Starting place", "I can go left or right")
level1Left = Room("Left from the starting place", "I can go forward.") # GGoblin + syringe
level1Right = Room("Right from the starting place", "I can go forward.") # GGoblin + smithing stone
level1Behind = Room("A huge staircase leads down", "I can go forward.")

level2Center = Room("Generator room", "Turn the generator into gear") # upgrade gear
level3Center = Room("The Goblin Master room", "A throneroom full of gold and diamonds.")# Goblin master lopputaistelu huone

# määritetään jokaiselle huoneelle poistumissuunta / suunnat
level1Center.add_exit("left", level1Left)
level1Center.add_exit("right", level1Right)
level1Center.add_exit("behind", level1Behind)

level1Left.add_exit("forward", level2Center)
level1Right.add_exit("forward", level2Center)
level1Behind.add_exit("forward", level2Center)

level2Center.add_exit("forward", level3Center)
level3Center.add_exit("forward", level0End)

#JSON määritetään jokaiselle huoneelle arvot
room_directory = {
    "Fields": level0Start,
    "Starting place": level1Center,
    "Left from the starting place": level1Left,
    "Right from the starting place": level1Right,
    "A huge staircase leads down": level1Behind,
    "Generator room": level2Center,
    "The Goblin Master room": level3Center,
}

# Asetetaan pelaaja aloittamaan level0Start huoneesta
current_room = level0Start

# Merkitään hirviöt huoneisiin
level1Center.monster = Goblin
level1Left.monster = GGoblin
level1Right.monster = GGoblin
level1Behind.monster = GGoblin
level3Center.monster = MGoblin

# Pelaaja luokan ominaisuudet, asetetaan nimi, ikä, elämäpisteet, vahinko (Gratos tarvitsee "deals" ominaisuuden. Muuten ase tekee vahingon) ja tavaraluettelo
player = Player("Unknown", 0, 100, 0, inventory=[])
gratos = Player("Gratos", 158, 200, 30, inventory=[])

# Asetetaan ehto Gratoksen mahdolliselle polulle, joka vaihdetaan True kun pelaaja astuu huoneeseen level2Behind
gratos_joined = False
game_loaded = False  # Lippu tarkistamaan ladattiinko peli

# Tarkistetaan pelaajan ikä. Kysytään aina ohjelman käynnnistyessä
while True:
    try:
        player_age = int(input("Enter your age: ")) # Vaihdetaan HTTP request ja JSON responseksi
        player.age = player_age
        break
    except ValueError:
        print("Error: Set value is not a number. Try again") # Vaihdetaan HTTP request ja JSON responseksi
    print(f"Player age: {player_age}.") # Vaihdetaan HTTP request ja JSON responseksi
# jos pelaaja on alle 12 peli sulkeutuu
if player_age < 12:
    sys.exit("This game is meant for people over the age of 12. Quitting game.")

# Avataan ohjeet.txt ja menu.txt pelin alkaessa
with open("ohjeet.txt", "r") as ohjeet:
    data = ohjeet.read()
    print(data) # Vaihdetaan HTTP request ja JSON responseksi

input("Press enter to continue: ") # Vaihdetaan HTTP request ja JSON responseksi

while True:
    with open("menu.txt", "r") as menu:
        data = menu.read()
        print(data) # Vaihdetaan HTTP request ja JSON responseksi

    navigation = input("Type to navigate: ").lower() # Vaihdetaan HTTP request ja JSON responseksi

    if navigation == "load":
        try:
            with open("savegame.json", "r", encoding="utf-8") as file:
                loaded_data = json.load(file)
                
                player.name = loaded_data["player_name"]
                player.age = loaded_data["player_age"]
                player.HP = loaded_data["player_hp"]
                player.inventory = loaded_data["player_inventory"]
                gratos_joined = loaded_data["gratos_joined"]
                
                # Ladataan ase takaisin weapon muuttujaan ja asetetaan sen vahinko
                weapon_name = loaded_data.get("weapon_name", "Sword")
                weapon_damage = loaded_data.get("weapon_damage", 6)

                # jos aseen nimi on aijemin luodussa json weapon_directoryssä. weapon_choice muuttuja saa tallennetun aseen arvon
                if weapon_name in weapon_directory:
                    weapon_choice = weapon_directory[weapon_name]
                else:
                    weapon_choice = sword
                weapon_choice.damage = weapon_damage  # Palautetaan päivitetty vaurio, jos asetta on parannettu

                # etsitään json mäppäyksestä pelaajan sijainti ja määritetään se nykyiseksi huoneeksi
                room_name = loaded_data["current_room"]
                if room_name in room_directory:
                    current_room = room_directory[room_name]
                
            print("Game loaded...") # Vaihdetaan HTTP request ja JSON responseksi
            print(f"Welcome back, {player.name} (HP: {player.HP}, Weapon: {weapon_choice.name} DMG: {weapon_choice.damage})!\n") # Vaihdetaan HTTP request ja JSON responseksi
            input("Press Enter to continue game: ") # Vaihdetaan HTTP request ja JSON responseksi
            game_loaded = True  # Merkitään, että peli ladattiin. Tämä hyppää pelin intron yli ja jatkaa tallennuspisteestä
            break
            
        except FileNotFoundError:
            print("\n Saved game file not found: Start a new game. \n") # Vaihdetaan HTTP request ja JSON responseksi
            input("Press Enter to continue: ") # Vaihdetaan HTTP request ja JSON responseksi

    # Peli alkaa start komennolla
    elif navigation == "start":
        with open("intro.txt", "r") as tiedosto:
            data = tiedosto.read()
            print(data) # Vaihdetaan HTTP request ja JSON responseksi
        input("Press enter to continue: ") # Vaihdetaan HTTP request ja JSON responseksi
        break

    else:
        print("This is not a menu option. Type again.") # Vaihdetaan HTTP request ja JSON responseksi

# Jos peli ladattiin niin ohitetaan pelin intro
if not game_loaded:
    player.name = input("Enter your name: ") # Vaihdetaan HTTP request ja JSON responseksi
    player_info = print (f"Hello, {player.name} Age: {player.age}")
    print("Stranger: Hey, you. You're finally awake! How are you feeling?")
    print("| Good |     | Bad |")
    answer1 = input(f"{player.name}: ").lower() # Vaihdetaan HTTP request ja JSON responseksi
    if answer1 == "good":
            print("Stranger: I highly doubt that. It's like you fell from the heavens.")
    elif answer1 == "bad":
            print("Stranger: I figured. You just fell from the sky.")
    else:
        print("Stranger: Hmm... Not quite sure if I understand. You took a bit of a fall.")

    # import time kirjaston avulla voidaan hidastaa tekstin tulostusta jotta dialogista tulee selkeämpää 
    print("Stranger: Do you remember your name?")
    print(f"{player.name}: Yes, my name is {player.name}.")
    print(f"Gratos: Haha, nice to meet you {player.name}! My name is Gratos.")
    print("Gratos: It seems you do not have a weapon yet. Here in the dungeon you will need one.")
    print("Gratos: I don't have much, but you can get one from me.\n")
    print("Obtained: Sword (6 dmg), 5/6 hit chance")

    weapon_choice = sword


    print(f"Gratos: {player.name} WATCH OUT! A .....\n")
    print(f"{player.name}: Wha... Where am I?")
    print(f"{player.name}: Huh..? How did I end up in the Dungeon?")
    print(f"{player.name}: It's dangerous, I need to move.")
    print(f"{player.name}: There's something in my pocket... A poster?")

    # avataan news.txt tekstitiedosto jossa anetaan pelaajalle tavoite pysäyttää Peikko Mestari
    with open("news.txt", "r") as news:
        data = news.read()
        print(data)
        input("Press Enter to continue: ") # Vaihdetaan HTTP request ja JSON responseksi

    print(f"{player.name}: I need to stop the Goblin Master!\n")

    # Pelaaja asetetaan level1Center, jossa ensimmäinen hirviö tulee vastaan
    current_room = level1Center
    print(f"A {current_room.monster.name} starts running towards {player.name} What do you do?")

    while current_room.monster.HP > 0:
        input(f"Press Enter to attack the {current_room.monster.name}!") # Vaihdetaan HTTP request ja JSON responseksi

        if weapon_choice.attack():
            print(f"You swing your {weapon_choice.name} and hit the {current_room.monster.name} for {weapon_choice.damage} damage!")
            current_room.monster.take_damage(weapon_choice.damage)
        else:
            print(f"You swing your {weapon_choice.name}, but you missed! You took 5 damage.\n")
            player.take_damage(5)
            if player.HP <=0:
                sys.exit(f"You were slain by {current_room.monster.name}")
            break

while True:
    print(f"\n{current_room.name}")

    if current_room.monster and current_room.monster.HP > 0:        
        print(f"{current_room.monster.name} is blocking your way.")
        # Jos aikaisemmin määritetty vipu gratoksen liittymiselle on tosi, niin suoritetaan gratoksen hyökkäys viholliseen 
        if gratos_joined == True:
            print(f"Gratos lifts his axes and launches himself towards the {current_room.monster.name} dealing {gratos.deals} damage!")
            current_room.monster.take_damage(gratos.deals)
            print(f"{player.name}: Woah! That was a crazy move {gratos.name}")

        # Sama while silmukka tähän, kun elämäpisteet osuu 0 niin silmukka päättyy        
        while current_room.monster.HP > 0:
                input("Press Enter to attack!\n") # Vaihdetaan HTTP request ja JSON responseksi
                if weapon_choice.attack():
                    print(f"You swing your {weapon_choice.name} and hit the {current_room.monster.name} for {weapon_choice.damage} damage!")
                    current_room.monster.take_damage(weapon_choice.damage)
                else:
                    print(f"You swing your {weapon_choice.name}, but you missed!")
                    player.take_damage(current_room.monster.deals)
                    if player.HP <=0:
                        # Peli päättyy kun pelaajan elämäpisteet osuu 0
                        sys.exit(f"You were slain by {current_room.monster.name}")

    #  Määritetään huoneet level1Right, left ja behind, jos huoneen esinettä ei ole kerätty niin seuraava koodi ajetaan
    if current_room == level1Right and not current_room.item_collected:
        print(f"The {current_room.monster.name} dropped a smithing stone in the ground")
        player.inventory.append("smithing stone")
        current_room.item_collected = True
        print("Obtained: Smithing stone for a weapon upgrade.")
    
    if current_room == level1Left and not current_room.item_collected:
        print(f"The {current_room.monster.name} dropped a syringe.")
        player.inventory.append("syringe")
        current_room.item_collected = True
        print("Obtained syringe for a health upgrade.")
        player.HP = 200
        print(f"{player.name}'s health set to {player.HP} HP.")


    if current_room == level1Behind and not current_room.item_collected:
        print(f"{current_room.monster.name} dropped a leather armour and a glowing bottle?")

        player.inventory.append("Leather armour")
        player.HP = 100
        player.HP += 50
        weapon_choice.damage += 5
        current_room.item_collected = True
        print(f"{player.name}: Hmm... I feel... Great! And now I got a cool armour!")
        print(f"Health restored and gained +50 HP and {weapon_choice.name} deals now {weapon_choice.damage} damage.")
        print(f"Health now: {player.HP}")
            
    # Taistelun jälkeen palautetaan pelaajan elämäpisteet ennen mahdollisen asepäivityksen tekoa
    if current_room == level1Right and current_room.item_collected == True:
        player.HP = 100
        print(f"Health restored to {player.HP}")
        if "smithing stone" in player.inventory:
            print("Upgraded weapon")
            weapon_choice.damage += 10
            player.inventory.remove("smithing stone")
            print(f"{weapon_choice.name} upgraded for +10! It now deals {weapon_choice.damage} damage.")

    
    if current_room == level2Center and not current_room.item_collected: # asetetaan current_room.item_collected sitä varten ettei pelaaja voi loputtomasti päivittää hahmoa silmukassa lähtemällä pelistä
        print("The generator is here. I can break it in pieces to upgrade my gear and stop the pollution.\n")
        time.sleep(1)
        print("Riks")
        time.sleep(1)
        print("Raks")
        time.sleep(1)
        print("Poks")
        # päivitetään pelaajan elämäpisteet ja aseen vahinko
        player.HP += 50
        weapon_choice.damage += 10
        current_room.item_collected = True
        print(f"{player.name}: Oh yeeah!\n Weapon damage upgraded to {weapon_choice.damage}\n Health upgraded to {player.HP}.")
        time.sleep(1)
        print(f"{player.name}: I am ready to take the Goblin Master down!\n")

    if current_room == level1Behind:
        print(f"Orc: {player.name}?? Is it really you?")
        time.sleep(1)
        print(f"{player.name}: Not a step closer I have a weapon and I know how to use it!")
        time.sleep(1)
        print(f"Gratos: Woah!... Chillax {player.name}. It's me Gratos. Man I am glad I found you.")
        time.sleep(1)
        print(f"{player.name}: Oh, it's just you. Gratos we don't have time. We have to defeat the Goblin Master!!")
        time.sleep(1)
        print(f"Gratos: I saw the news {player.name}. I am with you!\n")
        time.sleep(1)
        gratos_joined = True # asetetaan Gratos liittymään lopputaisteluun asettamalla tosi muuttujaan gratos_joined
        print(f"Gratos will now help you defeat the Master Goblin!\n")

    # Pelin loppuvaihe, jossa kerrotaan Peikko Mestarille miten voisi parantaa tapojaan
    if current_room == level3Center:
        print(f"{player.name}: I did it! {current_room.monster.name}, you have done a lot of bad things to the village.")
        time.sleep(1)
        print(f"{current_room.monster.name}: Me knows.... Feel bad I do.. Me just wanted to mine shiny ores.")
        time.sleep(1)
        print(f"{player.name}: I stopped the pollution coming from your generator and recycled the materials to upgrade my gear totally carbon neutral")
        time.sleep(1)
        print(f"{current_room.monster.name}: Wooooww... Incredible craftmanship me say!")
        time.sleep(1)
        print(f"{player.name}: Look {current_room.monster.name}. You don't need coal to power these machines.")
        time.sleep(1)
        print(f"{player.name}: You can make a watermill next to the lake or a wind turbine on the fields. This way you will create a lot of energy wihout damaging the environment.")
        time.sleep(1)
        print(f"{current_room.monster.name}: See I do. Thank you wise human!")
    # kun pelaaja saavuttaa level0End. Tulostetaan lopputekstit, jos Gratos oli mukana niin ending2 mutta muuten ending1 
    if current_room == level0End:
        if gratos_joined == True:
            with open("ending2.txt", "r") as end2:
                data = end2.read()
                print(data)
                break
        else:
            with open("ending1.txt", "r") as end1:
                data = end1.read()
                print(data)
                break
    # tulostetaan pelaajan konsoliin reitit mihin voi mennä    
    available_exits = list(current_room.exits.keys())
    print(f"Exits available: {', '.join(available_exits)}")

    move = input("Where do you want to move?: ").lower() # Vaihdetaan HTTP request ja JSON responseksi
    # pelistä poistuminen
    if move == "quit":
        print("Quitting game...")
        break

    elif move == "inventory":
        print(f"\nInventory: {player.inventory}")
        if weapon_choice is not None:
            print(f"Weapon: {weapon_choice.name} (Damage: {weapon_choice.damage})\n")
        else:
            print("Weapon: None\n")
        continue

    elif move in current_room.exits:
        current_room = current_room.exits[move]
        
        #tallennus JSON tiedostoon. Aseen nimi ja aseen vahinko, jos arvoa ei saada niin asetetaan varakeinoksi arvo 6
        current_weapon_name = weapon_choice.name if weapon_choice else "Sword"
        current_weapon_damage = weapon_choice.damage if weapon_choice else 6
        # tiedot mitä tallennetan savegame.json tiedostoon
        game_data = {
            "player_name": player.name,
            "player_age": player.age,
            "player_hp": player.HP,
            "player_inventory": player.inventory,
            "weapon_name": current_weapon_name,
            "weapon_damage": current_weapon_damage,
            "current_room": current_room.name,
            "gratos_joined": gratos_joined
        }
        # luodaan tai muokataan tiedosto savegame.json utf-8 enkoodauksella ja tallennetaan pelaajan arvot sinne 
        with open("savegame.json", "w", encoding="utf-8") as file:
            json.dump(game_data, file, indent=4)
        
        print("Game saved...")
    # jos pelaaja kirjoittaa suunnan väärin niin tulostetaan tämä
    else:
        print("A stone wall is blocking the way")