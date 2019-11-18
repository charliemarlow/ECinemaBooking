
DROP TABLE IF EXISTS `promo`;

CREATE TABLE `promo` (
  `promo_id` INTEGER PRIMARY KEY AUTOINCREMENT,
  `code` varchar(100) NOT NULL,
  `promo` double NOT NULL
)
