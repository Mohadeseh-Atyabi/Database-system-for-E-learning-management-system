create table course (
    course_id char(8),
    course_name nvarchar(512),
    professor_no char(5),
    foreign key (professor_no) references professor(professor_no),
    primary key (course_id)
);

-- ------------------ View list of courses of a user ------------------
CREATE PROCEDURE view_course (in input_user_id char(8))
begin
    if length(input_user_id) = 5 then
         SELECT course_id  FROM course WHERE professor_no = input_user_id;
    end if;

    if length(input_user_id) = 7 then
        SELECT course_id  FROM takes WHERE student_no = input_user_id;
    end if;
end;

