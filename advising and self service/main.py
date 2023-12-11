def prereqDictionary(file_path):
  course_dict = {}

  with open(file_path, 'r') as file:
    for line in file:
      # Split the line into course and prerequisites using the "|" separator
      parts = line.strip().split('|')
      if len(parts) < 2:
        course = parts[0].strip()
        prerequisites = []
      else:
        # Extract course and prerequisites
        course = parts[0].strip()
        prerequisites_str = parts[1].strip()

        # Split prerequisites using comma and store in an array
        prerequisites = prerequisites_str.split(',')

        # Store in the dictionary
        course_dict[course] = prerequisites
  return course_dict


def add_or_edit_course(course_dict):
  user_choice = input(
      "Do you want to add a new course (Enter 'A'), edit an existing course (Enter 'B')? "
  ).upper()
  if user_choice == 'A':
    new_course = input("Enter the full name of the new course: ").strip()
    new_prerequisites = input(
        "Enter the prerequisites separated by commas (Enter full course names): "
    ).strip().split(',')  #split by commas
    course_dict[new_course] = new_prerequisites
  elif user_choice == 'B':
    existing_course = input(
        "Enter the name of full name of the course you want to edit: ").strip(
        )
    if existing_course in course_dict:
      print(
          f"Current prerequisites for {existing_course}: {', '.join(course_dict[existing_course])}"
      )
      edit_choice = input(
          "Do you want to add (A) or remove (B) prerequisites? ").upper()
      if edit_choice == 'A':
        new_prerequisites = input(
            "Enter the prerequisites to add, separated by commas: ").strip(
            ).split(',')
        course_dict[existing_course].extend(
            new_prerequisites)  #adds new course to course dictionary
      elif edit_choice == 'B':
        remove_prerequisites = input(
            "Enter the prerequisites to remove, separated by commas: ").strip(
            ).split(',')
        course_dict[existing_course] = [
            prereq for prereq in course_dict[existing_course]
            if prereq not in remove_prerequisites
        ]  #only prints wanted courses to file
      else:
        print(
            "Invalid choice. Please enter 'A' to add or 'B' to remove prerequisites."
        )
    else:
      print(f"Course '{existing_course}' not found in the dictionary.")
  # Write the updated information to 'CoursePrerequisites.txt'
  with open('CoursePrerequisites.txt', 'w') as file:
    for course, prerequisites in course_dict.items():
       file.write(f"{course}| {', '.join(prerequisites)}\n")

def rubrikDictionary(file_path):
  rubrik_dict = {}
  with open(file_path, 'r') as file:
    for line in file:
      # Split the line into course and prerequisites using the "|" separator
      parts = line.strip().split('|')
      if len(parts) < 2:
        course = parts[0].strip()
        credits = []
      else:
        # Extract course and prerequisites
        course = parts[0].strip()
        courseCred_str = parts[1].strip()

        # Split prerequisites using comma and store in an array
        credits = courseCred_str.split(',')
        # Store in the dictionary
        rubrik_dict[course] = credits
  return rubrik_dict


def find_matching_courses(course_dict, search_terms):
  matching_courses = set()
  for course, prerequisites in course_dict.items():
    if search_terms in prerequisites:
      matching_courses.add(course)
  if len(matching_courses) > 0:
    return matching_courses
  return "Course not found in dictionary"


def print_prerequisites(course_dict, course_name):
  if course_name in course_dict:
    prerequisites = course_dict[course_name]
    print(f"Prerequisites for {course_name} are:")
    for prerequisite in prerequisites:
      print(prerequisite)
  else:
    print(f"Course '{course_name}' not found in the dictionary.")


def course_teachers(file_path):
  course_teacher_dict = {}
  with open(file_path, 'r') as file:
    for line in file:
      # Split the line into course and teachers using the "|" separator
      parts = line.strip().split('|')
      # Extract course and teachers
      course = parts[0].strip()
      if len(parts) > 1:
        teachers_str = parts[1].strip()
        # Split teachers using '-' and store in an array
        teachers = teachers_str.split('-')
        # Store in the dictionary
        course_teacher_dict[course] = teachers
      else:
        # If there are no teachers, store an empty list
        course_teacher_dict[course] = []

  return course_teacher_dict


