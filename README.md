<p align="center">
  <img src="https://img.shields.io/badge/Python-3.10+-blue?logo=python" alt="Python Version">
  <img src="https://img.shields.io/badge/Status-Work%20In%20Progress-yellow" alt="Status">
  <img src="https://img.shields.io/badge/Genre-Text--Based%20RPG-green" alt="Genre">
</p>

<h1 align="center">🗡️ Text-Based RPG 🛡️</h1>
<p align="center">
  <b>Embark on an epic adventure in a world of monsters, loot, and endless possibilities—all from your terminal!</b>
</p>

---

## 🚀 Features

- **Create your own hero**: Choose a name and class!
- **Battle monsters**: Face off against dragons, skeletons, and more!
- **Inventory system**: Collect, equip, and use items.
- **Level up**: Gain XP, gold, and skill points.
- **Autosave**: Never lose your progress.
- **English language support**: Standard edition in English.
- **Modular codebase**: Easy to extend and maintain.

---

## 🧙‍♂️ Playable Classes

| Class    |
|----------|
| Elf      |
| Demon    |
| Dwarf    |
| Orc      |
| Human    |
| Inchling |

---

## 🕹️ Quick Start

```bash
# Clone the repo
git clone https://github.com/InkyyPinkyy/text_based_rpg.git
cd text_based_rpg

# Run the game
python -m __main__
```

---

## 🗺️ Planned Features

- [ ] More events: dungeons, villages, NPC encounters
- [ ] Reworked inventory & weapon system (rarities, elements, durability)
- [ ] Respawn system
- [ ] Use inventory during combat
- [ ] Drop system
- [ ] structured save-file
- [x] Autosave
- [x] English as the standard edition
- [ ] Skill system (unique tree for every species)
- [ ] graphics/interactive CLI
---

## 🧩 Code Example

```python
def event_enemy_encounter(player):
    monster_data = Enemy.get_random_monster("normal")
    enemy = Enemy(monster_data)
    player.enemy_encounter(enemy)
```

---

## 📦 Project Structure

```text
text_based_rpg/
├── __main__.py         # Game entry point
├── classes.py          # Player, Enemy, Item classes
├── events.py           # Random events and encounters
├── dungeon.py          # First stuff for Dungeon later on
├── lists_and_dicts.py  # Data for classes, monsters, items
├── README.md           # This file!
```

---

## 💡 Contributing

Pull requests are welcome! For major changes, please open an issue first to discuss what you would like to change.

---

## 📜 License

[MIT](LICENSE)

---

<p align="center">
  <img src="https://img.shields.io/badge/Adventure%20Awaits-Play%20Now!-purple?style=for-the-badge" alt="Adventure Awaits">
</p>