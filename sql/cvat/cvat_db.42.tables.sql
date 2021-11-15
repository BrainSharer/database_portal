-- MariaDB dump 10.17  Distrib 10.4.13-MariaDB, for Linux (x86_64)
--
-- Host: 192.168.1.12    Database: cvat_db
-- ------------------------------------------------------
-- Server version	10.4.13-MariaDB-log

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `account_emailaddress`
--

DROP TABLE IF EXISTS `account_emailaddress`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `account_emailaddress` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `email` varchar(254) NOT NULL,
  `verified` tinyint(1) NOT NULL,
  `primary` tinyint(1) NOT NULL,
  `user_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `email` (`email`),
  KEY `account_emailaddress_user_id_2c513194_fk_auth_user_id` (`user_id`),
  CONSTRAINT `account_emailaddress_user_id_2c513194_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `account_emailconfirmation`
--

DROP TABLE IF EXISTS `account_emailconfirmation`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `account_emailconfirmation` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `created` datetime(6) NOT NULL,
  `sent` datetime(6) DEFAULT NULL,
  `key` varchar(64) NOT NULL,
  `email_address_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `key` (`key`),
  KEY `account_emailconfirm_email_address_id_5b7f8c58_fk_account_e` (`email_address_id`),
  CONSTRAINT `account_emailconfirm_email_address_id_5b7f8c58_fk_account_e` FOREIGN KEY (`email_address_id`) REFERENCES `account_emailaddress` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `auth_group`
--

DROP TABLE IF EXISTS `auth_group`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_group` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(150) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `auth_group_permissions`
--

DROP TABLE IF EXISTS `auth_group_permissions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_group_permissions` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `group_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_group_permissions_group_id_permission_id_0cd325b0_uniq` (`group_id`,`permission_id`),
  KEY `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` (`permission_id`),
  CONSTRAINT `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `auth_group_permissions_group_id_b120cbf9_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `auth_permission`
--

DROP TABLE IF EXISTS `auth_permission`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_permission` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `content_type_id` int(11) NOT NULL,
  `codename` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_permission_content_type_id_codename_01ab375a_uniq` (`content_type_id`,`codename`),
  CONSTRAINT `auth_permission_content_type_id_2f476e4b_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=61 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `auth_user`
--

DROP TABLE IF EXISTS `auth_user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_user` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `password` varchar(128) NOT NULL,
  `last_login` datetime(6) DEFAULT NULL,
  `is_superuser` tinyint(1) NOT NULL,
  `username` varchar(150) NOT NULL,
  `first_name` varchar(30) NOT NULL,
  `last_name` varchar(150) NOT NULL,
  `email` varchar(254) NOT NULL,
  `is_staff` tinyint(1) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `date_joined` datetime(6) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`)
) ENGINE=InnoDB AUTO_INCREMENT=24 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `auth_user_groups`
--

DROP TABLE IF EXISTS `auth_user_groups`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_user_groups` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `group_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_user_groups_user_id_group_id_94350c0c_uniq` (`user_id`,`group_id`),
  KEY `auth_user_groups_group_id_97559544_fk_auth_group_id` (`group_id`),
  CONSTRAINT `auth_user_groups_group_id_97559544_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`),
  CONSTRAINT `auth_user_groups_user_id_6a12ed8b_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `auth_user_user_permissions`
--

DROP TABLE IF EXISTS `auth_user_user_permissions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_user_user_permissions` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_user_user_permissions_user_id_permission_id_14a6b632_uniq` (`user_id`,`permission_id`),
  KEY `auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm` (`permission_id`),
  CONSTRAINT `auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `auth_user_user_permissions_user_id_a95ead1b_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `authtoken_token`
--

DROP TABLE IF EXISTS `authtoken_token`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `authtoken_token` (
  `key` varchar(40) NOT NULL,
  `created` datetime(6) NOT NULL,
  `user_id` int(11) NOT NULL,
  PRIMARY KEY (`key`),
  UNIQUE KEY `user_id` (`user_id`),
  CONSTRAINT `authtoken_token_user_id_35299eff_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `django_admin_log`
--

