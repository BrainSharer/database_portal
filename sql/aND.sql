-- MySQL dump 10.19  Distrib 10.3.34-MariaDB, for debian-linux-gnu (x86_64)
--
-- Host: localhost    Database: brainsharer
-- ------------------------------------------------------
-- Server version	10.3.34-MariaDB-0ubuntu0.20.04.1

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `available_neuroglancer_data`
--

DROP TABLE IF EXISTS `available_neuroglancer_data`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `available_neuroglancer_data` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `FK_animal_id` int(11) NOT NULL,
  `FK_lab_id` int(11) NOT NULL,
  `layer_name` varchar(25) NOT NULL,
  `description` varchar(2001) DEFAULT NULL,
  `url` varchar(2001) DEFAULT NULL,
  `layer_type` varchar(25) NOT NULL,
  `resolution` float NOT NULL DEFAULT 0,
  `zresolution` float NOT NULL DEFAULT 0,
  `active` tinyint(4) NOT NULL DEFAULT 1,
  `created` datetime NOT NULL,
  `updated` timestamp NULL DEFAULT current_timestamp(),
  PRIMARY KEY (`id`),
  KEY `K__available_nd_animal_id` (`FK_animal_id`),
  KEY `K__available_nd_lab_id` (`FK_lab_id`),
  CONSTRAINT `FK__available_nd_animal_id` FOREIGN KEY (`FK_animal_id`) REFERENCES `biosource` (`id`),
  CONSTRAINT `FK__available_nd_lab_id` FOREIGN KEY (`FK_lab_id`) REFERENCES `auth_lab` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=64 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `available_neuroglancer_data`
--

