create table Programm(
	id serial primary key,
	subject varchar(128)
);

create table Student(
	id serial primary key,
	fname varchar(20),
	lname varchar(40),
	login varchar(15),
	pass varchar(20),
	program_id int,
	student_no varchar(12),
	foreign key(program_id) references Programm(id)
);

create table Courses(
	id serial primary key,
	name varchar(256),
	program_id int,
	foreign key(program_id) references Programm(id)
);


create table Semester(
	id serial primary key,
	year int,
	semester_no int,
	mean decimal,
	student_id int,
	course_id int,
	foreign key(student_id) references Student(id),
	foreign key(course_id) references Courses(id)
);

create view students_program as
	select
		st.id, fname, lname, subject,
		program_id
	from student as st
	inner join programm as p on st.program_id=p.id;

create view courses_program as
	select
		c.id, name, subject, program_id
	from courses as c
	inner join programm as p on program_id=p.id;

create view semester_reports as
	select
		r.id, s.id as student_id, c.id as course_id,
		fname as first_name, lname as last_name,
		s.subject, name as course, semester_no, year,
		mean
	from semester as r
	inner join students_program as s on student_id=s.id
	inner join courses_program as c on course_id=c.id;
