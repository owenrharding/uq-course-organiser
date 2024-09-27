import json
import sys

# ANSI escape sequences for colours.
RED = "\033[91m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
BLUE = "\033[94m"
CYAN = "\033[96m"
RESET = "\033[0m"

# Command line arguments.
HELP = "-h"
ADD = "--add"
HISTORY = "--his"
PROGRESS = "--prog"
RECOMMEND = "--rec"

BEME = "Bachelor of Engineering (Honours) and Master of Engineering"

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
    print(f"\n{GREEN}COURSE ADDITION{RESET}\n")
    available_categories = []
    for category in degree_data[BEME]["unit_categories"]:
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

    for category in degree_data[BEME]["unit_categories"]:
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
    for category in degree_data[BEME]["unit_categories"]:
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

    print(f"\n{GREEN}COURSE HISTORY{RESET}\n")
    for year, sem in sorted_years_and_sems:
        print("==================================================")
        print(f"{BLUE}Semester {sem}, {year}{RESET}")
        print("==================================================")
        for course in sorted_courses:
            if course[0] == year and course[1] == sem:
                print(f"{course[2]} - {course[3]}")
        print()
    print()

def display_progress(degree_data):
    """
    Displays the progress of the degree completion.
    """
    degree_units_required = degree_data[BEME]["units_required"]
    overall_units_completed = 0
    compulsory_units_completed = 0
    compulsory_units_required = 0
    de_units_completed = 0
    general_units_completed = 0
    categories_completion = []

    for category in degree_data[BEME]["unit_categories"]:
        if "unit_categories" in category:
            for sub_cat in category["unit_categories"]:
                sub_cat_units_completed = 0
                for course in sub_cat["courses"]:
                    if course["completed"]:
                        sub_cat_units_completed += course["units"]
                categories_completion.append((sub_cat["category"], sub_cat_units_completed, sub_cat["min_units"], sub_cat["max_units"]))
        elif "courses" in category:
            cat_units_completed = 0
            for course in category["courses"]:
                if course["completed"]:
                    cat_units_completed += course["units"]
            categories_completion.append((category["category"], cat_units_completed, category["min_units"], category["max_units"]))
    
    print(f"\n{GREEN}DEGREE PROGRESS{RESET}\n")
    for category in categories_completion:
        overall_units_completed += category[1]
        if "Compulsory" in category[0] or "Core" in category[0]:
            compulsory_units_completed += category[1]
            compulsory_units_required += category[2]
        elif "General Elective" in category[0]:
            general_units_completed += category[1]
        else:
            de_units_completed += category[1]
        print("==================================================")
        print(f"{BLUE}{category[0]}{RESET}")
        print("==================================================")
        if category[1] >= category[2] and category[2] == category[3]:
            print(f"You have completed {category[1]} units in this category.")
            print(f"You have completed all units in this category.")
        elif category[1] >= category[2] and category[2] != category[3]:
            print(f"You have completed {category[1]} units in this category.")
            print(f"You have completed more than the required units in this category.")
            print(f"If you wanted to, you could complete up to {YELLOW}{category[3]}{RESET} more units.")
        elif category[1] < category[2] and category[2] == category[3]:
            print(f"You have completed {category[1]} units in this category.")
            print(f"You need to complete {RED}{category[2] - category[1]}{RESET} more units.")
        elif category[1] < category[2] and category[2] != category[3]:
            print(f"You have completed {category[1]} units in this category.")
            print(f"You need to complete between {RED}{category[2] - category[1]}{RESET} and {RED}{category[3] - category[1]}{RESET} more units.")
        else:
            print("Cannot compute :/")
        print()
    print("==================================================")
    print(f"{YELLOW}{BEME}{RESET}")
    print("==================================================")
    print(f"You have completed {overall_units_completed} units in total.")
    if overall_units_completed >= degree_units_required:
        print(f"You have completed all units required for the degree.")
    else:
        print(f"You need to complete {RED}{degree_units_required - overall_units_completed}{RESET} more units to complete the degree.")
        print(f"Of this, {RED}{compulsory_units_required - compulsory_units_completed}{RESET} are compulsory units.")
        print(f"This means you have {RED}{degree_units_required - overall_units_completed - (compulsory_units_required - compulsory_units_completed)}{RESET} units to complete using disciplinary or general electives.")
        print(f"This is roughly {RED}{(degree_units_required - overall_units_completed)/8/2}{RESET} more years.")
    print()

def recommend_courses(degree_data, semester):
    """
    Recommends courses based on the current progress of the degree.
    """
    courses = []
    categories = []

    for category in degree_data["Bachelor of Engineering (Honours) and Master of Engineering"]["unit_categories"]:
        if "unit_categories" in category:
            for sub_cat in category["unit_categories"]:
                categories.append(sub_cat["category"])
                for course in sub_cat["courses"]:
                    if not course["completed"]:
                        if (semester == 1 and course["semester_one"]) or (semester == 2 and course["semester_two"]):
                            courses.append((sub_cat["category"], course["code"], course["name"]))
        elif "courses" in category:
            categories.append(category["category"])
            for course in category["courses"]:
                if not course["completed"]:
                    if (semester == 1 and course["semester_one"]) or (semester == 2 and course["semester_two"]):
                        courses.append((category["category"], course["code"], course["name"]))
    
    print(f"\n{GREEN}RECOMMENDED COURSES{RESET}\n")
    print(f"The following courses are available to take in Semester {semester}:")
    for category in categories:
        print("==================================================")
        print(f"{BLUE}{category}{RESET}")
        print("==================================================")
        for course in courses:
            if course[0] == category:
                print(f"{course[1]} - {course[2]}")
        print()
    print()

def display_usage():
    print(f"Usage: python3 degree_manager.py [{HELP}] [{ADD}] [{HISTORY}] [{PROGRESS}] [{RECOMMEND} 1|2]")

def display_help():
    print()
    display_usage()
    print("Options:")
    print(f"{HELP}:  Show this help message and exit.")
    print(f"{ADD}:  Add a new course to the degree data.")
    print(f"{HISTORY}:  Show all completed courses so far.")
    print(f"{PROGRESS}:  Show progress of degree completion.")
    print(f"{RECOMMEND} 1|2:  Show recommended courses for the given semester.")
    print()

def main():
    degree_data = load_degree_data()

    if len(sys.argv) < 2:
        display_usage()
        return
    
    something_recognised = False

    if HELP in sys.argv:
        something_recognised = True
        display_help()
        return
    
    if ADD in sys.argv:
        something_recognised = True
        add = True
        while add:
            add_course(degree_data)
            add = input("Would you like to add another course? (y/n): ") == "y"
    
    if HISTORY in sys.argv:
        something_recognised = True
        display_course_history(degree_data)
    
    if PROGRESS in sys.argv:
        something_recognised = True
        display_progress(degree_data)
        recommend = input("Would you like to see recommended courses? (y/n): ") == "y"
        if recommend:
            semester = int(input("Enter the semester you would like to see courses for (1/2): "))
            recommend_courses(degree_data, semester)
    
    if RECOMMEND in sys.argv:
        # Get index of RECOMMEND argument.
        index = sys.argv.index(RECOMMEND)
        if sys.argv[index+1] != "1" and sys.argv[index+1] != "2":
            display_usage()
            return
        else:
            semester = int(sys.argv[index+1])
            something_recognised = True
            recommend_courses(degree_data, semester)
    
    if not something_recognised:
        display_usage()
        return

if __name__ == "__main__":
    main()