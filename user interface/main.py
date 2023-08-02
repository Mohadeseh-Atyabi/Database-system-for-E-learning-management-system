import user
import mysql.connector
from mysql.connector import Error

'''
student_user__test = "9231022"
student_pass_test = "1670072205Rk"

student_user__test = "9231001"
student_pass_test = "1696528178Ha"

student_user__test = "9231007"
student_pass_test = "8809363872Ar"

professor_user_test = "31002"
professor_pass_test = "3024641054Ab"
'''

if __name__ == "__main__":
    try:
        connection = mysql.connector.connect(host='localhost', database='DB', user='root')
        if connection.is_connected():
            print("connected to database successfully")
            print("Welcome!")
            user.login_menu(connection)
    except Error as error:
        print('Cannot communicate with Database! ** error : ')
        print(error)
        user.login_menu(connection)
