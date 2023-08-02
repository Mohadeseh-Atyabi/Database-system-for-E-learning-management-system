import user


def student_menu(username, password, connection):
    print("---------------------------")
    print("Please Enter one option : ")
    print("1) Change Password")
    print("2) View list of classes")
    print("3) View list of exams")
    print("4) View list of assignments")
    print("5) Take exam")
    print("6) View and answer to assignment")
    print("7) Review exam answers")
    print("8) View assignment answers")
    print("9) View grade in exam")
    print("10) Logout")
    option = int(input())
    print("---------------------------")
    if option == 1:
        user.change_password(username, password, 'S', connection)
    elif option == 2:
        view_classes(connection, username, password, True)
    elif option == 3:
        view_exams(connection, username, password, True)
    elif option == 4:
        view_assignments(connection, username, password, True)
    elif option == 5:
        take_exam(connection, username, password)
    elif option == 6:
        answer_assignment(connection, username, password)
    elif option == 7:
        view_exam_answer(connection, username, password)
    elif option == 8:
        view_assignment_answer(connection, username, password)
    elif option == 9:
        view_grade_in_exam(connection, username, password)
    elif option == 10:
        user.logout(username, connection)
        print("Bye!")
        user.login_menu(connection)
    else:
        print("Invalid Option!")
        student_menu(username, password, connection)


def view_classes(connection, username, password, get_back):
    myCursor = connection.cursor()
    args = [username]
    myCursor.callproc('student_view_classes', args)
    connection.commit()
    classes = []
    for result in myCursor.stored_results():
        classes = result.fetchall()
    print("List of classes (course, course_id):")
    for i in range(0, len(classes)):
        print(classes[i][0] + " " + classes[i][1] + "(" + str(i+1))
    connection.commit()
    if get_back:
        student_menu(username, password, connection)


def view_exams(connection, username, password, get_back):
    view_classes(connection, username, password, False)
    print("Enter course id:")
    course_id = input()
    myCursor = connection.cursor()
    args = [course_id]
    myCursor.callproc('student_view_exams', args)
    connection.commit()
    exams = []
    for result in myCursor.stored_results():
        exams = result.fetchall()
    connection.commit()
    if len(exams) == 0:
        print("No exam exists!")
        student_menu(username, password, connection)
    else:
        print("Exams like (id - name - start - end - duration):")
        for i in range(0, len(exams)):
            print(str(i + 1) + ") " + str(exams[i][0])
                  + ' - ' + str(exams[i][2])
                  + ' - ' + str(exams[i][3])
                  + ' - ' + str(exams[i][4])
                  + ' - ' + str(exams[i][5]))
    if get_back:
        student_menu(username, password, connection)


def view_assignments(connection, username, password, get_back):
    view_classes(connection, username, password, False)
    print("Enter course id:")
    course_id = input()
    myCursor = connection.cursor()
    args = [course_id]
    myCursor.callproc('student_view_assignment', args)
    connection.commit()
    assignments = []
    for result in myCursor.stored_results():
        assignments = result.fetchall()
    connection.commit()
    if len(assignments) == 0:
        print("No assignment exists!")
        student_menu(username, password, connection)
    else:
        print("Assignments like (id - name - deadline):")
        for i in range(0, len(assignments)):
            print(str(i + 1) + ") " + str(assignments[i][0])
                  + ' - ' + str(assignments[i][2])
                  + ' - ' + str(assignments[i][3]))
    if get_back:
        student_menu(username, password, connection)


def take_exam(connection, username, password):
    view_exams(connection, username, password, False)
    print("Enter quiz id :")
    q_id = int(input())
    myCursor = connection.cursor()
    res = ''
    args = [q_id, username]
    myCursor.callproc('take_exam', args)
    connection.commit()
    for result in myCursor.stored_results():
        res = result.fetchall()[0][0]
    if res == 'E':
        print("You have already taken this exam!")
        student_menu(username, password, connection)
    elif res == 'B':
        print("You can't enter exam before start time")
        student_menu(username, password, connection)
    elif res == 'A':
        print("You can't enter exam after end time")
        student_menu(username, password, connection)
    else:
        print("Don't panic, Take a Deep breath :)")
        show_exam(connection, username, password, q_id)


