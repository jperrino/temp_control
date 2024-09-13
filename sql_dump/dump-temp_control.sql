--
-- Create Database
--

CREATE DATABASE temp_control;

--
-- Table structure for table `chat_session`
--

DROP TABLE IF EXISTS `chat_session`;
CREATE TABLE `chat_session` (
  `id` int NOT NULL AUTO_INCREMENT,
  `phone_number` varchar(100) NOT NULL,
  `device` varchar(100) DEFAULT NULL,
  `created_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `end_time` timestamp NOT NULL,
  `flow_id` int DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `flow_FK` (`flow_id`),
  CONSTRAINT `flow_FK` FOREIGN KEY (`flow_id`) REFERENCES `flow` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=63 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Table structure for table `device`
--

DROP TABLE IF EXISTS `device`;
CREATE TABLE `device` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(100) NOT NULL,
  `created_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `temp_range_min` float DEFAULT NULL,
  `temp_range_max` float DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `device`
--

LOCK TABLES `device` WRITE;
INSERT INTO `device` VALUES (1,'test1','2023-07-17 06:22:47',17.4,25.4),(2,'test2','2023-07-17 06:43:13',NULL,NULL),(3,'test3','2023-07-17 06:46:36',NULL,NULL),(4,'test4','2023-07-28 22:51:07',NULL,NULL),(5,'test7','2023-09-10 17:30:13',10,21),(6,'test8','2023-09-20 22:44:16',10,15);
UNLOCK TABLES;

--
-- Table structure for table `flow`
--

DROP TABLE IF EXISTS `flow`;
CREATE TABLE `flow` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(100) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `flow`
--

LOCK TABLES `flow` WRITE;
INSERT INTO `flow` VALUES (1,'STARTED'),(2,'REQUEST_GRAPH'),(3,'SET_MIN_TEMPERATURE'),(4,'SET_MAX_TEMPERATURE'),(5,'COMPLETED');
UNLOCK TABLES;

--
-- Table structure for table `measure`
--

DROP TABLE IF EXISTS `measure`;
CREATE TABLE `measure` (
  `id` int NOT NULL AUTO_INCREMENT,
  `temperature` float NOT NULL,
  `created_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `device_id` int NOT NULL,
  PRIMARY KEY (`id`),
  KEY `measure_FK` (`device_id`),
  CONSTRAINT `measure_FK` FOREIGN KEY (`device_id`) REFERENCES `device` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=476 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
