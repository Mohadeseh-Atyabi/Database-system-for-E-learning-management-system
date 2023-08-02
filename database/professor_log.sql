create table professor_log (
    professor_no char(5),
    entrance_date timestamp,
    primary key (professor_no),
    foreign key (professor_no) references professor(professor_no)
);
