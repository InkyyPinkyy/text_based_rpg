import random
import os
import json

#from events import *
from dungeon import *
from lists_and_dicts import *

def clear_console():
    # Clear console based on the operating system
    if os.name == 'nt':
        os.system('cls')  # For Windows
    else:
        os.system('clear')  # For Unix/Linux/Mac


class pcolors: # print-colors
    PURPLE = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'

    BACKGROUND_CYAN = '\033[46m'
    BACKGROUND_PURPLE = '\033[45m'
    BACKGROUND_BLUE = '\033[44m'
    BACKGROUND_YELLOW = '\033[43m'
    BACKGROUND_GREEN = '\033[42m'
    BACKGROUND_RED = '\033[41m'
    
    DARK_CYAN = '\033[36m'
    DARK_PURPLE = '\033[35m'
    DARK_BLUE = '\033[34m'
    DARK_YELLOW = '\033[33m'
    DARK_GREEN = '\033[32m'
    DARK_RED = '\033[31m'

    END = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'



class Player:
    def __init__(self, name,player_species):
        self.name = name
        self.player_species = player_species
        self.name_of_player_species = player_species['name_of_player_species']
        
        self.skillpoints = 0
        self.level = 1
        self.xp = 0
        self.gold = 0
        self.inventory = []
        self.weapon = None
        self.armor = None
        self.ring = None
        self.necklace = None
        self.vitality = player_species['vitality'] + self.ring.ring_vitality if self.ring else player_species['vitality']
        self.base_hp = player_species['hp'] 
        self.max_hp = player_species['hp']
        self.max_max_hp = self.max_hp * self.vitality
        self.hp = self.max_max_hp
        self.strength = player_species['strength']
        self.attack_damage = player_species['attack_damage']
        self.weapons_created = 0
        self.luck = 0

        #settings, Quests and more:
        self.autosave_on = False

    def show_player_stats(self):
        """shows the player's stats"""
        print(f"\n{self.name}'s stats:")
        print(f"Class: {self.name_of_player_species}")
        print(f"{round(self.hp)}/{round(self.max_max_hp)} HP")
        print(f"Damage: {round((self.attack_damage + self.weapon.weapon_damage) * self.strength)}")
        print(f"Your weapon:\n    {self.weapon}")
        print(f"Your armor: {self.armor}")
        print(f"Your ring: {self.ring}")
        print(f"Your necklace: {self.necklace}")
        print(f"Your level: {self.level}")
        print(f"{self.xp}/{self.level * 32} XP until the next level")
        print(f"{self.skillpoints} skillpoints")
        print(f"{self.luck} Luck")
        next = input(f"\n{pcolors.RED}return (r):\n")
        if next.lower() == 'r':
            return
        else:
            print("Please provide a valid entry")

    def check_amount_self_xp(self):
        while self.xp >= (self.level * 32):
            self.xp -= (self.level * 32)
            self.level += 1
            self.skillpoints += 1
            self.max_max_hp += 5
            self.hp = self.max_max_hp        
            print(f"You reached level {self.level} and got a skillpoint!")
            print(f"Your max HP increased by 5!")
            print(f"Your hp had been restored!")

    def go_to_settings(self):
        """shows the settings menu"""
        print(f"\nSettings:")
        print(f"1. Change autosave on/off")
        print(f"2. {pcolors.RED}exit settings{pcolors.END}")
    
        choice = input("Choice: ")
    
        if choice == '1':
            self.autosave_on = not self.autosave_on
            print(f"Autosave is now {'on' if self.autosave_on else 'off'}")
        elif choice == '2':
            return
        else:
            print(f"Invalid choice!")
            return

    def player_attack(self, target):
        try: damage = random.uniform(
            ((self.attack_damage + self.weapon.weapon_damage) * self.strength) * 0.9,
            ((self.attack_damage + self.weapon.weapon_damage) * self.strength) * 1.1
            )
        except: damage = random.uniform(
            ((self.attack_damage) * self.strength) * 0.9,
            ((self.attack_damage) * self.strength) * 1.1
            )
        target.hp -= round(damage)
        # (f"{damage:.2f
        print(f"You are dealing {round(damage)} damage to the {target.name}!")
        if target.hp > 0:
            damage = random.uniform(
            target.attack_damage * self.strength * 0.5,
            target.attack_damage * self.strength * 0.7
        )
            self.hp -= round(damage)
            print(f"The target is dealing {round(damage)} damage to you!")

    def enemy_encounter(self, enemy):
        """
        initialises a battle with the player and an enemy.
        There is an option to flee, where the fight gets
        cancelled. The damage of the enemy scales with
        the players strength.
        """
        print(f"\nA {enemy.name} is attacking you!")

        while self.hp > 0 and enemy.hp > 0:
            print(f"\n{self.name}: {self.hp}/{self.max_max_hp} HP")
            print(f"{enemy.name}: {enemy.hp}/{enemy.max_hp} HP")

            action = input("Attack (a) or flee (f)? ")
            if action.lower() == 'a':
                clear_console()
                self.player_attack(enemy)

            elif action.lower() == 'f':
                print("You fled!")
                return

        if self.hp > 0:
            print(f"You won gainst the {enemy.name}!")
            gold_earned = random.randint(10, 20)
            self.gold += gold_earned
            print(f"You got {pcolors.YELLOW}{gold_earned} gold!{pcolors.END}")
            xp_earned = random.randint(enemy.max_hp // 10, enemy.max_hp // 3)
            self.xp += xp_earned
            print(f"You got {pcolors.GREEN}{xp_earned} XP{pcolors.END}!")
            self.check_amount_self_xp()
            next = input(f"\n{pcolors.RED}return (r):\n")
            if next.lower() == 'r':
                return
            else:
                print("Please provide a valid entry!")

        else:
            print("You lost...")
            exit()

    def pick_up_item(self, item):
        self.inventory.append(item)
        print(f"{self.name} picked up {item.name}!")

    def show_inventory(self, which_items_to_show = None):
        """
        legal values for which_items_to_show:\n
        - "everything": all items in the inventory\n
        - "weapons": only weapons in the inventory\n
        - "armor": all the armor in the inventory\n
        - "rings": all the rings in the inventory\n
        - "necklaces": all the necklaces in the inventory\n
        - "consumables": all the consumable items in the inventory\n
        - "weapons_armor_rings_necklaces": all the equippable items in the inventory\n
        """
        if which_items_to_show == "everything":
            print(f"\nYour inventory:")
            print(f"{pcolors.YELLOW}{self.gold}{pcolors.END} Gold")            
            for idx, item in enumerate(self.inventory, start = 1):
                print(f"{idx}. {item}")
        elif which_items_to_show == "weapons":
            weapons_inventory = [item for item in self.inventory if isinstance(item, Weapon)]
            print(f"\nYour weapons:")
            for idx, item in enumerate(weapons_inventory, start = 1):
                print(f"{idx}. {item}")
        elif which_items_to_show == "armor":    
            print(f"\nYour armor-sets:")
            for idx, item in enumerate(self.inventory, start = 1):
                if isinstance(item, armor):
                    print(f"{idx}. {item}")
        elif which_items_to_show == "rings":
            print(f"\nYour rings:")
            for idx, item in enumerate(self.inventory, start = 1):
                if isinstance(item, ring):
                    print(f"{idx}. {item}")
        elif which_items_to_show == "necklaces":
            necklaces_inventory = [item for item in self.inventory if isinstance(item, necklace)]
            print(f"\nYour necklaces:")
            for idx, item in enumerate(necklaces_inventory, start = 1):
                if isinstance(item, necklace):
                    print(f"{idx}. {item}")
        elif which_items_to_show == "consumables":
            consumables_inventory = [item for item in self.inventory if isinstance(item, consumable)]
            print(f"\nYour consumable items:")
            for idx, item in enumerate(consumables_inventory, start = 1):
                print(f"{idx}. {item}")
                return consumables_inventory
        elif which_items_to_show == "weapons_armor_rings_necklaces":
            equippable_inventory = [item for item in self.inventory if isinstance(item, Weapon) or isinstance(item, armor) or isinstance(item, ring) or isinstance(item, necklace)]
            print(f"\nEquippable items:")
            for idx, item in enumerate(equippable_inventory, start = 1):
                print(f"{idx}. {item}")
        else:
            print("Your inventory is empty!")

    def choose_equipment(self):
        self.show_inventory("weapons_armor_rings_necklaces")        
        print(f"Choose an item to equip")

        try:
            wahl = int(input(f"\nProvide the number of the item you want to equip: ")) -1
            if 0 <= wahl < len(self.inventory):
                item = self.inventory[wahl]
                if item.type == "weapon":
                    self.weapon = item
                    print(f"{self.name} equipped '{item.name}' as their weapon!")
                elif item.type == "armor":
                    self.armor = item
                    print(f"{self.name} equipped '{item.name}' as their armor!")
                elif item.type == "ring":
                    self.ring = item
                    print(f"{self.name} equipped '{item.name}' as their ring!")
                elif item.type == "necklace":
                    self.necklace = item
                    print(f"{self.name} equipped '{item.name}' as their necklace!")
                else:
                    print(f"This item can't be equipped!")
            else:
                print(f"invalid selection")
        except ValueError:
            print(f"Please provide a valid number")

    def consume_item(self):
        clear_console()
        consumable_items = self.show_inventory("consumables")
        wahl = int(input(f"\nProvide the number of the item you want to consume or exit (0):\n "))
        if wahl == 0:
            return
        try: 
            wahl -= 1       
            item = consumable_items[wahl]
            if 0 <= wahl < len(self.inventory):
                if item.consumable_type == "health":
                    if self.hp == self.max_max_hp:
                        print(f"{self.name} is already at max HP!")
                        return
                    elif self.hp + item.stats_player_gets > self.max_max_hp:
                        item.stats_player_gets = self.max_max_hp - self.hp
                        self.hp += item.stats_player_gets
                    else:
                        self.hp += item.stats_player_gets
                    print(f"{self.name} consumed {item.name} and got {item.stats_player_gets} HP!")
                    self.inventory.remove(item)
                elif item.consumable_type == "strength":
                    self.strength += item.stats_player_gets
                    print(f"{self.name} consumed {item.name} and got {item.stats_player_gets} strength!")
                    self.inventory.remove(item)
                elif item.consumable_type == "increase_max_health":
                    self.max_hp += item.stats_player_gets
                    print(f"{self.name} consumed {item.name} and got additional {item.stats_player_gets} max HP!")
                    self.inventory.remove(item)
                elif item.consumable_type == "increase_attack_damage":
                    self.attack_damage += item.stats_player_gets
                    print(f"{self.name} consumed {item.name} and got additional {item.stats_player_gets} strength!")
                    self.inventory.remove(item)
            else:
                return
        except ValueError:
            print(f"Please provide a valid number")
            return

    def do_inventory_shit(self):
        self.show_inventory("everything")
        action = input("\nEquip item (1), consume item (2) or return (3)? ")
        if action.lower() == '1':
            self.choose_equipment()
        elif action.lower() == '2':
            self.consume_item()
        elif action.lower() == '3':
            return

    def save_game(self):
        def item_to_dict(item):
            item_dict = vars(item).copy()
            

            # Exclude 'weapon_name' only for weapons
            if isinstance(item, Weapon) and ('weapon_name' and 'weapon_damage') in item_dict:
                del item_dict['weapon_name']
                del item_dict['weapon_damage']
                print(f"Is a weapon!")
                print(item_dict)
            #item_dict['item_type'] = type(item).__name__
            return item_dict
        save_data = {
            'name': self.name,
            'player_species': self.player_species,
            'name_of_player_species': self.name_of_player_species,
            'hp': self.hp, 
            'max_hp': self.max_hp, 
            'vitality': self.vitality, 
            'strength': self.strength, 
            'attack_damage': self.attack_damage,
            'skillpoints': self.skillpoints, 
            'level': self.level, 
            'xp': self.xp, 
            'gold': self.gold, 
            'weapons_created': self.weapons_created,
            'luck': self.luck,
            'inventory': [item_to_dict(item) for item in self.inventory],
            'weapon': item_to_dict(self.weapon) if self.weapon else None,            
            'armor': vars(self.armor) if self.armor else None,
            'ring': vars(self.ring) if self.ring else None,
            'necklace': vars(self.necklace) if self.necklace else None
        }
        with open(f"{self.name}_save.json", "w") as file:
            json.dump(save_data, file, indent = 4)
        
        settings_data = {
            'autosave_on' : self.autosave_on,
        }
        with open(f"{self.name}_settings.json", "w") as file:
            json.dump(settings_data, file)

    @staticmethod
    def load_game(player_file_name, settings_file_name):
        if not os.path.exists(player_file_name) or not os.path.exists(settings_file_name):
            print("Save file(s) not found.")
            return None

        try:
            # Load player data
            with open(player_file_name, "r") as file:
                data = json.load(file)

            player_species = data['player_species']
            player = Player(data['name'], player_species)

            # Basic attributes
            player.name_of_player_species = data['name_of_player_species']
            player.hp = data['hp']
            player.max_hp = data['max_hp']
            player.vitality = data['vitality']
            player.strength = data['strength']
            player.attack_damage = data['attack_damage']
            player.level = data['level']
            player.xp = data['xp']
            player.gold = data['gold']
            player.weapons_created = data['weapons_created']
            player.luck = data['luck']
            player.skillpoints = data.get('skillpoints', 0)  # Optional fallback

            # Inventory loading
            item_classes = {
                'weapon': Weapon,
                'armor': armor,
                'ring': ring,
                'necklace': necklace,
                'consumable': consumable
            }

            player.inventory = []
            for item_data in data['inventory']:
                item_type = item_data.get('item_type', '').lower()
                item_class = item_classes.get(item_type)

                if item_class:
                    # Remove 'type' before instantiating
                    item_data_clean = {k: v for k, v in item_data.items() if k != 'type'}
                    item = item_class(**item_data_clean)
                    player.inventory.append(item)
                else:
                    print(f"Warning: Unknown item type '{item_type}' found in inventory.")

            # Equipment
            def load_equipment(equip_data, cls):
                if equip_data:
                    clean_data = {k: v for k, v in equip_data.items() if k != 'type'}
                    return cls(**clean_data)
                return None

            player.weapon = load_equipment(data.get('weapon'), Weapon)
            player.armor = load_equipment(data.get('armor'), armor)
            player.ring = load_equipment(data.get('ring'), ring)
            player.necklace = load_equipment(data.get('necklace'), necklace)

            # Load settings
            with open(settings_file_name, "r") as file:
                settings = json.load(file)
                autosave = settings.get('autosave_on', False)

                # If autosave_on is part of Player, set it:
                if hasattr(player, 'autosave_on'):
                    player.autosave_on = autosave

            print(f"Game-file of {player.name} was successfully loaded!")
            return player

        except Exception as e:
            print(f"Failed to load game: {e}")
            return None

    # @staticmethod
    # def load_game(player_file_name, settings_file_name):
    #     if os.path.exists(player_file_name) and os.path.exists(settings_file_name):
    #         with open(player_file_name, "r") as file:
    #             data = json.load(file)
    #             player_species = data['player_species']
    #             player = Player(data['name'],player_species)
    #             player.name_of_player_species = data['name_of_player_species']
    #             player.hp = data['hp']
    #             player.max_hp = data['max_hp']
    #             player.vitality = data['vitality']
    #             player.strength = data['strength']
    #             player.attack_damage = data['attack_damage']
    #             player.level = data['level']
    #             player.xp = data['xp']
    #             player.gold = data['gold']
    #             player.weapons_created = data['weapons_created']
    #             player.luck = data['luck']

    #             player.inventory = []
    #             for item_data in data['inventory']:
    #                 item_type = item_data['type']
                    
    #                 if item_type == 'weapon':
    #                     item = Weapon(**item_data)
    #                 elif item_type == 'armor':
    #                     item = armor(**item_data)
    #                 elif item_type == 'ring':
    #                     item = ring(**item_data)
    #                 elif item_type == 'necklace':
    #                     item = necklace(**item_data)
    #                 elif item_type == 'consumable':
    #                     item = consumable(**item_data)
    #                 else:
    #                     item = item(**item_data)
    #                 player.inventory.append(item)
                
    #             player.weapon = Weapon(**data['weapon']) if data['weapon'] else None  # dict to object
    #             player.armor = armor(**data['armor']) if data['armor'] else None
    #             player.ring = ring(**data['ring']) if data['ring'] else None
    #             player.necklace = necklace(**data['necklace']) if data['necklace'] else None
    #             print(f"Game-file of {player.name} was succesfully loaded!")
                

    #         with open(settings_file_name, "r") as file:
    #             data = json.load(file)
    #             player.autosave_on = data['autosave_on']
    #             print(f"Settings-file of {player.name} was succesfully loaded!")
            
    #         return player

    #     else:
    #         # mention of the not existing file is in main() function
    #         return None

class NPC:
    def __init__(self, which_npc):
        self.name = which_npc[str('name')]
        self.species_name = which_npc['species_name']
        # same as player-races
        self.profession = which_npc['profession']

        self.profession_specialization = which_npc['profession_specialization']
        self.hp = which_npc['hp']
        self.max_hp = self.hp

        self.inventory = []

class Merchant(NPC):
    def __init__(self, which_merchant):
        super().__init__(which_merchant)
        self.gold = which_merchant['gold']
        self.items_for_sale = which_merchant['items_for_sale']
        self.items_to_buy = which_merchant['items_to_buy']

    def show_items_for_sale(self):
        print(f"\n{self.name}'s items for sale:")
        for idx, item in enumerate(self.items_for_sale, start = 1):
            print(f"{idx}. {item}")
    
    def show_items_to_buy(self):
        print(f"\n{self.name}'s items to buy:")
        for idx, item in enumerate(self.items_to_buy, start = 1):
            print(f"{idx}. {item}")

class Enemy:
    def __init__(self, which_monster):
        self.name = which_monster[str('name')]
        self.level = int
        self.weapon = {}
        self.armor = {}
        self.accuracy = float
        self.hp = which_monster['hp']
        self.max_hp = self.hp
        self.attack_damage = which_monster['attack_damage']
        self.species_name = ""
        self.inventory = []
        self.where_found = ""

    def get_random_monster(which_monster):
        """        self.name = name
        valid values for which_monster:\n
        - "normal": monsters for enemy_encounter()\n
        - "dungeon": dungeon monsters\n
        """
        if which_monster == "normal":
            monster = random.choice(list(monsters.values()))
        elif which_monster == "dungeon":
            monster = random.choice(list(dungeon_monsters.values()))
        return monster

    def enemy_attack(self, target, weapon):
        self.target = target
        final_damage_dealt = (self.attack_damage + weapon.weapon_damage) * (Player.level * 0.7)
        target.hp -= final_damage_dealt
        print(f"{self.name} attacks {target.name} and deals {final_damage_dealt} damage!")
        print(f"{target.name} still has {target.hp} HP!")
    

    def __str__(self):
        return f"{self.name} (HP: {self.hp}, Attack: {self.attack_damage})"

class item:
    def __init__(self, item_type, item_info):
        #self.name = ""
        self.item_type = item_type
        self.item_info = str(item_info)

    def __str__(self):
        return f"{self.name} ({self.type}): \n  {self.item_info}"
    
    def get_random_item(which_items):
        """
        valid values for which_items:\n
        - "from_big_pool": all items in the game\n
        - "small_chest": items from small chests\n
        """
        if which_items == "from_big_pool":
            which_item = random.choice(list(all_items.values()))
        if which_items == "small_chest":
            which_item = random.choice(list(items_from_small_chests.values()))
        return which_item
    
    
    
class Weapon(item):
    """legal values for weapon_type:\n
            - "dagger"
            - "sword"
            - "greatsword"
            - "fish"
            - "axe"
            - "spear"
            - "bow"
            - "crossbow"
            - "trident"
            - "staff"

        legal values for weapon_rarity:\n
            - "common"
            - "uncommon"
            - "rare"
            - "epic"
            - "legendary"
            - "godly"

        legal values for weapon_element:\n
            - "fire"
            - "water"
            - "earth"
            - "wind"
            - "ice"
            - "spark"
            - "blood"
            - "shadow"
            - "light"
            - "toxin"
            - "iron"
            - "magic"
    """
    def __init__(self, item_type, item_info, weapon_type, weapon_rarity, weapon_element, enchantments):
        super().__init__(item_type, item_info)
        self.item_type = item_type
        self.weapon_type = weapon_type    
        self.item_info = item_info
        self.weapon_rarity = weapon_rarity         

        self.weapon_element = weapon_element
        
        self.weapon_damage = self.weapon_type["base_damage_on_rarity"][self.weapon_rarity["symbol"]]
        
        self.weapon_name = f'{self.weapon_type["type_name"]} of {self.weapon_element["rarities"][self.weapon_rarity["symbol"]]}'
        
        self.enchantments = enchantments if enchantments else [] 
        #self.IsEnabled = true

    def __str__(self):
        return (
            f"{self.weapon_rarity['pcolors_string']}{self.weapon_name}{pcolors.END} "
            f"({self.weapon_rarity['symbol']} {self.weapon_element['symbol']}{self.weapon_type['type_name']}):\n"
            f"    - {self.weapon_damage} Damage\n"
            f"    - {self.item_info}\n"

            # debug
            # f"{self.weapon_type}\n"
            # f"{self.weapon_rarity}\n"
            # f"{self.weapon_element}\n"

        )

    @staticmethod
    def get_random_weapon(weapon_type, weapon_rarity, weapon_element):
        try:
            if Player and Player.luck > 0:
                random_value_for_loottable = random.random() + Player.luck * 0.001
            else:
                random_value_for_loottable = random.random()
        except:
            random_value_for_loottable = random.random()
        if weapon_type == "random":
            wtype_key = random.choice(list(weapon_types.keys()))
            wtype = weapon_types[wtype_key]
        else:
            wtype = weapon_types[weapon_type]
        if weapon_rarity == "random":
            rv = random_value_for_loottable
            if rv < weapon_rarities["common"]["chance"]:
                rarity = weapon_rarities["common"]
            elif rv < weapon_rarities["uncommon"]["chance"] + weapon_rarities["common"]["chance"]:
                rarity = weapon_rarities["uncommon"]
            elif rv < weapon_rarities["rare"]["chance"] + weapon_rarities["uncommon"]["chance"] + weapon_rarities["common"]["chance"]:
                rarity = weapon_rarities["rare"]
            elif rv < weapon_rarities["epic"]["chance"] + weapon_rarities["rare"]["chance"] + weapon_rarities["uncommon"]["chance"] + weapon_rarities["common"]["chance"]:
                rarity = weapon_rarities["epic"]
            else:
                rarity = weapon_rarities["legendary"]
        else:
            rarity = weapon_rarities[weapon_rarity]
        if weapon_element == "random":
            element_key = random.choice(list(weapon_elements.keys()))
            element = weapon_elements[element_key]
        else:
            element = weapon_elements[weapon_element]
        
        NewWeapon = Weapon("weapon", "", wtype, rarity, element, enchantments=None)
        return NewWeapon



class armor(item):
    def __init__(self, name, type, item_info, armor_type, armor_vitality):
        super().__init__(type, item_info)
        self.name = name
        self.armor_type = armor_type
        self.armor_vitality = armor_vitality

class ring(item):
    def __init__(self, name, type, item_info, ring_type, ring_vitality):
        super().__init__(type, item_info)
        self.name = name
        self.ring_type = ring_type
        self.ring_vitality = ring_vitality

    def __str__(self):
        return f"{self.name} ({self.type}): {self.ring_vitality} Vitality\n    {self.item_info}"

class necklace(item):
    def __init__(self, name, type, item_info, necklace_type, necklace_strength):
        super().__init__(type, item_info)
        self.name = name
        self.armor_type = necklace_type
        self.armor_vitality = necklace_strength

    def __str__(self):
        return f"{self.name} ({self.type}): {self.necklace_type}: {self.necklace_strength}\n    {self.item_info}"

class consumable(item):
    def __init__(self, name, item_type, item_info, consumable_type, stats_player_gets):
        super().__init__(item_type, item_info)
        self.name = name
        self.consumable_type = consumable_type
        self.stats_player_gets = int(stats_player_gets)

    def __str__(self):
        return f"{self.name} ({self.item_type}): {self.stats_player_gets} HP\n   {self.item_info}"