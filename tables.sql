CREATE TABLE Divers (
	id serial PRIMARY KEY,
	email VARCHAR(100) not null,
	hashpass CHAR(40) not null
);