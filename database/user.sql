create table user (
    national_code char(10) primary key
);

-- ------------------ Login user ------------------
create procedure login (in user_id char(7), password varchar(512))
begin
    declare result char(1) default 'N';

    if length(user_id) = 5 then
        select 'P' into result from professor p
                              where p.professor_no = user_id
                              and MD5(password) = p.password;
    end if;

    if length(user_id) = 7 then
        select 'S' into result from student s
                              where s.student_no = user_id
                              and MD5(password) = s.password;
    end if;

    if result = 'P' then
        insert into professor_log values (user_id, current_timestamp());
    end if;

    if result = 'S' then
        insert into student_log values (user_id, current_timestamp());
    end if;

    select result;
end;

-- ------------------ Logout user ------------------
create procedure logout (in user_id varchar(7))
begin
    if length(user_id) = 7 then
        delete from student_log where student_no = user_id;
    end if;

    if length(user_id) = 5 then
        delete from professor_log where professor_no = user_id;
    end if;

end;

-- ------------------ Change password ------------------
create procedure change_password (in user_id char(7), old_password varchar(512), new_password varchar(512))
begin
    declare result char(1) default 'E';

    if length(new_password) < 8  then
      set result = 'L';
    end if;

    if length(new_password) > 20  then
       set result = 'L';
    end if;

    if result != 'L' then
        if new_password REGEXP '[0-9]' and (new_password REGEXP '[a-z]' or new_password REGEXP '[A-Z]') then
            set result = 'S';
        end if;
    end if;

    if result = 'S' then
         if length(user_id) = 5 then
            update professor
            set password = MD5(new_password)
            where user_id = professor_no and password = MD5(old_password);
        end if;
        if length(user_id) = 7 then
            update student
            set password = MD5(new_password)
            where user_id = student_no and password = MD5(old_password);
        end if;
    end if;

    select result;
end;
