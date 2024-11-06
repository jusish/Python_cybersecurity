student_grades = {}

off = False

while not off:
    name = input("Enter name of the student: ")
    grade = input(f"Enter grades of {name}: ")
    student_grades[name] = grade
    print("Student added successfully")
    print(student_grades)
    add_another = input("Would you like to add another student? Y or N ").lower()
    if add_another == "y":
        pass
    else:
        off = True
