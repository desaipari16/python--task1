import json
import os
from datetime import datetime
import matplotlib.pyplot as plt

FILENAME = "expenses.json"

def load_expenses():
    if not os.path.exists(FILENAME):
        return []
    with open(FILENAME, "r") as file:
        try:
            return json.load(file)
        except json.JSONDecodeError:
            return []

def save_expenses(expenses):
    with open(FILENAME, "w") as file:
        json.dump(expenses, file, indent=4)

def add_expense(expenses):
    print("\n--- Add New Expense ---")
    date_str = input("Enter date (YYYY-MM-DD) or press Enter for today: ").strip()
    if not date_str:
        date_str = datetime.today().strftime('%Y-%m-%d')
    else:
        try:
            datetime.strptime(date_str, '%Y-%m-%d')
        except ValueError:
            print("Invalid date format. Using today's date.")
            date_str = datetime.today().strftime('%Y-%m-%d')

    category = input("Enter category (e.g., Food, Travel, Utilities): ").strip().capitalize()
    if not category:
        category = "General"

    description = input("Enter description: ").strip()

    try:
        amount = float(input("Enter amount ($): "))
        if amount <= 0:
            print("Amount must be a positive number.")
            return
    except ValueError:
        print("Invalid amount entered. Please enter a number.")
        return

    expense = {
        "date": date_str,
        "category": category,
        "description": description,
        "amount": amount
    }
    
    expenses.append(expense)
    save_expenses(expenses)
    print("Expense added successfully!")

def view_expenses(expenses):
    if not expenses:
        print("\nNo expenses recorded yet.")
        return
    print("\n--- All Expenses ---")
    print(f"{'Index':<6} {'Date':<12} {'Category':<15} {'Amount':<10} {'Description'}")
    print("-" * 60)
    for idx, exp in enumerate(expenses, 1):
        print(f"{idx:<6} {exp['date']:<12} {exp['category']:<15} ${exp['amount']:<9.2f} {exp['description']}")

def generate_summary(expenses):
    if not expenses:
        print("\nNo data available for summary.")
        return
    
    total_spent = sum(exp['amount'] for exp in expenses)
    category_totals = {}
    
    for exp in expenses:
        cat = exp['category']
        category_totals[cat] = category_totals.get(cat, 0) + exp['amount']
        
    print("\n--- Spending Summary ---")
    print(f"Total Spent: ${total_spent:.2f}\n")
    print("Category Breakdown:")
    print(f"{'Category':<18} {'Total ($)':<12} {'Percentage (%)'}")
    print("-" * 42)
    
    categories = []
    amounts = []
    
    for cat, amt in category_totals.items():
        percentage = (amt / total_spent) * 100 if total_spent > 0 else 0
        print(f"{cat:<18} ${amt:<11.2f} {percentage:.1f}%")
        categories.append(cat)
        amounts.append(amt)
        
    # Generate and display the Pie Chart
    print("\nGenerating visual breakdown window...")
    plt.figure(figsize=(8, 6))
    plt.pie(amounts, labels=categories, autopct='%1.1f%%', startangle=140, shadow=False)
    plt.title(f"Expense Breakdown by Category\nTotal Tracked: ${total_spent:.2f}")
    plt.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
    plt.tight_layout()
    plt.show()

def main():
    expenses = load_expenses()
    while True:
        print("\n=== Expense Tracker Menu ===")
        print("1. Add Expense")
        print("2. View All Expenses")
        print("3. Generate Summary Report & Chart")
        print("4. Exit")
        
        choice = input("Choose an option (1-4): ").strip()
        
        if choice == '1':
            add_expense(expenses)
        elif choice == '2':
            view_expenses(expenses)
        elif choice == '3':
            generate_summary(expenses)
        elif choice == '4':
            print("Exiting application. Goodbye!")
            break
        else:
            print("Invalid choice. Please pick a number from 1 to 4.")

if __name__ == "__main__":
    main()