def print_course_teachers(course_dict, course_name):
  if course_name in course_dict:
    teachers = course_dict[course_name]
    print(f'Teachers for {course_name}:')
    if teachers:
      print(', '.join(teachers))
    else:
      print('No teachers assigned to this course')
  else:
    print(f"Course '{course_name}' not found in the dictionary.")


#=---------------------------GET TEACHER EMAIL
def make_employee_dict(file_path):
  employee_dict = {}
  with open(file_path, 'r') as file:
    for line in file:
      # Separate employee from position and email at '|'
      employee_info = line.strip().split('|')
      # Extract employee and information
      employee = employee_info[0].strip()

      if len(employee_info) > 1:
        information_str = employee_info[1].strip()

        # Store information in an array
        information = [info.strip() for info in information_str.split(',')]

        # Store in the dictionary
        employee_dict[employee] = information
      else:
        # If there is no information, store an empty list
        employee_dict[employee] = []
  return employee_dict


def get_employee_email(employee_dict, employee_name):
  if employee_name in employee_dict:
    information = employee_dict[employee_name]
    print(f'Information for {employee_name}:')
    if information:
      print(', '.join(information))
    else:
      print('No information available for this employee')
  else:
    print(f"Employee '{employee_name}' not found in the dictionary.")


#-----------------------ADD OR EDIT COURSE
course_dict = prereqDictionary('CoursePrerequisites.txt')
add_or_edit_course(course_dict)
print("\n\n")

#____________________Search what class have search class as a prequisite
#file_path = 'CoursePrerequisites.txt'
file_path = 'PrerequisitesClass.txt'
course_dict = prereqDictionary(file_path)
#search_terms = ['CSCI 136 Computer Science II']
#you enter the course youve done to check what courses have it as a prerequiste
search_terms = input(
    "To find what classes have a specific class as a prequisite, please enter the name of the desired class\nEnter abbreviated name (eg. CSCI 136 = Computer Science II):  "
)
matching_courses = find_matching_courses(course_dict, search_terms)
# Print the matching courses
if matching_courses == "Course not found in dictionary":
  print("Course not found in dictionary")
else:
  print(f"Courses that have {search_terms} as a prerequisite:")
  for course in matching_courses:
    print(course)

print("\n\n")
#---------------------------------TEST PREREQUISITES WHEN GIVEN A CLASS
#search_class = 'CSCI 135 Computer Science I'
file_path = 'SearchClass.txt'
course_dict = prereqDictionary(file_path)
search_class = input(
    "Please type the name of a course you want to see the prequisites for.\nEnter abbreviated name (e.g CSCI 136 = Computer Science II) : "
)
#print(f"The prerequisites for class {search_class} are: ")
print_prerequisites(course_dict, search_class)
print('\n\n')
#------------------TEST Teacher CLASS ASSIGNMENT TEXT
#file_path = 'ClassAssignments.txt'
teacher_dict = course_teachers('ClassAssignments.txt')
#for course, teachers in teacher_dict.items():
# print(f'{course}: {teachers}')
#--------------------find teacher
search_course = input(
    "Please type course you are searching teachers for: (Use course abbreviation eg. CSCI 135 = Computer Science I)\nEnter course here: "
)
search_course = search_course.upper()
print_course_teachers(teacher_dict, search_course)
print('\n\n')
#----------------------------------SEARCH FOR TEACHER EMAIL
search_teacher = input(
    "Would you like to search for a teacher's email?\nEnter A for yes, B for no\nEnter choice here: "
).upper()
if search_teacher == 'A':
  employee_dict = make_employee_dict('EmployeeInfo.txt')
  find_teacher = input("Please type the teacher's name: ")
  get_employee_email(employee_dict, find_teacher)

#-----------------------------COURSE CALENDER
#print(
#    "Here is a list of major upcoming events for Spring 2024:\nMarch 25th - Fall 2024 Registration Begins\nApril 5th - Last day to Withdraw from Spring 2024 Course\nApril 12th - Last day to apply for Spring 2024 Graduation\nApril 23rd to 25th - Final Examinations for Prospective Spring 2024 Graduates\nApril 26th - Formal Classses Finish\nApril 29th to May 8th - Final Examinations\n\n"
#)
#academic_calendar_link = "https://howard.edu/sites/home.howard.edu/files/2023-04/2023-2024AcademicCalendar.pdf"
#print(f"Click the following link to view the full academic calendar: {academic_calendar_link}")
