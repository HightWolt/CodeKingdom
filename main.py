import json
import os

# Визуал
RESET = "\033[0m"
BOLD = "\033[1m"
GREEN = "\033[32m"
YELLOW = "\033[33m"
CYAN = "\033[36m"
RED = "\033[31m"

SAVE_FILE = "save.json"

def print_header():
    print(f"{BOLD}{CYAN}")
    print("  ╔══════════════════════════════╗")
    print("  ║      🌲 CODEKINGDOM 🌲       ║")
    print("  ╚══════════════════════════════╝")
    print(f"{RESET}")

def show_stats(hp, attack, inventory):
    # Текущие характеристики
    print(f"\n{BOLD}📊 Твои характеристики:{RESET}")
    print(f" ❤ Здоровье: {hp} | ⚔ Атака: {attack}")
    print(f" 🎒 Инвентарь: {', '.join(inventory)}")

def show_menu():
    print(f"\n{BOLD}📍 ПЕРЕД ТОБОЙ РАЗВИЛКА:{RESET}")
    print(f" {GREEN}1.{RESET} Пойти в тёмный лес 🌲")
    print(f" {CYAN}2.{RESET} Зайти в деревню 🏘")
    print(f" {YELLOW}3.{RESET} Отдохнуть у костра")
    print(f" {RED}4.{RESET} Выйти из игры 🚪 ")

def get_choice():
    # Валидация выбора
    valid_choices = {"1", "2", "3", "4"}
    while True:
        choice = input(f"\n{BOLD}Твоё решение? (1/2/3/4): {RESET}").strip()
        if choice == "":
            print(f"{RED}⚠ Пустота не ведёт никуда. Введи цифру!{RESET}")
        elif choice not in  valid_choices:
            print(f"{RED} ⚠ Неверная руна! Магия понимает только 1, 2, 3 или 4{RESET}")
        else:
            return choice

def proccess_choice(choice, hp, attack, inventory):
    if choice == "1":
        print(f"\n{GREEN}🍂 В лесу на тебя выскакивает волк! Ты отбиваешься.{RESET}")
        hp -= 10
        attack += 2
        print(f" ❤ Здоровье: {hp} (-10) | ⚔ Атака: {attack} (+2)")

        if "🐺 Волчий зуб" not in inventory:
            inventory.append("🐺 Волчий зуб")
            print(" 🎒 В рюкзак упал: Волчий зуб!")

    elif choice == "2":
        print(f"{CYAN}🏠 В деревне лекарь даёт тебе зелье.{RESET}")
        if "🧪 Зелье здоровья" not in inventory:
            inventory.append("🧪 Зелье здоровья")
            print(" 🎒 Получено: Зелье здоровья")
    
    elif choice == "3":
        print(f"\n{YELLOW}💤 Ты разводишь костёр и восстанавливаешь силы...")
        hp = min(100, hp + 20)
        print(f" ❤ Здоровье восстановлено до {hp}!")

    elif choice == "4":
        print(f"\n{RED}🌙 До встречи, герой! История сохраниться в памяти...{RESET}")
        return hp, attack, inventory, False

    # Проверка на конец игры
    if hp <= 0:
        print(f"\n{RED}💀 Твоё здоровье иссякло. Ты падаешь  без сил...{RESET}")
        print(" Игра окончена. Спасибо за приключение!")
        return hp, attack, inventory, False

    return hp, attack, inventory, True

def save_game(player_name, hp, attack, inventory):
    """Сохраняет прогресс в файл JSON"""
    data = {
        "player_name": player_name,
        "hp": hp,
        "attack": attack,
        "inventory": inventory
    }
    with open(SAVE_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)
    print(f"💾 Прогресс сохранён  в {SAVE_FILE}")

def load_game():
    """Загружает прогресс из файла, если он существует"""
    if not os.path.exists(SAVE_FILE):
        return None
    try:
        with open(SAVE_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError):
        return None

def main():
    print_header()
    saved_data = load_game()

    if saved_data:
        print(f"{GREEN}📜 Найдено сохранение: {saved_data['player_name']}(❤ {saved_data['hp']}){RESET}")
        start_choice = input(f"Загрузить прошлую историю? (1 - Да, 2 - Начать заново): {RESET}").strip()

        if start_choice == "1":
            player_name  = saved_data["player_name"]
            hp = saved_data["hp"]
            attack = saved_data["attack"]
            inventory = saved_data["inventory"]
            print(f"\n{CYAN}✨ Добро пожаловать обратно, {player_name}!{RESET}")
        else:
            player_name = input(f"{GREEN}Как тебя зовут, герой?{RESET}").strip()
            hp, attack, inventory = 100, 5, ["🗺 Карта мира", "🍞 Хлеб"]
    else:
        player_name = input(f"{GREEN}Как тебя зовут, герой?{RESET}").strip()
        hp, attack, inventory = 100, 5, ["🗺 Карта мира", "🍞 Хлеб"]

    print(f"\n{YELLOW}Привет, {player_name}! Твоя история начинается.{RESET}")
    playing = True

    while playing:
        show_stats(hp, attack, inventory)
        show_menu()
        choice = get_choice()
        hp, attack, inventory, playing = proccess_choice(choice, hp, attack, inventory)
    
    save_game(player_name, hp, attack, inventory)

if __name__ == "__main__":
    main()