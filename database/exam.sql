create table exam (
    exam_id int auto_increment,
    course_id char(8),
    exam_name nvarchar(512),
    start_date timestamp NULL,
    end_date timestamp NULL,
    duration integer,
    primary key (exam_id),
    foreign key (course_id) references course(course_id)
);

-- ------------------ Questions in exam ------------------
create table questions_in_exam(
    exam_id int,
    question_id int,
    primary key (exam_id, question_id),
    foreign key (question_id) references radio_button(question_id),
    foreign key (exam_id) references exam(exam_id)
);

-- ------------------ Students in exam ------------------
create table participate (
     student_no char(7),
     exam_id int,
     grade numeric(4,2) default 0.0,
     date timestamp,
     primary key (student_no, exam_id),
     foreign key (student_no) references student(student_no),
     foreign key (exam_id) references exam(exam_id)
);

-- ------------------ Answers of student in exam ------------------
create table exam_student_answer (
     question_id int,
     student_no char(7),
     student_input int,
     primary key (question_id, student_no),
     foreign key (question_id) references radio_button(question_id),
     foreign key (student_no) references student(student_no)
);

