-- MySQL dump 10.13  Distrib 8.0.20, for Win64 (x86_64)
--
-- Host: localhost    Database: my_database
-- ------------------------------------------------------
-- Server version	8.0.20

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `blogs`
--

DROP TABLE IF EXISTS `blogs`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `blogs` (
  `id` int NOT NULL AUTO_INCREMENT,
  `title` varchar(256) NOT NULL,
  `body` varchar(1280) NOT NULL,
  `timecreated` datetime NOT NULL,
  `timemodified` datetime NOT NULL,
  `user` varchar(32) DEFAULT NULL,
  `likes` int DEFAULT '0',
  `category` varchar(128) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `user` (`user`),
  CONSTRAINT `blogs_ibfk_1` FOREIGN KEY (`user`) REFERENCES `employee` (`username`)
) ENGINE=InnoDB AUTO_INCREMENT=10 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `blogs`
--

LOCK TABLES `blogs` WRITE;
/*!40000 ALTER TABLE `blogs` DISABLE KEYS */;
INSERT INTO `blogs` VALUES (2,'How to start with UiPath RPA','UiPath is a Robotic process automation tool used for Windows desktop automation. It is founded in the year 2005 by the Romanian entrepreneurs Daniel Dines and Marius Tirca. It is used to automate boring repetitive tasks. It also eliminates the human intervention.','2020-08-08 20:36:05','2020-08-08 20:36:05','arti.tripathi',0,'Technical'),(3,'Python with MongoDB','MongoDB stores data in JSON-like documents, which makes the database very flexible and scalable.\r\n\r\nTo be able to experiment with the code examples in this tutorial, you will need access to a MongoDB database.\r\nYou can download a free MongoDB database at https://www.mongodb.com.\r\n\r\nOr get started right away with a MongoDB cloud service at https://www.mongodb.com/cloud/atlas.','2020-08-08 20:37:01','2020-08-08 20:37:01','arti.tripathi',0,'Technical'),(5,'My Future Goal','<h1>Hi My name is <strong>Tuhin S Samanta</strong></h1>\r\n\r\n<p>I am currently working in UiPath as a&nbsp;<strong>product Consultant.</strong></p>\r\n\r\n<p>Soon I am going to join as an <strong>Automation Engineer. <samp>My Journey up to now remains fantastic.&nbsp;</samp></strong></p>\r\n\r\n<p><strong><samp>We never lose</samp></strong></p>\r\n','2020-08-09 14:51:42','2020-08-09 14:51:42','tuhinssam',0,'Motivation'),(7,'My journey till date','<h2>Hello, I&#39;m Arti. I started my journey in <strong>Ericsson</strong>. After that, I moved to <strong>Infosys</strong>. Though I started with lot of hope, I couldn&#39;t sustain there for long. I had to leave soon.&nbsp;</h2>\r\n\r\n<h2>After Infosys, I joined <strong>EY </strong>as <strong>RPA Consultant</strong>. I switched my technical role as well.</h2>\r\n\r\n<h2>Here I got respect and recognition. Recently I got promoted to Senior Consultant.&nbsp;</h2>\r\n','2020-08-09 18:59:00','2020-08-09 18:59:00','arti.tripathi',0,'Motivation'),(8,'Disco Blog','<p><span class=\"marker\">Disco Disco Dosco</span></p>\r\n\r\n<h1><ins>Disco Disco Dosco</ins></h1>\r\n\r\n<p><del>Disco Disco Dosco</del></p>\r\n\r\n<h2><samp>Disco Disco Disco</samp></h2>\r\n','2020-08-10 16:19:24','2020-08-10 16:19:24','tuhinssam',0,'Motivation'),(9,'Hajabarala','<h1><span class=\"marker\">Hajabarala</span></h1>\r\n\r\n<h3><del>Hajabarala</del></h3>\r\n\r\n<h2><ins>Hajabarala</ins></h2>\r\n\r\n<h1><q>Hajabarala</q></h1>\r\n','2020-08-12 10:46:36','2020-08-12 10:46:36','tuhinssam',0,'Travel');
/*!40000 ALTER TABLE `blogs` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `employee`
--

DROP TABLE IF EXISTS `employee`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `employee` (
  `name` varchar(128) NOT NULL,
  `age` int DEFAULT NULL,
  `username` varchar(32) NOT NULL,
  `password` varchar(1024) DEFAULT NULL,
  `introduction` varchar(10000) NOT NULL,
  PRIMARY KEY (`username`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `employee`
--

LOCK TABLES `employee` WRITE;
/*!40000 ALTER TABLE `employee` DISABLE KEYS */;
INSERT INTO `employee` VALUES ('admin',111,'admin','pbkdf2:sha256:150000$g6EjKPMF$077bd702c94b84b124b6083f6c22b76272fd2938755c87d1650ce4faf2bbe245','this is for admin'),('Arti Tripathi',31,'arti.tripathi','pbkdf2:sha256:150000$gRujdAkC$66accfd1dcc09ebe4fef0cec7c5c940cf81077e155825e3640f5f17ff7be1131','I am enthusiatic UiPath RPA developer'),('senjuti samanta',29,'sensam','pbkdf2:sha256:150000$6L0AV8OK$1e84fb1017b1f6c82bc88db916e53675b294324c66a9d10be5fc97237f3cd2a0','Hi I\'m Senjuti. I work in IBM'),('Subhash Ch Samanta',62,'subsam','pbkdf2:sha256:150000$uMurS82x$a1fb44543d3e47000406f59fc7091243cd53cfa4ff70faaa745f2ee7f1395c22','I love gardening'),('Arti Tripathi',31,'triart','pbkdf2:sha256:150000$Ovu4A6KC$e6443146cdea91c0be2bc699941f63d8e2b457d0c73499e563489edc5ea098d0','Arti is an UiPath Developer. She likes giving \'Gyan\' to Others'),('Tuhin',32,'tuhinssam','pbkdf2:sha256:150000$ncUrzIst$07a79486010b3efb1acf5d50e467b0066f33e6d5771037c03cd95797a25ca4ca','I am a curious learner. I try learning whatever comes on my way. Though I keep special interest on Data Science and Automation Technologies. I have implemented saveral Projects on Machine Learning, Predictive analysis, Deep Learning and NLP. Other than that I love blogging and travelling off-beat places. Please reach out to me if you think I can assist you or your company in solving any problem.');
/*!40000 ALTER TABLE `employee` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `user`
--

DROP TABLE IF EXISTS `user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `user` (
  `user_name` varchar(30) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `user`
--

LOCK TABLES `user` WRITE;
/*!40000 ALTER TABLE `user` DISABLE KEYS */;
INSERT INTO `user` VALUES ('Tuhin'),('Arti'),('Mike'),('Rahul');
/*!40000 ALTER TABLE `user` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2020-08-12 11:32:31
