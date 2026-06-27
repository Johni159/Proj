import json
from datetime import datetime
from pathlib import Path

DATA_FILE = Path("expenses.json")


def load_expenses():
    if not DATA_FILE.exists():
        return []
    with DATA_FILE.open("r", encoding="utf-8") as f:
        return json.load(f)


def save_expenses(expenses):
    with DATA_FILE.open("w", encoding="utf-8") as f:
        json.dump(expenses, f, ensure_ascii=False, indent=2)


def add_expense(expenses):
    try:
        amount = float(input("Сума: ").replace(",", "."))
        if amount <= 0:
            print("Сума має бути більше нуля.")
            return
    except ValueError:
        print("Некоректна сума.")
        return

    category = input("Категорія: ").strip()
    if not category:
        print("Категорія не може бути порожньою.")
        return

    date_str = input("Дата (YYYY-MM-DD, Enter = сьогодні): ").strip()
    if not date_str:
        date_str = datetime.now().strftime("%Y-%m-%d")
    else:
        try:
            datetime.strptime(date_str, "%Y-%m-%d")
        except ValueError:
            print("Некоректний формат дати.")
            return

    expenses.append({
        "amount": amount,
        "category": category,
        "date": date_str,
    })
    save_expenses(expenses)
    print("Запис додано.")


def show_expenses(expenses):
    if not expenses:
        print("Записів поки немає.")
        return

    print("\n--- Список витрат ---")
    total = 0
    for i, item in enumerate(expenses, start=1):
        print(f"{i}. {item['date']} | {item['category']} | {item['amount']:.2f}")
        total += item["amount"]
    print(f"Загалом: {total:.2f}\n")


def main():
    expenses = load_expenses()

    while True:
        print("=== Облік витрат ===")
        print("1. Додати запис")
        print("2. Переглянути всі записи")
        print("3. Вийти")

        choice = input("Оберіть дію: ").strip()

        if choice == "1":
            add_expense(expenses)
        elif choice == "2":
            show_expenses(expenses)
        elif choice == "3":
            print("До побачення!")
            break
        else:
            print("Невірний вибір. Спробуйте ще раз.")


if __name__ == "__main__":
    main()
