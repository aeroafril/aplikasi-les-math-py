-- MariaDB dump 10.19  Distrib 10.4.32-MariaDB, for Win64 (AMD64)
--
-- Host: localhost    Database: daftarlesmath
-- ------------------------------------------------------
-- Server version	10.4.32-MariaDB

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
-- Table structure for table `pengajar`
--

DROP TABLE IF EXISTS `pengajar`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `pengajar` (
  `id_pengajar` varchar(20) NOT NULL,
  `nama_pengajar` varchar(50) DEFAULT NULL,
  `tanggal_lahir_pengajar` date DEFAULT NULL,
  `tingkatLulusTerakhir` varchar(10) DEFAULT NULL,
  `prestasi` varchar(255) DEFAULT NULL,
  `asal_kampus` varchar(30) DEFAULT NULL,
  `pendidikan` varchar(20) NOT NULL,
  `nomor_pengajar` varchar(20) DEFAULT NULL,
  `gender` tinyint(1) NOT NULL,
  PRIMARY KEY (`id_pengajar`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `pengajar`
--

LOCK TABLES `pengajar` WRITE;
/*!40000 ALTER TABLE `pengajar` DISABLE KEYS */;
INSERT INTO `pengajar` VALUES ('P1','ardi simanjuntak','1992-12-16','S2','champion 1st ifrom olimpiade math international','Universitas Stanford','SD/Sederajat','081234125235',1),('P2','janaka susilo','1990-12-19','S1','lomba catur','University Harvard','SMP/Sederajat','0832467252715',1),('P3','multo','1989-03-08','S2','lomba math 1st sedunia','University Stanford','SMA/SMK/Sederajat','08233784287',1);
/*!40000 ALTER TABLE `pengajar` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `users`
--

DROP TABLE IF EXISTS `users`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `users` (
  `id_pendaftar` int(20) NOT NULL AUTO_INCREMENT,
  `nama_pendaftar` varchar(50) NOT NULL,
  `tanggal_lahir` date NOT NULL,
  `nomorTelepon` varchar(15) NOT NULL,
  `desaKelurahan` varchar(20) NOT NULL,
  `kecamatan` varchar(20) NOT NULL,
  `kabupatenKota` varchar(20) NOT NULL,
  `pendidikan` varchar(20) NOT NULL,
  `gender` tinyint(1) NOT NULL,
  `motivasi` varchar(30) NOT NULL,
  `langganan` varchar(20) NOT NULL,
  `total` int(20) NOT NULL,
  `pembayaran` tinyint(1) NOT NULL,
  PRIMARY KEY (`id_pendaftar`)
) ENGINE=InnoDB AUTO_INCREMENT=16 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `users`
--

LOCK TABLES `users` WRITE;
/*!40000 ALTER TABLE `users` DISABLE KEYS */;
INSERT INTO `users` VALUES (12,'albert','2004-10-21','0832283642','kranggan','ngasem','kabupaten kediri','SMP/Sederajat',1,'Olimpiade','Tahunan',3640000,1),(14,'amelia zahra','2007-12-05','02345245252','ngasem','ngasem','kabupaaten kediri','SD/Sederajat',0,'Olimpiade','Bulanan',150000,1),(15,'ko melvin','2006-04-06','0834657836','paron','ngasem','kabupaten kediri','SMA/SMK/Sederajat',1,'Masuk Universitas Ternama','Tahunan',5460000,1);
/*!40000 ALTER TABLE `users` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-12-30 15:45:30