DROP TABLE IF EXISTS `django_admin_log`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `django_admin_log` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `action_time` datetime(6) NOT NULL,
  `object_id` longtext DEFAULT NULL,
  `object_repr` varchar(200) NOT NULL,
  `action_flag` smallint(5) unsigned NOT NULL CHECK (`action_flag` >= 0),
  `change_message` longtext NOT NULL,
  `content_type_id` int(11) DEFAULT NULL,
  `user_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `django_admin_log_content_type_id_c4bce8eb_fk_django_co` (`content_type_id`),
  KEY `django_admin_log_user_id_c564eba6_fk_auth_user_id` (`user_id`),
  CONSTRAINT `django_admin_log_content_type_id_c4bce8eb_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`),
  CONSTRAINT `django_admin_log_user_id_c564eba6_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `django_content_type`
--

DROP TABLE IF EXISTS `django_content_type`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `django_content_type` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `app_label` varchar(100) NOT NULL,
  `model` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `django_content_type_app_label_model_76bd3d3b_uniq` (`app_label`,`model`)
) ENGINE=InnoDB AUTO_INCREMENT=38 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `django_migrations`
--

DROP TABLE IF EXISTS `django_migrations`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `django_migrations` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `app` varchar(255) NOT NULL,
  `name` varchar(255) NOT NULL,
  `applied` datetime(6) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=29 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `django_session`
--

