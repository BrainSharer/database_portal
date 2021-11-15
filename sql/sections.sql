-- MySQL dump 10.19  Distrib 10.3.31-MariaDB, for debian-linux-gnu (x86_64)
--
-- Host: localhost    Database: active_atlas_development
-- ------------------------------------------------------
-- Server version	10.3.31-MariaDB-0ubuntu0.20.04.1

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
-- Temporary table structure for view `sections`
--

DROP TABLE IF EXISTS `sections`;
/*!50001 DROP VIEW IF EXISTS `sections`*/;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8;
/*!50001 CREATE TABLE `sections` (
  `id` tinyint NOT NULL,
  `prep_id` tinyint NOT NULL,
  `czi_file` tinyint NOT NULL,
  `slide_physical_id` tinyint NOT NULL,
  `file_name` tinyint NOT NULL,
  `tif_id` tinyint NOT NULL,
  `scene_number` tinyint NOT NULL,
  `scene_index` tinyint NOT NULL,
  `channel` tinyint NOT NULL,
  `channel_index` tinyint NOT NULL,
  `active` tinyint NOT NULL,
  `created` tinyint NOT NULL
) ENGINE=MyISAM */;
SET character_set_client = @saved_cs_client;

--
-- Final view structure for view `sections`
--

/*!50001 DROP TABLE IF EXISTS `sections`*/;
/*!50001 DROP VIEW IF EXISTS `sections`*/;
/*!50001 SET @saved_cs_client          = @@character_set_client */;
/*!50001 SET @saved_cs_results         = @@character_set_results */;
/*!50001 SET @saved_col_connection     = @@collation_connection */;
/*!50001 SET character_set_client      = utf8 */;
/*!50001 SET character_set_results     = utf8 */;
/*!50001 SET collation_connection      = utf8_general_ci */;
/*!50001 CREATE ALGORITHM=UNDEFINED */
/*!50013 DEFINER=`brainsharer`@`localhost` SQL SECURITY DEFINER */
/*!50001 VIEW `sections` AS select `sc`.`id` AS `id`,`a`.`prep_id` AS `prep_id`,`s`.`file_name` AS `czi_file`,`s`.`slide_physical_id` AS `slide_physical_id`,`sc`.`file_name` AS `file_name`,`sc`.`id` AS `tif_id`,`sc`.`scene_number` AS `scene_number`,`sc`.`scene_index` AS `scene_index`,`sc`.`channel` AS `channel`,`sc`.`channel` - 1 AS `channel_index`,`sc`.`active` AS `active`,`sc`.`created` AS `created` from (((`animal` `a` join `scan_run` `sr` on(`a`.`prep_id` = `sr`.`prep_id`)) join `slide` `s` on(`sr`.`id` = `s`.`scan_run_id`)) join `slide_czi_to_tif` `sc` on(`s`.`id` = `sc`.`slide_id`)) where `s`.`slide_status` = 'Good' and `sc`.`active` = 1 */;
/*!50001 SET character_set_client      = @saved_cs_client */;
/*!50001 SET character_set_results     = @saved_cs_results */;
/*!50001 SET collation_connection      = @saved_col_connection */;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2021-11-15  8:18:18
