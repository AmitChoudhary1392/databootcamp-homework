--DATA ANALYSIS QUERIES
--------------------------------------------
--List the following details of each employee: employee number, last name, first name, gender, and salary.

SELECT e.emp_no, e.last_name, e.first_name, e.gender, s.salary 
FROM employees AS e
INNER JOIN  salary AS s ON s.emp_no=e.emp_no;
------------------------------------------------------------------------------------------------------------

--List employees who were hired in 1986.

SELECT * FROM employees WHERE hire_date BETWEEN '1986-01-01' and '1987-01-01';
-------------------------------------------------------------------------------------------------------------

--List the manager of each department with the following information: department number,
--department name, the manager's employee number, last name, first name, and start and end employment dates.

SELECT d.dept_no, d.dept_name,e.emp_no, e.last_name, e.first_name,dm.FROM_date, dm.to_date 
FROM employees AS e
INNER JOIN  dept_manager AS dm ON dm.emp_no=e.emp_no
INNER JOIN departments AS d ON dm.dept_no = d.dept_no ;
--------------------------------------------------------------------------------------------------------------

--List the department of each employee with the following information: 
--employee number, last name, first name, and department name

SELECT e.emp_no, e.last_name, e.first_name, de.dept_no, d.dept_name
FROM employees as e
INNER JOIN dept_emp as de ON e.emp_no=de.emp_no
INNER JOIN departments as d ON de.dept_no= d.dept_no;
---------------------------------------------------------------------------------------------------------------

--List all employees whose first name is "Hercules" and last names begin with "B."

SELECT e.first_name, e.last_name
FROM employees as e
WHERE e.first_name='Hercules' AND e.last_name LIKE 'B%';
---------------------------------------------------------------------------------------------------------------

--List all employees in the Sales department, 
--including their employee number, last name, first name, and department name.
		
		---- using SUBQUERIES
SELECT e.emp_no, e.last_name, e.first_name,(SELECT d.dept_name FROM departments as d WHERE d.dept_name='Sales') AS dept_name
FROM employees AS e
WHERE e.emp_no IN (
		SELECT de.emp_no
		FROM dept_emp as de
		WHERE de.dept_no IN (
							SELECT d.dept_no
							FROM departments as d
							WHERE d.dept_name='Sales')
					);
					
	----using INNER JOIN
SELECT e.emp_no,e.last_name, e.first_name, d.dept_name FROM employees AS e 
INNER JOIN dept_emp AS de ON de.emp_no=e.emp_no
INNER JOIN departments AS d ON de.dept_no = d.dept_no WHERE dept_name='Sales';
------------------------------------------------------------------------------------------------------------------

--List all employees in the Sales and Development departments, including their employee number, last name, first name, 
--and department name.

		-----Using INNER JOIN
SELECT e.emp_no,e.last_name, e.first_name, d.dept_name FROM employees AS e 
INNER JOIN dept_emp AS de ON de.emp_no=e.emp_no
INNER JOIN departments AS d ON de.dept_no = d.dept_no WHERE dept_name IN ('Sales','Development');
-------------------------------------------------------------------------------------------------------------------

--In descending order, list the frequency count of employee last names, 
--i.e., how many employees share each last name.

SELECT e.last_name, COUNT(e.last_name)
FROM employees as e
GROUP BY e.last_name
ORDER BY COUNT(e.last_name) DESC;
---------------------------------------------------------------------------------------------------------------------