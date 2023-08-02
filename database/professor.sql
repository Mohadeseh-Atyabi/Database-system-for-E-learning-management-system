create table professor (
    national_code char(10),
    professor_no char(5),
    name_fa nvarchar(512),
    name_en varchar(512),
    father_name varchar(512),
    birth_date char(10),
    mobile char(11),
    department varchar(512),
    title varchar(512) check (title in ('استاد', 'استادیار','دانشیار')),
    primary key (professor_no),
    foreign key (national_code) references user(national_code)
);

-- add password columns
alter table professor add password varchar(512);

-- update password
update professor
set password = MD5(concat( national_code , upper(left(name_en, 1)) , lower(left(SUBSTRING_INDEX(name_en, ' - ', -1), 1))));

-- add email columns
alter table professor add email varchar(512);

-- update emails
update professor
set email = concat(lower(left(name_en, 1)),'.' , SUBSTRING_INDEX(name_en, ' - ', -1), '@aut.ac.ir');

-- ------------------ View classes ------------------
CREATE PROCEDURE professor_view_classes (in input_professor_no char(5))
begin
    select *
    from course c
    where c.professor_no = input_professor_no;
end;

-- ------------------ View students ------------------
CREATE PROCEDURE professor_view_students (in input_course_id char(8))
begin
    select t.student_no
    from takes t, course c
    where c.course_id = input_course_id and c.course_id = t.course_id;
end;

-- ------------------ View exams ------------------
CREATE PROCEDURE professor_view_exams (in course_id char(8))
begin
    select *
    from exam e
    where e.course_id = course_id;
end;

-- ------------------ View assignments ------------------
CREATE PROCEDURE professor_view_assignment (in course_id char(8))
begin
    select *
    from assignment a
    where a.course_id = course_id;
end;

-- ------------------ View grades of exam ------------------
CREATE PROCEDURE professor_view_exam_grades (in input_exam_id int)
begin
    select p.student_no , p.grade
    from participate p
    where p.exam_id = input_exam_id;
end;

-- ------------------ View answers for exam ------------------
CREATE PROCEDURE professor_view_exam_answer (in input_exam_id int)
begin
    select a.student_no , a.student_input, r.description
    from exam_student_answer a join questions_in_exam q join radio_button r
    where a.question_id = q.question_id and
          r.question_id = q.question_id and q.exam_id = input_exam_id;
end;

-- ------------------ View submissions ------------------
CREATE PROCEDURE professor_view_submission (in input_assignment_id int)
begin
    select q.question_id, s.description ,a.student_no, a.student_input
    from question_in_assignment q, short_answer s, assignment_student_answer a
    where a.question_id = q.question_id and
          input_assignment_id = q.assignment_id and
          s.question_id = q.question_id;
end;

-- ------------------ Score to submissions ------------------
create procedure score_submission (in input_assignment_id int, in input_student_no char(7), in input_grade numeric(4,2))
begin
    declare temp_end timestamp;
    declare result int default 0;

    select deadline into temp_end from assignment where assignment_id = input_assignment_id;

    if unix_timestamp(current_timestamp()) < unix_timestamp(temp_end) then
        set result = 1;

        update submission
        set grade = input_grade
        where assignment_id = input_assignment_id and student_no = input_student_no;
    end if;

    select result;
end;

-- ------------------ Create new assignment ------------------
CREATE PROCEDURE create_assignment (in input_course_id char(8), input_assignment_name nvarchar(512), input_deadline timestamp)
begin
	declare count int;
	insert into assignment(course_id, assignment_name, deadline ) values (input_course_id, input_assignment_name, input_deadline);

	-- To find the latest added assignment
	select max(assignment_id) into count from assignment;

	insert into submission(student_no, assignment_id) select student_no,count from takes where takes.course_id = input_course_id;
end;

-- ------------------ Create new exam ------------------
CREATE PROCEDURE create_exam (in input_course_id char(8), input_exam_name nvarchar(512), input_start_date timestamp,
                              input_end_date timestamp, input_duration int)
begin
    declare count int;
    insert into exam(course_id, exam_name, start_date, end_date, duration)
        values (input_course_id, input_exam_name , input_start_date, input_end_date, input_duration);

    -- To find the latest added exam
    select max(exam_id) into count from exam;

    insert into participate(student_no, exam_id) select student_no,count from takes where takes.course_id = input_course_id;
end;

-- ------------------ View_exam_grades ------------------
CREATE PROCEDURE view_exam_grades (in input_exam_id int)
begin
    declare temp_end timestamp;

    select end_date into temp_end from exam where exam_id = input_exam_id;

    if unix_timestamp(current_timestamp()) > unix_timestamp(temp_end) then
        select p.student_no, p.grade
        from participate p
        where p.exam_id = input_exam_id;
    end if;
end;