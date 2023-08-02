import user


def professor_menu(username, password, connection):
    print("---------------------------")
    print("Please enter one option's number: ")
    print("1) Change password")
    print("2) View list of students")
    print("3) View list of classes")
    print("4) View list of exams")
    print("5) View list of assignments")
    print("6) Create new exam")
    print("7) Create new submission")
    print("8) Score submissions")
    print("9) View exam answers")
    print("10) View submission answers")
    print("11) View exam grades")
    print("12) Logout")
    option = int(input())
    print("---------------------------")
    if option == 1:
        user.change_password(username, password, 'P', connection)
    elif option == 2:
        view_students_list(connection, username, password)
    elif option == 3:
        view_classes(connection, username, password, True)
    elif option == 4:
        view_List_of_exams(connection, username, password, True)
    elif option == 5:
        view_list_of_assignments(connection, username, password, True)
    elif option == 6:
        create_new_exam(connection, username, password)
    elif option == 7:
        create_new_submission(connection, username, password)
    elif option == 8:
        score_submission(connection, username, password)
    elif option == 9:
        view_exam_answer(connection, username, password)
    elif option == 10:
        view_submission_answer(connection, username, password, True)
    elif option == 11:
        view_exam_grades(connection, username, password)
    elif option == 12:
        user.logout(username, connection)
        print("Bye !")
        user.login_menu(connection)
    else:
        print("Invalid Option!")
        professor_menu(username, password, connection)


def view_classes(connection, username, password, get_back):
    myCursor = connection.cursor()
    args = [username]
    myCursor.callproc('professor_view_classes', args)
    connection.commit()
    classes = []
    for result in myCursor.stored_results():
        classes = result.fetchall()
    print("List of classes (course, course_id):")
    for i in range(0, len(classes)):
        print(classes[i][0] + " " + classes[i][1] + "(" + str(i+1))
    connection.commit()
    if get_back:
        professor_menu(username, password, connection)


def view_students_list(connection, username, password):
    view_classes(connection, username, password, False)
    print("Enter course id:")
    course_id = input()
    myCursor = connection.cursor()
    args = [course_id]
    myCursor.callproc('professor_view_students', args)
    connection.commit()
    students = []
    for result in myCursor.stored_results():
        students = result.fetchall()
    connection.commit()
    print("Students :")
    for i in range(0, len(students)):
        print(str(i + 1) + ") " + students[i][0])
    professor_menu(username, password, connection)


def view_List_of_exams(connection, username, password, get_back):
    view_classes(connection, username, password, False)
    print("Please enter the course_id: ")
    course_id = input()
    myCursor = connection.cursor()
    args = [course_id]
    myCursor.callproc('professor_view_exams', args)
    connection.commit()
    exams = []
    for result in myCursor.stored_results():
        exams = result.fetchall()
    connection.commit()
    print("Exams like (name - id):")
    for i in range(0, len(exams)):
        print(str(i + 1) + ") " + str(exams[i][2]) + " - " + str(exams[i][0]))
    if get_back:
        if len(exams) > 0:
            print("Do you want add new questions? (Y/N) ")
            ans = input()
            if ans == "Y":
                print("Enter exam id:")
                exam_id = int(input())
                add_question_to_exam(connection, exam_id)
        professor_menu(username, password, connection)


def view_list_of_assignments(connection, username, password, get_back):
    view_classes(connection, username, password, False)
    print("Please enter the course_id: ")
    course_id = input()
    myCursor = connection.cursor()
    args = [course_id]
    myCursor.callproc('professor_view_assignment', args)
    connection.commit()
    assignments = []
    for result in myCursor.stored_results():
        assignments = result.fetchall()
    connection.commit()
    print("Assignments like (name - id):")
    for i in range(0, len(assignments)):
        print(str(i + 1) + ") " + str(assignments[i][2]) + " - " + str(assignments[i][0]))
    if get_back:
        if len(assignments) > 0:
            print("Do you want add new questions? (Y/N) ")
            ans = input()
            if ans == "Y":
                print("Enter submission id:")
                a_id = int(input())
                add_question_to_assignment(connection, a_id)
        professor_menu(username, password, connection)


def create_new_exam(connection, username, password):
    view_classes(connection, username, password, False)
    print("Please enter the course_id: ")
    course_id = input()
    print("Enter a name for exam:")
    name = input()
    print("Enter a start date (like YYYY-MM-DD HH:MM:SS) :")
    start_date = input()
    print("Enter an end date (like YYYY-MM-DD HH:MM:SS) :")
    end_date = input()
    print("Enter duration:")
    duration = int(input())
    myCursor = connection.cursor()
    args = [course_id, name, start_date, end_date, duration]
    myCursor.callproc('create_exam', args)
    connection.commit()
    for result in myCursor.stored_results():
        result.fetchall()
    connection.commit()
    print('Exam created successfully!')
    professor_menu(username, password, connection)


