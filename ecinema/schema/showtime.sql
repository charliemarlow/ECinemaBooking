
DROP TABLE IF EXISTS `showtime`;

CREATE TABLE `showtime` (
  `showtime_id` INTEGER PRIMARY KEY AUTOINCREMENT,
  `time` datetime NOT NULL,
  `available_seats` int(11) NOT NULL,
  `movie_id` int(11) NOT NULL,
  `showroom_id` int(11) NOT NULL,
  FOREIGN KEY (movie_id) REFERENCES movie (movie_id),
  FOREIGN KEY (showroom_id) REFERENCES showroom (showroom_id)
)
