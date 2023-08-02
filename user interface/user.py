import sys
import student
import professor


def login_menu(connection):
    login_state = False
    while not login_state:
        print("---------------------------")
        print("Please enter your username or enter E to exit: ")
        username = input()
        if username == 'E':
            sys.exit()
        print("Please enter your password: ")
        password = input()
        user_type = login(connection, username, password)
        if user_type == 'P' or user_type == 'S':
            print("Login successful")
            login_state = True
            if user_type == 'P':
                professor.professor_menu(username, password, connection)
            elif user_type == 'S':
                student.student_menu(username, password, connection)
        else:
            print("Your username or password in sot valid!")


def login(connection, username, password):
    myCursor = connection.cursor()
    args = [username, password]
    myCursor.callproc('login', args)
    connection.commit()
    user_type = ''
    for result in myCursor.stored_results():
        user_type = result.fetchall()[0][0]
    connection.commit()
    return user_type


def change_password(username, password, user_type, connection):
    print("Please Enter your old password:")
    old_password = input()
    print("Please Enter your new password:")
    new_password = input()

    if password == old_password:
        myCursor = connection.cursor()
        args = [username, old_password, new_password]
        myCursor.callproc('change_password', args)
        connection.commit()
        change_result = 0
        for result in myCursor.stored_results():
            change_result = result.fetchall()[0][0]
        connection.commit()
        if change_result == 'L':
            print("Length of password must be between 8 and 20")
        elif change_result == 'E':
            print("Password must contain both letters and numbers")
        elif change_result == 'S':
            print("Password updates successfully")
    else:
        print("Old password is not correct!")

    if user_type == 'P':
        professor.professor_menu(username, password, connection)
    elif user_type == 'S':
        student.student_menu(username, password, connection)


def logout(username, connection):
    myCursor = connection.cursor()
    args = [username]
    myCursor.callproc('logout', args)
    connection.commit()