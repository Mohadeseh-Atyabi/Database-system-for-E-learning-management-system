create table radio_button (
     question_id int auto_increment,
     description nvarchar(512),
     choice1 nvarchar(512),
     choice2 nvarchar(512),
     choice3 nvarchar(512),
     choice4 nvarchar(512),
     correct_answer int,
     primary key (question_id)
);

create table short_answer (
    question_id int auto_increment,
    description nvarchar(512),
    correct_answer nvarchar(512),
    primary key (question_id)
);

-- ------------------ Create new radio button question ------------------
CREATE PROCEDURE create_radio_button ( in input_exam_id int, in input_description nvarchar(512),
                                           in input_choice1 nvarchar(512), in input_choice2 nvarchar(512),
                                           in input_choice3 nvarchar(512), in input_choice4 nvarchar(512),
                                           in input_correct_answer nvarchar(512))
begin
    declare temp_id int default 0;

    insert into radio_button(description, choice1, choice2, choice3, choice4, correct_answer)
        values (input_description, input_choice1, input_choice2, input_choice3, input_choice4, input_correct_answer);

    -- Get the id of the inserted question
    select max(question_id) into temp_id from radio_button;

    insert into questions_in_exam(exam_id, question_id) values (input_exam_id, temp_id);
end;

-- ------------------ Create new short answer question ------------------
CREATE PROCEDURE create_short_answer (in input_assignment_id int, in input_description nvarchar(512),
                                      in input_correct_answer nvarchar(512))
begin
    declare temp_id int default 0;

    insert into short_answer(description,correct_answer) values (input_description,input_correct_answer);

    -- Get the id of the inserted question
    select max(question_id) into temp_id from short_answer;

    insert into question_in_assignment(assignment_id, question_id) values (input_assignment_id,temp_id);
end;