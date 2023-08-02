create table student (
    national_code char(10),
    student_no char(7),
    name_fa nvarchar(512),
    name_en varchar(512),
    father_name varchar(512),
    birth_date char(10),
    mobile char(11),
    major nvarchar(512),
    primary key (student_no),
    foreign key (national_code) references user(national_code)
);

# add password column
alter table student add password varchar(512);
# update password
update student
set password = MD5(concat(national_code, upper(left(name_en, 1)), lower(left(SUBSTRING_INDEX(name_en, ' - ', -1), 1))));

# add email column
alter table student add email varchar(512);
# update emails
update student
set email = concat(lower(left(name_en, 1)), '.', SUBSTRING_INDEX(name_en, ' - ', -1), '@aut.ac.ir');

-- ------------------ View classes ------------------
CREATE PROCEDURE student_view_classes (in input_student_no char(7))
begin
    select course.course_id, course.course_name
    from takes , course
    where takes.student_no = input_student_no and takes.course_id = course.course_id;
end;

-- ------------------ View exams ------------------
CREATE PROCEDURE student_view_exams (in input_course_id char(8))
begin
    select *
    from exam e
    where e.course_id = input_course_id;
end;

-- ------------------ View assignments ------------------
CREATE PROCEDURE student_view_assignment (in input_course_id char(8))
begin
    select *
    from assignment a
    where a.course_id = input_course_id;
end;

-- ------------------ Take the exam ------------------
CREATE PROCEDURE take_exam (in input_exam_id int, in input_student_no char(7))
begin
    declare temp_start timestamp;
    declare temp_end timestamp;
    declare result char(1) default 'O';

    -- result = 'E' means user has already taken the exam
    select 'E' into result from participate as p where input_student_no = p.student_no and input_exam_id = p.exam_id
                                                       and p.date IS NOT NULL;

    select start_date into temp_start from exam e where e.exam_id = input_exam_id;
    select end_date into temp_end from exam e where e.exam_id = input_exam_id;

    -- result = 'B' means student tries enter exam before start date
    if unix_timestamp(current_timestamp()) < unix_timestamp(temp_start) then
        set result = 'B';
    end if;

    -- result = 'A' means student tries enter exam after end date
    if unix_timestamp(current_timestamp()) > unix_timestamp(temp_end) then
        set result = 'A';
    end if;

    select result;
end;

-- ------------------ View exam questions ------------------
CREATE PROCEDURE view_exam_questions (in input_exam_id int, in input_student_no char(7))
begin
    select r.question_id, r.description, r.choice1, r.choice2, r.choice3, r.choice4
    from questions_in_exam q , radio_button as r
    where q.question_id = r.question_id and q.exam_id = input_exam_id;

    update participate
    set date = current_timestamp()
    where participate.student_no = input_student_no;
end;

-- ------------------ Submit answer to exam ------------------
CREATE PROCEDURE submit_exam_answer (in input_exam_id int, in input_question_id int, in input_student_no char(7), in input_answer int)
begin
    declare temp_end timestamp;
    -- result 'S' means submitted successfully
    declare result char(1) default 'S';

    select end_date into temp_end from exam e where e.exam_id = input_exam_id;
    if unix_timestamp(current_timestamp()) > unix_timestamp(temp_end) then
        -- result 'A' means submitting after deadline
        set result = 'A';
    end if;

    if result = 'S' then
        insert into exam_student_answer(question_id, student_no, student_input) values (input_question_id, input_student_no, input_answer);
        -- call update_quiz_score(input_student_no,input_quiz_id,input_question_id,input_answer);
    end if;

    select result;
end;

-- ------------------ View list of questions in an assignment ------------------
CREATE PROCEDURE student_view_submission_questions (in input_student_no char(7), in input_assignment_id int)
begin
    select a.question_id, s.description, a.student_input
    from question_in_assignment q, assignment_student_answer a, short_answer as s
    where q.assignment_id = input_assignment_id
        and q.question_id = a.question_id
        and s.question_id = q.question_id
        and a.student_no = input_student_no;
end;

-- ------------------ Update answers to assignments ------------------
CREATE PROCEDURE student_update_submissions (in input_assignment_id int, in input_question_id int,
                                             in input_student_no char(7),in input_student_input nvarchar(512))
begin
		declare exist int default 0;
		declare temp_end timestamp;
		declare result int default 0;

        select deadline into temp_end from assignment where assignment_id = input_assignment_id;

		if unix_timestamp(current_timestamp()) > unix_timestamp(temp_end) then
		    -- result = 1 means deadline is passed
            set result = 1;
        end if;

		-- find whether user exists
		select 1 into exist from assignment_student_answer where student_no = input_student_no
		                                                     and question_id = input_question_id;

		if result = 0 then
		    -- Student didn't submit previously
            if exist = 0 then
                insert into assignment_student_answer(question_id, student_no, student_input,upload_date)
                    values (input_question_id, input_student_no, input_student_input,current_timestamp());
            end if;
            -- Student wants to update the answer
            if exist = 1 then
                update assignment_student_answer
                set student_input = input_student_input, upload_date = current_timestamp()
                where student_no = input_student_no and question_id = input_question_id;
            end if;
        end if;

		select result;
end;

-- ------------------ Get questions of assignment ------------------
create procedure get_assignment_questions(in input_assignment_id int)
begin
    select q.question_id , s.description
    from question_in_assignment as q, short_answer as s
    where q.question_id = s.question_id and q.assignment_id = input_assignment_id;
end;


-- ------------------ Get score in exam ------------------
create procedure get_score(in input_exam_id int, in input_student_no char(7))
begin
    declare temp_end timestamp;

    select end_date into temp_end from exam where exam_id = input_exam_id;

    if unix_timestamp(current_timestamp()) > unix_timestamp(temp_end) then
        select participate.grade
        from participate
        where exam_id = input_exam_id and student_no = input_student_no;
    end if;
end;

-- ------------------ Review answers in exam ------------------
create procedure review_exam(in input_exam_id int, in input_student_no char(7))
begin
    declare temp_end timestamp;

    select end_date into temp_end from exam where exam_id = input_exam_id;

    if unix_timestamp(current_timestamp()) > unix_timestamp(temp_end) then
        select r.description, r.correct_answer, e.student_input
        from radio_button r, exam_student_answer e
        where e.student_no = input_student_no and e.question_id = r.question_id
              and e.student_no = input_student_no;
    end if;
end;

-- ------------------ Review answers in assignment ------------------
create procedure review_assignment(in input_assignment_id int, in input_student_no char(7))
begin
    declare temp_end timestamp;

    select deadline into temp_end from assignment where assignment_id = input_assignment_id;

    if unix_timestamp(current_timestamp()) > unix_timestamp(temp_end) then
        select s.description, s.correct_answer, a.student_input
        from short_answer s, assignment_student_answer a
        where a.student_no = input_student_no and a.question_id = s.question_id
              and a.student_no = input_student_no;
    end if;
end;

-- ------------------ Update the score of student in exam ------------------
create procedure update_quiz_score(in input_student_no char(7), in input_exam_id int , in input_question_id int ,
                                   in input_student_answer int)
begin
    declare correct int;
    select correct_answer into correct from radio_button where radio_button.question_id = input_question_id;

    if correct = input_student_answer then
        update participate
        set grade = grade + 1
        where input_student_no = student_no and
              input_exam_id = exam_id;
    end if;
end;
