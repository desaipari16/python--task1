import json
import os

DATA_FILE = "students_oop.json"

class Student:
    """Represents an individual student record."""
    def __init__(self, student_id: str, name: str, age: int, marks: float):
        self.student_id = student_id
        self.name = name
        self.age = age
        self.marks = marks

    def to_dict(self) -> dict:
        """Converts object attributes to a dictionary for JSON serialization."""
        return {
            "name": self.name,
            "age": self.age,
            "marks": self.marks
        }

    @classmethod
    def from_dict(cls, student_id: str, data: dict):
        """Factory method to instantiate a Student object from a dictionary."""
        return cls(
            student_id=student_id,
            name=data["name"],
            age=data["age"],
            marks=data["marks"]
        )


class StudentManager:
    """Manages collection operations and storage persistence for students."""
    def __init__(self, storage_file: str = DATA_FILE):
        self.storage_file = storage_file
        self.students = {}  # Dictionary mapping student_id -> Student object
        self._load_from_file()

    # ==========================
    # FILE PERSISTENCE METHODS
    # ==========================

    def _load_from_file(self):
        """Loads data from JSON file and reconstitutes Student instances."""
        if not os.path.exists(self.storage_file):
            return
        try:
            with open(self.storage_file, "r") as file:
                raw_data = json.load(file)
                for sid, details in raw_data.items():
                    self.students[sid] = Student.from_dict(sid, details)
        except (json.JSONDecodeError, IOError):
            print("⚠️  Warning: Failed to load existing database file. Starting fresh.")

    def save_to_file(self) -> bool:
        """Saves current student collection to the JSON file."""
        try:
            serialized_data = {
                sid: student.to_dict() for sid, student in self.students.items()
            }
            with open(self.storage_file, "w") as file:
                json.dump(serialized_data, file, indent=4)
            return True
        except IOError as e:
            print(f"❌ Error saving to file: {e}")
            return False

    # ==========================
    # INPUT VALIDATION HELPERS
    # ==========================

    @staticmethod
    def _validate_int(prompt: str, min_val: int = 0, max_val: int = 120) -> int:
        """Prompts until a valid integer in range is provided."""
        while True:
            try:
                val = int(input(prompt))
                if min_val <= val <= max_val:
                    return val
                print(f"⚠️  Please enter a number between {min_val} and {max_val}.")
            except ValueError:
                print("⚠️  Invalid input! Please enter a valid integer.")

    @staticmethod
    def _validate_float(prompt: str, min_val: float = 0.0, max_val: float = 100.0) -> float:
        """Prompts until a valid float in range is provided."""
        while True:
            try:
                val = float(input(prompt))
                if min_val <= val <= max_val:
                    return val
                print(f"⚠️  Please enter a value between {min_val} and {max_val}.")
            except ValueError:
                print("⚠️  Invalid input! Please enter a valid decimal number.")

    # ==========================
    # CRUD & SEARCH METHODS
    # ==========================

    def add_student(self):
        """Adds a new student to the system."""
        print("\n--- ➕ Add Student ---")
        student_id = input("Enter Student ID: ").strip()
        
        if not student_id:
            print("❌ Student ID cannot be empty.")
            return
        if student_id in self.students:
            print("❌ A student with this ID already exists.")
            return

        name = input("Enter Name: ").strip()
        if not name:
            print("❌ Name cannot be empty.")
            return

        age = self._validate_int("Enter Age (5-100): ", min_val=5, max_val=100)
        marks = self._validate_float("Enter Marks (0.0-100.0): ", min_val=0.0, max_val=100.0)

        # Create new student object and save
        new_student = Student(student_id, name, age, marks)
        self.students[student_id] = new_student

        if self.save_to_file():
            print(f"✅ Student '{name}' (ID: {student_id}) added successfully!")

    def view_all_students(self):
        """Displays all student records formatted in a clean table."""
        print("\n--- 📜 All Student Records ---")
        if not self.students:
            print("No student records found.")
            return

        print("-" * 52)
        print(f"| {'ID':<8} | {'Name':<20} | {'Age':<5} | {'Marks':<6} |")
        print("-" * 52)
        for sid, student in self.students.items():
            print(f"| {sid:<8} | {student.name:<20} | {student.age:<5} | {student.marks:<6.2f} |")
        print("-" * 52)

    def search_student(self):
        """Finds and displays details for a given Student ID."""
        print("\n--- 🔍 Search Student ---")
        sid = input("Enter Student ID to search: ").strip()

        student = self.students.get(sid)
        if student:
            print("\nRecord Found:")
            print(f"  ID    : {student.student_id}")
            print(f"  Name  : {student.name}")
            print(f"  Age   : {student.age}")
            print(f"  Marks : {student.marks:.2f}")
        else:
            print("❌ Student ID not found.")

    def update_student(self):
        """Updates attributes for an existing student record."""
        print("\n--- ✏️ Update Student ---")
        sid = input("Enter Student ID to update: ").strip()

        if sid not in self.students:
            print("❌ Student ID not found.")
            return

        student = self.students[sid]
        print(f"Updating '{student.name}' (Leave blank to keep existing value):")

        # Optional updates
        new_name = input(f"New Name [{student.name}]: ").strip()
        if new_name:
            student.name = new_name

        age_input = input(f"New Age [{student.age}]: ").strip()
        if age_input:
            try:
                age_val = int(age_input)
                if 5 <= age_val <= 100:
                    student.age = age_val
                else:
                    print("⚠️ Invalid age range. Keeping original value.")
            except ValueError:
                print("⚠️ Invalid input format. Keeping original age.")

        marks_input = input(f"New Marks [{student.marks}]: ").strip()
        if marks_input:
            try:
                marks_val = float(marks_input)
                if 0.0 <= marks_val <= 100.0:
                    student.marks = marks_val
                else:
                    print("⚠️ Invalid marks range. Keeping original value.")
            except ValueError:
                print("⚠️ Invalid input format. Keeping original marks.")

        if self.save_to_file():
            print("✅ Student record updated successfully!")

    def delete_student(self):
        """Removes a student record by ID."""
        print("\n--- 🗑️ Delete Student ---")
        sid = input("Enter Student ID to delete: ").strip()

        if sid not in self.students:
            print("❌ Student ID not found.")
            return

        removed_student = self.students.pop(sid)
        if self.save_to_file():
            print(f"✅ Record for '{removed_student.name}' (ID: {sid}) deleted successfully!")


# ==========================
# CLI APPLICATION DRIVER
# ==========================

def main():
    manager = StudentManager()

    while True:
        print("\n==================================")
        print("   STUDENT MANAGEMENT SYSTEM (OOP)")
        print("==================================")
        print("1. Add Student")
        print("2. View All Students")
        print("3. Search Student")
        print("4. Update Student")
        print("5. Delete Student")
        print("6. Exit")
        print("==================================")

        choice = input("Select an option (1-6): ").strip()

        if choice == '1':
            manager.add_student()
        elif choice == '2':
            manager.view_all_students()
        elif choice == '3':
            manager.search_student()
        elif choice == '4':
            manager.update_student()
        elif choice == '5':
            manager.delete_student()
        elif choice == '6':
            print("Exiting application. Goodbye!")
            break
        else:
            print("⚠️ Invalid option! Please select a choice from 1 to 6.")


if __name__ == "__main__":
    main()