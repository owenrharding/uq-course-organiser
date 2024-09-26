import json
import sys

HELP = "-h"
ADD = "--add"
HISTORY = "--his"

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

def add_course(degree_data):
    """
    Adds a new degree to the json file through prompting user input.
    """
    print("\nCOURSE ADDITION\n")
    available_categories = []
    for category in degree_data["Bachelor of Engineering (Honours) and Master of Engineering"]["unit_categories"]:
        print(f"Category: {category['category']}")
        if "unit_categories" in category:
            for sub_cat in category["unit_categories"]:
                available_categories.append((sub_cat["category"], category["category"]))
        else:
            available_categories.append((category["category"], None))
    
    print("These categories can be added to:")
    for i, category in enumerate(available_categories):
        if category[1] is not None:
            print(f"{i+1}. {category[1]} -> {category[0]}")
        else:
            print(f"{i+1}. {category[0]}")
    print()
    
    category_index = int(input("Enter the number of the category you would like to add to: "))

    if category_index < 1 or category_index > len(available_categories):
        print("Invalid category number.")
        return
    
    main_category = None
    sub_category = None
    if available_categories[category_index-1][1] is not None:
        main_category = available_categories[category_index-1][1]
        sub_category = available_categories[category_index-1][0]
    else:
        main_category = available_categories[category_index-1][0]

    for category in degree_data["Bachelor of Engineering (Honours) and Master of Engineering"]["unit_categories"]:
        if category["category"] == main_category:
            print(f"Main category: {main_category}.")
            # Check if there's a sub-category
            if "unit_categories" in category:
                for sub_cat in category["unit_categories"]:
                    if sub_cat["category"] == sub_category:
                        print(f"Sub-category: {sub_category}.")
                        # For now just add to hardcoded category.
                        course_code = input("Enter course code: ")
                        course_name = input("Enter course name: ")
                        course_units = int(input("Enter the unit value of this course: "))
                        sem_one = input("Is this course offered in semester one? (y/n): ") == "y"
                        sem_two = input("Is this course offered in semester two? (y/n): ") == "y"
                        completed = input("Have you completed this course? (y/n): ") == "y"
                        completed_year = None
                        completed_sem = None
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
    # Inefficient, but works for now.
    completed_courses = []
    years_and_sems = []

    # Extract al courses which are true for "completed".
    for category in degree_data["Bachelor of Engineering (Honours) and Master of Engineering"]["unit_categories"]:
        if "unit_categories" in category:
            for sub_cat in category["unit_categories"]:
                for course in sub_cat["courses"]:
                    if course["completed"]:
                        completed_courses.append((course["completed_year"], course["completed_sem"], course["code"], course["name"]))
                        # Keep track of all years and semesters, keeping them unique.
                        if (course["completed_year"], course["completed_sem"]) not in years_and_sems:
                            years_and_sems.append((course["completed_year"], course["completed_sem"]))
        elif "courses" in category:
            for course in category["courses"]:
                if course["completed"]:
                    completed_courses.append((course["completed_year"], course["completed_sem"], course["code"], course["name"]))
                    # Keep track of all years and semesters, keeping them unique.
                    if (course["completed_year"], course["completed_sem"]) not in years_and_sems:
                        years_and_sems.append((course["completed_year"], course["completed_sem"]))
    
    # Sort the completed courses by completed_year and completed_sem.
    # Thanks chatgpt for this.
    sorted_courses = sorted(completed_courses, key=lambda x: (x[0], x[1]))
    sorted_years_and_sems = sorted(years_and_sems, key=lambda x: (x[0], x[1]))

    print("\nCOURSE HISTORY\n")
    for year, sem in sorted_years_and_sems:
        print("==============================")
        print(f"Semester {sem}, {year}")
        print("==============================")
        for course in sorted_courses:
            if course[0] == year and course[1] == sem:
                print(f"{course[2]} - {course[3]}")
    print()

def display_usage():
    print(f"Usage: python3 degree_manager.py [{HELP}] [{ADD}] [{HISTORY}]")

def display_help():
    print()
    display_usage()
    print("Options:")
    print(f"{HELP}:  Show this help message and exit.")
    print(f"{ADD}:  Add a new course to the degree data.")
    print(f"{HISTORY}:  Show all completed courses so far.")
    print()

def main():
    degree_data = load_degree_data()

    if len(sys.argv) < 2:
        display_usage()

    if HELP in sys.argv:
        display_help()
    
    if ADD in sys.argv:
        add = True
        while add:
            add_course(degree_data)
            add = input("Would you like to add another course? (y/n): ") == "y"
    
    if HISTORY in sys.argv:
        display_course_history(degree_data)

if __name__ == "__main__":
    main()