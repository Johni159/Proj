import json
from collections import defaultdict
from datetime import datetime
from pathlib import Path

from tabulate import tabulate
import matplotlib.pyplot as plt

DATA_FILE = Path("expenses.json")

MONTHS_UA = {
    1: "Січень", 2: "Лютий", 3: "Березень", 4: "Квітень",
    5: "Травень", 6: "Червень", 7: "Липень", 8: "Серпень",
    9: "Вересень", 10: "Жовтень", 11: "Листопад", 12: "Грудень",
}


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

    rows = [
        [i, item["date"], item["category"], f"{item['amount']:.2f}"]
        for i, item in enumerate(expenses, start=1)
    ]

    print("\n--- Список витрат ---")
    print(tabulate(
        rows,
        headers=["№", "Дата", "Категорія", "Сума (грн)"],
        tablefmt="pretty",
    ))

    total = sum(item["amount"] for item in expenses)
    print(f"Загалом: {total:.2f} грн\n")


def show_available_categories(expenses):
    categories = sorted({item["category"] for item in expenses})
    if categories:
        print("Наявні категорії:", ", ".join(categories))


def analyze_by_category(expenses):
    if not expenses:
        print("Записів поки немає.")
        return

    show_available_categories(expenses)

    category = input("Категорія для аналізу: ").strip()
    if not category:
        print("Категорія не може бути порожньою.")
        return

    matched = [
        item for item in expenses
        if item["category"].lower() == category.lower()
    ]

    if not matched:
        print(f"Записів у категорії «{category}» не знайдено.")
        return

    rows = [
        [item["date"], item["category"], f"{item['amount']:.2f}"]
        for item in matched
    ]

    total = sum(item["amount"] for item in matched)

    print(f"\n--- Аналіз: {category} ---")
    print(tabulate(
        rows,
        headers=["Дата", "Категорія", "Сума (грн)"],
        tablefmt="pretty",
    ))
    print(f"\nРазом: {total:.2f} грн ({len(matched)} записів)\n")


def get_current_month_expenses(expenses):
    now = datetime.now()
    month_expenses = []

    for item in expenses:
        try:
            date = datetime.strptime(item["date"], "%Y-%m-%d")
        except ValueError:
            continue

        if date.year == now.year and date.month == now.month:
            month_expenses.append(item)

    return month_expenses, now


def monthly_report(expenses):
    if not expenses:
        print("Записів поки немає.")
        return

    month_expenses, now = get_current_month_expenses(expenses)
    month_name = f"{MONTHS_UA[now.month]} {now.year}"

    if not month_expenses:
        print(f"За {month_name} записів немає.")
        return

    total = sum(item["amount"] for item in month_expenses)

    by_category = defaultdict(float)
    for item in month_expenses:
        by_category[item["category"]] += item["amount"]

    rows = [
        [category, f"{amount:.2f}"]
        for category, amount in sorted(by_category.items())
    ]

    print(f"\n--- Звіт за {month_name} ---")
    print(f"Загальна сума витрат: {total:.2f} грн\n")
    print(tabulate(
        rows,
        headers=["Категорія", "Сума (грн)"],
        tablefmt="pretty",
    ))
    print()


def show_expenses_chart(expenses):
    """Діаграма витрат за поточний місяць."""
    if not expenses:
        print("Записів поки немає.")
        return

    month_expenses, now = get_current_month_expenses(expenses)
    month_name = f"{MONTHS_UA[now.month]} {now.year}"

    if not month_expenses:
        print(f"За {month_name} немає даних для графіка.")
        return

    by_category = defaultdict(float)
    for item in month_expenses:
        by_category[item["category"]] += item["amount"]

    categories = list(by_category.keys())
    amounts = list(by_category.values())

    fig, axes = plt.subplots(1, 2, figsize=(12, 5))
    fig.suptitle(f"Витрати за {month_name}", fontsize=14)

    # Кругова діаграма
    axes[0].pie(
        amounts,
        labels=categories,
        autopct="%1.1f%%",
        startangle=90,
    )
    axes[0].set_title("Частка за категоріями")

    # Стовпчикова діаграма
    axes[1].bar(categories, amounts, color="steelblue")
    axes[1].set_title("Сума за категоріями (грн)")
    axes[1].set_ylabel("Сума (грн)")
    axes[1].tick_params(axis="x", rotation=30)

    plt.tight_layout()
    plt.show()


def main():
    expenses = load_expenses()

    while True:
        print("\n=== Облік витрат ===")
        print("1. Додати запис")
        print("2. Переглянути всі записи")
        print("3. Аналіз за категорією")
        print("4. Звіт за місяць")
        print("5. Графік витрат")
        print("6. Вийти")

        choice = input("Оберіть дію: ").strip()

        if choice == "1":
            add_expense(expenses)
        elif choice == "2":
            show_expenses(expenses)
        elif choice == "3":
            analyze_by_category(expenses)
        elif choice == "4":
            monthly_report(expenses)
        elif choice == "5":
            show_expenses_chart(expenses)
        elif choice == "6":
            print("До побачення!")
            break
        else:
            print("Невірний вибір. Спробуйте ще раз.")


if __name__ == "__main__":
    main()
