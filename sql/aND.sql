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
  `group_name` varchar(50) NOT NULL,
  `FK_lab_id` int(11) NOT NULL,
  `layer_name` varchar(25) NOT NULL,
  `description` varchar(2001) DEFAULT NULL,
  `url` varchar(2001) DEFAULT NULL,
  `thumbnail_url` varchar(2001) DEFAULT NULL,
  `layer_type` varchar(25) NOT NULL,
  `cross_section_orientation` varchar(255) DEFAULT NULL,
  `resolution` float NOT NULL DEFAULT 0,
  `zresolution` float NOT NULL DEFAULT 0,
  `width` int(11) NOT NULL DEFAULT 60000,
  `height` int(11) NOT NULL DEFAULT 30000,
  `depth` int(11) NOT NULL DEFAULT 450,
  `active` tinyint(4) NOT NULL DEFAULT 1,
  `created` datetime NOT NULL,
  `updated` timestamp NULL DEFAULT current_timestamp(),
  PRIMARY KEY (`id`),
  KEY `K__available_nd_lab_id` (`FK_lab_id`),
  KEY `K__AND_group_name` (`group_name`),
  CONSTRAINT `FK__available_nd_lab_id` FOREIGN KEY (`FK_lab_id`) REFERENCES `auth_lab` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=67 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `available_neuroglancer_data`
--

