import os
import json
import random

# Визуал
RESET = "\033[0m"
BOLD = "\033[1m"
GREEN = "\033[32m"
YELLOW = "\033[33m"
CYAN = "\033[36m"
RED = "\033[31m"

class Hero:
    """Чертёж героя. Описывает, кто он и что умеет"""
    def __init__(self, name="Герой", hp=100, attack=5, inventory=None):
        self.name = name
        self.hp = hp
        self.attack = attack
        self.inventory = inventory or ["🗺 Карта мира", "🍞 Хлеб"]
    
    def show_stats(self):
        print(f"\n{BOLD}📊 Твои характеристики:{RESET}")
        print(f" ❤ Здоровье: {self.hp} | ⚔ Атака: {self.attack}")
        print(f" 🎒 Инвентарь: {', '.join(self.inventory)}")
    
    def take_damage(self, amount):
        self.hp = max(0, self.hp - amount)
    
    def heal(self, amount):
        self.hp = min(100, self.hp + amount)
    
    def add_item(self, item):
        if item not in self.inventory:
            self.inventory.append(item)
            print(f" 🎒 В рюкзак упал: {item}!")

class GameEngine:
    """Движок игры. Управление циклом, вводом, сохранением и миром"""
    def __init__(self):
        self.hero = Hero()
        self.save_file = "save.json"
        self.is_running = True
        self.turn_count = 0
        self.is_night = False

    def start(self):
        print(f"{BOLD}{CYAN}")
        print("  ╔══════════════════════════════╗")
        print("  ║      🌲 CODEKINGDOM 🌲       ║")
        print("  ╚══════════════════════════════╝")
        print(f"{RESET}")

        self._load_or_create_hero()

        print(f"\n{YELLOW}Твоя история начинается, {self.hero.name}!{RESET}")

        while self.is_running:
            self.hero.show_stats()
            self._show_menu()
            choice = self._get_choice()
            self._proccess_choice(choice)
    
    def _load_or_create_hero(self):
        """Загружает прогресс из файла, если он существует"""
        if os.path.exists(self.save_file):
            try:
                with open(self.save_file, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    print(f"{GREEN}📜 Найдено сохранение: {data['name']}(❤ {data['hp']}){RESET}")
                    if input(f"{YELLOW}1. Новая игра | 2. Продолжить (1/2): {RESET}").strip() == "2":
                        self.hero = Hero(data["name"], data["hp"], data["attack"], data["inventory"])
                        self.turn_count = data.get("turn_count", 0)
                        self.is_night = data.get("is_night", False)
                        return
            except Exception:
                pass
        self.hero = Hero(input(f"\n{GREEN}Как тебя зовут, герой? {RESET}").strip())

    def _show_menu(self):
        time_icon = "🌙" if  self.is_night else "☀"
        print(f"\n{BOLD}{time_icon} ПЕРЕД ТОБОЙ РАЗВИЛКА:{RESET}")
        print(f" {GREEN}1.{RESET} Пойти в тёмный лес 🌲")
        print(f" {CYAN}2.{RESET} Зайти в деревню 🏘")
        print(f" {YELLOW}3.{RESET} Отдохнуть у костра 💤")
        print(f" {RED}4.{RESET} Выйти и сохранить прогресс 🚪💾")

    def _get_choice(self):
        while True:
            choice = input(f"\n{BOLD}Твоё решение? (1/2/3/4): {RESET}").strip()
            if choice in {"1", "2", "3", "4"}:
                return choice
            print(f"{RED} ⚠ Неверная руна! Магия понимает только 1, 2, 3 или 4{RESET}")
    
    def _advance_time(self):
        self.turn_count += 1
        if self.turn_count % 5 == 0:
            self.is_night = not self.is_night
            if self.is_night:
                print(f"\n{BOLD}🌙 Ночь опустилась на CodeKingdom...{RESET}")
                print(f"{RED}⚠ Ночные твари стали агрессивнее! Урон в лесу +50%{RESET}")
            else:
                print(f"\n{BOLD}☀ Рассвет разгоняет тени...{RESET}")
                print(f"{GREEN}✨ Дневной свет лечит раны. (+5 здоровья){RESET}")
                self.hero.heal(5)
    
    def _trigger_random_event(self):
        if random.random() <  0.35:
            event = random.randint(1, 4)
            if event == 1:
                print(f"\n{YELLOW}🦉 Сова роняет перо мудрости! (+1 к атаке){RESET}")
                self.hero.attack += 1
            elif event == 2:
                print(f"\n{YELLOW}💎 Ты находишь скрытый сундук! (+10 здоровья){RESET}")
                self.hero.heal(10)
            elif event == 3:
                print(f"\n{YELLOW}🌫 Густой туман сбивает с пути! (-5 здоровья){RESET}")
                self.hero.take_damage(5)
            else:
                print(f"\n{YELLOW}🍄 Ты съел странный гриб. Ветер попутный! (Ничего не изменилось){RESET}")

    def _proccess_choice(self, choice):
        if choice == "1":
            print(f"\n{GREEN}🍂 В лесу на тебя выскакивает волк! Ты отбиваешься.{RESET}")
            dmg  = 15 if self.is_night else 10
            self.hero.take_damage(dmg)
            self.hero.attack += 2
            print(f" ❤ Здоровье: {self.hero.hp} (-{dmg}) | ⚔ Атака: {self.hero.attack} (+2)")
            self.hero.add_item("🐺 Волчий зуб")

        elif choice == "2":
            print(f"{CYAN}🏠 В деревне лекарь даёт тебе зелье.{RESET}")
            self.hero.add_item("🧪 Зелье здоровья")

        elif choice == "3":
            print(f"\n{YELLOW}💤 Ты разводишь костёр и восстанавливаешь силы...")
            self.hero.heal(20)
            print(f" ❤ Здоровье восстановлено до {self.hero.hp}!")

        elif choice == "4":
            print(f"\n{RED}🌙 До встречи, герой! История сохраниться в памяти...{RESET}")
            self.is_running = False
        
        self._advance_time()
        self._trigger_random_event()

        if self.hero.hp <= 0:
            print(f"\n{RED}💀 Твоё здоровье иссякло. Ты падаешь  без сил...{RESET}")
            print(" Игра окончена. Спасибо за приключение!")
            self.is_running = False

        if not self.is_running:
            self._save_game()

    def _save_game(self):
        data = {
            "name": self.hero.name,
            "hp": self.hero.hp,
            "attack": self.hero.attack,
            "inventory": self.hero.inventory,
            "turn_count": self.turn_count,
            "is_night": self.is_night
        }
        with open(self.save_file, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
        print(f"💾 Прогресс сохранён  в {self.save_file}")

if __name__ == "__main__":
    game = GameEngine()
    game.start()