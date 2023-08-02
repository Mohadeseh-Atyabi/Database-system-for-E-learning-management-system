create table student_log (
    student_no char(7),
    entrance_date timestamp,
    primary key (student_no),
    foreign key (student_no) references student(student_no)
);