LOCK TABLES `available_neuroglancer_data` WRITE;
/*!40000 ALTER TABLE `available_neuroglancer_data` DISABLE KEYS */;
INSERT INTO `available_neuroglancer_data` VALUES (1,'DK39',2,'C1',NULL,'https://activebrainatlas.ucsd.edu/data/DK39/neuroglancer_data/C1',NULL,'image',NULL,0.325,10,60000,30000,450,1,'2022-04-15 00:48:11','2022-04-21 02:20:51'),(2,'DK39',2,'C2',NULL,'https://activebrainatlas.ucsd.edu/data/DK39/neuroglancer_data/C2',NULL,'image',NULL,0.325,10,60000,30000,450,1,'2022-04-15 00:48:11','2022-04-21 02:20:51'),(3,'DK39',2,'C3',NULL,'https://activebrainatlas.ucsd.edu/data/DK39/neuroglancer_data/C3',NULL,'image',NULL,0.325,10,60000,30000,450,1,'2022-04-15 00:48:11','2022-04-21 02:20:51'),(4,'DK40',2,'C2',NULL,'https://activebrainatlas.ucsd.edu/data/DK40/neuroglancer_data/C2',NULL,'image',NULL,0.325,10,60000,30000,450,1,'2022-04-15 00:48:11','2022-04-21 02:20:51'),(5,'DK40',2,'C1',NULL,'https://activebrainatlas.ucsd.edu/data/DK40/neuroglancer_data/C1',NULL,'image',NULL,0.325,10,60000,30000,450,1,'2022-04-15 00:48:11','2022-04-21 02:20:51'),(6,'DK40',2,'C3',NULL,'https://activebrainatlas.ucsd.edu/data/DK40/neuroglancer_data/C3',NULL,'image',NULL,0.325,10,60000,30000,450,1,'2022-04-15 00:48:11','2022-04-21 02:20:51'),(7,'DK41',2,'C2',NULL,'https://activebrainatlas.ucsd.edu/data/DK41/neuroglancer_data/C2',NULL,'image',NULL,0.325,10,60000,30000,450,1,'2022-04-15 00:48:11','2022-04-21 02:20:51'),(8,'DK41',2,'C1',NULL,'https://activebrainatlas.ucsd.edu/data/DK41/neuroglancer_data/C1',NULL,'image',NULL,0.325,10,60000,30000,450,1,'2022-04-15 00:48:11','2022-04-21 02:20:51'),(9,'DK41',2,'C3',NULL,'https://activebrainatlas.ucsd.edu/data/DK41/neuroglancer_data/C3',NULL,'image',NULL,0.325,10,60000,30000,450,1,'2022-04-15 00:48:11','2022-04-21 02:20:51'),(10,'DK43',2,'C3',NULL,'https://activebrainatlas.ucsd.edu/data/DK43/neuroglancer_data/C3',NULL,'image',NULL,0.325,10,60000,30000,450,1,'2022-04-15 00:48:11','2022-04-21 02:20:51'),(11,'DK43',2,'C1',NULL,'https://activebrainatlas.ucsd.edu/data/DK43/neuroglancer_data/C1',NULL,'image',NULL,0.325,10,60000,30000,450,1,'2022-04-15 00:48:11','2022-04-21 02:20:51'),(12,'DK43',2,'C2',NULL,'https://activebrainatlas.ucsd.edu/data/DK43/neuroglancer_data/C2',NULL,'image',NULL,0.325,10,60000,30000,450,1,'2022-04-15 00:48:11','2022-04-21 02:20:51'),(13,'DK46',2,'C3',NULL,'https://activebrainatlas.ucsd.edu/data/DK46/neuroglancer_data/C3',NULL,'image',NULL,0.325,10,60000,30000,450,1,'2022-04-15 00:48:11','2022-04-21 02:20:51'),(14,'DK46',2,'C2',NULL,'https://activebrainatlas.ucsd.edu/data/DK46/neuroglancer_data/C2',NULL,'image',NULL,0.325,10,60000,30000,450,1,'2022-04-15 00:48:11','2022-04-21 02:20:51'),(15,'DK46',2,'C1',NULL,'https://activebrainatlas.ucsd.edu/data/DK46/neuroglancer_data/C1',NULL,'image',NULL,0.325,10,60000,30000,450,1,'2022-04-15 00:48:11','2022-04-21 02:20:51'),(16,'DK50',2,'C3',NULL,'https://activebrainatlas.ucsd.edu/data/DK50/neuroglancer_data/C3',NULL,'image',NULL,0.325,10,60000,30000,450,1,'2022-04-15 00:48:11','2022-04-21 02:20:51'),(17,'DK50',2,'C2',NULL,'https://activebrainatlas.ucsd.edu/data/DK50/neuroglancer_data/C2',NULL,'image',NULL,0.325,10,60000,30000,450,1,'2022-04-15 00:48:11','2022-04-21 02:20:51'),(18,'DK50',2,'C1',NULL,'https://activebrainatlas.ucsd.edu/data/DK50/neuroglancer_data/C1',NULL,'image',NULL,0.325,10,60000,30000,450,1,'2022-04-15 00:48:11','2022-04-21 02:20:51'),(19,'DK52',2,'C2',NULL,'https://activebrainatlas.ucsd.edu/data/DK52/neuroglancer_data/C2',NULL,'image',NULL,0.325,10,60000,30000,450,1,'2022-04-15 00:48:11','2022-04-21 02:20:51'),(20,'DK52',2,'C1',NULL,'https://activebrainatlas.ucsd.edu/data/DK52/neuroglancer_data/C1',NULL,'image',NULL,0.325,10,60000,30000,450,1,'2022-04-15 00:48:11','2022-04-21 02:20:51'),(21,'DK52',2,'C3',NULL,'https://activebrainatlas.ucsd.edu/data/DK52/neuroglancer_data/C3',NULL,'image',NULL,0.325,10,60000,30000,450,1,'2022-04-15 00:48:11','2022-04-21 02:20:51'),(22,'DK54',2,'C2',NULL,'https://activebrainatlas.ucsd.edu/data/DK54/neuroglancer_data/C2',NULL,'image',NULL,0.325,10,60000,30000,450,1,'2022-04-15 00:48:11','2022-04-21 02:20:51'),(23,'DK54',2,'C1',NULL,'https://activebrainatlas.ucsd.edu/data/DK54/neuroglancer_data/C1',NULL,'image',NULL,0.325,10,60000,30000,450,1,'2022-04-15 00:48:11','2022-04-21 02:20:51'),(24,'DK54',2,'C3',NULL,'https://activebrainatlas.ucsd.edu/data/DK54/neuroglancer_data/C3',NULL,'image',NULL,0.325,10,60000,30000,450,1,'2022-04-15 00:48:11','2022-04-21 02:20:51'),(25,'DK55',2,'C1',NULL,'https://activebrainatlas.ucsd.edu/data/DK55/neuroglancer_data/C1',NULL,'image',NULL,0.325,10,60000,30000,450,1,'2022-04-15 00:48:11','2022-04-21 02:20:51'),(26,'DK55',2,'C2',NULL,'https://activebrainatlas.ucsd.edu/data/DK55/neuroglancer_data/C2',NULL,'image',NULL,0.325,10,60000,30000,450,1,'2022-04-15 00:48:11','2022-04-21 02:20:51'),(27,'DK55',2,'C3',NULL,'https://activebrainatlas.ucsd.edu/data/DK55/neuroglancer_data/C3',NULL,'image',NULL,0.325,10,60000,30000,450,1,'2022-04-15 00:48:11','2022-04-21 02:20:51'),(28,'DK60',2,'C2',NULL,'https://activebrainatlas.ucsd.edu/data/DK60/neuroglancer_data/C2',NULL,'image',NULL,0.325,10,60000,30000,450,1,'2022-04-15 00:48:11','2022-04-21 02:20:51'),(29,'DK60',2,'C1',NULL,'https://activebrainatlas.ucsd.edu/data/DK60/neuroglancer_data/C1',NULL,'image',NULL,0.325,10,60000,30000,450,1,'2022-04-15 00:48:11','2022-04-21 02:20:51'),(30,'DK60',2,'C3',NULL,'https://activebrainatlas.ucsd.edu/data/DK60/neuroglancer_data/C3',NULL,'image',NULL,0.325,10,60000,30000,450,1,'2022-04-15 00:48:11','2022-04-21 02:20:51'),(31,'DK61',2,'C3',NULL,'https://activebrainatlas.ucsd.edu/data/DK61/neuroglancer_data/C3',NULL,'image',NULL,0.325,10,60000,30000,450,1,'2022-04-15 00:48:11','2022-04-21 02:20:51'),(32,'DK61',2,'C2',NULL,'https://activebrainatlas.ucsd.edu/data/DK61/neuroglancer_data/C2',NULL,'image',NULL,0.325,10,60000,30000,450,1,'2022-04-15 00:48:11','2022-04-21 02:20:51'),(33,'DK61',2,'C1',NULL,'https://activebrainatlas.ucsd.edu/data/DK61/neuroglancer_data/C1',NULL,'image',NULL,0.325,10,60000,30000,450,1,'2022-04-15 00:48:11','2022-04-21 02:20:51'),(34,'DK62',2,'C2',NULL,'https://activebrainatlas.ucsd.edu/data/DK62/neuroglancer_data/C2',NULL,'image',NULL,0.325,10,60000,30000,450,1,'2022-04-15 00:48:11','2022-04-21 02:20:51'),(35,'DK62',2,'C1',NULL,'https://activebrainatlas.ucsd.edu/data/DK62/neuroglancer_data/C1',NULL,'image',NULL,0.325,10,60000,30000,450,1,'2022-04-15 00:48:11','2022-04-21 02:20:51'),(36,'DK62',2,'C3',NULL,'https://activebrainatlas.ucsd.edu/data/DK62/neuroglancer_data/C3',NULL,'image',NULL,0.325,10,60000,30000,450,1,'2022-04-15 00:48:11','2022-04-21 02:20:51'),(37,'DK63',2,'C2',NULL,'https://activebrainatlas.ucsd.edu/data/DK63/neuroglancer_data/C2',NULL,'image',NULL,0.325,10,60000,30000,450,1,'2022-04-15 00:48:11','2022-04-21 02:20:51'),(38,'DK63',2,'C1',NULL,'https://activebrainatlas.ucsd.edu/data/DK63/neuroglancer_data/C1',NULL,'image',NULL,0.325,10,60000,30000,450,1,'2022-04-15 00:48:11','2022-04-21 02:20:51'),(39,'DK73',2,'C1',NULL,'https://activebrainatlas.ucsd.edu/data/DK73/neuroglancer_data/C1',NULL,'image',NULL,0.325,10,60000,30000,450,1,'2022-04-15 00:48:11','2022-04-21 02:20:51'),(64,'Princeton',1,'Atlas','Allen atlas from 2017','https://lightsheetatlas.pni.princeton.edu/public/allenatlas_2017','Princeton.Atlas.png','segmentation',NULL,25,25,60000,30000,450,1,'2022-05-20 03:28:05','2022-05-20 03:28:05'),(65,'UCSD',2,'Atlas','Version 7 of UCSD atlas','https://activebrainatlas.ucsd.edu/data/structures/atlasV7','UCSD.Atlas.png','segmentation',NULL,10,20,1000,1000,300,1,'2022-05-20 03:29:03','2022-05-26 02:38:01'),(66,'DKX',2,'3D_Vascular','A 3D representation of the entire vascular system of a mouse.','https://activebrainatlas.ucsd.edu/data/X/neuroglancer_data/mesh_10','DKX.3D_Vascular.png','segmentation',NULL,10,10,1036,789,1332,1,'2022-05-24 19:14:27','2022-05-26 01:58:53');
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

-- Dump completed on 2022-05-26 13:59:54
