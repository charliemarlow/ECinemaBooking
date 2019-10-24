DROP TABLE IF EXISTS `admin`;

CREATE TABLE `admin` (
  `admin_id` INTEGER PRIMARY KEY AUTOINCREMENT,
  `username` varchar(100) NOT NULL,
  `password` binary(64) NOT NULL
)

