-- MySQL dump 10.19  Distrib 10.3.32-MariaDB, for debian-linux-gnu (x86_64)
--
-- Host: localhost    Database: brainsharer
-- ------------------------------------------------------
-- Server version 10.3.32-MariaDB-0ubuntu0.20.04.1

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
-- Dumping data for table `authentication_lab`
--

LOCK TABLES `authentication_lab` WRITE;
/*!40000 ALTER TABLE `authentication_lab` DISABLE KEYS */;
insert into authentication_lab (lab_name,active,created,lab_url) values ('Princeton',1,NOW(),'https://princeton.edu');
insert into authentication_lab (lab_name,active,created,lab_url) values ('UCSD',1,NOW(),'https://activebrainatlas.ucsd.edu/data');
insert into authentication_lab (lab_name,active,created,lab_url) values ('Duke',1,NOW(),'https://duke.edu');
/*!40000 ALTER TABLE `authentication_lab` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping data for table `biocyc`
--

LOCK TABLES `biocyc` WRITE;
/*!40000 ALTER TABLE `biocyc` DISABLE KEYS */;
insert into biocyc (id, bio_name, active, created) values (1, 'mouse', 1, NOW());
/*!40000 ALTER TABLE `biocyc` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping data for table `biosource`
--

LOCK TABLES `biosource` WRITE;
/*!40000 ALTER TABLE `biosource` DISABLE KEYS */;
insert into biosource (animal, active, created, lab_id, FK_ORGID) values ('DK52',1,NOW(),2,1);
/*!40000 ALTER TABLE `biosource` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping data for table `biosource`
--

LOCK TABLES `brain_region` WRITE;
/*!40000 ALTER TABLE `brain_region` DISABLE KEYS */;
insert into brain_region (abbreviation,description,active,created) values ('point','Point data described by x,y,z',1,NOW());
/*!40000 ALTER TABLE `brain_region` ENABLE KEYS */;
UNLOCK TABLES;



--
-- Dumping data for table `account_emailaddress`
--

LOCK TABLES `account_emailaddress` WRITE;
/*!40000 ALTER TABLE `account_emailaddress` DISABLE KEYS */;
INSERT INTO `account_emailaddress` VALUES (2,'duane.rinehart@gmail.com',1,1,3);
INSERT INTO `account_emailaddress` VALUES (3,'austinthomashoag@gmail.com',1,1,4);
INSERT INTO `account_emailaddress` VALUES (4,'eddy.odonnell@gmail.com',1,1,5);
/*!40000 ALTER TABLE `account_emailaddress` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping data for table `auth_group`
--

LOCK TABLES `auth_group` WRITE;
/*!40000 ALTER TABLE `auth_group` DISABLE KEYS */;
INSERT INTO `auth_group` VALUES (1,'Neuroglancer Editor');
/*!40000 ALTER TABLE `auth_group` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping data for table `auth_group_permissions`
--

LOCK TABLES `auth_group_permissions` WRITE;
/*!40000 ALTER TABLE `auth_group_permissions` DISABLE KEYS */;
INSERT INTO `auth_group_permissions` VALUES (1,1,57);
INSERT INTO `auth_group_permissions` VALUES (2,1,58);
INSERT INTO `auth_group_permissions` VALUES (3,1,60);
/*!40000 ALTER TABLE `auth_group_permissions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping data for table `authentication_user`
--

LOCK TABLES `authentication_user` WRITE;
/*!40000 ALTER TABLE `authentication_user` DISABLE KEYS */;
INSERT INTO `authentication_user` VALUES (3,'!Q1wUD2JtkyjwWe0BxbQMRf25qVhNYw5HRtuVclLn','2021-12-23 12:25:36.000000',1,'duane','Duane','Rinehart','duane.rinehart@gmail.com',1,1,'2021-12-23 12:25:36.000000',2);
INSERT INTO `authentication_user` VALUES (4,'!j24nsBxqlWcn6B0DbjnUYbZuYZ456EXsaI7dlRO7','2021-12-23 14:17:53.616047',1,'austin','Austin','Hoag','austinthomashoag@gmail.com',1,1,'2021-12-23 12:34:29.000000',1);
/*!40000 ALTER TABLE `authentication_user` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping data for table `authentication_user_labs`
--

LOCK TABLES `authentication_user_labs` WRITE;
/*!40000 ALTER TABLE `authentication_user_labs` DISABLE KEYS */;
INSERT INTO `authentication_user_labs` VALUES (2,3,1);
INSERT INTO `authentication_user_labs` VALUES (3,3,2);
INSERT INTO `authentication_user_labs` VALUES (4,3,3);
INSERT INTO `authentication_user_labs` VALUES (5,4,1);
INSERT INTO `authentication_user_labs` VALUES (6,4,2);
INSERT INTO `authentication_user_labs` VALUES (7,4,3);
/*!40000 ALTER TABLE `authentication_user_labs` ENABLE KEYS */;
UNLOCK TABLES;


--
-- Dumping data for table `django_site`
--

LOCK TABLES `django_site` WRITE;
/*!40000 ALTER TABLE `django_site` DISABLE KEYS */;
INSERT INTO `django_site` VALUES (3,'https://www.brainsharer.org','https://www.brainsharer.org');
/*!40000 ALTER TABLE `django_site` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping data for table `input_type`
--

LOCK TABLES `input_type` WRITE;
/*!40000 ALTER TABLE `input_type` DISABLE KEYS */;
INSERT INTO `input_type` VALUES (1,'manual','Data entered by user in Neuroglancer',1,'2021-12-23 14:58:04.000000','2021-12-23 14:58:04.000000');
INSERT INTO `input_type` VALUES (2,'detected','Data created by scripts',1,'2021-12-23 14:58:04.000000','2021-12-23 14:58:04.000000');
/*!40000 ALTER TABLE `input_type` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping data for table `scan_run`
--

LOCK TABLES `scan_run` WRITE;
/*!40000 ALTER TABLE `scan_run` DISABLE KEYS */;
INSERT INTO `scan_run` VALUES (1,1,'2021-12-23 12:24:04.916298','60X',0.325,20,100,NULL,NULL,NULL,60000,35000,'',1);
/*!40000 ALTER TABLE `scan_run` ENABLE KEYS */;
UNLOCK TABLES;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2021-12-24 14:20:28