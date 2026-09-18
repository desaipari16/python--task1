import csv
import os
from datetime import datetime

FILE_NAME = "expenses.csv"
SUMMARY_FILE = "expense_summary.txt"


# -------------------- FILE HANDLING --------------------

def initialize_file():
    if not os.path.exists(FILE_NAME):
        try:
            with open(FILE_NAME, "w", newline="", encoding="utf-8") as file:
                writer = csv.writer(file)
                writer.writerow(["Date", "Category", "Description", "Amount"])
        except OSError as e:
            print(f"Error creating file: {e}")


def load_expenses():
    initialize_file()
    expenses = []

    try:
        with open(FILE_NAME, "r", newline="", encoding="utf-8") as file:
            reader = csv.DictReader(file)

            for row in reader:
                try:
                    expenses.append({
                        "date": row["Date"],
                        "category": row["Category"],
                        "description": row["Description"],
                        "amount": float(row["Amount"])
                    })
                except (ValueError, KeyError):
                    print("Warning: Invalid record found. Skipping it.")

    except FileNotFoundError:
        initialize_file()

    except OSError as e:
        print(f"Error reading file: {e}")

    return expenses


def save_expense(expense):
    try:
        with open(FILE_NAME, "a", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)

            writer.writerow([
                expense["date"],
                expense["category"],
                expense["description"],
                expense["amount"]
            ])

        print("\nExpense saved successfully!")

    except OSError as e:
        print(f"Error saving expense: {e}")


# -------------------- VALIDATION --------------------

def get_date():
    while True:
        date_input = input("Enter date (DD-MM-YYYY): ").strip()

        if not date_input:
            print("Date cannot be empty.")
            continue

        try:
            date_obj = datetime.strptime(date_input, "%d-%m-%Y")
            return date_obj.strftime("%d-%m-%Y")

        except ValueError:
            print("Invalid date. Use DD-MM-YYYY.")


def get_non_empty_input(message):
    while True:
        value = input(message).strip()

        if value:
            return value

        print("This field cannot be empty.")


def get_amount():
    while True:
        try:
            amount = float(input("Enter amount: "))

            if amount <= 0:
                print("Amount must be greater than 0.")
                continue

            return amount

        except ValueError:
            print("Invalid amount. Enter a number.")


# -------------------- ADD EXPENSE --------------------

def add_expense(expenses):
    print("\n===== Add New Expense =====")

    expense = {
        "date": get_date(),
        "category": get_non_empty_input("Enter category: "),
        "description": get_non_empty_input("Enter description: "),
        "amount": get_amount()
    }

    save_expense(expense)
    expenses.append(expense)


# -------------------- VIEW EXPENSES --------------------

def view_expenses(expenses):
    print("\n===== All Expenses =====")

    if not expenses:
        print("No expenses found.")
        return

    print("-" * 80)
    print(
        f"{'No.':<5}"
        f"{'Date':<15}"
        f"{'Category':<15}"
        f"{'Description':<25}"
        f"{'Amount':>10}"
    )
    print("-" * 80)

    for index, expense in enumerate(expenses, start=1):
        print(
            f"{index:<5}"
            f"{expense['date']:<15}"
            f"{expense['category']:<15}"
            f"{expense['description'][:23]:<25}"
            f"{expense['amount']:>10.2f}"
        )

    print("-" * 80)


# -------------------- SEARCH BY CATEGORY --------------------

def search_by_category(expenses):
    print("\n===== Search by Category =====")

    if not expenses:
        print("No expenses found.")
        return

    category = input("Enter category: ").strip().lower()

    if not category:
        print("Category cannot be empty.")
        return

    results = [
        expense for expense in expenses
        if expense["category"].lower() == category
    ]

    if not results:
        print("No expenses found for this category.")
        return

    print(f"\nExpenses in category: {category.title()}")

    print("-" * 70)

    for expense in results:
        print(
            f"{expense['date']:<15}"
            f"{expense['category']:<15}"
            f"{expense['description']:<25}"
            f"{expense['amount']:>10.2f}"
        )

    print("-" * 70)


# -------------------- TOTAL EXPENSE --------------------

def calculate_total(expenses):
    total = sum(expense["amount"] for expense in expenses)

    print("\n===== Total Expenses =====")
    print(f"Total Amount Spent: {total:.2f}")


# -------------------- SUMMARY REPORT --------------------

