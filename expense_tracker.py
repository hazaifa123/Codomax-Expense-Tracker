import json
import os
from datetime import datetime

DATA_FILE = "expenses.json"


def load_expenses():
    if not os.path.exists(DATA_FILE):
        return []
    with open(DATA_FILE, "r") as file:
        try:
            return json.load(file)
        except json.JSONDecodeError:
            return []


def save_expenses(expenses):
    with open(DATA_FILE, "w") as file:
        json.dump(expenses, file, indent=4)


def add_expense(expenses):
    print("\n--- Add New Expense ---")
    title = input("Enter expense title (e.g., Lunch, Books, Transport): ").strip()
    category = input("Enter category (Food, Study, Travel, Other): ").strip().capitalize()
    
    try:
        amount = float(input("Enter amount (PKR): "))
        if amount <= 0:
            print("Amount must be greater than zero.")
            return
    except ValueError:
        print("Invalid input! Please enter a numeric value for amount.")
        return

    expense = {
        "id": len(expenses) + 1,
        "title": title,
        "category": category if category else "Other",
        "amount": amount,
        "date": datetime.now().strftime("%Y-%m-%d %H:%M")
    }
    expenses.append(expense)
    save_expenses(expenses)
    print(f"Success: '{title}' (PKR {amount:.2f}) added!")


def view_expenses(expenses):
    print("\n--- All Recorded Expenses ---")
    if not expenses:
        print("No expenses found yet.")
        return

    print(f"{'ID':<4} | {'Date':<16} | {'Category':<12} | {'Title':<20} | {'Amount (PKR)':>12}")
    print("-" * 74)
    for item in expenses:
        print(f"{item['id']:<4} | {item['date']:<16} | {item['category']:<12} | {item['title']:<20} | {item['amount']:>12.2f}")


def view_summary(expenses):
    print("\n--- Expense Summary ---")
    if not expenses:
        print("No data available to summarize.")
        return

    total = sum(item["amount"] for item in expenses)
    category_totals = {}
    for item in expenses:
        cat = item["category"]
        category_totals[cat] = category_totals.get(cat, 0) + item["amount"]

    print(f"Total Spending: PKR {total:.2f}\n")
    print("Breakdown by Category:")
    for cat, amt in category_totals.items():
        percentage = (amt / total) * 100
        print(f"  - {cat}: PKR {amt:.2f} ({percentage:.1f}%)")


def delete_expense(expenses):
    view_expenses(expenses)
    if not expenses:
        return

    try:
        exp_id = int(input("\nEnter the ID of the expense to delete: "))
    except ValueError:
        print("Invalid ID.")
        return

    for i, item in enumerate(expenses):
        if item["id"] == exp_id:
            removed = expenses.pop(i)
            # Re-index IDs
            for idx, exp in enumerate(expenses, start=1):
                exp["id"] = idx
            save_expenses(expenses)
            print(f"Deleted: '{removed['title']}'")
            return

    print("Expense ID not found.")


def main():
    expenses = load_expenses()
    while True:
        print("\n===============================")
        print("   CLI EXPENSE TRACKER (v1.0)  ")
        print("===============================")
        print("1. Add Expense")
        print("2. View All Expenses")
        print("3. View Spending Summary")
        print("4. Delete an Expense")
        print("5. Exit")

        choice = input("\nSelect an option (1-5): ").strip()

        if choice == "1":
            add_expense(expenses)
        elif choice == "2":
            view_expenses(expenses)
        elif choice == "3":
            view_summary(expenses)
        elif choice == "4":
            delete_expense(expenses)
        elif choice == "5":
            print("Exiting Expense Tracker. Goodbye!")
            break
        else:
            print("Invalid choice. Please enter a number between 1 and 5.")


if __name__ == "__main__":
    main()
