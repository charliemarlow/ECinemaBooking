DROP TABLE IF EXISTS `ticket`;

CREATE TABLE `ticket` (
  `ticket_id` INTEGER PRIMARY KEY AUTOINCREMENT,
  showtime_id int(11) NOT NULL,
  `booking_id` int(11) DEFAULT NULL,
  `age` TEXT CHECK( age IN ('child','student','adult','senior') ) NOT NULL DEFAULT 'adult',
  seat_number varchar(100) NOT NULL,
  FOREIGN KEY (booking_id) REFERENCES booking (booking_id)
)
