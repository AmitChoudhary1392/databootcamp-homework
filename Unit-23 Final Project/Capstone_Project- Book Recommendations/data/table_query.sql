-- Drop table if exists
DROP TABLE Library;

-- Create Library table
CREATE TABLE Library (
	id_book VARCHAR PRIMARY KEY,
    title VARCHAR,
    description VARCHAR,
    category VARCHAR,
    sub_category VARCHAR,
    isbn FLOAT,
    image_url VARCHAR,
    author VARCHAR,
    published_date VARCHAR,
    publisher VARCHAR,
    language VARCHAR,
    num_pages INT,
    ratings_count FLOAT,
    reviews_count FLOAT,
    text_reviews_count FLOAT,
    average_rating FLOAT
);

-- Drop table if exists
DROP TABLE Book;

-- Create Library table
CREATE TABLE Book (
	id_book VARCHAR	PRIMARY KEY, 
    title VARCHAR,
    description VARCHAR,
    category VARCHAR,
    isbn FLOAT,
    image_url VARCHAR,
    author VARCHAR,
    published_date VARCHAR,
    publisher VARCHAR,
    language VARCHAR
);

-- Drop table if exists
DROP TABLE Owner;

-- Create Library table
CREATE TABLE Owner (
	id_book VARCHAR,
    owner_email VARCHAR,
    ratings FLOAT,
	review VARCHAR,
	location VARCHAR,
	lat FLOAT,
	lon	FLOAT,
	contact_details VARCHAR,
	available INT,
	PRIMARY KEY (id_book, Owner_email)
);

--IMPORT DATA TO library Table

--Query to see import
SELECT * FROM Library