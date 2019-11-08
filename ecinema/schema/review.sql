
DROP TABLE IF EXISTS review;

CREATE TABLE review (
       review_id INTEGER PRIMARY KEY AUTOINCREMENT,
       customer_id int(11) NOT NULL,
       movie_id int(11) NOT NULL,
       rating int(11) NOT NULL,
       subject varchar(100) NOT NULL,
       review varchar(1024) NOT NULL,
       FOREIGN KEY (movie_id) REFERENCES movie (movie_id),
       FOREIGN KEY (customer_id) REFERENCES customer (customer_id)
)
