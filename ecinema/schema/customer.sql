DROP TABLE IF EXISTS `customer`;

CREATE TABLE `customer` (
  `customer_id` INTEGER PRIMARY KEY AUTOINCREMENT,
  `first_name` varchar(100) DEFAULT NULL,
  `last_name` varchar(100) DEFAULT NULL,
  `email` varchar(100) NOT NULL,
  `subscribe_to_promo` tinyint(1) DEFAULT NULL,
  `username` varchar(100) NOT NULL,
  `password` binary(64) NOT NULL,
  `status` TEXT CHECK( status IN ('active', 'inactive', 'suspended') ) NOT NULL DEFAULT 'active'
)