create table assignment (
    assignment_id int auto_increment,
    course_id char(8),
    assignment_name nvarchar(512),
    deadline timestamp,
    primary key (assignment_id),
    foreign key (course_id) references course(course_id)
);

-- ------------------ Answers of student in assignment ------------------
create table assignment_student_answer (
     question_id int,
     student_no char(7),
     student_input varchar(512),
     upload_date timestamp,
     primary key (question_id, student_no),
     foreign key (question_id) references short_answer(question_id),
     foreign key (student_no) references student(student_no)
);

-- ------------------ Students in assignment ------------------
create table submission (
     student_no char(7),
     assignment_id int,
     grade numeric(4,2),
     primary key (student_no, assignment_id),
     foreign key (student_no) references student(student_no),
     foreign key (assignment_id) references assignment(assignment_id)
);

-- ------------------ Questions in assignment ------------------
create table question_in_assignment (
    assignment_id int,
    question_id int,
    primary key (assignment_id, question_id),
    foreign key (question_id) references short_answer(question_id),
    foreign key (assignment_id) references assignment(assignment_id)
);