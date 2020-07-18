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