def create_new_submission(connection, username, password):
    view_classes(connection, username, password, False)
    print("Please enter the course_id: ")
    course_id = input()
    print("Enter a name for assignment:")
    name = input()
    print("Enter a deadline (like YYY-MM-DD HH:MM:SS) :")
    deadline = input()
    myCursor = connection.cursor()
    args = [course_id, name, deadline]
    myCursor.callproc('create_assignment', args)
    connection.commit()
    for result in myCursor.stored_results():
        result.fetchall()
    connection.commit()
    print('Assignment created successfully!')
    professor_menu(username, password, connection)


def add_question_to_exam(connection, exam_id):
    while True:
        print("Enter Description:")
        description = input()
        print("Enter option1:")
        option1 = input()
        print("Enter option2:")
        option2 = input()
        print("Enter option3:")
        option3 = input()
        print("Enter option4:")
        option4 = input()
        print("Enter correct answer:")
        correct_answer = int(input())
        myCursor = connection.cursor()
        args = [exam_id, description, option1, option2, option3, option4, correct_answer]
        myCursor.callproc('create_radio_button', args)
        connection.commit()
        for result in myCursor.stored_results():
            result.fetchall()
        connection.commit()
        print('Added successfully')
        print("Do you want to add new question ?(Y/N) ")
        option = input()
        if option == "N":
            break


def add_question_to_assignment(connection, a_id):
    while True:
        print("Enter Description:")
        description = input()
        print("Enter correct answer:")
        correct_answer = input()
        myCursor = connection.cursor()
        args = [a_id, description, correct_answer]
        myCursor.callproc('create_short_answer', args)
        connection.commit()
        for result in myCursor.stored_results():
            result.fetchall()
        connection.commit()
        print('Added successfully')
        print("Do you want to add new question ?(Y/N)")
        option = input()
        if option == "N":
            break


def view_submission_answer(connection, username, password, get_back):
    view_list_of_assignments(connection, username, password, False)
    print("Enter assignment id :")
    a_id = int(input())
    myCursor = connection.cursor()
    args = [a_id]
    myCursor.callproc('professor_view_submission', args)
    connection.commit()
    answers = []
    for result in myCursor.stored_results():
        answers = result.fetchall()
    connection.commit()
    print("Answers (description / student_id / answer) :")
    for i in range(0, len(answers)):
        print(str(i + 1) + ") " + str(answers[i][1]) + " - " + str(answers[i][2]) + " - " + str(answers[i][3]))
    if get_back:
        professor_menu(username, password, connection)


def view_exam_answer(connection, username, password):
    view_List_of_exams(connection, username, password, False)
    print("Enter exam id :")
    e_id = int(input())
    myCursor = connection.cursor()
    args = [e_id]
    myCursor.callproc('professor_view_exam_answer', args)
    connection.commit()
    answers = []
    for result in myCursor.stored_results():
        answers = result.fetchall()
    connection.commit()
    print("answers (description / student_id / answer) :")
    for i in range(0, len(answers)):
        print(str(i + 1) + ") " + str(answers[i][2]) + " - " + str(answers[i][0]) + " - " + str(answers[i][1]))
    professor_menu(username, password, connection)


def score_submission(connection, username, password):
    view_submission_answer(connection, username, password, False)
    print("Enter assignment id: ")
    a_id = int(input())
    print("Enter student_id: ")
    s_id = int(input())
    print("Enter grade: ")
    grade = float(input())
    myCursor = connection.cursor()
    res = ''
    args = [a_id, s_id, grade]
    myCursor.callproc('score_submission', args)
    connection.commit()
    for result in myCursor.stored_results():
        res = result.fetchall()[0][0]
    if res == 0:
        print("You can set grades after deadline!")
    else:
        for result in myCursor.stored_results():
            result.fetchall()
        connection.commit()
        print("Grade inserted successfully")
    print("Do you want to continue getting score? (Y/N)")
    ans = input()
    if ans == 'Y':
        score_submission(connection, username, password)
    elif ans == 'N':
        professor_menu(username, password, connection)


def view_exam_grades(connection, username, password):
    view_List_of_exams(connection, username, password, False)
    print("Enter exam id: ")
    e_id = int(input())
    myCursor = connection.cursor()
    args = [e_id]
    myCursor.callproc('view_exam_grades', args)
    connection.commit()
    grades = []
    for result in myCursor.stored_results():
        grades = result.fetchall()
    connection.commit()
    if len(grades) == 0:
        print("No grade exists!")
    else:
        print("Results like (student_id - grade):")
        for i in range(0, len(grades)):
            print(str(i + 1) + ") " + str(grades[i][0]) + ' - ' + str(grades[i][1]))
    professor_menu(username, password, connection)