DROP TABLE IF EXISTS `django_session`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `django_session` (
  `session_key` varchar(40) NOT NULL,
  `session_data` longtext NOT NULL,
  `expire_date` datetime(6) NOT NULL,
  PRIMARY KEY (`session_key`),
  KEY `django_session_expire_date_a5c62663` (`expire_date`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `django_site`
--

DROP TABLE IF EXISTS `django_site`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `django_site` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `domain` varchar(100) NOT NULL,
  `name` varchar(50) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `django_site_domain_a2e37b91_uniq` (`domain`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `engine_attributespec`
--

DROP TABLE IF EXISTS `engine_attributespec`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `engine_attributespec` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(64) NOT NULL,
  `mutable` tinyint(1) NOT NULL,
  `input_type` varchar(16) NOT NULL,
  `default_value` varchar(128) NOT NULL,
  `values` varchar(4096) NOT NULL,
  `label_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `engine_attributespec_label_id_name_d85e616c_uniq` (`label_id`,`name`),
  CONSTRAINT `engine_attributespec_label_id_274838ef_fk_engine_label_id` FOREIGN KEY (`label_id`) REFERENCES `engine_label` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `engine_clientfile`
--

DROP TABLE IF EXISTS `engine_clientfile`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `engine_clientfile` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `file` varchar(1024) NOT NULL,
  `data_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `engine_data`
--

DROP TABLE IF EXISTS `engine_data`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `engine_data` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `chunk_size` int(10) unsigned DEFAULT NULL CHECK (`chunk_size` >= 0),
  `size` int(10) unsigned NOT NULL CHECK (`size` >= 0),
  `image_quality` smallint(5) unsigned NOT NULL CHECK (`image_quality` >= 0),
  `start_frame` int(10) unsigned NOT NULL CHECK (`start_frame` >= 0),
  `stop_frame` int(10) unsigned NOT NULL CHECK (`stop_frame` >= 0),
  `frame_filter` varchar(256) NOT NULL,
  `compressed_chunk_type` varchar(32) NOT NULL,
  `original_chunk_type` varchar(32) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=13 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `engine_image`
--

DROP TABLE IF EXISTS `engine_image`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `engine_image` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `path` varchar(1024) NOT NULL,
  `frame` int(10) unsigned NOT NULL CHECK (`frame` >= 0),
  `width` int(10) unsigned NOT NULL CHECK (`width` >= 0),
  `height` int(10) unsigned NOT NULL CHECK (`height` >= 0),
  `data_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `engine_image_data_id_e89da547_fk_engine_data_id` (`data_id`),
  CONSTRAINT `engine_image_data_id_e89da547_fk_engine_data_id` FOREIGN KEY (`data_id`) REFERENCES `engine_data` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `engine_job`
--

DROP TABLE IF EXISTS `engine_job`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `engine_job` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `status` varchar(32) NOT NULL,
  `assignee_id` int(11) DEFAULT NULL,
  `segment_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `engine_job_segment_id_f615a866_fk_engine_segment_id` (`segment_id`),
  KEY `engine_job_assignee_id_b80bea03_fk_auth_user_id` (`assignee_id`),
  CONSTRAINT `engine_job_assignee_id_b80bea03_fk_auth_user_id` FOREIGN KEY (`assignee_id`) REFERENCES `auth_user` (`id`),
  CONSTRAINT `engine_job_segment_id_f615a866_fk_engine_segment_id` FOREIGN KEY (`segment_id`) REFERENCES `engine_segment` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=10 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `engine_jobcommit`
--

DROP TABLE IF EXISTS `engine_jobcommit`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `engine_jobcommit` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `version` int(10) unsigned NOT NULL CHECK (`version` >= 0),
  `timestamp` datetime(6) NOT NULL,
  `message` varchar(4096) NOT NULL,
  `author_id` int(11) DEFAULT NULL,
  `job_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `engine_jobcommit_author_id_fe2728f3_fk_auth_user_id` (`author_id`),
  KEY `engine_jobcommit_job_id_02b6da1d_fk_engine_job_id` (`job_id`),
  CONSTRAINT `engine_jobcommit_author_id_fe2728f3_fk_auth_user_id` FOREIGN KEY (`author_id`) REFERENCES `auth_user` (`id`),
  CONSTRAINT `engine_jobcommit_job_id_02b6da1d_fk_engine_job_id` FOREIGN KEY (`job_id`) REFERENCES `engine_job` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `engine_label`
--

DROP TABLE IF EXISTS `engine_label`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `engine_label` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(64) NOT NULL,
  `task_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `engine_label_task_id_name_00e8779a_uniq` (`task_id`,`name`),
  CONSTRAINT `engine_label_task_id_f11c5c1a_fk_engine_task_id` FOREIGN KEY (`task_id`) REFERENCES `engine_task` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `engine_labeledimage`
--

DROP TABLE IF EXISTS `engine_labeledimage`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `engine_labeledimage` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `frame` int(10) unsigned NOT NULL CHECK (`frame` >= 0),
  `group` int(10) unsigned DEFAULT NULL CHECK (`group` >= 0),
  `job_id` int(11) NOT NULL,
  `label_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `engine_labeledimage_job_id_7406d161_fk_engine_job_id` (`job_id`),
  KEY `engine_labeledimage_label_id_b22eb9f7_fk_engine_label_id` (`label_id`),
  CONSTRAINT `engine_labeledimage_job_id_7406d161_fk_engine_job_id` FOREIGN KEY (`job_id`) REFERENCES `engine_job` (`id`),
  CONSTRAINT `engine_labeledimage_label_id_b22eb9f7_fk_engine_label_id` FOREIGN KEY (`label_id`) REFERENCES `engine_label` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `engine_labeledimageattributeval`
--

DROP TABLE IF EXISTS `engine_labeledimageattributeval`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `engine_labeledimageattributeval` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `value` varchar(4096) NOT NULL,
  `image_id` bigint(20) NOT NULL,
  `spec_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `engine_labeledimagea_image_id_f4c34a7a_fk_engine_la` (`image_id`),
  KEY `engine_labeledimagea_spec_id_911f524c_fk_engine_at` (`spec_id`),
  CONSTRAINT `engine_labeledimagea_image_id_f4c34a7a_fk_engine_la` FOREIGN KEY (`image_id`) REFERENCES `engine_labeledimage` (`id`),
  CONSTRAINT `engine_labeledimagea_spec_id_911f524c_fk_engine_at` FOREIGN KEY (`spec_id`) REFERENCES `engine_attributespec` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `engine_labeledshape`
--

DROP TABLE IF EXISTS `engine_labeledshape`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `engine_labeledshape` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `frame` int(10) unsigned NOT NULL CHECK (`frame` >= 0),
  `group` int(10) unsigned DEFAULT NULL CHECK (`group` >= 0),
  `type` varchar(16) NOT NULL,
  `occluded` tinyint(1) NOT NULL,
  `z_order` int(11) NOT NULL,
  `points` longtext NOT NULL,
  `job_id` int(11) NOT NULL,
  `label_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `engine_labeledshape_job_id_b7694c3a_fk_engine_job_id` (`job_id`),
  KEY `engine_labeledshape_label_id_872e4658_fk_engine_label_id` (`label_id`),
  CONSTRAINT `engine_labeledshape_job_id_b7694c3a_fk_engine_job_id` FOREIGN KEY (`job_id`) REFERENCES `engine_job` (`id`),
  CONSTRAINT `engine_labeledshape_label_id_872e4658_fk_engine_label_id` FOREIGN KEY (`label_id`) REFERENCES `engine_label` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `engine_labeledshapeattributeval`
--

DROP TABLE IF EXISTS `engine_labeledshapeattributeval`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `engine_labeledshapeattributeval` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `value` varchar(4096) NOT NULL,
  `shape_id` bigint(20) NOT NULL,
  `spec_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `engine_labeledshapea_shape_id_26c4daab_fk_engine_la` (`shape_id`),
  KEY `engine_labeledshapea_spec_id_144b73fa_fk_engine_at` (`spec_id`),
  CONSTRAINT `engine_labeledshapea_shape_id_26c4daab_fk_engine_la` FOREIGN KEY (`shape_id`) REFERENCES `engine_labeledshape` (`id`),
  CONSTRAINT `engine_labeledshapea_spec_id_144b73fa_fk_engine_at` FOREIGN KEY (`spec_id`) REFERENCES `engine_attributespec` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `engine_labeledtrack`
--

DROP TABLE IF EXISTS `engine_labeledtrack`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `engine_labeledtrack` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `frame` int(10) unsigned NOT NULL CHECK (`frame` >= 0),
  `group` int(10) unsigned DEFAULT NULL CHECK (`group` >= 0),
  `job_id` int(11) NOT NULL,
  `label_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `engine_labeledtrack_job_id_e00d9f2f_fk_engine_job_id` (`job_id`),
  KEY `engine_labeledtrack_label_id_75d2c39b_fk_engine_label_id` (`label_id`),
  CONSTRAINT `engine_labeledtrack_job_id_e00d9f2f_fk_engine_job_id` FOREIGN KEY (`job_id`) REFERENCES `engine_job` (`id`),
  CONSTRAINT `engine_labeledtrack_label_id_75d2c39b_fk_engine_label_id` FOREIGN KEY (`label_id`) REFERENCES `engine_label` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `engine_labeledtrackattributeval`
--

DROP TABLE IF EXISTS `engine_labeledtrackattributeval`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `engine_labeledtrackattributeval` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `value` varchar(4096) NOT NULL,
  `spec_id` int(11) NOT NULL,
  `track_id` bigint(20) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `engine_labeledtracka_spec_id_b7ee6fd2_fk_engine_at` (`spec_id`),
  KEY `engine_labeledtracka_track_id_4ed9e160_fk_engine_la` (`track_id`),
  CONSTRAINT `engine_labeledtracka_spec_id_b7ee6fd2_fk_engine_at` FOREIGN KEY (`spec_id`) REFERENCES `engine_attributespec` (`id`),
  CONSTRAINT `engine_labeledtracka_track_id_4ed9e160_fk_engine_la` FOREIGN KEY (`track_id`) REFERENCES `engine_labeledtrack` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `engine_plugin`
--

DROP TABLE IF EXISTS `engine_plugin`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `engine_plugin` (
  `name` varchar(32) NOT NULL,
  `description` varchar(8192) NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  `maintainer_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`name`),
  KEY `engine_plugin_maintainer_id_b9b0530e_fk_auth_user_id` (`maintainer_id`),
  CONSTRAINT `engine_plugin_maintainer_id_b9b0530e_fk_auth_user_id` FOREIGN KEY (`maintainer_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `engine_pluginoption`
--

DROP TABLE IF EXISTS `engine_pluginoption`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `engine_pluginoption` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(32) NOT NULL,
  `value` varchar(1024) NOT NULL,
  `plugin_id` varchar(32) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `engine_pluginoption_plugin_id_569cfeff_fk_engine_plugin_name` (`plugin_id`),
  CONSTRAINT `engine_pluginoption_plugin_id_569cfeff_fk_engine_plugin_name` FOREIGN KEY (`plugin_id`) REFERENCES `engine_plugin` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `engine_project`
--

DROP TABLE IF EXISTS `engine_project`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `engine_project` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(256) NOT NULL,
  `bug_tracker` varchar(2000) NOT NULL,
  `created_date` datetime(6) NOT NULL,
  `updated_date` datetime(6) NOT NULL,
  `status` varchar(32) NOT NULL,
  `assignee_id` int(11) DEFAULT NULL,
  `owner_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `engine_project_assignee_id_77655de8_fk_auth_user_id` (`assignee_id`),
  KEY `engine_project_owner_id_de2a8424_fk_auth_user_id` (`owner_id`),
  CONSTRAINT `engine_project_assignee_id_77655de8_fk_auth_user_id` FOREIGN KEY (`assignee_id`) REFERENCES `auth_user` (`id`),
  CONSTRAINT `engine_project_owner_id_de2a8424_fk_auth_user_id` FOREIGN KEY (`owner_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `engine_remotefile`
--

DROP TABLE IF EXISTS `engine_remotefile`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `engine_remotefile` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `file` varchar(1024) NOT NULL,
  `data_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `engine_remotefile_data_id_ff16acda_fk_engine_data_id` (`data_id`),
  CONSTRAINT `engine_remotefile_data_id_ff16acda_fk_engine_data_id` FOREIGN KEY (`data_id`) REFERENCES `engine_data` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `engine_segment`
--

DROP TABLE IF EXISTS `engine_segment`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `engine_segment` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `start_frame` int(11) NOT NULL,
  `stop_frame` int(11) NOT NULL,
  `task_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `engine_segment_task_id_37d935cf_fk_engine_task_id` (`task_id`),
  CONSTRAINT `engine_segment_task_id_37d935cf_fk_engine_task_id` FOREIGN KEY (`task_id`) REFERENCES `engine_task` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=10 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `engine_serverfile`
--

DROP TABLE IF EXISTS `engine_serverfile`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `engine_serverfile` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `file` varchar(1024) NOT NULL,
  `data_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `engine_serverfile_data_id_2364110a_fk_engine_data_id` (`data_id`),
  CONSTRAINT `engine_serverfile_data_id_2364110a_fk_engine_data_id` FOREIGN KEY (`data_id`) REFERENCES `engine_data` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `engine_task`
--

DROP TABLE IF EXISTS `engine_task`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `engine_task` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(256) NOT NULL,
  `mode` varchar(32) NOT NULL,
  `bug_tracker` varchar(2000) NOT NULL,
  `created_date` datetime(6) NOT NULL,
  `updated_date` datetime(6) NOT NULL,
  `overlap` int(10) unsigned DEFAULT NULL CHECK (`overlap` >= 0),
  `segment_size` int(10) unsigned NOT NULL CHECK (`segment_size` >= 0),
  `z_order` tinyint(1) NOT NULL,
  `status` varchar(32) NOT NULL,
  `assignee_id` int(11) DEFAULT NULL,
  `data_id` int(11) DEFAULT NULL,
  `owner_id` int(11) DEFAULT NULL,
  `project_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `engine_task_assignee_id_51c82720_fk_auth_user_id` (`assignee_id`),
  KEY `engine_task_data_id_e98ffd9b_fk_engine_data_id` (`data_id`),
  KEY `engine_task_owner_id_95de3361_fk_auth_user_id` (`owner_id`),
  KEY `engine_task_project_id_2dced848_fk_engine_project_id` (`project_id`),
  CONSTRAINT `engine_task_assignee_id_51c82720_fk_auth_user_id` FOREIGN KEY (`assignee_id`) REFERENCES `auth_user` (`id`),
  CONSTRAINT `engine_task_data_id_e98ffd9b_fk_engine_data_id` FOREIGN KEY (`data_id`) REFERENCES `engine_data` (`id`),
  CONSTRAINT `engine_task_owner_id_95de3361_fk_auth_user_id` FOREIGN KEY (`owner_id`) REFERENCES `auth_user` (`id`),
  CONSTRAINT `engine_task_project_id_2dced848_fk_engine_project_id` FOREIGN KEY (`project_id`) REFERENCES `engine_project` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=15 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `engine_trackedshape`
--

DROP TABLE IF EXISTS `engine_trackedshape`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `engine_trackedshape` (
  `type` varchar(16) NOT NULL,
  `occluded` tinyint(1) NOT NULL,
  `z_order` int(11) NOT NULL,
  `points` longtext NOT NULL,
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `frame` int(10) unsigned NOT NULL CHECK (`frame` >= 0),
  `outside` tinyint(1) NOT NULL,
  `track_id` bigint(20) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `engine_trackedshape_track_id_a6dc58bd_fk_engine_labeledtrack_id` (`track_id`),
  CONSTRAINT `engine_trackedshape_track_id_a6dc58bd_fk_engine_labeledtrack_id` FOREIGN KEY (`track_id`) REFERENCES `engine_labeledtrack` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `engine_trackedshapeattributeval`
--

DROP TABLE IF EXISTS `engine_trackedshapeattributeval`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `engine_trackedshapeattributeval` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `value` varchar(4096) NOT NULL,
  `shape_id` bigint(20) NOT NULL,
  `spec_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `engine_trackedshapea_shape_id_361f0e2f_fk_engine_tr` (`shape_id`),
  KEY `engine_trackedshapea_spec_id_a944a532_fk_engine_at` (`spec_id`),
  CONSTRAINT `engine_trackedshapea_shape_id_361f0e2f_fk_engine_tr` FOREIGN KEY (`shape_id`) REFERENCES `engine_trackedshape` (`id`),
  CONSTRAINT `engine_trackedshapea_spec_id_a944a532_fk_engine_at` FOREIGN KEY (`spec_id`) REFERENCES `engine_attributespec` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `engine_video`
--

DROP TABLE IF EXISTS `engine_video`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `engine_video` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `path` varchar(1024) NOT NULL,
  `width` int(10) unsigned NOT NULL CHECK (`width` >= 0),
  `height` int(10) unsigned NOT NULL CHECK (`height` >= 0),
  `data_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `data_id` (`data_id`),
  CONSTRAINT `engine_video_data_id_b37015e9_fk_engine_data_id` FOREIGN KEY (`data_id`) REFERENCES `engine_data` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `git_gitdata`
--

DROP TABLE IF EXISTS `git_gitdata`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `git_gitdata` (
  `task_id` int(11) NOT NULL,
  `url` varchar(2000) NOT NULL,
  `path` varchar(256) NOT NULL,
  `sync_date` datetime(6) NOT NULL,
  `status` varchar(20) NOT NULL,
  `lfs` tinyint(1) NOT NULL,
  PRIMARY KEY (`task_id`),
  CONSTRAINT `git_gitdata_task_id_a6f2ea20_fk_engine_task_id` FOREIGN KEY (`task_id`) REFERENCES `engine_task` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `socialaccount_socialaccount`
--

DROP TABLE IF EXISTS `socialaccount_socialaccount`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `socialaccount_socialaccount` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `provider` varchar(30) NOT NULL,
  `uid` varchar(191) NOT NULL,
  `last_login` datetime(6) NOT NULL,
  `date_joined` datetime(6) NOT NULL,
  `extra_data` longtext NOT NULL,
  `user_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `socialaccount_socialaccount_provider_uid_fc810c6e_uniq` (`provider`,`uid`),
  KEY `socialaccount_socialaccount_user_id_8146e70c_fk_auth_user_id` (`user_id`),
  CONSTRAINT `socialaccount_socialaccount_user_id_8146e70c_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `socialaccount_socialapp`
--

DROP TABLE IF EXISTS `socialaccount_socialapp`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `socialaccount_socialapp` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `provider` varchar(30) NOT NULL,
  `name` varchar(40) NOT NULL,
  `client_id` varchar(191) NOT NULL,
  `secret` varchar(191) NOT NULL,
  `key` varchar(191) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `socialaccount_socialapp_sites`
--

DROP TABLE IF EXISTS `socialaccount_socialapp_sites`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `socialaccount_socialapp_sites` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `socialapp_id` int(11) NOT NULL,
  `site_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `socialaccount_socialapp_sites_socialapp_id_site_id_71a9a768_uniq` (`socialapp_id`,`site_id`),
  KEY `socialaccount_socialapp_sites_site_id_2579dee5_fk_django_site_id` (`site_id`),
  CONSTRAINT `socialaccount_social_socialapp_id_97fb6e7d_fk_socialacc` FOREIGN KEY (`socialapp_id`) REFERENCES `socialaccount_socialapp` (`id`),
  CONSTRAINT `socialaccount_socialapp_sites_site_id_2579dee5_fk_django_site_id` FOREIGN KEY (`site_id`) REFERENCES `django_site` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `socialaccount_socialtoken`
--

DROP TABLE IF EXISTS `socialaccount_socialtoken`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `socialaccount_socialtoken` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `token` longtext NOT NULL,
  `token_secret` longtext NOT NULL,
  `expires_at` datetime(6) DEFAULT NULL,
  `account_id` int(11) NOT NULL,
  `app_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `socialaccount_socialtoken_app_id_account_id_fca4e0ac_uniq` (`app_id`,`account_id`),
  KEY `socialaccount_social_account_id_951f210e_fk_socialacc` (`account_id`),
  CONSTRAINT `socialaccount_social_account_id_951f210e_fk_socialacc` FOREIGN KEY (`account_id`) REFERENCES `socialaccount_socialaccount` (`id`),
  CONSTRAINT `socialaccount_social_app_id_636a42d7_fk_socialacc` FOREIGN KEY (`app_id`) REFERENCES `socialaccount_socialapp` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2020-09-19 11:14:21
