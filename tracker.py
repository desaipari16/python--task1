import csv
from datetime import datetime
from collections import defaultdict

FILE_NAME = "expenses.csv"


# -------------------------------
# Load expenses from CSV
# -------------------------------
def load_expenses():
    expenses = []

    try:
        with open(FILE_NAME, "r", newline="") as file:
            reader = csv.DictReader(file)

            for row in reader:
                expenses.append({
                    "amount": float(row["amount"]),
                    "category": row["category"],
                    "description": row["description"],
                    "date": row["date"]
                })

    except FileNotFoundError:
        pass

    return expenses


# -------------------------------
# Save expenses to CSV
# -------------------------------
def save_expenses(expenses):
    with open(FILE_NAME, "w", newline="") as file:
        fieldnames = ["amount", "category", "description", "date"]

        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(expenses)


# -------------------------------
# Add Expense
# -------------------------------
def add_expense(expenses):
    print("\n--- Add Expense ---")

    while True:
        try:
            amount = float(input("Enter amount: ₹"))

            if amount <= 0:
                print("Amount must be greater than 0.")
                continue

            break

        except ValueError:
            print("Please enter a valid number.")

    category = input("Enter category: ").strip()

    while not category:
        print("Category cannot be empty.")
        category = input("Enter category: ").strip()

    description = input("Enter description: ").strip()

    while True:
        date = input("Enter date (YYYY-MM-DD): ")

        try:
            datetime.strptime(date, "%Y-%m-%d")
            break
        except ValueError:
            print("Invalid date format.")

    expense = {
        "amount": amount,
        "category": category,
        "description": description,
        "date": date
    }

    expenses.append(expense)
    save_expenses(expenses)

    print("Expense added successfully!")


# -------------------------------
# View Expenses
# -------------------------------
def view_expenses(expenses):
    print("\n--- All Expenses ---")

    if not expenses:
        print("No expenses found.")
        return

    print("-" * 75)
    print(f"{'No.':<5}{'Amount':<12}{'Category':<15}"
          f"{'Description':<20}{'Date':<15}")
    print("-" * 75)

    for i, expense in enumerate(expenses, 1):
        print(
            f"{i:<5}"
            f"₹{expense['amount']:<11.2f}"
            f"{expense['category']:<15}"
            f"{expense['description']:<20}"
            f"{expense['date']:<15}"
        )

    print("-" * 75)


# -------------------------------
# Filter by Category
# -------------------------------
def filter_by_category(expenses):
    category = input("Enter category: ").strip().lower()

    result = [
        expense for expense in expenses
        if expense["category"].lower() == category
    ]

    print("\n--- Category Results ---")
    view_expenses(result)


# -------------------------------
# Filter by Date Range
# -------------------------------
def filter_by_date_range(expenses):
    start_date = input("Enter start date (YYYY-MM-DD): ")
    end_date = input("Enter end date (YYYY-MM-DD): ")

    try:
        start = datetime.strptime(start_date, "%Y-%m-%d")
        end = datetime.strptime(end_date, "%Y-%m-%d")

        if start > end:
            print("Start date cannot be after end date.")
            return

    except ValueError:
        print("Invalid date format.")
        return

    result = []

    for expense in expenses:
        expense_date = datetime.strptime(
            expense["date"], "%Y-%m-%d"
        )

        if start <= expense_date <= end:
            result.append(expense)

    print("\n--- Date Range Results ---")
    view_expenses(result)


# -------------------------------
# Monthly Summary
# -------------------------------
def monthly_summary(expenses):
    month = input("Enter month (YYYY-MM): ")

    try:
        datetime.strptime(month, "%Y-%m")
    except ValueError:
        print("Invalid month format.")
        return

    category_totals = defaultdict(float)

    for expense in expenses:
        if expense["date"].startswith(month):
            category_totals[expense["category"]] += expense["amount"]

    if not category_totals:
        print("No expenses found for this month.")
        return

    total = sum(category_totals.values())

    print(f"\n--- Monthly Summary: {month} ---")

    for category, amount in category_totals.items():
        print(f"{category:<15} ₹{amount:.2f}")

    print("-" * 30)
    print(f"Total Spending: ₹{total:.2f}")


# -------------------------------
# Category Percentage
# -------------------------------
def category_percentage(expenses):
    if not expenses:
        print("No expenses available.")
        return

    category_totals = defaultdict(float)

    for expense in expenses:
        category_totals[expense["category"]] += expense["amount"]

    total = sum(category_totals.values())

    print("\n--- Spending Percentage by Category ---")

    for category, amount in category_totals.items():
        percentage = (amount / total) * 100

        print(
            f"{category:<15} "
            f"₹{amount:<10.2f} "
            f"{percentage:.2f}%"
        )


# -------------------------------
# Main Menu
# -------------------------------
def main():
    expenses = load_expenses()

    while True:
        print("\n")
        print("=" * 40)
        print("       EXPENSE TRACKER")
        print("=" * 40)

        print("1. Add Expense")
        print("2. View All Expenses")
        print("3. Filter by Category")
        print("4. Filter by Date Range")
        print("5. Monthly Summary")
        print("6. Category Percentage")
        print("7. Exit")

        choice = input("\nEnter your choice: ")

        if choice == "1":
            add_expense(expenses)

        elif choice == "2":
            view_expenses(expenses)

        elif choice == "3":
            filter_by_category(expenses)

        elif choice == "4":
            filter_by_date_range(expenses)

        elif choice == "5":
            monthly_summary(expenses)

        elif choice == "6":
            category_percentage(expenses)

        elif choice == "7":
            save_expenses(expenses)
            print("Thank you for using Expense Tracker!")
            break

        else:
            print("Invalid choice. Please try again.")


# Start program
if __name__ == "__main__":
    main()