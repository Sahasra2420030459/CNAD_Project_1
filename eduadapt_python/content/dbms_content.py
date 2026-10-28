"""
Database Management Systems (DBMS) Curriculum for EduAdapt-AI
Contains full structured content for Easy, Medium, and Complex levels.
Uses a consistent University Schema (students, departments, courses, enrollments).
"""

DBMS_DATA = {
    'id': 'dbms',
    'title': 'Database Management Systems',
    'badge_color': 'success',
    'icon': 'bi-database',
    'short_summary': 'Master relational database architecture, relational algebra, SQL, normalization, and ACID concurrency.',
    'description': 'A comprehensive curriculum from database fundamentals, schemas, keys, and relational algebra to complex SQL joins, subqueries, normalization (1NF through BCNF), and distributed transactions.',
    'difficulty': 'Beginner to Advanced',
    'levels': {
        'easy': {
            'level_number': 1,
            'name': 'Easy (Level 1 - Foundational Relational Models)',
            'description': 'DBMS architectures, relational concepts, keys, ER diagrams, integrity constraints, and SQL DDL commands.',
            'topics': [
                {
                    'id': 'dbms-intro-arch',
                    'title': '1. Introduction to DBMS & 3-Schema Architecture',
                    'read_time': '9 min',
                    'summary': 'Understand why DBMS replaced file processing systems and explore the ANSI/SPARC 3-tier schema architecture.',
                    'concept': """A Database Management System (DBMS) is specialized system software designed to define, construct, manipulate, and share relational data among multiple users and applications.

The ANSI/SPARC 3-Schema Architecture provides data independence:
1. **Physical / Internal Level**: Describes how data is physically stored on disk (block structures, indexes, hashing).
2. **Logical / Conceptual Level**: Describes what data is stored in the database and the relationships between entities (tables, primary/foreign keys). Independent of physical disk storage.
3. **External / View Level**: Describes individual user views. Different departments or users see customized slices of data while hiding sensitive columns.

**Data Independence**:
- Physical Data Independence: Ability to modify internal disk storage without altering conceptual schemas.
- Logical Data Independence: Ability to modify conceptual schemas without altering external user views.""",
                    'syntax': """-- Physical Level: B-Tree Indexes on Disk Blocks
-- Conceptual Level: Tables, Columns, Constraints
-- External Level: Views tailored for end-users
""",
                    'code_example': """-- Conceptual Level Schema Definition
-- Consistent University Schema
CREATE TABLE departments (
    dept_id VARCHAR(10) PRIMARY KEY,
    dept_name VARCHAR(100) NOT NULL,
    building VARCHAR(50),
    budget NUMERIC(12, 2)
);

-- Inspect table metadata
DESCRIBE departments;
""",
                    'expected_output': """Query OK, 0 rows affected (0.02 sec)
+-----------+---------------+------+-----+---------+-------+
| Field     | Type          | Null | Key | Default | Extra |
+-----------+---------------+------+-----+---------+-------+
| dept_id   | varchar(10)   | NO   | PRI | NULL    |       |
| dept_name | varchar(100)  | NO   |     | NULL    |       |
| building  | varchar(50)   | YES  |     | NULL    |       |
| budget    | decimal(12,2) | YES  |     | NULL    |       |
+-----------+---------------+------+-----+---------+-------+
""",
                    'common_mistakes': 'Confusing logical data independence with physical data independence. Physical data independence insulates against disk hardware changes; logical protects views against schema evolution.',
                    'practice_question': 'Which level of the 3-schema architecture defines the end-user perspectives and security views? (Answer: The External or View Level).'
                },
                {
                    'id': 'dbms-relational-model',
                    'title': '2. Relational Model Concepts: Relations, Tuples & Domains',
                    'read_time': '9 min',
                    'summary': 'Learn the mathematical foundations of E.F. Codd relational model, relations, tuples, and atomic domains.',
                    'concept': """Formulated by Edgar F. Codd in 1970, the Relational Model represents data as a collection of two-dimensional tables called **Relations**.

Formal Terminology vs Practical SQL:
- **Relation** = Table
- **Tuple** = Row / Record
- **Attribute** = Column / Field
- **Domain** = Set of permitted atomic values for an attribute (e.g. data type and range)
- **Degree** = Number of attributes (columns) in a relation
- **Cardinality** = Number of tuples (rows) in a relation

Rule of Atomicity: Every cell in a relational table must contain a single, indivisible (atomic) value. Multivalued or nested attributes violate the relational model.""",
                    'syntax': """RelationName(Attribute1: Domain1, Attribute2: Domain2, ...)
Degree = count(Attributes)
Cardinality = count(Tuples)
""",
                    'code_example': """-- Relation: students (Degree = 5)
CREATE TABLE students (
    student_id VARCHAR(12) PRIMARY KEY,
    full_name VARCHAR(100) NOT NULL,
    email VARCHAR(120) UNIQUE NOT NULL,
    department_id VARCHAR(10),
    gpa NUMERIC(3, 2)
);

-- Cardinality initially = 0 tuples
SELECT COUNT(*) AS cardinality, 5 AS degree FROM students;
""",
                    'expected_output': """+-------------+--------+
| cardinality | degree |
+-------------+--------+
|           0 |      5 |
+-------------+--------+
""",
                    'common_mistakes': 'Storing comma-separated values in a single column (e.g. `phone_numbers = "123, 456"`). This violates first normal form and relational atomicity.',
                    'practice_question': 'In relational database theory, what is the term used to describe the number of rows in a relation? (Answer: Cardinality).'
                },
                {
                    'id': 'dbms-vs-files',
                    'title': '3. DBMS vs Traditional File Systems',
                    'read_time': '8 min',
                    'summary': 'Analyze why flat-file data storage fails for concurrent, mission-critical multi-user systems.',
                    'concept': """Prior to DBMS, organizations stored data in flat operating system files (e.g. CSVs, raw binaries) processed by custom application code.

Major Drawbacks of File Systems Solved by DBMS:
1. **Data Redundancy & Inconsistency**: The same student address stored across multiple files leads to conflicting updates.
2. **Difficulty Accessing Data**: Ad-hoc questions require writing brand new application code rather than declarative SQL.
3. **Data Isolation**: Data scattered across different files and formats.
4. **Integrity Problems**: Constraints must be coded manually in every application program.
5. **Atomicity & Concurrency Anomalies**: A crash during a funds transfer leaves money deducted from one account without deposit in the other.
6. **Security & Access Control**: OS file permissions cannot enforce row- or column-level visibility.""",
                    'syntax': """-- DBMS solves redundancy via relational normalization and foreign key constraints
""",
                    'code_example': """-- Demonstrating declarative constraints in SQL
CREATE TABLE courses (
    course_id VARCHAR(10) PRIMARY KEY,
    course_title VARCHAR(100) NOT NULL,
    department_id VARCHAR(10) NOT NULL,
    credits INT CHECK (credits BETWEEN 1 AND 6),
    FOREIGN KEY (department_id) REFERENCES departments(dept_id)
);
""",
                    'expected_output': """Query OK, 0 rows affected (0.02 sec)
""",
                    'common_mistakes': 'Assuming flat files are sufficient for multi-user transactional writes. Without concurrency control, race conditions overwrite and corrupt file data.',
                    'practice_question': 'Which property guarantees that all operations in a database transaction complete successfully or none do? (Answer: Atomicity).'
                },
                {
                    'id': 'dbms-keys',
                    'title': '4. Database Keys: Super, Candidate, Primary & Foreign Keys',
                    'read_time': '11 min',
                    'summary': 'Master the hierarchy of database keys, candidate selection, surrogate keys, and foreign key references.',
                    'concept': """Keys are fundamental mechanisms to identify tuples and establish relationships between relations:
- **Super Key**: Any set of one or more attributes that uniquely identifies a tuple in a relation.
- **Candidate Key**: A minimal super key (no proper subset is a super key). A table can have multiple candidate keys.
- **Primary Key**: The specific candidate key chosen by the database architect to uniquely identify rows. Cannot be `NULL`.
- **Alternate Key**: Any candidate key not chosen as the primary key (enforced using `UNIQUE NOT NULL`).
- **Foreign Key**: An attribute in a relation that references the primary key of another relation, enforcing referential integrity.""",
                    'syntax': """-- Primary Key and Foreign Key constraints
ALTER TABLE enrollments 
ADD CONSTRAINT fk_enrollment_student 
FOREIGN KEY (student_id) REFERENCES students(student_id);
""",
                    'code_example': """-- Demonstrating Primary Key and Foreign Key definition
CREATE TABLE enrollments (
    enrollment_id INT PRIMARY KEY,
    student_id VARCHAR(12) NOT NULL,
    course_id VARCHAR(10) NOT NULL,
    term VARCHAR(20) NOT NULL,
    grade VARCHAR(2),
    CONSTRAINT fk_stu FOREIGN KEY (student_id) REFERENCES students(student_id),
    CONSTRAINT fk_crs FOREIGN KEY (course_id) REFERENCES courses(course_id),
    CONSTRAINT uq_enrollment UNIQUE (student_id, course_id, term)
);
""",
                    'expected_output': """Query OK, 0 rows affected (0.03 sec)
""",
                    'common_mistakes': 'Assuming a Primary Key can contain `NULL` values. By relational definition, a Primary Key must be unique and non-null.',
                    'practice_question': 'What is the definition of a Candidate Key? (Answer: A minimal super key that has no proper subset capable of uniquely identifying a tuple).'
                },
                {
                    'id': 'dbms-er-modeling',
                    'title': '5. ER Modeling: Entities, Attributes & Cardinality Ratios',
                    'read_time': '10 min',
                    'summary': 'Design conceptual database models using Peter Chen ER notation, cardinality ratios (1:1, 1:N, M:N), and weak entities.',
                    'concept': """Entity-Relationship (ER) modeling diagrams real-world domains into conceptual database schemas before writing physical SQL tables.

Key ER Elements:
- **Entity**: A real-world object distinguishable from others (represented by a rectangle).
- **Attribute**: Properties of an entity (represented by an ellipse).
  - Simple vs Composite (e.g. `full_name` decomposed into `first_name`, `last_name`).
  - Single-valued vs Multi-valued (double ellipse, e.g. `phone_numbers`).
  - Derived (dashed ellipse, e.g. `age` derived from `birth_date`).
- **Relationship**: Association between entities (represented by a diamond).
- **Cardinality Ratios**:
  - One-to-One (1:1): Dean manages Department.
  - One-to-Many (1:N): Department employs Professors.
  - Many-to-Many (M:N): Students enroll in Courses (requires a junction/associative table in relational implementations!).""",
                    'syntax': """-- Mapping M:N relationship to relational junction table
-- Students (M) <--- Enrollments ---> (N) Courses
""",
                    'code_example': """-- Junction table resolving Many-to-Many relationship
-- A student has many courses, a course has many students
SELECT 
    'Students' AS Entity_A, 
    'Courses' AS Entity_B, 
    'Many-to-Many (M:N)' AS Relationship_Type,
    'enrollments table with composite foreign keys' AS Relational_Solution;
""",
                    'expected_output': """+----------+----------+-------------------+----------------------------------------------+
| Entity_A | Entity_B | Relationship_Type | Relational_Solution                          |
+----------+----------+-------------------+----------------------------------------------+
| Students | Courses  | Many-to-Many (M:N)| enrollments table with composite foreign keys|
+----------+----------+-------------------+----------------------------------------------+
""",
                    'common_mistakes': 'Attempting to implement a Many-to-Many (M:N) relationship directly in a single table without an intermediate junction table.',
                    'practice_question': 'How is a Many-to-Many relationship between two entities implemented in a relational database? (Answer: By creating an intermediate junction / associative table with foreign keys referencing both entities).'
                },
                {
                    'id': 'dbms-integrity-constraints',
                    'title': '6. Integrity Constraints & Referential Actions',
                    'read_time': '10 min',
                    'summary': 'Enforce domain, entity, and referential integrity with ON DELETE CASCADE and ON DELETE SET NULL.',
                    'concept': """Integrity constraints guard the database against accidental damage and maintain data consistency:
1. **Domain Integrity**: Attribute values must adhere to their data type, length, and `CHECK` predicates.
2. **Entity Integrity**: Primary keys must be unique and cannot contain `NULL`.
3. **Referential Integrity**: A foreign key value must either match an existing primary key in the referenced relation or be `NULL`.

Referential Actions on Parent Deletion/Update:
- `ON DELETE RESTRICT / NO ACTION`: Rejects the parent deletion if matching child rows exist.
- `ON DELETE CASCADE`: Automatically deletes all child rows when the parent row is deleted.
- `ON DELETE SET NULL`: Sets child foreign key columns to `NULL` when the parent is deleted.""",
                    'syntax': """FOREIGN KEY (dept_id) REFERENCES departments(dept_id)
    ON DELETE CASCADE
    ON UPDATE CASCADE
""",
                    'code_example': """CREATE TABLE audit_logs (
    log_id INT PRIMARY KEY,
    student_id VARCHAR(12),
    action VARCHAR(50),
    FOREIGN KEY (student_id) REFERENCES students(student_id)
        ON DELETE SET NULL
);
""",
                    'expected_output': """Query OK, 0 rows affected (0.02 sec)
""",
                    'common_mistakes': 'Using `ON DELETE CASCADE` blindly on critical audit tables, which accidentally wipes out historical compliance logs when a user account is deleted.',
                    'practice_question': 'What does `ON DELETE CASCADE` do when a referenced parent row is deleted? (Answer: It automatically deletes all corresponding child rows in the foreign key table).'
                },
                {
                    'id': 'dbms-relational-algebra',
                    'title': '7. Relational Algebra Fundamentals: Select, Project & Joins',
                    'read_time': '11 min',
                    'summary': 'Understand the procedural query language underpinning SQL: Select (σ), Project (π), Cartesian Product (×), and Natural Join (⨝).',
                    'concept': """Relational Algebra is a theoretical procedural query language that takes one or two relations as input and produces a new relation as output. Query optimizers translate declarative SQL into relational algebra trees to find the most efficient execution plan.

Fundamental Operators:
1. **Select ($\\sigma$)**: Filters rows satisfying a predicate $\\sigma_{gpa \\ge 3.5}(Students)$ $\\rightarrow$ Equivalent to SQL `WHERE`.
2. **Project ($\\pi$)**: Filters columns, eliminating duplicate tuples $\\pi_{full\\_name, email}(Students)$ $\\rightarrow$ Equivalent to SQL `SELECT column1, column2`.
3. **Cartesian Product ($\\times$)**: Combines all tuples from two relations.
4. **Natural Join ($\\bowtie$)**: Combines tuples having identical values on shared attributes.
5. **Set Operators**: Union ($\\cup$), Set Difference ($-$), Intersection ($\\cap$).""",
                    'syntax': """-- Relational Algebra: π_{full_name, gpa}(σ_{gpa >= 3.5}(students))
-- SQL Equivalence:
SELECT full_name, gpa FROM students WHERE gpa >= 3.5;
""",
                    'code_example': """-- Relational Algebra translation in SQL
SELECT full_name, gpa 
FROM students 
WHERE gpa >= 3.5;
""",
                    'expected_output': """+-----------+------+
| full_name | gpa  |
+-----------+------+
| Marcus V  | 3.85 |
| Elena R   | 3.92 |
+-----------+------+
""",
                    'common_mistakes': 'Confusing the relational algebra Select operator ($\\sigma$, row filtering) with the SQL `SELECT` clause (which actually maps to the Project operator $\\pi$).',
                    'practice_question': 'Which relational algebra operator selects specific columns and discards others? (Answer: Project / $\\pi$).'
                },
                {
                    'id': 'dbms-sql-ddl',
                    'title': '8. SQL Data Definition Language (DDL): CREATE, ALTER & DROP',
                    'read_time': '10 min',
                    'summary': 'Manage database objects using DDL statements: CREATE TABLE, ALTER TABLE, DROP TABLE, and TRUNCATE.',
                    'concept': """Data Definition Language (DDL) statements define, modify, and delete the physical metadata schema of database objects. DDL statements in most enterprise RDBMS trigger an automatic implicit `COMMIT`.

Core DDL Statements:
- `CREATE TABLE`: Defines table name, columns, data types, and constraints.
- `ALTER TABLE`: Adds (`ADD`), modifies (`MODIFY` / `ALTER COLUMN`), or removes (`DROP COLUMN`) columns and constraints from existing tables.
- `DROP TABLE`: Permanently deletes the table structure, its indexes, and all contained data from disk.
- `TRUNCATE TABLE`: Fast deletion of all rows by deallocating disk pages without scanning rows individually. Cannot be rolled back in some engines and resets identity counters.""",
                    'syntax': """ALTER TABLE students ADD COLUMN graduation_year INT;
ALTER TABLE students DROP COLUMN graduation_year;
DROP TABLE IF EXISTS old_table;
TRUNCATE TABLE temp_submissions;
""",
                    'code_example': """-- Adding and modifying schema columns
ALTER TABLE students ADD COLUMN status VARCHAR(20) DEFAULT 'ACTIVE';
ALTER TABLE students ADD CONSTRAINT chk_gpa CHECK (gpa BETWEEN 0.00 AND 4.00);

-- Query schema definition
SELECT column_name, data_type, column_default 
FROM information_schema.columns 
WHERE table_name = 'students' AND column_name = 'status';
""",
                    'expected_output': """+-------------+-----------+----------------+
| column_name | data_type | column_default |
+-------------+-----------+----------------+
| status      | varchar   | 'ACTIVE'       |
+-------------+-----------+----------------+
""",
                    'common_mistakes': 'Confusing `TRUNCATE` with `DELETE`. `DELETE` removes rows one-by-one logging individual undo records, whereas `TRUNCATE` deallocates data pages directly.',
                    'practice_question': 'Does the `DROP TABLE` command delete only the data or also the table schema definition? (Answer: It deletes both the table structure and all data permanently).'
                },
                {
                    'id': 'dbms-sql-constraints',
                    'title': '9. Enforcing Column Constraints: PRIMARY, UNIQUE, CHECK & NOT NULL',
                    'read_time': '10 min',
                    'summary': 'Protect data quality at the database engine tier with declarative SQL column and table constraints.',
                    'concept': """Constraints are declarative rules enforced by the database management engine on columns or tables to guarantee data validity:
- `NOT NULL`: Prevents insertion of `NULL` into an attribute.
- `UNIQUE`: Guarantees all non-null values in the column are distinct.
- `PRIMARY KEY`: Combines `NOT NULL` and `UNIQUE` to establish the primary row identifier.
- `CHECK (expression)`: Enforces that inserted or updated values satisfy a boolean expression.
- `DEFAULT value`: Supplies a fallback value when the insert statement omits the attribute.""",
                    'syntax': """CREATE TABLE table_name (
    col_id INT PRIMARY KEY,
    col_str VARCHAR(50) NOT NULL UNIQUE,
    col_num INT CHECK (col_num > 0) DEFAULT 1
);
""",
                    'code_example': """-- University Course Catalog with comprehensive constraints
CREATE TABLE course_catalog (
    course_code VARCHAR(8) PRIMARY KEY,
    course_name VARCHAR(100) NOT NULL,
    capacity INT NOT NULL CHECK (capacity > 0 AND capacity <= 500),
    is_active BOOLEAN DEFAULT TRUE
);

INSERT INTO course_catalog VALUES ('CS101', 'Intro to Programming', 150, TRUE);
SELECT * FROM course_catalog;
""",
                    'expected_output': """+-------------+----------------------+----------+-----------+
| course_code | course_name          | capacity | is_active |
+-------------+----------------------+----------+-----------+
| CS101       | Intro to Programming |      150 |         1 |
+-------------+----------------------+----------+-----------+
""",
                    'common_mistakes': 'Relying exclusively on frontend client-side validation without database constraints. If an external script or API interacts directly with the database, invalid data corrupts the system.',
                    'practice_question': 'Can a table have multiple `UNIQUE` constraints? (Answer: Yes, unlike `PRIMARY KEY` which allows only one per table, multiple `UNIQUE` constraints are permitted).'
                }
            ]
        },
        'medium': {
            'level_number': 2,
            'name': 'Medium (Level 2 - Relational Queries & SQL Manipulation)',
            'description': 'DML statements, complex queries, filtering, aggregation, groupings, multi-table joins, subqueries, and views.',
            'topics': [
                {
                    'id': 'dbms-sql-dml',
                    'title': '1. SQL Data Manipulation Language (DML): INSERT, UPDATE & DELETE',
                    'read_time': '10 min',
                    'summary': 'Manipulate table rows using transactional INSERT with multi-row values, targeted UPDATE, and DELETE with WHERE filters.',
                    'concept': """Data Manipulation Language (DML) manages data stored within tables:
- `INSERT INTO`: Adds new rows. Supports single or multi-row batch inserts: `INSERT INTO table (cols) VALUES (...), (...)`.
- `UPDATE`: Modifies existing attribute values in rows matching a `WHERE` condition. Omitting `WHERE` modifies EVERY row in the table!
- `DELETE FROM`: Deletes rows matching a `WHERE` condition. Omitting `WHERE` empties the table!""",
                    'syntax': """INSERT INTO departments (dept_id, dept_name, building, budget) 
VALUES ('CS', 'Computer Science', 'Turing Hall', 1200000.00),
       ('MATH', 'Mathematics', 'Euler Hall', 850000.00);

UPDATE students SET gpa = 3.90 WHERE student_id = 'STU-101';
DELETE FROM enrollments WHERE grade = 'W';
""",
                    'code_example': """-- Seeding sample database data
INSERT INTO departments VALUES ('CS', 'Computer Science', 'Turing Hall', 1200000.00);
INSERT INTO students VALUES ('STU-101', 'Maya Lin', 'maya@uni.edu', 'CS', 3.82);

-- Safe update with WHERE clause
UPDATE students 
SET gpa = 3.95 
WHERE student_id = 'STU-101';

SELECT student_id, full_name, gpa FROM students WHERE student_id = 'STU-101';
""",
                    'expected_output': """+------------+-----------+------+
| student_id | full_name | gpa  |
+------------+-----------+------+
| STU-101    | Maya Lin  | 3.95 |
+------------+-----------+------+
""",
                    'common_mistakes': 'Executing an `UPDATE` or `DELETE` statement without a `WHERE` clause in production, modifying or deleting all records in the table.',
                    'practice_question': 'What happens if you run `DELETE FROM students;` without a `WHERE` clause? (Answer: All rows in the students table are permanently deleted).'
                },
                {
                    'id': 'dbms-sql-select-where',
                    'title': '2. SELECT Queries, Filtering (WHERE) & Sorting (ORDER BY)',
                    'read_time': '10 min',
                    'summary': 'Retrieve and sort records using SELECT, column aliases, WHERE predicates, pattern matching (LIKE), and pagination (LIMIT/OFFSET).',
                    'concept': """The `SELECT` statement queries data from one or more tables.
Execution order of SQL clauses:
1. `FROM` & `JOIN` (identify tables)
2. `WHERE` (filter individual rows)
3. `GROUP BY` (aggregate rows)
4. `HAVING` (filter grouped rows)
5. `SELECT` (project expressions and aliases)
6. `ORDER BY` (sort output)
7. `LIMIT` / `OFFSET` (paginate)

Filtering Operators:
- Comparison: `=`, `<>`, `!=`, `<`, `>`, `<=`, `>=`
- Range: `BETWEEN low AND high`
- List: `IN (val1, val2, ...)`
- Null check: `IS NULL`, `IS NOT NULL`
- Pattern matching: `LIKE '%pattern%'` (`%` = wildcard sequence, `_` = single character).""",
                    'syntax': """SELECT col1, col2 AS alias 
FROM table_name 
WHERE condition 
ORDER BY col1 ASC, col2 DESC 
LIMIT 10 OFFSET 0;
""",
                    'code_example': """-- Querying high-achieving CS students sorted by GPA
SELECT student_id, full_name, gpa 
FROM students 
WHERE department_id = 'CS' AND gpa >= 3.50 
ORDER BY gpa DESC, full_name ASC 
LIMIT 5;
""",
                    'expected_output': """+------------+---------------+------+
| student_id | full_name     | gpa  |
+------------+---------------+------+
| STU-101    | Maya Lin      | 3.95 |
| STU-104    | Alex Chen     | 3.88 |
| STU-108    | Sarah Jenkins | 3.75 |
+------------+---------------+------+
""",
                    'common_mistakes': 'Using `= NULL` in a `WHERE` clause. In SQL ternary logic, `val = NULL` evaluates to `UNKNOWN`. You must use `IS NULL` or `IS NOT NULL`.',
                    'practice_question': 'What is the correct SQL syntax to test whether a column `email` has no value? (Answer: `WHERE email IS NULL`).'
                },
                {
                    'id': 'dbms-aggregates',
                    'title': '3. SQL Aggregate Functions: COUNT, SUM, AVG, MIN & MAX',
                    'read_time': '10 min',
                    'summary': 'Compute summary statistics over rows using standard SQL aggregates and handle NULL value nuances.',
                    'concept': """Aggregate functions operate on a collection of values across multiple rows and return a single summary value:
- `COUNT(*)`: Returns the total number of rows, including rows with NULLs.
- `COUNT(column)`: Returns the count of non-NULL values in that column.
- `COUNT(DISTINCT column)`: Returns the count of unique non-NULL values.
- `SUM(column)`: Returns the sum of numerical values (ignores NULLs).
- `AVG(column)`: Returns the arithmetic mean (ignores NULLs).
- `MIN(column)` / `MAX(column)`: Returns the minimum or maximum value.""",
                    'syntax': """SELECT COUNT(*) AS total_students,
       AVG(gpa) AS mean_gpa,
       MAX(gpa) AS top_gpa
FROM students;
""",
                    'code_example': """SELECT 
    COUNT(*) AS total_enrolled,
    COUNT(DISTINCT department_id) AS active_depts,
    ROUND(AVG(gpa), 2) AS average_cohort_gpa,
    MIN(gpa) AS lowest_gpa,
    MAX(gpa) AS highest_gpa
FROM students;
""",
                    'expected_output': """+----------------+--------------+--------------------+------------+-------------+
| total_enrolled | active_depts | average_cohort_gpa | lowest_gpa | highest_gpa |
+----------------+--------------+--------------------+------------+-------------+
|            150 |            8 |               3.42 |       2.15 |        4.00 |
+----------------+--------------+--------------------+------------+-------------+
""",
                    'common_mistakes': 'Assuming `COUNT(column)` counts nulls. Only `COUNT(*)` counts rows regardless of column nullability.',
                    'practice_question': 'How does `AVG(score)` treat rows where `score` is NULL? (Answer: It ignores NULL rows completely and divides the sum by the non-null count).'
                },
                {
                    'id': 'dbms-group-by-having',
                    'title': '4. Grouping Data with GROUP BY & Filtering with HAVING',
                    'read_time': '11 min',
                    'summary': 'Partition rows into subsets with GROUP BY and filter aggregated groups using the HAVING clause.',
                    'concept': """The `GROUP BY` clause groups rows that share identical values in specified columns into summary rows.
Every column listed in the `SELECT` list that is not part of an aggregate function MUST appear in the `GROUP BY` clause.

**Difference between WHERE and HAVING**:
- `WHERE`: Filters individual records *before* aggregation occurs. It cannot contain aggregate functions!
- `HAVING`: Filters aggregated groups *after* grouping. It evaluates aggregate predicates like `HAVING COUNT(*) > 5`.""",
                    'syntax': """SELECT dept_id, COUNT(*) AS stu_count, AVG(gpa) AS avg_gpa
FROM students
WHERE gpa >= 2.0  -- Row filter
GROUP BY dept_id
HAVING COUNT(*) >= 3; -- Group filter
""",
                    'code_example': """SELECT 
    department_id,
    COUNT(student_id) AS student_count,
    ROUND(AVG(gpa), 2) AS dept_average_gpa
FROM students
GROUP BY department_id
HAVING COUNT(student_id) >= 2 AND AVG(gpa) >= 3.50
ORDER BY dept_average_gpa DESC;
""",
                    'expected_output': """+---------------+---------------+------------------+
| department_id | student_count | dept_average_gpa |
+---------------+---------------+------------------+
| CS            |            45 |             3.68 |
| MATH          |            28 |             3.54 |
+---------------+---------------+------------------+
""",
                    'common_mistakes': 'Placing aggregate conditions like `WHERE AVG(gpa) > 3.0` inside the `WHERE` clause. Aggregates must be placed in `HAVING`.',
                    'practice_question': 'Why can aggregate functions not be used in a SQL `WHERE` clause? (Answer: Because the `WHERE` clause filters individual rows before grouping and aggregation take place).'
                },
                {
                    'id': 'dbms-joins',
                    'title': '5. Relational Joins: INNER, LEFT, RIGHT & FULL OUTER JOIN',
                    'read_time': '12 min',
                    'summary': 'Combine columns from multiple tables using join predicates, foreign keys, and Venn diagram join models.',
                    'concept': """Joins combine records from two or more tables based on a related column between them:
- **INNER JOIN**: Returns only rows with matching values in both tables.
- **LEFT (OUTER) JOIN**: Returns all rows from the left table, matched with corresponding rows from the right table (unmatched right columns return `NULL`).
- **RIGHT (OUTER) JOIN**: Returns all rows from the right table, matched with left table rows (`NULL` if no match).
- **FULL (OUTER) JOIN**: Returns all rows when there is a match in either left or right table.
- **CROSS JOIN**: Produces the Cartesian Product of both relations ($N \\times M$ rows).""",
                    'syntax': """SELECT s.full_name, d.dept_name
FROM students s
INNER JOIN departments d ON s.department_id = d.dept_id;

SELECT s.full_name, e.course_id
FROM students s
LEFT JOIN enrollments e ON s.student_id = e.student_id;
""",
                    'code_example': """-- University schema join: Students and their departments
SELECT 
    s.student_id, 
    s.full_name, 
    d.dept_name, 
    d.building
FROM students s
INNER JOIN departments d ON s.department_id = d.dept_id
ORDER BY s.full_name;
""",
                    'expected_output': """+------------+---------------+------------------+-------------+
| student_id | full_name     | dept_name        | building    |
+------------+---------------+------------------+-------------+
| STU-104    | Alex Chen     | Computer Science | Turing Hall |
| STU-101    | Maya Lin      | Computer Science | Turing Hall |
| STU-108    | Sarah Jenkins | Computer Science | Turing Hall |
+------------+---------------+------------------+-------------+
""",
                    'common_mistakes': 'Omitting the join condition (`ON s.dept_id = d.dept_id`), which turns the query into an accidental Cartesian cross join with astronomical row counts.',
                    'practice_question': 'Which join type returns all rows from the first table even if there is no match in the second table? (Answer: LEFT OUTER JOIN).'
                },
                {
                    'id': 'dbms-subqueries',
                    'title': '6. Subqueries: Scalar, Correlated & IN / EXISTS Predicates',
                    'read_time': '11 min',
                    'summary': 'Nest SQL queries inside WHERE, FROM, and SELECT clauses, and contrast correlated vs uncorrelated subqueries.',
                    'concept': """A subquery is a `SELECT` query nested inside another SQL statement:
- **Scalar Subquery**: Returns exactly one row and one column. Can be placed anywhere a single literal value is expected.
- **Multi-row Subquery**: Returns multiple rows. Evaluated using `IN`, `NOT IN`, `ANY`, or `ALL`.
- **Correlated Subquery**: References columns from the outer query relation. The subquery executes once for every candidate row evaluated by the outer query!
- **`EXISTS` / `NOT EXISTS`**: Efficiently tests whether the subquery yields at least one row, terminating immediately upon the first match (semi-join optimization).""",
                    'syntax': """-- Scalar subquery
SELECT full_name, gpa 
FROM students 
WHERE gpa > (SELECT AVG(gpa) FROM students);

-- EXISTS correlated subquery
SELECT d.dept_name 
FROM departments d
WHERE EXISTS (SELECT 1 FROM students s WHERE s.department_id = d.dept_id);
""",
                    'code_example': """-- Students scoring above cohort average
SELECT 
    student_id, 
    full_name, 
    gpa 
FROM students 
WHERE gpa > (SELECT AVG(gpa) FROM students)
ORDER BY gpa DESC;
""",
                    'expected_output': """+------------+-----------+------+
| student_id | full_name | gpa  |
+------------+-----------+------+
| STU-101    | Maya Lin  | 3.95 |
| STU-104    | Alex Chen | 3.88 |
+------------+-----------+------+
""",
                    'common_mistakes': 'Using `NOT IN` with a subquery that returns a `NULL` value. If any row returned by the subquery is `NULL`, the entire `NOT IN` expression evaluates to `UNKNOWN`, yielding zero rows.',
                    'practice_question': 'What is the key performance advantage of `EXISTS` over `COUNT(*) > 0` in a subquery? (Answer: `EXISTS` halts scanning as soon as the first matching row is found, whereas `COUNT(*)` must scan the entire table). '
                },
                {
                    'id': 'dbms-set-operations',
                    'title': '7. Set Operations: UNION, UNION ALL, INTERSECT & EXCEPT',
                    'read_time': '10 min',
                    'summary': 'Combine query results with relational set algebra, maintaining union compatibility of column types.',
                    'concept': """Set operations combine results from two or more `SELECT` queries into a single result set.
Requirements for **Union Compatibility**:
1. Both queries must select the same number of columns.
2. Corresponding columns must have compatible data types.

Set Operators:
- `UNION`: Combines results and eliminates duplicate rows (involves an internal sort/hash operation).
- `UNION ALL`: Combines results preserving all duplicates. Significantly faster because no deduplication sort is required.
- `INTERSECT`: Returns only rows present in both result sets.
- `EXCEPT` / `MINUS`: Returns rows from the first query that do not appear in the second query.""",
                    'syntax': """SELECT student_id FROM students WHERE department_id = 'CS'
UNION
SELECT student_id FROM enrollments WHERE course_id = 'CS101';
""",
                    'code_example': """-- Active learners across both subjects
SELECT 'Python Course' AS course_track, full_name FROM students WHERE department_id = 'CS'
UNION ALL
SELECT 'DBMS Course' AS course_track, full_name FROM students WHERE gpa >= 3.8;
""",
                    'expected_output': """+---------------+---------------+
| course_track  | full_name     |
+---------------+---------------+
| Python Course | Maya Lin      |
| Python Course | Alex Chen     |
| Python Course | Sarah Jenkins |
| DBMS Course   | Maya Lin      |
| DBMS Course   | Alex Chen     |
+---------------+---------------+
""",
                    'common_mistakes': 'Using `UNION` when duplicate removal is unnecessary. `UNION ALL` avoids expensive sorting operations on large datasets.',
                    'practice_question': 'What is the difference between `UNION` and `UNION ALL` in SQL? (Answer: `UNION` eliminates duplicate rows via sorting/hashing, while `UNION ALL` retains all rows and is faster).'
                },
                {
                    'id': 'dbms-views',
                    'title': '8. Views: Virtual Tables, Data Security & Materialization',
                    'read_time': '10 min',
                    'summary': 'Encapsulate complex query logic with virtual views, enforce row-level security, and understand materialized views.',
                    'concept': """A **View** is a virtual table defined by a stored SQL query. It contains no physical data on disk (unless materialized); instead, whenever a view is queried, the database dynamically executes the underlying query.

Benefits:
1. **Security**: Hides sensitive columns (e.g. expose student name and department without exposing social security numbers or phone numbers).
2. **Simplicity**: Encapsulates multi-table joins into a single callable view.
3. **Consistency**: Changes to the underlying base tables can be smoothed over by altering the view definition.

**Materialized View**: Physically caches the query result on disk for high-speed reporting, requiring periodic refresh strategies.""",
                    'syntax': """CREATE VIEW student_honor_roll AS
SELECT student_id, full_name, gpa 
FROM students 
WHERE gpa >= 3.80;

SELECT * FROM student_honor_roll;
""",
                    'code_example': """CREATE VIEW v_dept_summary AS
SELECT 
    d.dept_name,
    COUNT(s.student_id) AS student_count,
    ROUND(AVG(s.gpa), 2) AS average_gpa
FROM departments d
LEFT JOIN students s ON d.dept_id = s.department_id
GROUP BY d.dept_name;

SELECT * FROM v_dept_summary WHERE student_count > 0;
""",
                    'expected_output': """+------------------+---------------+-------------+
| dept_name        | student_count | average_gpa |
+------------------+---------------+-------------+
| Computer Science |             3 |        3.86 |
+------------------+---------------+-------------+
""",
                    'common_mistakes': 'Assuming standard views store data on disk. Standard views are executed on-the-fly and consume CPU on every invocation.',
                    'practice_question': 'Does a standard relational view physically store its own copy of the row data on disk? (Answer: No, it is a virtual table that executes the underlying query dynamically).'
                },
                {
                    'id': 'dbms-tcl-transactions',
                    'title': '9. Transaction Control Language: COMMIT, ROLLBACK & SAVEPOINT',
                    'read_time': '10 min',
                    'summary': 'Manage transactional state boundaries using COMMIT to persist changes, ROLLBACK to revert, and SAVEPOINT for checkpoints.',
                    'concept': """Transaction Control Language (TCL) commands manage the transactions that encapsulate DML changes:
- `BEGIN TRANSACTION` / `START TRANSACTION`: Marks the beginning of an atomic logical unit of work.
- `COMMIT`: Permanently saves all changes made during the current transaction to disk and releases database locks.
- `ROLLBACK`: Discards all modifications made during the transaction, restoring data to its pre-transaction state.
- `SAVEPOINT savepoint_name`: Creates a checkpoint within a transaction allowing partial rollbacks via `ROLLBACK TO SAVEPOINT` without aborting the entire transaction.""",
                    'syntax': """BEGIN TRANSACTION;
UPDATE accounts SET balance = balance - 500 WHERE id = 1;
UPDATE accounts SET balance = balance + 500 WHERE id = 2;
COMMIT;
""",
                    'code_example': """-- Transaction simulation with rollback
-- Simulating enrollment processing
BEGIN;

INSERT INTO enrollments (enrollment_id, student_id, course_id, term, grade)
VALUES (9901, 'STU-101', 'CS101', 'Fall 2026', 'A');

SAVEPOINT enrollment_recorded;

-- If course capacity check fails:
ROLLBACK TO SAVEPOINT enrollment_recorded;

COMMIT;
SELECT 'Transaction Safely Committed' AS status;
""",
                    'expected_output': """+-------------------------------+
| status                        |
+-------------------------------+
| Transaction Safely Committed  |
+-------------------------------+
""",
                    'common_mistakes': 'Leaving database transactions open without an explicit `COMMIT` or `ROLLBACK`, holding exclusive table locks and blocking all concurrent queries.',
                    'practice_question': 'Which TCL command allows partial rollback to an intermediate state within an active transaction? (Answer: `ROLLBACK TO SAVEPOINT`).'
                }
            ]
        },
        'complex': {
            'level_number': 3,
            'name': 'Complex (Level 3 - Theory, Normalization & Internal Architecture)',
            'description': 'Functional dependencies, 1NF to BCNF, ACID transactions, 2PL locking, deadlocks, B+ Tree indexing, and WAL recovery.',
            'topics': [
                {
                    'id': 'dbms-fd-axioms',
                    'title': '1. Functional Dependencies & Armstrong\'s Axioms',
                    'read_time': '12 min',
                    'summary': 'Analyze formal functional dependencies ($X \\rightarrow Y$), minimal covers, and deduce closures using Armstrong\'s Axioms.',
                    'concept': """A Functional Dependency (FD) $X \\rightarrow Y$ across relation $R$ states that whenever two tuples agree on attribute set $X$, they must agree on attribute set $Y$. $X$ uniquely determines $Y$.

**Armstrong's Axioms** (Sound and Complete inference rules):
1. **Reflexivity**: If $Y \\subseteq X$, then $X \\rightarrow Y$. (Trivial dependency)
2. **Augmentation**: If $X \\rightarrow Y$, then $XZ \\rightarrow YZ$ for any attribute set $Z$.
3. **Transitivity**: If $X \\rightarrow Y$ and $Y \\rightarrow Z$, then $X \\rightarrow Z$.

Secondary Rules:
- Union: If $X \\rightarrow Y$ and $X \\rightarrow Z$, then $X \\rightarrow YZ$.
- Decomposition: If $X \\rightarrow YZ$, then $X \\rightarrow Y$ and $X \\rightarrow Z$.
- Attribute Closure $X^+$: The set of all attributes functionally determined by $X$. If $X^+ = R$, then $X$ is a Super Key!""",
                    'syntax': """-- Given R(A, B, C, D) with FDs: {A -> B, B -> C, C -> D}
-- Closure A+ = {A, B, C, D}  => A is a candidate key.
""",
                    'code_example': """-- Conceptual verification of Functional Dependency: student_id -> full_name, email
SELECT student_id, COUNT(DISTINCT full_name) AS name_variations
FROM students
GROUP BY student_id
HAVING COUNT(DISTINCT full_name) > 1;
-- Returns 0 rows if student_id -> full_name holds strictly!
""",
                    'expected_output': """Empty set (0.01 sec) - Functional Dependency holds!
""",
                    'common_mistakes': 'Assuming an FD holds just because current sample data matches it. Functional dependencies are semantic domain constraints that must hold for all possible future tuples.',
                    'practice_question': 'If $X \\rightarrow Y$ and $Y \\rightarrow Z$, which Armstrong axiom proves that $X \\rightarrow Z$? (Answer: Transitivity).'
                },
                {
                    'id': 'dbms-normalization-3nf',
                    'title': '2. Database Normalization: 1NF, 2NF & 3NF Step-by-Step',
                    'read_time': '13 min',
                    'summary': 'Eliminate update, insertion, and deletion anomalies through systematic schema decomposition.',
                    'concept': """Normalization is the process of structuring a relational database to reduce data redundancy and eliminate anomalies:
- **First Normal Form (1NF)**: All column values must be atomic (no repeating groups or arrays). Every row must have a unique identifier.
- **Second Normal Form (2NF)**: Must be in 1NF, AND no non-prime attribute may be partially dependent on any candidate key (Eliminate **Partial Dependency**: a non-key attribute dependent on only part of a composite primary key).
- **Third Normal Form (3NF)**: Must be in 2NF, AND no non-prime attribute may be transitively dependent on candidate keys (Eliminate **Transitive Dependency**: $X \\rightarrow Y$ and $Y \\rightarrow Z$ where $Z$ is non-prime).
  - Formal 3NF test: For every non-trivial FD $X \\rightarrow Y$, either $X$ is a Super Key OR $Y$ is a Prime Attribute (member of a candidate key).""",
                    'syntax': """-- 1NF: Atomic cells
-- 2NF: No Partial Dependencies (A, B) -> C where A -> C
-- 3NF: No Transitive Dependencies A -> B and B -> C
""",
                    'code_example': """-- Decomposing Unnormalized Enrollments into 3NF:
-- Table 1: students(student_id, full_name, department_id)
-- Table 2: departments(dept_id, dept_name, building)
-- Table 3: enrollments(enrollment_id, student_id, course_id, grade)

SELECT 'Original relation decomposed into 3NF' AS normalization_status,
       'No partial dependencies & no transitive dependencies' AS explanation;
""",
                    'expected_output': """+--------------------------------------+------------------------------------------------------+
| normalization_status                 | explanation                                          |
+--------------------------------------+------------------------------------------------------+
| Original relation decomposed into 3NF| No partial dependencies & no transitive dependencies |
+--------------------------------------+------------------------------------------------------+
""",
                    'common_mistakes': 'Decomposing tables without verifying Dependency Preservation or Lossless Join property, causing lost queries or phantom tuples.',
                    'practice_question': 'What type of dependency is eliminated when moving a schema from 1NF to 2NF? (Answer: Partial dependency of non-prime attributes on a composite candidate key).'
                },
                {
                    'id': 'dbms-bcnf-4nf',
                    'title': '3. Boyce-Codd Normal Form (BCNF) & Multivalued Dependencies',
                    'read_time': '12 min',
                    'summary': 'Enforce strict Boyce-Codd Normal Form ($X$ must be a super key) and handle multivalued dependencies in 4NF.',
                    'concept': """**Boyce-Codd Normal Form (BCNF)** is a stricter version of 3NF.
Rule: A relation $R$ is in BCNF if and only if for every non-trivial functional dependency $X \\rightarrow Y$, **$X$ is a Super Key**.

Unlike 3NF, BCNF does not permit $Y$ to be a prime attribute if $X$ is not a super key. Every relation in BCNF is guaranteed to be in 3NF, but a 3NF relation might not be in BCNF if candidate keys overlap.

**Fourth Normal Form (4NF)**:
Eliminates **Multivalued Dependencies (MVD)** $X \\twoheadrightarrow Y$, where attribute set $X$ determines a set of values for $Y$ independently of all other attributes.""",
                    'syntax': """-- BCNF Condition:
-- For every non-trivial FD X -> Y, X MUST be a Super Key!
""",
                    'code_example': """-- Example: Advisor(student_id, advisor_name, department)
-- If student_id, department -> advisor_name AND advisor_name -> department
-- advisor_name is NOT a super key, violating BCNF!
-- Decomposition into BCNF:
-- R1(advisor_name, department) where advisor_name is primary key
-- R2(student_id, advisor_name) where student_id, advisor_name is primary key
SELECT 'BCNF Decomposition Complete' AS status;
""",
                    'expected_output': """+-----------------------------+
| status                      |
+-----------------------------+
| BCNF Decomposition Complete |
+-----------------------------+
""",
                    'common_mistakes': 'Assuming 3NF and BCNF are always equivalent. When a table has multiple overlapping composite candidate keys, 3NF may still harbor redundancy that only BCNF resolves.',
                    'practice_question': 'What is the singular requirement for a non-trivial functional dependency $X \\rightarrow Y$ to satisfy BCNF? (Answer: $X$ must be a super key).'
                },
                {
                    'id': 'dbms-acid-states',
                    'title': '4. ACID Properties & Transaction Lifecycle States',
                    'read_time': '12 min',
                    'summary': 'Examine Atomicity, Consistency, Isolation, and Durability, alongside transaction state machine transitions.',
                    'concept': """A transaction is a logical unit of database processing consisting of one or more read/write operations.
**ACID Guarantees**:
- **Atomicity**: All-or-nothing execution. Maintained by the DBMS Recovery Manager via Write-Ahead Logging (WAL).
- **Consistency**: Execution of a transaction in isolation preserves database integrity constraints.
- **Isolation**: Concurrent transactions execute without interfering with one another. Maintained by Concurrency Control.
- **Durability**: Once committed, changes survive any system crash or power outage. Maintained by redundant non-volatile logs.

**Transaction State Machine**:
`Active` $\\rightarrow$ `Partially Committed` $\\rightarrow$ `Committed`
`Active` / `Partially Committed` $\\rightarrow$ `Failed` $\\rightarrow$ `Aborted` (Rolled back).""",
                    'syntax': """-- ACID in practice:
BEGIN;
-- Sequence of operations
COMMIT; -- Transitions from Partially Committed to Committed
""",
                    'code_example': """-- Conceptual state demonstration
SELECT 
    'Atomicity' AS property, 'Write-Ahead Log (WAL) undo' AS implementation_mechanism
UNION ALL
SELECT 'Isolation', 'Two-Phase Locking (2PL) & MVCC'
UNION ALL
SELECT 'Durability', 'Redo log flushed to non-volatile disk'
UNION ALL
SELECT 'Consistency', 'Integrity constraint enforcement';
""",
                    'expected_output': """+-------------+---------------------------------------+
| property    | implementation_mechanism              |
+-------------+---------------------------------------+
| Atomicity   | Write-Ahead Log (WAL) undo            |
| Isolation   | Two-Phase Locking (2PL) & MVCC        |
| Durability  | Redo log flushed to non-volatile disk |
| Consistency | Integrity constraint enforcement      |
+-------------+---------------------------------------+
""",
                    'common_mistakes': 'Believing that "Durability" means data is never lost even if the physical storage medium is destroyed. Durability guarantees data survives server reboots/crashes, but disk redundancy (RAID/backups) protects against hardware loss.',
                    'practice_question': 'At what exact state does a transaction transition from Partially Committed to Committed? (Answer: After the last log record for the transaction is successfully written to non-volatile disk storage).'
                },
                {
                    'id': 'dbms-concurrency-serializability',
                    'title': '5. Concurrency Control & Conflict Serializability',
                    'read_time': '13 min',
                    'summary': 'Detect conflicting operations (read-write, write-write) and evaluate precedence / serialization graphs.',
                    'concept': """When multiple transactions execute concurrently, their instructions interleave to form a **Schedule**.
A schedule is **Conflict Serializable** if it is conflict equivalent to some purely serial schedule of the same transactions.

Two operations $I_i$ and $I_j$ belonging to different transactions conflict if and only if:
1. They access the exact same data item $Q$.
2. At least one of the operations is a **Write** operation ($W(Q)$).
Types of conflicts: Read-Write ($R-W$), Write-Read ($W-R$), Write-Write ($W-W$).

**Precedence Graph (Serialization Graph)**:
- Directed graph where nodes represent transactions $T_1, T_2, \\dots$.
- Draw a directed edge $T_i \\rightarrow T_j$ if an operation of $T_i$ conflicts with and executes before an operation of $T_j$.
- **Theorem**: A schedule is conflict serializable if and only if its precedence graph contains **NO CYCLES**!""",
                    'syntax': """-- Schedule S: R1(A), W1(A), R2(A), W2(A)
-- Precedence edge: T1 -> T2 (No cycle => Serializable!)
""",
                    'code_example': """SELECT 
    'T1 -> T2' AS edge, 
    'Conflict on item A: W1(A) before R2(A)' AS reason,
    'Acyclic' AS graph_property,
    'Serializable' AS evaluation;
""",
                    'expected_output': """+----------+---------------------------------------+----------------+--------------+
| edge     | reason                                | graph_property | evaluation   |
+----------+---------------------------------------+----------------+--------------+
| T1 -> T2 | Conflict on item A: W1(A) before R2(A)| Acyclic        | Serializable |
+----------+---------------------------------------+----------------+--------------+
""",
                    'common_mistakes': 'Assuming Read-Read operations conflict. Two concurrent transactions reading the same item never conflict with each other.',
                    'practice_question': 'What structural property of a precedence graph proves that a concurrent schedule is conflict serializable? (Answer: The graph is a Directed Acyclic Graph / has no directed cycles).'
                },
                {
                    'id': 'dbms-two-phase-locking',
                    'title': '6. Lock-Based Protocols: Two-Phase Locking (2PL) & Strict 2PL',
                    'read_time': '12 min',
                    'summary': 'Prevent isolation anomalies using Shared (S) and Exclusive (X) locks with growing and shrinking phases.',
                    'concept': """Locks govern concurrent access to database items:
- **Shared Lock (S)**: Read-only lock. Multiple transactions can hold S-locks concurrently.
- **Exclusive Lock (X)**: Read/Write lock. Only one transaction can hold an X-lock; blocks all other S and X locks.

**Two-Phase Locking (2PL) Protocol**:
Guarantees conflict serializability. A transaction must acquire and release locks in two distinct phases:
1. **Growing Phase**: Transaction may acquire new locks, but cannot release any lock.
2. **Shrinking Phase**: Transaction may release locks, but cannot acquire any new lock.
Once a transaction releases its first lock, it enters the shrinking phase forever.

**Strict 2PL**:
Requires that all Exclusive (X) locks be held until the transaction commits or aborts. Prevents cascading rollbacks!""",
                    'syntax': """-- Transaction 1:
Lock-S(A); Read(A); Lock-X(B); Write(B); -- Growing
Unlock(A); Unlock(B);                    -- Shrinking
""",
                    'code_example': """SELECT 
    '2PL Protocol' AS protocol,
    'Guarantees Conflict Serializability' AS primary_benefit,
    'May cause deadlocks' AS potential_hazard;
""",
                    'expected_output': """+--------------+-------------------------------------+------------------+
| protocol     | primary_benefit                     | potential_hazard |
+--------------+-------------------------------------+------------------+
| 2PL Protocol | Guarantees Conflict Serializability | May cause deadlocks|
+--------------+-------------------------------------+------------------+
""",
                    'common_mistakes': 'Believing 2PL prevents deadlocks. 2PL guarantees serializability, but transactions can still easily deadlock while waiting for each other\'s locks.',
                    'practice_question': 'What is the distinguishing requirement of Strict 2PL compared to basic 2PL? (Answer: Strict 2PL requires all exclusive locks to be held until the transaction officially commits or aborts).'
                },
                {
                    'id': 'dbms-deadlocks',
                    'title': '7. Deadlock Handling: Wait-For Graphs, Wait-Die & Wound-Wait',
                    'read_time': '11 min',
                    'summary': 'Detect and break deadlocks using Wait-For Graphs or prevent them using timestamp-based protocols.',
                    'concept': """A **Deadlock** occurs when two or more transactions are in a simultaneous circular wait state, each waiting for a lock held by the other.

Deadlock Detection:
- **Wait-For Graph (WFG)**: Directed graph where nodes are active transactions. An edge $T_i \\rightarrow T_j$ means $T_i$ is waiting for $T_j$ to release a lock.
- If the WFG contains a cycle, a deadlock exists. The engine selects a "victim" transaction and aborts/rolls it back.

Deadlock Prevention (Timestamp Schemes):
Each transaction is assigned a monotonically increasing timestamp $TS(T)$ when starting (older = smaller TS):
1. **Wait-Die** (Non-preemptive): Older waits for younger; younger dies (aborts) if requesting lock from older.
2. **Wound-Wait** (Preemptive): Older wounds (preempts/aborts) younger; younger waits for older.""",
                    'syntax': """-- Wait-For Graph: T1 -> T2 -> T1 (Cycle detected => Deadlock victim chosen)
""",
                    'code_example': """SELECT 
    'Wait-Die' AS scheme, 'Older waits for younger, younger aborts' AS rule
UNION ALL
SELECT 'Wound-Wait', 'Older preempts younger, younger waits';
""",
                    'expected_output': """+------------+------------------------------------------+
| scheme     | rule                                     |
+------------+------------------------------------------+
| Wait-Die   | Older waits for younger, younger aborts  |
| Wound-Wait | Older preempts younger, younger waits    |
+------------+------------------------------------------+
""",
                    'common_mistakes': 'Assuming deadlocks resolve themselves over time. Without timeout mechanisms or deadlock detection engines, deadlocked transactions wait indefinitely.',
                    'practice_question': 'In the Wait-Die deadlock prevention scheme, what happens when an older transaction requests a lock held by a younger transaction? (Answer: The older transaction is allowed to wait).'
                },
                {
                    'id': 'dbms-indexing-btrees',
                    'title': '8. Indexing Architecture: B-Trees, B+ Trees & Clustered Indexes',
                    'read_time': '13 min',
                    'summary': 'Understand disk block access, balanced tree node splitting, clustered vs non-clustered indexes, and O(log N) lookups.',
                    'concept': """Without indexes, finding a record requires a full table scan ($O(N)$ disk page reads). Indexes provide auxiliary search structures yielding $O(\\log N)$ disk I/O.

**B+ Tree Index Architecture** (Standard in MySQL InnoDB, PostgreSQL):
- Self-balancing $m$-way search tree.
- Internal nodes contain only routing search keys and child page pointers (high fanout).
- **All actual record pointers and data reside exclusively in the leaf nodes**.
- All leaf nodes are linked sequentially in a doubly-linked list, providing lightning-fast range scans (`BETWEEN` queries).

**Clustered vs Non-Clustered Indexes**:
- **Clustered Index**: Dictates the physical storage order of rows on disk. A table can have at most ONE clustered index (typically the Primary Key).
- **Non-Clustered (Secondary) Index**: Separate index structure whose leaf nodes store pointers (or primary keys) back to the base table rows.""",
                    'syntax': """-- Creating a secondary B+ Tree index
CREATE INDEX idx_student_gpa ON students(gpa);

-- Range scan utilizing B+ Tree leaf pointer chain
SELECT * FROM students WHERE gpa BETWEEN 3.5 AND 3.9;
""",
                    'code_example': """EXPLAIN 
SELECT full_name, gpa 
FROM students 
WHERE gpa >= 3.80;
""",
                    'expected_output': """+----+-------------+----------+------------+-------+---------------+-----------------+
| id | select_type | table    | partitions | type  | possible_keys | key             |
+----+-------------+----------+------------+-------+---------------+-----------------+
|  1 | SIMPLE      | students | NULL       | range | idx_student_gpa| idx_student_gpa|
+----+-------------+----------+------------+-------+---------------+-----------------+
""",
                    'common_mistakes': 'Creating indexes on every single column. Every index incurs write overhead on `INSERT`, `UPDATE`, and `DELETE` operations because the B+ tree must be rebalanced.',
                    'practice_question': 'Why are B+ Trees preferred over standard Binary Search Trees for database disk storage? (Answer: High fanout reduces tree height, minimizing the number of expensive disk I/O operations required to locate a block).'
                },
                {
                    'id': 'dbms-query-optimization-wal',
                    'title': '9. Query Optimization & Write-Ahead Logging (WAL)',
                    'read_time': '12 min',
                    'summary': 'Explore Cost-Based Optimizers (CBO), execution plans, and crash recovery with Write-Ahead Logging and ARIES.',
                    'concept': """The Database Engine combines declarative SQL parsing with physical execution:
1. **Query Optimizer**: Explores multiple relational algebra plans (e.g. Hash Join vs Index Nested Loop Join) and chooses the plan with minimal estimated disk I/O and CPU cost using table statistics (`ANALYZE`).
2. **Write-Ahead Logging (WAL)**: The fundamental durability rule stating that no data block modification may be written to non-volatile disk until the corresponding log record describing the update is safely flushed to non-volatile log storage.
3. **ARIES Recovery Algorithm**:
   - **Analysis Phase**: Identifies dirty pages in buffer pool and active uncommitted transactions at crash time.
   - **Redo Phase**: Replays all logged actions forward from the last checkpoint to restore database state.
   - **Undo Phase**: Rolls back all transactions that were active at crash time, undoing uncommitted changes.""",
                    'syntax': """-- Analyzing optimizer execution plan in PostgreSQL / SQLite
EXPLAIN QUERY PLAN
SELECT s.full_name, c.course_title 
FROM enrollments e 
JOIN students s ON e.student_id = s.student_id 
JOIN courses c ON e.course_id = c.course_id;
""",
                    'code_example': """SELECT 
    'Query Optimizer' AS component, 'Selects minimal-cost physical execution path' AS function
UNION ALL
SELECT 'Write-Ahead Log', 'Guarantees Atomicity and Durability before disk writes'
UNION ALL
SELECT 'Checkpoints', 'Flushes dirty pages to truncate recovery log replay time';
""",
                    'expected_output': """+-----------------+---------------------------------------------------------+
| component       | function                                                |
+-----------------+---------------------------------------------------------+
| Query Optimizer | Selects minimal-cost physical execution path            |
| Write-Ahead Log | Guarantees Atomicity and Durability before disk writes  |
| Checkpoints     | Flushes dirty pages to truncate recovery log replay time|
+-----------------+---------------------------------------------------------+
""",
                    'common_mistakes': 'Flushing data pages to disk before flushing the WAL log. If the server crashes in between, the database is irrevocably corrupted.',
                    'practice_question': 'What core rule does Write-Ahead Logging enforce before modified data pages can be written to disk? (Answer: Log records describing the change must be flushed to non-volatile storage first).'
                }
            ]
        }
    }
}
