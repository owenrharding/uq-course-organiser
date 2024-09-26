import json
import sys

def load_degree_data(filename="degree.json"):
    try:
        with open(filename, "r") as file:
            return json.load(file)
    except FileNotFoundError:
        print("Degree data file not found.")
        return None

def save_degree_data(degree_data, filename="degree.json"):
    with open(filename, "w") as file:
        json.dump(degree_data, file)
    print("Degree data saved successfully.")

def add_course(degree_data, main_category, sub_category):
    """
    Adds a new degree to the json file through prompting user input.
    """
    print("\nCOURSE ADDITION\n")
    for category in degree_data["Bachelor of Engineering (Honours) and Master of Engineering"]["unit_categories"]:
        if category["category"] == main_category:
            # Check if there's a sub-category
            if "unit_categories" in category:
                for sub_cat in category["unit_categories"]:
                    if sub_cat["category"] == sub_category:
                        # For now just add to hardcoded category.
                        course_code = input("Enter course code: ")
                        course_name = input("Enter course name: ")
                        course_units = int(input("Enter the unit value of this course: "))
                        sem_one = input("Is this course offered in semester one? (y/n): ") == "y"
                        sem_two = input("Is this course offered in semester two? (y/n): ") == "y"
                        completed = input("Have you completed this course? (y/n): ") == "y"
                        completed_year = json.null
                        completed_sem = json.null
                        if completed:
                            completed_year = int(input("Enter the year you completed this course (YYYY): "))
                            completed_sem = int(input("Enter the semester you completed this course (1/2): "))  

                        new_course = {
                            "code": course_code,
                            "name": course_name,
                            "units": course_units,
                            "semester_one": sem_one,
                            "semester_two": sem_two,
                            "completed": completed,
                            "completed_year": completed_year,
                            "completed_sem": completed_sem
                        }

                        print("\nYou entered the following course:")
                        print("===")
                        print(f"{course_code} - {course_name}")
                        print(f"Units: {course_units}")
                        print("Offered in: ", end="")
                        if sem_one and sem_two:
                            print("Semesters 1 and 2")
                        elif sem_one:
                            print("Semester 1")
                        elif sem_two:
                            print("Semester 2")
                        else: 
                            print("Not Available")
                        if completed:
                            print(f"Completed in Semester {completed_sem}, {completed_year}")
                        else:
                            print("Not completed yet.")
                        print("===\n")
                        confirm = input("Would you like to add this course to the degree data? (y/n): ") == "y"

                        if confirm:
                            sub_cat["courses"].append(new_course)
                            save_degree_data(degree_data)
                            print("Course added to sub-category.\n")
                            return
                        else:
                            print("Course not added.")
                            return

    print("Category not found.")
    return

def display_course_history(degree_data):
    """
    Displays all comepleted courses so far.
    """
    pass

def display_usage():
    print("Usage: python3 degree_manager.py [-h] [-a] [-c] []")

def display_help():
    print()
    display_usage()
    print("Options:")
    print("    -h:  Show this help message and exit.")
    print("    -a:  Add a new course to the degree data.")
    print("    -c:  Show all completed courses so far.")
    print()

def main():
    degree_data = load_degree_data()

    if len(sys.argv) <= 2:
        display_usage()

    if "-h" in sys.argv:
        display_help()
    
    if "-a" in sys.argv:
        add = True
        while add:
            add_course(degree_data, "Field of Software Engineering", "Software Engineering Compulsory Courses")
            add = input("Would you like to add another course? (y/n): ") == "y"
    
    if "-c" in sys.argv:
        display_course_history(degree_data)

if __name__ == "__main__":
    main()