def generate_summary(expenses):
    print("\n===== Expense Summary =====")

    if not expenses:
        print("No expenses available.")
        return

    total_entries = len(expenses)
    total_spent = sum(expense["amount"] for expense in expenses)
    highest = max(expenses, key=lambda x: x["amount"])

    print(f"Total Entries: {total_entries}")
    print(f"Total Spent: {total_spent:.2f}")

    print(
        f"Highest Expense: "
        f"{highest['category']} - "
        f"{highest['amount']:.2f}"
    )

    category_totals = {}

    for expense in expenses:
        category = expense["category"]

        if category not in category_totals:
            category_totals[category] = 0

        category_totals[category] += expense["amount"]

    print("\nCategory-wise Totals:")

    for category, amount in category_totals.items():
        print(f"{category:<20}: {amount:.2f}")


# -------------------- MONTHLY SUMMARY --------------------

def monthly_summary(expenses):
    print("\n===== Monthly Expense Summary =====")

    if not expenses:
        print("No expenses available.")
        return

    monthly_totals = {}

    for expense in expenses:
        try:
            date_obj = datetime.strptime(
                expense["date"],
                "%d-%m-%Y"
            )

            month = date_obj.strftime("%m-%Y")

            if month not in monthly_totals:
                monthly_totals[month] = 0

            monthly_totals[month] += expense["amount"]

        except ValueError:
            continue

    for month, amount in sorted(monthly_totals.items()):
        print(f"{month:<15}: {amount:.2f}")


# -------------------- SORT BY AMOUNT --------------------

def sort_by_amount(expenses):
    print("\n===== Expenses Sorted by Amount =====")

    if not expenses:
        print("No expenses found.")
        return

    sorted_expenses = sorted(
        expenses,
        key=lambda x: x["amount"],
        reverse=True
    )

    print("-" * 70)

    for expense in sorted_expenses:
        print(
            f"{expense['date']:<15}"
            f"{expense['category']:<15}"
            f"{expense['description']:<25}"
            f"{expense['amount']:>10.2f}"
        )

    print("-" * 70)


# -------------------- EXPORT SUMMARY --------------------

def export_summary(expenses):
    if not expenses:
        print("\nNo expenses available to export.")
        return

    try:
        total_entries = len(expenses)
        total_spent = sum(expense["amount"] for expense in expenses)
        highest = max(expenses, key=lambda x: x["amount"])

        category_totals = {}

        for expense in expenses:
            category = expense["category"]

            category_totals[category] = (
                category_totals.get(category, 0)
                + expense["amount"]
            )

        with open(SUMMARY_FILE, "w", encoding="utf-8") as file:

            file.write("===== EXPENSE SUMMARY =====\n\n")
            file.write(f"Total Entries: {total_entries}\n")
            file.write(f"Total Spent: {total_spent:.2f}\n")

            file.write(
                f"Highest Expense: "
                f"{highest['category']} - "
                f"{highest['amount']:.2f}\n\n"
            )

            file.write("Category-wise Totals:\n")

            for category, amount in category_totals.items():
                file.write(
                    f"{category:<20}: {amount:.2f}\n"
                )

        print(
            f"\nSummary exported successfully to "
            f"'{SUMMARY_FILE}'."
        )

    except OSError as e:
        print(f"Error exporting summary: {e}")


# -------------------- MAIN MENU --------------------

def main():

    print("=" * 50)
    print("        PERSONAL EXPENSE TRACKER")
    print("=" * 50)

    expenses = load_expenses()

    while True:

        print("\n========== MENU ==========")
        print("1. Add New Expense")
        print("2. View All Expenses")
        print("3. Search by Category")
        print("4. Calculate Total Expenses")
        print("5. Generate Summary Report")
        print("6. Monthly Expense Summary")
        print("7. Sort Expenses by Amount")
        print("8. Export Summary to File")
        print("9. Exit")
        print("===========================")

        choice = input("Enter your choice (1-9): ").strip()

        if choice == "1":
            add_expense(expenses)

        elif choice == "2":
            view_expenses(expenses)

        elif choice == "3":
            search_by_category(expenses)

        elif choice == "4":
            calculate_total(expenses)

        elif choice == "5":
            generate_summary(expenses)

        elif choice == "6":
            monthly_summary(expenses)

        elif choice == "7":
            sort_by_amount(expenses)

        elif choice == "8":
            export_summary(expenses)

        elif choice == "9":
            print("\nThank you for using Expense Tracker!")
            print("Goodbye!")
            break

        else:
            print("Invalid choice. Please enter 1-9.")


# -------------------- PROGRAM START --------------------

if __name__ == "__main__":
    main()
    