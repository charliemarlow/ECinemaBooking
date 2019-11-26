DROP TABLE IF EXISTS `movie`;

CREATE TABLE `movie` (
  `movie_id` INTEGER PRIMARY KEY AUTOINCREMENT,
  `title` varchar(100) NOT NULL,
  `category` TEXT CHECK( category IN ('action', 'comedy', 'drama', 'sci-fi', 'mystery', 'crime', 'fantasy', 'thriller', 'romance') ) NOT NULL DEFAULT 'action',
  `director` varchar(100) NOT NULL,
  `producer` varchar(100) NOT NULL,
  `synopsis` varchar(1024) NOT NULL,
  'cast' varchar(1024) NOT NULL,
  `picture` varchar(100) NOT NULL,
  `video` varchar(100) NOT NULL,
  `duration_as_minutes` int(11) NOT NULL,
  `rating` TEXT CHECK( rating IN ('G','PG','PG-13','R','NC-17','NR') ) NOT NULL DEFAULT 'PG',
  `status` TEXT CHECK( status IN ('active', 'inactive') ) NOT NULL DEFAULT 'inactive'

)
