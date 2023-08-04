# Database-system-for-E-learning-management-system
This project implements a database system for a university E-learning management system using Python and MySQL. This project aims to implement the database model, work with SQL directly and implement relationships, data management, and work with the implemented model from a separate user interface. To use the E-learning management system, we must have a list of students, professors and related items, including the courses offered by each professor and the courses taken by each student. For this purpose, along with the project form, there is an [excel file](https://github.com/Mohadeseh-Atyabi/Database-system-for-E-learning-management-system/files/12237827/DB-00-2-FinalPrjData.xlsx)
 containing several pages that contain the required data in persian.

 # Entities
- Student: The attributes for a student are national code, student number, first name, last name, father's name, birth date, phone number, and major.
- Professor: The attributes of a professor are similar to students with the difference that instead of student number, professor number is mentioned. Moreover, a professor doesn't have a major and has a department and title (assistant professor, associate professor, and professor) instead. Because of the common attributes between stdent and professor, we have a user entity which is the super entity for student and professor, and store the common attributes.
- Course: Each course has course id, course name, and professor's name as its attributes.
- Exam: The attributes of an exam are exam id, course id, exam name, start and end date, and duration.
- Assignments: The attributes of an assignment are assignment id, course id, assignment name, and deadline.
- Question: Here, we have two types of questions which are divided into radio button questions and short answer questions. For radio button questions, the attributes are question id, description, four choices, and correct answer. For short answer questions, the attributes are question id, description, and correct answer.
- Takes: This entity stores the information about which student contributes to which course. So, its attributes are course id and student number.
  
# Relations
- question_in_exam: Shows which questions are used in which exam
- question_in_assignment: Shows which questions are used in which assignment
- participate: Showa which student participates in which exam and what is the score
- exam_student_answer: Shows the student's answer to a question in an exam
- assignment_student_answer: Shows the student's answer to a question in an assignment
- submission: Shows the student's grade in an assignment

# Capabalities
- User (both student and professor)
  - Login
  - Logout
  - Change the password
  - View list of courses (for a professor, it is the list of courses to teach, and for a student, it is the list of taken courses)
- Professor
  - View the list of students for each class
  - View the list of exams and assignments for each course
  - Create new exams and assignments
  - View the answers to each exam or assignment by selecting them
  - Score each of the assignments
- Student
  - View the list of exams and assignments for each course
  - Enter an exam in the legal time
  - Answer each assignment and view their answers
# UI

# How to run