LOCK TABLES `available_neuroglancer_data` WRITE;
/*!40000 ALTER TABLE `available_neuroglancer_data` DISABLE KEYS */;
INSERT INTO `available_neuroglancer_data` VALUES (1,4,2,'C1',NULL,'https://activebrainatlas.ucsd.edu/data/DK39/neuroglancer_data/C1','image',0.325,10,1,'2022-04-15 00:48:11','2022-04-21 02:20:51'),(2,4,2,'C2',NULL,'https://activebrainatlas.ucsd.edu/data/DK39/neuroglancer_data/C2','image',0.325,10,1,'2022-04-15 00:48:11','2022-04-21 02:20:51'),(3,4,2,'C3',NULL,'https://activebrainatlas.ucsd.edu/data/DK39/neuroglancer_data/C3','image',0.325,10,1,'2022-04-15 00:48:11','2022-04-21 02:20:51'),(4,5,2,'C2',NULL,'https://activebrainatlas.ucsd.edu/data/DK40/neuroglancer_data/C2','image',0.325,10,1,'2022-04-15 00:48:11','2022-04-21 02:20:51'),(5,5,2,'C1',NULL,'https://activebrainatlas.ucsd.edu/data/DK40/neuroglancer_data/C1','image',0.325,10,1,'2022-04-15 00:48:11','2022-04-21 02:20:51'),(6,5,2,'C3',NULL,'https://activebrainatlas.ucsd.edu/data/DK40/neuroglancer_data/C3','image',0.325,10,1,'2022-04-15 00:48:11','2022-04-21 02:20:51'),(7,6,2,'C2',NULL,'https://activebrainatlas.ucsd.edu/data/DK41/neuroglancer_data/C2','image',0.325,10,1,'2022-04-15 00:48:11','2022-04-21 02:20:51'),(8,6,2,'C1',NULL,'https://activebrainatlas.ucsd.edu/data/DK41/neuroglancer_data/C1','image',0.325,10,1,'2022-04-15 00:48:11','2022-04-21 02:20:51'),(9,6,2,'C3',NULL,'https://activebrainatlas.ucsd.edu/data/DK41/neuroglancer_data/C3','image',0.325,10,1,'2022-04-15 00:48:11','2022-04-21 02:20:51'),(10,7,2,'C3',NULL,'https://activebrainatlas.ucsd.edu/data/DK43/neuroglancer_data/C3','image',0.325,10,1,'2022-04-15 00:48:11','2022-04-21 02:20:51'),(11,7,2,'C1',NULL,'https://activebrainatlas.ucsd.edu/data/DK43/neuroglancer_data/C1','image',0.325,10,1,'2022-04-15 00:48:11','2022-04-21 02:20:51'),(12,7,2,'C2',NULL,'https://activebrainatlas.ucsd.edu/data/DK43/neuroglancer_data/C2','image',0.325,10,1,'2022-04-15 00:48:11','2022-04-21 02:20:51'),(13,8,2,'C3',NULL,'https://activebrainatlas.ucsd.edu/data/DK46/neuroglancer_data/C3','image',0.325,10,1,'2022-04-15 00:48:11','2022-04-21 02:20:51'),(14,8,2,'C2',NULL,'https://activebrainatlas.ucsd.edu/data/DK46/neuroglancer_data/C2','image',0.325,10,1,'2022-04-15 00:48:11','2022-04-21 02:20:51'),(15,8,2,'C1',NULL,'https://activebrainatlas.ucsd.edu/data/DK46/neuroglancer_data/C1','image',0.325,10,1,'2022-04-15 00:48:11','2022-04-21 02:20:51'),(16,9,2,'C3',NULL,'https://activebrainatlas.ucsd.edu/data/DK50/neuroglancer_data/C3','image',0.325,10,1,'2022-04-15 00:48:11','2022-04-21 02:20:51'),(17,9,2,'C2',NULL,'https://activebrainatlas.ucsd.edu/data/DK50/neuroglancer_data/C2','image',0.325,10,1,'2022-04-15 00:48:11','2022-04-21 02:20:51'),(18,9,2,'C1',NULL,'https://activebrainatlas.ucsd.edu/data/DK50/neuroglancer_data/C1','image',0.325,10,1,'2022-04-15 00:48:11','2022-04-21 02:20:51'),(19,1,2,'C2',NULL,'https://activebrainatlas.ucsd.edu/data/DK52/neuroglancer_data/C2','image',0.325,10,1,'2022-04-15 00:48:11','2022-04-21 02:20:51'),(20,1,2,'C1',NULL,'https://activebrainatlas.ucsd.edu/data/DK52/neuroglancer_data/C1','image',0.325,10,1,'2022-04-15 00:48:11','2022-04-21 02:20:51'),(21,1,2,'C3',NULL,'https://activebrainatlas.ucsd.edu/data/DK52/neuroglancer_data/C3','image',0.325,10,1,'2022-04-15 00:48:11','2022-04-21 02:20:51'),(22,11,2,'C2',NULL,'https://activebrainatlas.ucsd.edu/data/DK54/neuroglancer_data/C2','image',0.325,10,1,'2022-04-15 00:48:11','2022-04-21 02:20:51'),(23,11,2,'C1',NULL,'https://activebrainatlas.ucsd.edu/data/DK54/neuroglancer_data/C1','image',0.325,10,1,'2022-04-15 00:48:11','2022-04-21 02:20:51'),(24,11,2,'C3',NULL,'https://activebrainatlas.ucsd.edu/data/DK54/neuroglancer_data/C3','image',0.325,10,1,'2022-04-15 00:48:11','2022-04-21 02:20:51'),(25,12,2,'C1',NULL,'https://activebrainatlas.ucsd.edu/data/DK55/neuroglancer_data/C1','image',0.325,10,1,'2022-04-15 00:48:11','2022-04-21 02:20:51'),(26,12,2,'C2',NULL,'https://activebrainatlas.ucsd.edu/data/DK55/neuroglancer_data/C2','image',0.325,10,1,'2022-04-15 00:48:11','2022-04-21 02:20:51'),(27,12,2,'C3',NULL,'https://activebrainatlas.ucsd.edu/data/DK55/neuroglancer_data/C3','image',0.325,10,1,'2022-04-15 00:48:11','2022-04-21 02:20:51'),(28,13,2,'C2',NULL,'https://activebrainatlas.ucsd.edu/data/DK60/neuroglancer_data/C2','image',0.325,10,1,'2022-04-15 00:48:11','2022-04-21 02:20:51'),(29,13,2,'C1',NULL,'https://activebrainatlas.ucsd.edu/data/DK60/neuroglancer_data/C1','image',0.325,10,1,'2022-04-15 00:48:11','2022-04-21 02:20:51'),(30,13,2,'C3',NULL,'https://activebrainatlas.ucsd.edu/data/DK60/neuroglancer_data/C3','image',0.325,10,1,'2022-04-15 00:48:11','2022-04-21 02:20:51'),(31,14,2,'C3',NULL,'https://activebrainatlas.ucsd.edu/data/DK61/neuroglancer_data/C3','image',0.325,10,1,'2022-04-15 00:48:11','2022-04-21 02:20:51'),(32,14,2,'C2',NULL,'https://activebrainatlas.ucsd.edu/data/DK61/neuroglancer_data/C2','image',0.325,10,1,'2022-04-15 00:48:11','2022-04-21 02:20:51'),(33,14,2,'C1',NULL,'https://activebrainatlas.ucsd.edu/data/DK61/neuroglancer_data/C1','image',0.325,10,1,'2022-04-15 00:48:11','2022-04-21 02:20:51'),(34,15,2,'C2',NULL,'https://activebrainatlas.ucsd.edu/data/DK62/neuroglancer_data/C2','image',0.325,10,1,'2022-04-15 00:48:11','2022-04-21 02:20:51'),(35,15,2,'C1',NULL,'https://activebrainatlas.ucsd.edu/data/DK62/neuroglancer_data/C1','image',0.325,10,1,'2022-04-15 00:48:11','2022-04-21 02:20:51'),(36,15,2,'C3',NULL,'https://activebrainatlas.ucsd.edu/data/DK62/neuroglancer_data/C3','image',0.325,10,1,'2022-04-15 00:48:11','2022-04-21 02:20:51'),(37,16,2,'C2',NULL,'https://activebrainatlas.ucsd.edu/data/DK63/neuroglancer_data/C2','image',0.325,10,1,'2022-04-15 00:48:11','2022-04-21 02:20:51'),(38,16,2,'C1',NULL,'https://activebrainatlas.ucsd.edu/data/DK63/neuroglancer_data/C1','image',0.325,10,1,'2022-04-15 00:48:11','2022-04-21 02:20:51'),(39,17,2,'C1',NULL,'https://activebrainatlas.ucsd.edu/data/DK73/neuroglancer_data/C1','image',0.325,10,1,'2022-04-15 00:48:11','2022-04-21 02:20:51');
/*!40000 ALTER TABLE `available_neuroglancer_data` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2022-04-21 11:34:15
