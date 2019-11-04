
DROP TABLE IF EXISTS `showroom`;

CREATE TABLE `showroom` (
  `showroom_id` INTEGER PRIMARY KEY AUTOINCREMENT,
  `number_of_seats` int(11) NOT NULL,
  `theater_id` int(11) NOT NULL,
  `showroom_name` varchar(100) NOT NULL,
  FOREIGN KEY (theater_id) REFERENCES theater (theater_id)
)