def show_exam(connection, username, password, exam_id):
    myCursor = connection.cursor()
    args = [exam_id, username]
    myCursor.callproc('view_exam_questions', args)
    connection.commit()
    questions = []
    for result in myCursor.stored_results():
        questions = result.fetchall()
    connection.commit()
    print("---------- Exam #" + str(exam_id) + " ----------")
    for i in range(0, len(questions)):
        print("Question #", str(i + 1))
        print('Description : ', str(questions[i][1]))
        print("1)", str(questions[i][2]))
        print("2)", str(questions[i][3]))
        print("3)", str(questions[i][4]))
        print("4)", str(questions[i][5]))
        print("Answer:")
        answer = int(input())
        myCursor = connection.cursor()
        res = ''
        args = [exam_id, questions[i][0], username, answer]
        myCursor.callproc('submit_exam_answer', args)
        connection.commit()
        for result in myCursor.stored_results():
            res = result.fetchall()[0][0]
        if res == 'S':
            myCursor1 = connection.cursor()
            args1 = [username, exam_id, questions[i][0], answer]
            myCursor1.callproc('update_quiz_score', args1)
            connection.commit()
            for result in myCursor1.stored_results():
                result.fetchall()
            connection.commit()
            print("submitted successfully")
        if res == 'A':
            print("Time is over!")
            student_menu(username, password, connection)

    student_menu(username, password, connection)


def answer_assignment(connection, username, password):
    view_assignments(connection, username, password, False)
    print("Enter assignment id:")
    a_id = int(input())
    print("Assignment questions:")
    myCursor = connection.cursor()
    args = [a_id]
    myCursor.callproc('get_assignment_questions', args)
    connection.commit()
    questions = []
    for result in myCursor.stored_results():
        questions = result.fetchall()
    connection.commit()
    print("Questions like (question_id - description):")
    for i in range(0, len(questions)):
        print(str(i + 1) + ") " + str(questions[i][0])
              + ' - ' + str(questions[i][1]))

    print("Do you want to answer ?(Y/N)")
    option = input()
    if option == 'Y':
        print("Enter Question id :")
        q_id = int(input())
        print("Enter Your answer :")
        answer = input()
        myCursor = connection.cursor()
        res = ''
        args = [a_id, q_id, username, answer]
        myCursor.callproc('student_update_submissions', args)
        connection.commit()
        res = ''
        for result in myCursor.stored_results():
            res = result.fetchall()[0][0]
        connection.commit()
        if res == 0:
            print("Answer updated")
        if res == 1:
            print("time is over!")
    student_menu(username, password, connection)


def view_exam_answer(connection, username, password):
    view_exams(connection, username, password, False)
    print("Enter exam id: ")
    e_id = int(input())
    myCursor = connection.cursor()
    args = [e_id, username]
    myCursor.callproc('review_exam', args)
    connection.commit()
    answers = []
    for result in myCursor.stored_results():
        answers = result.fetchall()
    connection.commit()
    if len(answers) == 0:
        print("You didn't take this exam or end time is left")
    else:
        print("Results like (question description - correct answer - your answer):")
        for i in range(0, len(answers)):
            print(str(i + 1) + ") " + str(answers[i][0])
                  + ' - ' + str(answers[i][1]) + ' - ' + str(answers[i][2]))
    student_menu(username, password, connection)


def view_assignment_answer(connection, username, password):
    view_assignments(connection, username, password, False)
    print("Enter assignment id: ")
    a_id = int(input())
    myCursor = connection.cursor()
    args = [a_id, username]
    myCursor.callproc('review_assignment', args)
    connection.commit()
    answers = []
    for result in myCursor.stored_results():
        answers = result.fetchall()
    connection.commit()
    if len(answers) == 0:
        print("You didn't submit anything or deadline is left")
    else:
        print("Results like (question description - correct answer - your answer):")
        for i in range(0, len(answers)):
            print(str(i + 1) + ") " + str(answers[i][0])
                  + ' - ' + str(answers[i][1]) + ' - ' + str(answers[i][2]))
    student_menu(username, password, connection)


def view_grade_in_exam(connection, username, password):
    view_exams(connection, username, password, False)
    print("Enter exam id: ")
    e_id = int(input())
    myCursor = connection.cursor()
    args = [e_id, username]
    myCursor.callproc('get_score', args)
    connection.commit()
    answers = []
    for result in myCursor.stored_results():
        answers = result.fetchall()
    connection.commit()
    print("Your grade is " + str(answers[0][0]))
    student_menu(username, password, connection)