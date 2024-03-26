--  CREATE TABLE USERS
--  (
--     ID SERIAL PRIMARY KEY,
--     NAME VARCHAR(50) UNIQUE NOT NULL,
--     EMAIL VARCHAR(50) UNIQUE NOT NULL,
--     IS_DONE BOOLEAN NOT NULL,
--     STREAK INTEGER NOT NULL);

-- DROP TABLE USERS

-- CREATE TABLE tests (
--     id SERIAL PRIMARY KEY,
--     user_id INTEGER NOT NULL,
--     path VARCHAR NOT NULL,
--     inference1 JSONB,
--     inference2 FLOAT NOT NULL,
--     inference3 JSONB,
--     q_num INTEGER NOT NULL,
--     createdDate DATE NOT NULL
-- );

-- CREATE TABLE questions (
--     id SERIAL PRIMARY KEY,
--     date DATE UNIQUE NOT NULL,
--     q1 VARCHAR NOT NULL,
--     q2 VARCHAR NOT NULL,
--     q3 VARCHAR NOT NULL
-- );