DROP TABLE IF EXISTS departments, dept_emp, dept_manager, employees, salary, titles;

-- Create tables with required data fields:

CREATE TABLE departments (
	dept_no VARCHAR NOT NULL PRIMARY KEY, 
	dept_name VARCHAR(30) Not Null
);

CREATE TABLE employees (
	emp_no		INTEGER NOT NULL PRIMARY KEY,
	birth_date	DATE	NOT NULL,
	first_name	VARCHAR(30)	NOT NULL,
	last_name	VARCHAR(30),
	gender		VARCHAR(5)	NOT NULL,
	hire_date	DATE	NOT NULL
	
);

CREATE TABLE dept_emp (
	emp_no	INTEGER NOT NULL,
	dept_no	VARCHAR(15)	NOT NULL,
	from_date DATE NOT NULL,
	to_date	DATE NOT NULL,
	PRIMARY KEY (emp_no, dept_no),
	FOREIGN KEY (emp_no)	REFERENCES employees(emp_no),
	FOREIGN KEY (dept_no)	REFERENCES departments(dept_no)
);

CREATE TABLE dept_manager (
	dept_no VARCHAR(15)	NOT NULL,
	emp_no	INTEGER	NOT NULL,
	from_date	DATE	NOT NULL,
	to_date	DATE,
	PRIMARY KEY (dept_no, emp_no),
	FOREIGN KEY (dept_no) REFERENCES departments(dept_no),
	FOREIGN KEY (emp_no) REFERENCES employees(emp_no)

);


CREATE TABLE titles (
	emp_no INTEGER	NOT NULL,
	title VARCHAR (30)	NOT NULL,
	from_date	DATE	NOT NULL,
	to_date	DATE,
	PRIMARY KEY (emp_no, title, from_date, to_date),
	FOREIGN KEY (emp_no)	REFERENCES employees(emp_no)
);

CREATE TABLE salary(
	emp_no	INTEGER	NOT NULL	PRIMARY KEY,
	salary	INTEGER	NOT NULL	,
	from_date	DATE	NOT NULL,
	to_date	DATE	NOT NULL,
	FOREIGN KEY (emp_no)	REFERENCES employees(emp_no)
);

--Import data into tables

--Query data to check

SELECT * FROM departments;
SELECT * FROM dept_emp;
SELECT * FROM dept_manager;
SELECT * FROM employees;
SELECT * FROM salary;
SELECT * FROM titles;