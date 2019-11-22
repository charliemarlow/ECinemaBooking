DROP TABLE IF EXISTS `booking`;

CREATE TABLE `booking` (
  `booking_id` INTEGER PRIMARY KEY AUTOINCREMENT,
  `order_id` varchar(100) NOT NULL,
  `total_price` double NOT NULL,
  `credit_card_id` int(11) NOT NULL,
  `promo_id` int(11) DEFAULT NULL,
  `movie_id` int(11) NOT NULL,
  `customer_id` int(11) NOT NULL,
  `showtime_id` int(11) NOT NULL,
  order_date datetime NOT NULL,
  FOREIGN KEY (promo_id) REFERENCES promo (promo_id),
  FOREIGN KEY (movie_id) REFERENCES movie (movie_id),
  FOREIGN KEY (customer_id) REFERENCES customer (customer_id),
  FOREIGN KEY (showtime_id) REFERENCES showtime (showtime_id)
)
