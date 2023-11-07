-- MySQL dump 10.13  Distrib 8.0.34, for Win64 (x86_64)
--
-- Host: localhost    Database: db_monitoring
-- ------------------------------------------------------
-- Server version	5.5.5-10.4.25-MariaDB

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
-- Table structure for table `alembic_version`
--

DROP TABLE IF EXISTS `alembic_version`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `alembic_version` (
  `version_num` varchar(32) NOT NULL,
  PRIMARY KEY (`version_num`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `alembic_version`
--

LOCK TABLES `alembic_version` WRITE;
/*!40000 ALTER TABLE `alembic_version` DISABLE KEYS */;
INSERT INTO `alembic_version` VALUES ('3c8bf98265cb');
/*!40000 ALTER TABLE `alembic_version` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_status_user_login`
--

DROP TABLE IF EXISTS `auth_status_user_login`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_status_user_login` (
  `id` varchar(36) NOT NULL,
  `user_login_id` int(11) DEFAULT NULL,
  `status_login` tinyint(1) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `user_login_id` (`user_login_id`),
  CONSTRAINT `auth_status_user_login_ibfk_1` FOREIGN KEY (`user_login_id`) REFERENCES `auth_user` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_status_user_login`
--

LOCK TABLES `auth_status_user_login` WRITE;
/*!40000 ALTER TABLE `auth_status_user_login` DISABLE KEYS */;
INSERT INTO `auth_status_user_login` VALUES ('02d7e8f6-91a9-4ca9-a2e7-de048799f593',18,1),('34411d51-16e0-4639-8358-cdc47f868e54',21,1),('38e9c1f5-6c5e-4d23-862b-1c51aeecf26d',17,1),('42efb905-f0fe-4d6a-8f05-b9323594478c',20,0),('97fdd1d2-f001-4548-b01f-2de850fe19b5',25,1),('bdbf5fb2-3b8d-49dd-8f19-8ab20acc87a6',16,1),('ff3c3643-e739-4c4e-8b5a-9497c45bf3c4',19,0);
/*!40000 ALTER TABLE `auth_status_user_login` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_token_block`
--

DROP TABLE IF EXISTS `auth_token_block`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_token_block` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `jti` varchar(36) NOT NULL,
  `created_at` datetime NOT NULL,
  `user_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `ix_auth_token_block_jti` (`jti`),
  KEY `user_id` (`user_id`),
  CONSTRAINT `auth_token_block_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=202 DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_token_block`
--

LOCK TABLES `auth_token_block` WRITE;
/*!40000 ALTER TABLE `auth_token_block` DISABLE KEYS */;
INSERT INTO `auth_token_block` VALUES (170,'f4ef693f-0ba2-45cf-afa3-536c1e01b535','2023-09-28 00:37:18',7),(171,'0be71150-2800-4c37-804f-ae8751cac775','2023-10-02 22:35:17',6),(172,'3e310e1d-036c-4a0f-ba9a-6ffbf8853038','2023-10-03 23:14:17',6),(173,'ba6de103-01f0-4d3c-839f-2d121b3c006f','2023-10-03 23:47:47',17),(174,'c5823232-bab7-498c-8cbb-8fade0c25a06','2023-10-03 23:56:13',17),(175,'0c187955-6a9f-4f38-853a-c3e89eefcf61','2023-10-04 01:05:23',17),(176,'7c229bc9-f44e-4219-96c3-7b19d1c3334b','2023-10-04 01:10:36',6),(177,'05ceed11-8a57-4fd7-84f4-1ab5501c61c7','2023-10-04 01:12:47',16),(178,'bcd041f3-1c37-4b1e-87ff-b1653e0e4771','2023-10-04 01:20:26',21),(179,'61bf5d7d-e80e-46cb-b38f-3b5fecbeb2c3','2023-10-05 14:59:58',21),(180,'d0d3f2d7-5122-482f-baae-e2d9371fe267','2023-10-05 15:15:55',9),(181,'5118a06f-8fbf-4168-8c2a-f1e0b52c5201','2023-10-05 15:16:31',6),(182,'1935f2a0-8cb0-4902-beec-0d7c5a4f9534','2023-10-04 15:18:01',6),(183,'7c157332-eaa9-4397-8563-ef3a03a20b2b','2023-10-05 23:38:02',6),(184,'b3cd5d97-7c55-403f-a7f7-9775094208c1','2023-10-05 23:44:29',21),(185,'e24f5e39-3f06-4dbf-b062-d68b778d78a0','2023-10-06 00:24:07',6),(186,'b6542150-99ed-446d-95af-493c528520c3','2023-10-05 14:59:18',6),(187,'46833766-38c3-42cc-8a1f-34c56b9db5be','2023-10-05 14:59:23',6),(188,'a7d03129-94bd-417e-aef3-0c23cf8d1ac8','2023-10-07 15:45:59',6),(189,'15d79879-10d3-4e57-8932-c53aa0ff148d','2023-10-09 18:29:45',6),(190,'057e9c0a-4370-427b-bf31-a1a17dbeeeff','2023-10-09 19:57:48',6),(191,'df4b3967-ab9a-4b78-b709-5805b70ed66e','2023-10-10 00:27:56',6),(192,'7871bee7-f300-470b-bc55-eccdbbd33c3d','2023-10-09 15:13:14',16),(193,'d60ce8e0-b193-4279-a235-ff6697f9f87a','2023-10-12 23:49:01',6),(194,'2fc51ebf-6bba-4517-95d0-3bec36e08a42','2023-10-12 23:55:42',6),(195,'15954c79-7d36-4cc1-85d9-cb891100905b','2023-10-12 23:56:21',6),(196,'0f2cef6f-fcc7-4f30-9aee-4687957fead4','2023-10-22 10:34:35',6),(197,'1e9930f4-3c1d-40d7-9d66-4344e26df240','2023-10-22 13:15:32',6),(198,'707118e6-f97d-4db3-9785-3adcf02961ba','2023-10-22 13:15:40',6),(199,'b96300ae-3932-49c7-b5a2-ff8c7b0f8c33','2023-10-22 13:39:17',6),(200,'8067309f-4699-48c5-a78b-294ca5f81e34','2023-10-30 15:58:51',6),(201,'a41ff969-1991-4e15-b029-cc633cbb0a6e','2023-10-30 15:58:56',6);
/*!40000 ALTER TABLE `auth_token_block` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_user`
--

DROP TABLE IF EXISTS `auth_user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_user` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `username` varchar(128) NOT NULL,
  `password` varchar(256) NOT NULL,
  `group` varchar(128) NOT NULL,
  `join_date` datetime DEFAULT NULL,
  `update_date` datetime DEFAULT NULL,
  `is_active` varchar(2) NOT NULL,
  `user_last_login` datetime DEFAULT NULL,
  `user_logout` datetime DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=67 DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_user`
--

LOCK TABLES `auth_user` WRITE;
/*!40000 ALTER TABLE `auth_user` DISABLE KEYS */;
INSERT INTO `auth_user` VALUES (5,'admin','pbkdf2:sha256:600000$5WKG5kHGKmWr0mUv$ed6173be5f4f145be71bbdf4af09b1251d6f7dcc43d48ae7a4e741360d6aeb19','admin','2022-11-21 08:59:26','2023-11-04 23:34:37','1','2023-11-07 11:04:07',NULL),(6,'196606271996022001','pbkdf2:sha256:600000$JB1XTUdmXOyqLn1X$89593d106414b24376abc1bdd8574c838173f945e4755b8f268dc9ebac107c65','guru','2022-11-23 10:45:46','2023-09-28 02:31:39','1','2023-10-30 23:50:24','2023-09-30 15:42:21'),(7,'196204141987032019','pbkdf2:sha256:260000$MMeaDwSNRQ3ARN4U$e44985c1d72630be619674e95c137060cb16ae3d1d3c43f3dcdea8f0b8957cbd','guru','2022-11-23 11:08:44','2023-09-06 18:17:10','1','2023-10-17 14:14:16','2023-09-27 17:25:11'),(8,'196910171992032008','pbkdf2:sha256:260000$e3HYbX7VHSGCtjhd$513d24d883d654425540fe9982e4dbe546d29bb08251aa73cabb5fb1f13bff0d','guru','2022-11-23 11:08:44',NULL,'1','2023-10-22 10:29:31','2023-06-07 14:13:26'),(9,'196501021987032021','pbkdf2:sha256:260000$ciDiGmznZ6r9LyqS$57b7487d7f19b9b918c94358c91de9afac0cef2c907af4da0752dd48b6072245','guru','2022-11-23 11:08:44',NULL,'1','2023-10-05 15:00:24',NULL),(10,'196905041998022004','pbkdf2:sha256:260000$5CCTPpKEwU4uxlek$1e036fd3e8a23aba35d8057445c3a41a77e91098cc264c5d446182943c8bf79b','guru','2022-11-23 11:08:44',NULL,'1',NULL,NULL),(11,'198512072011011008','pbkdf2:sha256:260000$7x53OC52o0UTJopc$eeda5256c88e04eaf2ed9eeb0babb6937007a3583a6af81c7d32d31a45d7db49','guru','2022-11-23 11:08:44',NULL,'1','2023-09-12 21:06:09','2023-09-12 21:19:07'),(12,'197209152000032003','pbkdf2:sha256:260000$ARFmTsYoMDqWj6ad$0c06f0c7fc0652906caaf0c6d21d22d4c03b46c39d9dac30622c406f6c851b3e','guru','2022-11-23 11:08:44',NULL,'1','2023-11-07 00:10:39',NULL),(13,'197008182006042000','pbkdf2:sha256:260000$5iJn2hLZzxofDs27$abf40d5b69774e87cb2ca22b685280269695e39cfec43895403647b5e40d8666','guru','2022-11-23 11:08:44',NULL,'1','2023-05-24 06:38:43','2023-05-24 06:47:44'),(14,'197008182006042008','pbkdf2:sha256:260000$yV565KKXayH4cvjP$de6cb43b94ad125f04be9667652e43109db405600d205c6b6c0128f2a1340d85','guru','2022-11-23 11:08:44',NULL,'1','2023-05-24 06:48:00','2023-05-24 08:44:47'),(15,'196701221995122001','pbkdf2:sha256:260000$TRNddbol1pvrXoFk$914ff1b2d7fa445ef6aef3df9a887aefb3c234599418acd1d3965ed68f8f230b','guru','2022-11-23 11:08:44','2022-11-23 11:47:21','1','2023-10-18 11:34:53',NULL),(16,'0094755743','pbkdf2:sha256:260000$ML9TPvjwvoRkXRlc$2ac7283adc7e2b23210aa4cc815891f760cd7288c45fb92ca7f2f087b75b003c','siswa','2022-11-23 11:31:51',NULL,'1','2023-10-04 01:11:36','2023-09-30 20:27:42'),(17,'0099789908','pbkdf2:sha256:600000$BvGFZIGQ9mG8OOOR$f05aa3eae32d5ffe387fa0229081226976152d57ea1d7470093040162fd6b210','siswa','2022-11-23 11:31:51','2023-09-27 23:33:23','1','2023-10-31 14:08:39','2023-10-01 20:44:07'),(18,'0094125167','pbkdf2:sha256:260000$XiEMZ3lc84rxmSNg$5547334703162b6d5de070e528bda10cefb54c1d89065ade98e80810e5622db2','siswa','2022-11-23 11:31:51',NULL,'1','2023-11-04 17:30:48',NULL),(19,'0095787926','pbkdf2:sha256:260000$JTRY49t1Ldzu55kr$d6460b91f9e943fece13de1e894c6544a6a642b142b192edc670477e9fc0a5d3','siswa','2022-11-23 11:31:51',NULL,'1','2023-05-17 12:54:34','2023-05-17 12:54:38'),(20,'0085321166','pbkdf2:sha256:260000$72p1lOU3A4KG9Uc2$72a55d99071debe3833a857d3a8c1be9ead96587b74adbee12c497dd871abe55','siswa','2022-11-23 11:31:51','2023-01-02 15:34:22','1','2023-05-18 11:48:02','2023-05-18 11:48:06'),(21,'0096991422','pbkdf2:sha256:260000$h3fqF2lWUhcL6Cf4$4c2f1714a947969eea806afc551de8a2ee41a51b3269c172144901e3a87ae66e','siswa','2022-11-23 11:31:51',NULL,'1','2023-10-05 23:38:42','2023-06-14 15:27:42'),(22,'0082803614','pbkdf2:sha256:260000$QJHf5FUGh55IGbB0$42718f61c621dc341516ba04fc3f455d789064eaeff17f06556314d1aec24dd4','siswa','2022-11-23 11:31:51',NULL,'1',NULL,NULL),(23,'0081227491','pbkdf2:sha256:260000$rdn8mzlaaRTY4NOP$043dc8641b48ad01d4fe0865bb1d63c77eaa2e475e1c56f242010bd85b15f97f','siswa','2022-11-23 11:31:51',NULL,'1',NULL,NULL),(24,'0084835186','pbkdf2:sha256:260000$52kFS3XISmvOzgAr$aad75485875917b109c501b76eb69f95696003dbe21db4c7f3ae102d63f24ce0','siswa','2022-11-23 11:31:51',NULL,'1',NULL,NULL),(25,'0095267997','pbkdf2:sha256:260000$gZodkTyvH5gnho4h$2c5eb6a9be688d53af8efae986493a1b86cf1f62e4f87710b49484bc958fefa0','siswa','2022-11-23 11:31:51',NULL,'1','2023-09-12 21:20:05',NULL),(26,'0086737425','pbkdf2:sha256:260000$V0rgIzgrlMVjonrc$83d96778abe92ae8b56e8abe80c220f81c9febf9713cb2fc6a7a725388d415b0','siswa','2022-11-23 11:31:51',NULL,'1',NULL,NULL),(27,'0088283893','pbkdf2:sha256:260000$ziJz2NHvmkU50TvG$1480e329fe8b85f4bf2956f47ff411cfb5aa06d90c38efed65c34a86eb595f96','siswa','2022-11-23 11:31:51',NULL,'1',NULL,NULL),(28,'0098182346','pbkdf2:sha256:260000$5JCO14IKtRK1ko1v$1beabc030166114030395b3f8d012f8f0f5792dbcd668cff5d496e6298d63c27','siswa','2022-11-23 11:31:51',NULL,'1',NULL,NULL),(29,'0096041815','pbkdf2:sha256:260000$AnEY9J7FmVPzcWll$ac102a317ea0684961ed1e0bbac15dc3567b493af21e45ef437303cd8ef3c11e','siswa','2022-11-23 11:31:51',NULL,'1',NULL,NULL),(30,'0097282248','pbkdf2:sha256:260000$rJHbrYsXaPv7S3L8$4dc317566a9ae65963763e3259f8299516ed42e9abf912d1b3078895357f7284','siswa','2022-11-23 11:31:51',NULL,'1',NULL,NULL),(31,'0099049864','pbkdf2:sha256:260000$ooA2Wg5ZfbPKG5OS$08e060ae798530c488a6838dde29d3b6ea2349a13bc21d744f87ff6f35ea141a','siswa','2022-11-23 11:31:51',NULL,'1','2023-03-29 02:01:39',NULL),(32,'0071412829','pbkdf2:sha256:260000$rZ9HEEPohgO8fC9j$4a07f87a2126af570d1f2e98874bfb2a6bee43570dc61f85a715c8b193ef2406','siswa','2022-11-23 11:31:51',NULL,'1','2022-11-23 12:06:34',NULL),(33,'0083083027','pbkdf2:sha256:260000$obSCRkge0aCgToLi$68d66ec4019e5b5591bfaa21cba5370a2009b878b0c50817df3cdcb07d6833fc','siswa','2022-12-01 00:18:15',NULL,'1',NULL,NULL),(34,'0099631922','pbkdf2:sha256:260000$up3QPN9hgOSj6Z67$c53daca0c82c704c8d5295b4765bfa22bfba667f12b42689001f6cf8f48a5f83','siswa','2022-12-01 00:18:15',NULL,'1',NULL,NULL),(35,'0095459342','pbkdf2:sha256:260000$gYDnabg5ky8XHn8v$554f6856c28572550019c64f00789bc75a03221f52cef31ec4822a525dad6d26','siswa','2022-12-01 00:18:15',NULL,'1',NULL,NULL),(36,'0091604225','pbkdf2:sha256:260000$rBBOl2DoD7PBpocT$47985d62393ffd6671d37785ad18469624d9e3f53994cca81269315022bd4dfa','siswa','2022-12-01 00:18:15',NULL,'1',NULL,NULL),(37,'0091746861','pbkdf2:sha256:260000$dEmD4yWdFE0JmcHo$0d2a8e6fff9e28c961b5b0a6ea8c7dacf093d320464d33d354cd7f918eabf10a','siswa','2022-12-21 21:01:38',NULL,'1',NULL,NULL),(38,'0094595250','pbkdf2:sha256:260000$Zs5NouVQmGciuPlf$24ab81a22cc9aafd3e2e422ce53c97b873f8154b0b54edaf9ea5461241807884','siswa','2022-12-21 21:01:38',NULL,'1',NULL,NULL),(39,'0087800776','pbkdf2:sha256:260000$3DNixgIqHpUbXTfw$e20bf32b2686bb8c960105f20c6d3409cce46562564cb85453f332336088777e','siswa','2022-12-21 21:01:38',NULL,'1',NULL,NULL),(40,'0096678822','pbkdf2:sha256:260000$4FFtcbqrQdjSZK8f$4513c3c7e2507c6a3cd79f26915a0c4c2c01975c023a741f1c5b4550b1cb7d89','siswa','2022-12-21 21:01:38',NULL,'1',NULL,NULL),(41,'197312221999032007','pbkdf2:sha256:260000$cKqtj4FgvVUBfQQc$92e34e373800f6c9c1fb8c157e8e3ebd2d6f9bf3e6d5a5a50b31b48bdebaeee6','guru','2023-01-03 19:34:33',NULL,'1','2023-06-14 15:28:14','2023-06-14 16:07:21'),(42,'198109122009022008','pbkdf2:sha256:260000$Ey4gA0RLQ95t7eDY$57a4397769588a3eae028250728faca20f360fa6f682c79dc1e0024870ba830d','guru','2023-01-03 19:34:33',NULL,'1',NULL,NULL),(43,'196312311988032109','pbkdf2:sha256:260000$lkvfeYneHJ1NSsCQ$514f4531f96788ca5f6ec9089a72c71b50cbf41f603c342b3e2c53303abb8c55','guru','2023-01-03 19:34:33',NULL,'1',NULL,NULL),(44,'196512311989032117','pbkdf2:sha256:260000$u2aFy7r2VgYZ0k4u$27bb5858363ec031fedd3df4673093fb416c7782ea86f657dcf3bfce27d8da04','guru','2023-01-03 23:23:19',NULL,'1',NULL,NULL),(45,'196509141991032011','pbkdf2:sha256:600000$EW2PSpvUd0G4hk7C$9b33ee73d4e74a495ee0368095210a3275af40b47197cc3221003f204bd662e0','bk','2023-01-03 23:23:19',NULL,'1','2023-10-10 23:48:33',NULL),(47,'admin123','pbkdf2:sha256:600000$gcCpiUW8j3l5QgFL$cc5be645d66c35c8db0c36079dba5c69234b011cefb703359653e5e09927f587','admin','2023-09-03 13:41:25',NULL,'1',NULL,NULL),(50,'12345678','pbkdf2:sha256:600000$5TVyeoGNFpiPNxNq$34f750f8e6988a30660433582ad149bf2adacc90e03399af434bc7b81ead136e','siswa','2023-11-02 00:20:39',NULL,'1',NULL,NULL),(51,'12345678','pbkdf2:sha256:600000$yNRGkdG8gfu16Wd0$70a7c42e587984ecc0c8700312354506bf5382fea4a6f4bb8766950659e20451','siswa','2023-11-02 00:34:21',NULL,'1',NULL,NULL),(52,'12345678','pbkdf2:sha256:600000$39WRZmYr8idJw8up$08b8754aa24c93e66dc0d7e6f180e15a5a144af16d102b459e0e03e73843a0f8','siswa','2023-11-02 00:34:59',NULL,'1',NULL,NULL),(53,'12345678','pbkdf2:sha256:600000$VvX7np5E8BMLqN8U$e2faf0099aff5cda45bf9c0dfe3aa7d3889c7a80a9df3a9787051935d6229953','siswa','2023-11-02 00:35:23',NULL,'1',NULL,NULL),(54,'12345678','pbkdf2:sha256:600000$2NELtAgmPqn6jsth$751b2c8b004707f96e33acbf61469790349fc6b4607ecfbebcd654b85300fbb9','siswa','2023-11-02 00:35:34',NULL,'1',NULL,NULL),(55,'12345678','pbkdf2:sha256:600000$6F6Ab8DtcTa6D3kV$2af8f323a7b73589fa64a53188338665c1904faa9aa21830326009d1faf4f7ee','siswa','2023-11-02 00:36:48',NULL,'1',NULL,NULL),(56,'17024014158','pbkdf2:sha256:600000$HFTjsqQRaTAEzO3z$a3913efd81ef6bdc012111a1318a38a3918a8af7463670c941e8d33de64ffa62','siswa','2023-11-02 00:36:48',NULL,'1',NULL,NULL),(59,'1234567890845','pbkdf2:sha256:600000$ORu3CKK5MshfqFin$a61a8bace525d78c4de7b6590c415989c69a239f6a8aeb5a5fd81cc2ffbf4e4c','guru','2023-11-04 11:14:10',NULL,'1',NULL,NULL),(63,'17024014048','pbkdf2:sha256:600000$sp0SlbPtKJsYaZo0$728671008b6846b5f023f8386395519ede7502255b72ee39ef6a72eb6c4a2363','guru','2023-11-04 22:27:21',NULL,'1',NULL,NULL),(64,'17024014048','pbkdf2:sha256:600000$SvxyqMUzJ7e0z06i$6ed38cbe1ae04b81d03d5e7e5916e58df3f7d513f9dfe165f85cf1fd816cb1ac','guru','2023-11-04 22:27:21',NULL,'1',NULL,NULL),(66,'17024014048','pbkdf2:sha256:600000$WRBWgYgRVWOtSDoC$39a3d08d6f13aa6280271d6b6fec1213ad939516c44faec37f9ae71ba8573e62','guru','2023-11-04 22:27:21',NULL,'1',NULL,NULL);
/*!40000 ALTER TABLE `auth_user` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `data_absensi`
--

DROP TABLE IF EXISTS `data_absensi`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `data_absensi` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `mengajar_id` int(11) DEFAULT NULL,
  `siswa_id` int(11) DEFAULT NULL,
  `tgl_absen` date DEFAULT NULL,
  `ket` varchar(16) DEFAULT NULL,
  `pertemuan_ke` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `mengajar_id` (`mengajar_id`),
  KEY `siswa_id` (`siswa_id`),
  CONSTRAINT `data_absensi_ibfk_1` FOREIGN KEY (`mengajar_id`) REFERENCES `master_jadwal_mengajar` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `data_absensi_ibfk_2` FOREIGN KEY (`siswa_id`) REFERENCES `detail_siswa` (`user_id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=864 DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `data_absensi`
--

LOCK TABLES `data_absensi` WRITE;
/*!40000 ALTER TABLE `data_absensi` DISABLE KEYS */;
/*!40000 ALTER TABLE `data_absensi` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `data_jenis_pelanggaran`
--

DROP TABLE IF EXISTS `data_jenis_pelanggaran`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `data_jenis_pelanggaran` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `jenis_pelanggaran` text DEFAULT NULL,
  `status` varchar(64) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=14 DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `data_jenis_pelanggaran`
--

LOCK TABLES `data_jenis_pelanggaran` WRITE;
/*!40000 ALTER TABLE `data_jenis_pelanggaran` DISABLE KEYS */;
INSERT INTO `data_jenis_pelanggaran` VALUES (4,'Bolos','1'),(5,'Baju tidak rapi','1'),(6,'Berkelahi','1'),(7,'Terlambat','1'),(8,'Rambut gondrong','1'),(9,'Tidur di kelas','1'),(10,'Membawa Senjata Tajam','1'),(11,'Miras','1');
/*!40000 ALTER TABLE `data_jenis_pelanggaran` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `data_notifikasi_siswa`
--

DROP TABLE IF EXISTS `data_notifikasi_siswa`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `data_notifikasi_siswa` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) DEFAULT NULL,
  `msg` varchar(128) NOT NULL,
  `created_at` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `user_id` (`user_id`),
  CONSTRAINT `data_notifikasi_siswa_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `detail_siswa` (`user_id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=35 DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `data_notifikasi_siswa`
--

LOCK TABLES `data_notifikasi_siswa` WRITE;
/*!40000 ALTER TABLE `data_notifikasi_siswa` DISABLE KEYS */;
INSERT INTO `data_notifikasi_siswa` VALUES (1,16,'Login Berhasil...','2023-09-30 13:57:01'),(2,16,'Login Berhasil...','2023-09-30 13:57:01'),(3,16,'Login Berhasil...','2023-09-30 13:57:01'),(4,16,'Login Berhasil...','2023-09-30 20:20:03'),(5,16,'Login Berhasil...','2023-09-30 20:20:03'),(6,16,'Login Berhasil...','2023-09-30 20:20:03'),(7,16,'Login Berhasil...','2023-10-01 00:47:41'),(8,17,'Login Berhasil...','2023-10-01 20:27:52'),(9,16,'Login Berhasil...','2023-09-27 23:03:19'),(10,16,'Login Berhasil...','2023-09-27 23:16:25'),(11,16,'Login Berhasil...','2023-09-27 23:26:12'),(12,16,'Login Berhasil...','2023-09-27 23:27:27'),(13,17,'Login Berhasil...','2023-10-03 22:56:55'),(14,17,'Login Berhasil...','2023-10-03 23:20:49'),(15,17,'Login Berhasil...','2023-10-04 00:59:56'),(16,16,'Login Berhasil...','2023-10-04 00:59:56'),(17,21,'Login Berhasil...','2023-10-04 00:59:56'),(18,21,'Login Berhasil...','2023-10-04 00:59:56'),(19,17,'Login Berhasil...','2023-10-04 20:57:32'),(20,17,'Absen mapel Matematika','2023-10-05 14:13:18'),(21,17,'Absen mapel Ilmu Pengetahuan Sosial','2023-10-05 15:14:57'),(22,17,'Absen mapel Ilmu Pengetahuan Sosial','2023-10-05 15:14:57'),(23,17,'Absen mapel Ilmu Pengetahuan Sosial','2023-10-05 15:41:48'),(24,17,'Absen mapel Ilmu Pengetahuan Sosial','2023-10-05 15:44:18'),(25,17,'Absen mapel Ilmu Pengetahuan Sosial','2023-10-05 15:47:18'),(26,17,'Absen mapel Ilmu Pengetahuan Sosial','2023-10-05 15:50:20'),(27,17,'Absen mapel Ilmu Pengetahuan Sosial','2023-10-05 15:50:20'),(28,17,'Absen mapel Ilmu Pengetahuan Sosial','2023-10-05 16:24:23'),(29,17,'Absen mapel Ilmu Pengetahuan Sosial','2023-10-05 16:52:37'),(30,17,'Absen mapel Ilmu Pengetahuan Sosial','2023-10-05 16:55:41'),(31,21,'Login Berhasil...','2023-10-05 23:35:31'),(32,17,'Login Berhasil...','2023-10-30 23:04:35'),(33,17,'Login Berhasil...','2023-10-30 23:04:35'),(34,18,'Login Berhasil...','2023-11-04 17:26:13');
/*!40000 ALTER TABLE `data_notifikasi_siswa` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `data_pelanggaran`
--

DROP TABLE IF EXISTS `data_pelanggaran`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `data_pelanggaran` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `siswa_id` int(11) DEFAULT NULL,
  `jenis_pelanggaran_id` int(11) DEFAULT NULL,
  `note` text DEFAULT NULL,
  `tgl_report` date NOT NULL,
  `status` varchar(128) DEFAULT NULL,
  `guru_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `jenis_pelanggaran_id` (`jenis_pelanggaran_id`),
  KEY `siswa_id` (`siswa_id`),
  KEY `guru_id` (`guru_id`),
  CONSTRAINT `data_pelanggaran_ibfk_5` FOREIGN KEY (`jenis_pelanggaran_id`) REFERENCES `data_jenis_pelanggaran` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `data_pelanggaran_ibfk_6` FOREIGN KEY (`siswa_id`) REFERENCES `detail_siswa` (`user_id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `data_pelanggaran_ibfk_7` FOREIGN KEY (`guru_id`) REFERENCES `detail_guru` (`user_id`)
) ENGINE=InnoDB AUTO_INCREMENT=65 DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `data_pelanggaran`
--

LOCK TABLES `data_pelanggaran` WRITE;
/*!40000 ALTER TABLE `data_pelanggaran` DISABLE KEYS */;
INSERT INTO `data_pelanggaran` VALUES (41,16,4,'pulang tanpa izin sebelum jam pulang sekolah','2023-08-22','Pelanggaran Ke-1',45),(42,16,5,'tidak rapi dalam berpakaian, selalu mengelurkan baju','2023-08-22','Pelanggaran Ke-2',15),(43,16,7,'tidak menguki upacara bendera','2023-08-22','Pelanggaran Ke-3',12),(47,16,6,'berkelahi dengan sekolah lain','2023-08-22','Pelanggaran Ke-4',14),(49,19,4,'pulang tanpa izin sebelum jam pulang sekolah','2023-08-22','Pelanggaran Ke-1',6),(50,19,7,'tidak menguki upacara bendera','2023-08-22','Pelanggaran Ke-2',44),(51,19,6,'berkelahi dengan sekolah lain','2023-08-22','Pelanggaran Ke-3',45),(58,23,7,'terlambat masuk kelas','2023-08-23','Pelanggaran Ke-1',41),(59,26,6,'berkelahi dengan teman sekelas','2023-08-01','Pelanggaran Ke-1',11),(60,26,9,'Tidak saat jam pelajaran sedang berlangsung.','2023-08-23','Pelanggaran Ke-2',8),(62,16,4,'Bolos sebelum mulai jam pelajaran','2023-08-24','Pelanggaran Ke-5',42),(63,16,8,'Tidak sesuai dengan ketentuan sekolah.','2023-08-24','Pelanggaran Ke-6',10),(64,16,7,'Tidak mengikuti upacara hari senin','2023-09-13','Pelanggaran Ke-7',8);
/*!40000 ALTER TABLE `data_pelanggaran` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `data_pembinaan`
--

DROP TABLE IF EXISTS `data_pembinaan`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `data_pembinaan` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `bina` int(11) DEFAULT NULL,
  `tgl_bina` date DEFAULT NULL,
  `pelanggaran_id` int(11) NOT NULL,
  `siswa_id` int(11) NOT NULL,
  `status` varchar(2) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `pelanggaran_id` (`pelanggaran_id`),
  KEY `siswa_id` (`siswa_id`),
  CONSTRAINT `data_pembinaan_ibfk_4` FOREIGN KEY (`pelanggaran_id`) REFERENCES `data_pelanggaran` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `data_pembinaan_ibfk_5` FOREIGN KEY (`siswa_id`) REFERENCES `detail_siswa` (`user_id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=27 DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `data_pembinaan`
--

LOCK TABLES `data_pembinaan` WRITE;
/*!40000 ALTER TABLE `data_pembinaan` DISABLE KEYS */;
INSERT INTO `data_pembinaan` VALUES (20,1,'2023-08-22',47,16,'1'),(22,1,'2023-09-06',51,19,'1'),(24,2,'2023-08-24',62,16,'1'),(25,3,'2023-08-24',63,16,'1'),(26,4,'2023-09-13',64,16,'0');
/*!40000 ALTER TABLE `data_pembinaan` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `data_tata_tertib`
--

DROP TABLE IF EXISTS `data_tata_tertib`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `data_tata_tertib` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `tata_tertib` varchar(255) DEFAULT NULL,
  `status` varchar(16) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=34 DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `data_tata_tertib`
--

LOCK TABLES `data_tata_tertib` WRITE;
/*!40000 ALTER TABLE `data_tata_tertib` DISABLE KEYS */;
INSERT INTO `data_tata_tertib` VALUES (1,'wajib berada dilingkungan sekolah jam 07.15 wita dan pelajaran dimulai jam 07.30 wita.',NULL),(2,'wajib mengikuti upacara bendera setiap hari senin / upacara hari besar nasional yang diadakan oleh sekolah dengan berpakaian seragam sesuai ketentuan sekolah.',NULL),(3,'wajib mengerjakan tugas pembelajaran dari masing-masing guru dengan tepat waktu.',NULL),(4,'siswa yang terlambat akan diedukasi oleh guru bk.',NULL),(5,'senin: berpakaian putih biru, berdasi, badge osis dan identitas sekolah lengkap, sepatu hitam, berkaos kaki putih setengah lutut, dan ikat pinggang hitam.',NULL),(6,'selasa: berpakaian seragam batik kotak coklat, sepatu hitam, berkaos kaki putih setengah lutut, dan ikat pinggang hitam.',NULL),(7,'rabu: berpakaian seragam rompi hijau, sepatu hitam, berkaos kaki putih setengah lutut, dan ikat pinggang hitam.',NULL),(8,'kamis: berpakaian seragam batik kota, sepatu hitam, berkaos kaki putih setengah lutut, dan ikat pinggang hitam.',NULL),(9,'jumat: berpakaian pramuka, sepatu hitam, berkaos kaki hitam setengah lutut, dan ikat pinggang hitam.',NULL),(10,'Hari Senin- Kamis memakai kerudung putih dan mangset putih (Islam)',NULL),(11,'Hari Jumat memakai kerudung coklat tua dan mangset coklat tua (Islam)',NULL),(12,'Setiap jam pelajaran olahraga siswa diwajibkan memakai pakaian olahraga, berkerudung putih, dan mangset putih (Islam). Setelah selesai praktek olahraga siswa Kembali menganti pakaiannya sesuai aturan tata tertib sekolah.',NULL),(13,'Wajib mengikuti kegiatan Ekstrakurikuler (minimal 1 kegiatan Ekstrakurikuler).',NULL),(14,'Wajib menjaga ketenangan belajar baik dikelas, perpustakaan, laboratorium maupun ditempat lain dilingkungan sekolah.',NULL),(15,'Wajib menjaga nama baik sekolah baik didalam maupun diluar sekolah.',NULL),(16,'Wajib menghormati sesama warga sekolah (Kepala sekolah,Guru, Karyawan dan Siswa).',NULL),(17,'Membeli makanan waktu jam pelajaran / bergerombol di warung / kantin.',NULL),(18,'Membuang sampah tidak pada tempatnya (5).',NULL),(19,'Berhias yang berlebihan, memakai aksesories bagi peserta didik putri.',NULL),(20,'Rambut gondrong / disemir berwarna / tidak rapi (dicukur rapi 1 cm).',NULL),(21,'Mencoret-coret tembok, pintu, jendela, meja dan kursi.',NULL),(22,'Membolos / meninggalkan sekolah tanpa izin.',NULL),(23,'Membawa buku, majalah, VCD, dan gambar porno.',NULL),(24,'Membawa kendaraan bermotor di lingkungan sekolah.',NULL),(25,'Membawa dan merokok di lingkungan sekolah dan sekitarnya.',NULL),(26,'Berkelahi / main hakim sendiri / mengancam.',NULL),(27,'Merusak sarana prasarana sekolah.',NULL),(28,'Mencuri / memeras.',NULL),(29,'Membawa, mengancam dan melukai dengan senjata tajam dan sejenisnya.',NULL);
/*!40000 ALTER TABLE `data_tata_tertib` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `detail_admin`
--

DROP TABLE IF EXISTS `detail_admin`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `detail_admin` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `first_name` varchar(128) NOT NULL,
  `last_name` varchar(128) NOT NULL,
  `gender` varchar(32) DEFAULT NULL,
  `alamat` varchar(128) DEFAULT NULL,
  `user_id` int(11) DEFAULT NULL,
  `telp` varchar(20) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `user_id` (`user_id`),
  CONSTRAINT `detail_admin_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `detail_admin`
--

LOCK TABLES `detail_admin` WRITE;
/*!40000 ALTER TABLE `detail_admin` DISABLE KEYS */;
INSERT INTO `detail_admin` VALUES (2,'ADMIN','admin','laki-laki',NULL,5,NULL),(3,'Ar','iEfen','laki-laki','',47,NULL);
/*!40000 ALTER TABLE `detail_admin` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `detail_guru`
--

DROP TABLE IF EXISTS `detail_guru`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `detail_guru` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `first_name` varchar(128) NOT NULL,
  `last_name` varchar(128) NOT NULL,
  `gender` varchar(32) NOT NULL,
  `agama` varchar(32) DEFAULT NULL,
  `alamat` varchar(256) DEFAULT NULL,
  `telp` varchar(16) DEFAULT NULL,
  `user_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `user_id` (`user_id`),
  CONSTRAINT `detail_guru_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=22 DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `detail_guru`
--

LOCK TABLES `detail_guru` WRITE;
/*!40000 ALTER TABLE `detail_guru` DISABLE KEYS */;
INSERT INTO `detail_guru` VALUES (1,'Dra.','Rosmawati','perempuan','islam','-','-',6),(2,'Dra.','Haslinda','perempuan','islam','','',7),(3,'Harnidah,','S.Pd.','Perempuan','Islam','Makassar','08123535222222',8),(4,'Hj.','St. Nurbaya, S.Pd., M.Pd.','perempuan','islam','','',9),(5,'Hj.','Suriani, S.Ag.','perempuan','islam','','',10),(6,'Ruslan','Talebe, S.Pd.','laki-laki','islam','-','-',11),(7,'Rahmini,','S.Pd., M.MPd','perempuan','islam','','',12),(8,'Mariyani','Mannya, S.Pd.','perempuan','islam','','',13),(9,'Hj.','Sahiah, S.Pd','perempuan','islam','','',14),(10,'Sahabuddin,','S.Pd.','laki-laki','islam','Makassar','',15),(11,'Enny,','S.Pd, M.Pd.','perempuan','islam','','',41),(12,'Herlina,','S.Pd.','perempuan','islam','','',42),(13,'Nuraeny','Palesang, S.Pd.','perempuan','islam','','',43),(14,'Andi','Muliati, S.Pd., M.Pd.','perempuan','islam','','',44),(15,'Septri','Tangke, S.Pd.','perempuan','kristen','Makassar','-',45);
/*!40000 ALTER TABLE `detail_guru` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `detail_siswa`
--

DROP TABLE IF EXISTS `detail_siswa`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `detail_siswa` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `first_name` varchar(128) NOT NULL,
  `last_name` varchar(128) NOT NULL,
  `gender` varchar(32) NOT NULL,
  `tempat_lahir` varchar(128) DEFAULT NULL,
  `tgl_lahir` date DEFAULT NULL,
  `agama` varchar(128) NOT NULL,
  `nama_ortu_or_wali` varchar(128) DEFAULT NULL,
  `no_telp` varchar(16) DEFAULT NULL,
  `alamat` varchar(250) DEFAULT NULL,
  `qr_code` text DEFAULT NULL,
  `pic` text DEFAULT NULL,
  `user_id` int(11) DEFAULT NULL,
  `kelas_id` int(11) DEFAULT NULL,
  `id_card` varchar(128) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `kelas_id` (`kelas_id`),
  KEY `user_id` (`user_id`),
  CONSTRAINT `detail_siswa_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `detail_siswa_ibfk_2` FOREIGN KEY (`kelas_id`) REFERENCES `master_kelas` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=37 DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `detail_siswa`
--

LOCK TABLES `detail_siswa` WRITE;
/*!40000 ALTER TABLE `detail_siswa` DISABLE KEYS */;
INSERT INTO `detail_siswa` VALUES (5,'Ar','Rijal Dhaffa Nugraha','laki-laki',NULL,NULL,'islam',NULL,'',NULL,'VIII-1_rijal_3fb661f3f82b97dec979e77d66abf644.png','VIII-1_rijal_010f870e51fa978466e650643a3774ce.jpg',16,9,'VIII-1_Ar_64d7.png'),(6,'ALISYAH','Putri Ramadhani','perempuan','Makassar','2023-09-29','islam','','','','VIII-1_alisyah_90dc225705eeaeb5abb97227413647fa.png','VIII-1_alisyah_ef250c179ad9761f7cf7a7540bde7bc7.jpg',17,9,'VIII-1_Alisyah_0502.png'),(7,'ANANDA','PUTRI AURELIA AKBAR','perempuan',NULL,NULL,'islam',NULL,'',NULL,'VIII-1_ananda_48ddf3afe6e410cbeca3ad26d07d393a.png','VIII-1_ananda_2723e6507466a67487fec0d4146addb2.jpg',18,9,'VIII-1_Ananda_000d.png'),(8,'RHIFQI','ASHRAF SHANDY','laki-laki',NULL,NULL,'islam',NULL,'',NULL,'VIII-1_rhifqi_a80b09af269cd4d0691b5a7efc0833e0.png','VIII-1_rhifqi_cbade01b0230afdd162297c8156bc79f.jpg',19,9,'VIII-1_Rhifqi_6bd0.png'),(9,'Salsabila','Azisah Az Zahra','perempuan',NULL,NULL,'islam',NULL,'',NULL,'VIII-1_salsabila_1fc49a06f936cdc6ee3b10f1ccead8a3.png','VIII-1_salsabila_d7835a77f3a7b813b4c0911379437063.jpg',20,9,'VIII-1_Salsabila_bcb1.png'),(10,'A.','ZHIL ZHILLAH ANUGRAH TANDIARI','perempuan',NULL,NULL,'islam',NULL,'',NULL,'VIII-2_zhil_dd1cb5affc968d080340660d82a0c7d7.png','VIII-2_zhil_ed6d3d7d3323f0301bb2e3ed348ac92b.jpg',21,10,'VIII-2_A._fc56.png'),(11,'ADZKIYAH','ADELIAH','perempuan',NULL,NULL,'islam',NULL,'',NULL,'VIII-2_adzkiyah_dd1b9da82be2cd5725f675ff0f4bf7b6.png','VIII-2_adzkiyah_fe043f36b17e2a605a95bda25717f2a0.jpg',22,10,'VIII-2_Adzkiyah_551f.png'),(12,'M.','Dede Irza Saputra','laki-laki',NULL,NULL,'islam',NULL,'',NULL,'VIII-2_dede_ae5b11e8c4054c34156d5ff925e47434.png','VIII-2_dede_728a686e00c14393052e995ea82b4053.jpg',23,10,'VIII-2_dede_9691.png'),(13,'Lingga','Gwen Safitri','perempuan',NULL,NULL,'islam',NULL,'',NULL,'VIII-2_lingga_d953813380050d002e3ecf8bf1971fb7.png','VIII-2_lingga_b68c5f417b5b7f403b21f1a5e317fac7.jpg',24,10,'VIII-2_Lingga_8128.png'),(14,'RAFA','PUTRA RAMADHAN. A','laki-laki',NULL,NULL,'islam',NULL,'',NULL,'VIII-2_rafa_8276b7f00c93e5002951d8c5bf0845dc.png','VIII-2_rafa_22ce238586bc6c688fbb03137c473aaf.jpg',25,10,'VIII-2_Rafa_efa8.png'),(15,'Ahmad','Fachri Al Farabi','laki-laki',NULL,NULL,'islam',NULL,'',NULL,'VIII-3_ahmad_b9d2adcdc32768ecb2c6349191572ee4.png','VIII-3_ahmad_10da75cd962ef04bf5093ce2039f3896.jpg',26,11,'VIII-3_Ahmad_244b.png'),(16,'ALIKA','ZAYRAH DWI SEPTIA K','perempuan',NULL,NULL,'islam',NULL,'',NULL,'VIII-3_alika_5bb0ff40069dcd55d595dc599f444542.png','VIII-3_alika_d2c973235ba921ca9f4f4c5acbbe645e.jpg',27,11,'VIII-3_Alika_faff.png'),(17,'Aqyla','Utami Putri Patriot','perempuan',NULL,NULL,'islam',NULL,'',NULL,'VIII-3_aqyla_374cce385e9aaad0c2a6ea26b19f0bdb.png','VIII-3_aqyla_97ffc205467692eac894a09cf5031b36.jpg',28,11,'VIII-3_Aqyla_8f04.png'),(18,'BIMA','SASTRANEGARA ARY PUTRA','laki-laki',NULL,NULL,'islam',NULL,'',NULL,'VIII-3_bima_e7cd529a1f13434c8ec679c36ce914a4.png','VIII-3_bima_686769f092919202ad1b36706c89010b.jpg',29,11,'VIII-3_Bima_d777.png'),(19,'Sitti','Adelia Mukarramah Munafr','perempuan',NULL,NULL,'islam',NULL,'',NULL,'VIII-3_sitti_e45ca191eefb3a31625c5a63bd5ce75d.png','VIII-3_sitti_34ebec4cd16d3d83c1abdc377eadb593.jpg',30,11,NULL),(20,'A.','AYU APRILIA','perempuan',NULL,NULL,'islam',NULL,'',NULL,'VIII-4_ayu_9d49bef99066e1c3f618c44241004454.png','VIII-4_ayu_e7c5a463e7e7b33bf94c15fa44ea2b49.jpg',31,12,NULL),(21,'Andi','Irgi','laki-laki',NULL,NULL,'islam',NULL,'',NULL,NULL,NULL,32,13,NULL),(22,'AHMAD','AL FAHREZI','laki-laki',NULL,NULL,'islam',NULL,'',NULL,'VIII-4_ahmad_68d329bbd833b043d37b83277cd7240c.png','VIII-4_ahmad_d78b659a3ea2c7a774d7c35d045ed21f.jpg',33,12,NULL),(23,'Andi','Wafiqah Raidah Khamilah','perempuan',NULL,NULL,'islam',NULL,'',NULL,'VIII-4_andi_4f441d35a139d245dec241ad857b325b.png','VIII-4_andi_1d94afc59469fcf5e93aa1f578bf68a9.jpg',34,12,NULL),(24,'Muh.','Rifqy Athaillah Hamran','laki-laki',NULL,NULL,'islam',NULL,'',NULL,'VIII-4_muh._d8a219fd4387911794e0bc6543e14172.png','VIII-4_muh._db3d7b9e17883ddac285a6e222a355fc.jpg',35,12,NULL),(25,'SARIFA','ALIFIYAH ISWANDI','perempuan',NULL,NULL,'islam',NULL,'',NULL,'VIII-4_sarifa_41a96a537bf0d6524be4b47d24d20d2c.png','VIII-4_sarifa_1e5ecb3e077c9424888e9c8a75c04c4f.jpg',36,12,NULL),(26,'Andini','Nur Rahmania','perempuan',NULL,NULL,'islam',NULL,'',NULL,NULL,NULL,37,13,NULL),(27,'Fadlan','Nurrahman','laki-laki',NULL,NULL,'islam',NULL,'',NULL,NULL,NULL,38,13,NULL),(28,'MUH.','SUPOMO GUNTUR IRWAN','laki-laki',NULL,NULL,'islam',NULL,'',NULL,NULL,NULL,39,13,NULL),(29,'Nur','Aini Indira Rihaz','perempuan',NULL,NULL,'islam',NULL,'',NULL,NULL,NULL,40,13,NULL);
/*!40000 ALTER TABLE `detail_siswa` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `master_guru_bk`
--

DROP TABLE IF EXISTS `master_guru_bk`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `master_guru_bk` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `guru_id` int(11) DEFAULT NULL,
  `status` varchar(1) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `guru_id` (`guru_id`),
  CONSTRAINT `master_guru_bk_ibfk_1` FOREIGN KEY (`guru_id`) REFERENCES `detail_guru` (`user_id`) ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=12 DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `master_guru_bk`
--

LOCK TABLES `master_guru_bk` WRITE;
/*!40000 ALTER TABLE `master_guru_bk` DISABLE KEYS */;
INSERT INTO `master_guru_bk` VALUES (1,45,NULL),(11,6,'0');
/*!40000 ALTER TABLE `master_guru_bk` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `master_hari`
--

DROP TABLE IF EXISTS `master_hari`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `master_hari` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `hari` varchar(32) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `master_hari`
--

LOCK TABLES `master_hari` WRITE;
/*!40000 ALTER TABLE `master_hari` DISABLE KEYS */;
INSERT INTO `master_hari` VALUES (1,'senin'),(2,'selasa'),(3,'rabu'),(4,'kamis'),(5,'jumat');
/*!40000 ALTER TABLE `master_hari` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `master_jadwal_mengajar`
--

DROP TABLE IF EXISTS `master_jadwal_mengajar`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `master_jadwal_mengajar` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `kode_mengajar` varchar(32) DEFAULT NULL,
  `guru_id` int(11) DEFAULT NULL,
  `mapel_id` int(11) DEFAULT NULL,
  `jam_ke` varchar(6) DEFAULT NULL,
  `hari_id` int(11) DEFAULT NULL,
  `jam_mulai` varchar(12) DEFAULT NULL,
  `jam_selesai` varchar(12) DEFAULT NULL,
  `kelas_id` int(11) DEFAULT NULL,
  `semester_id` int(11) DEFAULT NULL,
  `tahun_ajaran_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `guru_id` (`guru_id`),
  KEY `hari_id` (`hari_id`),
  KEY `kelas_id` (`kelas_id`),
  KEY `mapel_id` (`mapel_id`),
  KEY `semester_id` (`semester_id`),
  KEY `tahun_ajaran_id` (`tahun_ajaran_id`),
  CONSTRAINT `master_jadwal_mengajar_ibfk_1` FOREIGN KEY (`tahun_ajaran_id`) REFERENCES `master_tahun_ajaran` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `master_jadwal_mengajar_ibfk_2` FOREIGN KEY (`mapel_id`) REFERENCES `master_mapel` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `master_jadwal_mengajar_ibfk_3` FOREIGN KEY (`kelas_id`) REFERENCES `master_kelas` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `master_jadwal_mengajar_ibfk_4` FOREIGN KEY (`hari_id`) REFERENCES `master_hari` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `master_jadwal_mengajar_ibfk_5` FOREIGN KEY (`guru_id`) REFERENCES `detail_guru` (`user_id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `master_jadwal_mengajar_ibfk_6` FOREIGN KEY (`semester_id`) REFERENCES `master_semester` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=195 DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `master_jadwal_mengajar`
--

LOCK TABLES `master_jadwal_mengajar` WRITE;
/*!40000 ALTER TABLE `master_jadwal_mengajar` DISABLE KEYS */;
INSERT INTO `master_jadwal_mengajar` VALUES (33,'MPL-955566',9,2,'1-3',1,'07:30','09:30',9,1,2),(34,'MPL-642394',14,3,'4-5',1,'09:30','11:00',9,1,2),(35,'MPL-2049658',8,6,'6-8',1,'11:00','12:55',9,1,2),(36,'MPL-649138',8,6,'1-3',1,'07:30','09:30',10,1,2),(37,'MPL-8917823',15,5,'4-5',1,'09:30','11:00',10,1,2),(38,'MPL-2699945',12,1,'6-8',1,'11:00','12:55',10,1,2),(39,'MPL-9091926',12,1,'1-2',1,'07:30','08:50',11,1,2),(40,'MPL-0855632',15,5,'3',1,'08:50','09:30',11,1,2),(41,'MPL-496497',10,8,'4-6',1,'09:30','11:40',11,1,2),(42,'MPL-1266716',14,3,'7-8',1,'11:40','12:55',11,1,2),(43,'MPL-4209483',13,4,'1-3',1,'07:30','09:30',12,1,2),(44,'MPL-7297764',42,2,'4-5',1,'09:30','11:00',12,1,2),(45,'MPL-2787924',43,1,'6-8',1,'11:00','12:55',12,1,2),(46,'MPL-964149',14,3,'1-2',1,'07:30','08:50',13,1,2),(47,'MPL-935434',43,1,'3-5',1,'08:50','11:00',13,1,2),(48,'MPL-7705064',13,4,'6-8',1,'11:00','12:55',13,1,2),(49,'MPL-769659',13,4,'1-3',2,'07:15','09:15',9,1,2),(50,'MPL-4828076',41,7,'4-5',2,'09:15','10:45',9,1,2),(51,'MPL-971107',10,8,'6-8',2,'10:45','12:40',9,1,2),(52,'MPL-624748',8,6,'1-2',2,'07:15','08:35',10,1,2),(53,'MPL-9747136',10,8,'3-5',2,'08:35','10:45',10,1,2),(54,'MPL-5785005',12,1,'6-8',2,'10:45','12:40',10,1,2),(55,'MPL-3774605',9,2,'1-3',2,'07:15','09:15',11,1,2),(56,'MPL-4230661',13,4,'4-6',2,'09:15','11:25',11,1,2),(57,'MPL-2690954',41,7,'7-8',2,'11:25','12:40',11,1,2),(58,'MPL-3618176',6,7,'1-2',2,'07:15','08:35',12,1,2),(59,'MPL-6286607',8,6,'3-5',2,'08:35','10:45',12,1,2),(60,'MPL-2728553',42,2,'6-8',2,'10:45','12:40',12,1,2),(61,'MPL-2372444',11,10,'1-3',2,'07:15','09:15',13,1,2),(62,'MPL-4727843',6,7,'4-5',2,'09:15','10:45',13,1,2),(63,'MPL-145499',8,6,'6-8',2,'10:45','12:40',13,1,2),(64,'MPL-0572498',12,1,'1-3',3,'07:15','09:15',9,1,2),(65,'MPL-9665446',8,6,'4-5',3,'09:15','10:45',9,1,2),(66,'MPL-1854267',7,9,'6-8',3,'10:45','12:40',9,1,2),(67,'MPL-3523862',13,4,'1-3',3,'07:15','09:15',10,1,2),(68,'MPL-7090046',11,10,'4-6',3,'09:15','11:25',10,1,2),(69,'MPL-553489',14,3,'7-8',3,'11:25','12:40',10,1,2),(70,'MPL-9910965',8,6,'1-3',3,'07:15','09:15',11,1,2),(71,'MPL-7209883',12,1,'4-5',3,'09:15','10:45',11,1,2),(72,'MPL-8258874',15,5,'6',3,'10:45','11:25',11,1,2),(73,'MPL-030209',9,2,'7-8',3,'11:25','12:40',11,1,2),(74,'MPL-8716755',7,9,'1-3',3,'07:15','09:15',12,1,2),(75,'MPL-3001113',14,3,'4-5',3,'09:15','10:45',12,1,2),(76,'MPL-9592643',10,8,'6-8',3,'10:45','12:40',12,1,2),(77,'MPL-8577526',42,2,'1-2',3,'07:15','08:35',13,1,2),(78,'MPL-6703382',15,5,'3-4',3,'08:35','09:50',13,1,2),(79,'MPL-10255',6,7,'5-6',3,'10:05','11:25',13,1,2),(80,'MPL-079401',8,6,'7-8',3,'11:25','12:40',13,1,2),(81,'MPL-5040846',41,7,'1-2',4,'07:15','08:35',9,1,2),(82,'MPL-2512572',9,2,'3-4',4,'08:35','09:50',9,1,2),(83,'MPL-33468',15,5,'5-6',4,'10:05','11:25',9,1,2),(84,'MPL-6281545',14,3,'7-8',4,'11:25','12:40',9,1,2),(85,'MPL-069096',7,9,'1-3',4,'07:15','09:15',10,1,2),(86,'MPL-3795192',6,7,'4-5',4,'09:15','10:45',10,1,2),(87,'MPL-9334261',9,2,'6-8',4,'10:45','12:40',10,1,2),(88,'MPL-7867444',11,10,'1-3',4,'07:15','09:15',11,1,2),(89,'MPL-363804',12,1,'4-5',4,'09:15','10:45',11,1,2),(90,'MPL-9890945',7,9,'6-8',4,'10:45','12:40',11,1,2),(91,'MPL-2045546',43,1,'1-3',4,'07:15','09:15',12,1,2),(92,'MPL-832374',11,10,'4-6',4,'09:15','11:25',12,1,2),(93,'MPL-9587512',6,7,'7-8',4,'11:25','12:40',12,1,2),(94,'MPL-9440625',10,8,'1-3',4,'07:15','09:15',13,1,2),(95,'MPL-2316525',14,3,'4-5',4,'09:15','10:45',13,1,2),(96,'MPL-889407',42,2,'6-8',4,'10:45','12:40',13,1,2),(97,'MPL-5329022',12,1,'1-3',5,'07:15','09:15',9,1,2),(98,'MPL-6249998',11,10,'4-6',5,'09:15','11:30',9,1,2),(99,'MPL-364484',9,2,'1-2',5,'07:15','08:35',10,1,2),(100,'MPL-4111667',41,7,'3-4',5,'08:35','10:10',10,1,2),(101,'MPL-7619693',14,3,'5-6',5,'10:10','11:30',10,1,2),(102,'MPL-1705787',14,3,'1-2',5,'07:15','08:35',11,1,2),(103,'MPL-1095114',8,6,'3-4',5,'08:35','10:10',11,1,2),(104,'MPL-8916461',41,7,'5-6',5,'10:10','11:30',11,1,2),(105,'MPL-8990536',8,6,'1-2',5,'07:15','08:35',12,1,2),(106,'MPL-9599771',14,3,'3-4',5,'08:35','10:10',12,1,2),(107,'MPL-1323905',15,5,'5-6',5,'10:10','11:30',12,1,2),(108,'MPL-668466',43,1,'1-3',5,'07:15','09:15',13,1,2),(109,'MPL-028389',7,9,'4-6',5,'09:15','11:30',13,1,2),(112,'MPL-755727',8,6,'1-3',1,'07:30','09:30',9,2,3),(113,'MPL-435962',14,3,'4-5',1,'09:30','11:00',9,2,3),(115,'MPL-6679351',6,7,'1-2',1,'07:30','08:50',10,2,3),(116,'MPL-8708794',12,1,'3-5',1,'08:50','11:00',10,2,3),(117,'MPL-2415986',14,3,'6-8',1,'11:00','12:55',10,2,3),(118,'MPL-3027883',13,4,'1-3',1,'07:30','09:30',11,2,3),(119,'MPL-6737182',8,6,'3-5',1,'09:30','11:00',11,2,3),(120,'MPL-6186533',12,1,'6-8',1,'11:00','12:55',11,2,3),(121,'MPL-5969248',42,2,'1-3',1,'07:30','09:30',12,2,3),(122,'MPL-605567',43,1,'4-5',1,'09:30','11:00',12,2,3),(123,'MPL-2748168',13,4,'6-8',1,'11:00','12:55',12,2,3),(124,'MPL-833579',14,3,'1-2',1,'07:30','08:50',13,2,3),(125,'MPL-0531113',13,4,'3-5',1,'08:50','11:00',13,2,3),(126,'MPL-5996518',8,6,'6-8',1,'11:00','12:55',13,2,3),(127,'MPL-0325942',8,6,'1-2',2,'07:15','08:35',9,2,3),(128,'MPL-2878656',10,8,'3-5',2,'08:35','10:45',9,2,3),(129,'MPL-6375954',13,4,'6-8',2,'10:45','12:40',9,2,3),(130,'MPL-6180506',13,4,'1-3',2,'07:15','09:15',10,2,3),(131,'MPL-3506382',6,7,'4-5',2,'09:15','10:45',10,2,3),(132,'MPL-1222904',7,9,'6-8',2,'10:45','12:40',10,2,3),(133,'MPL-0286024',14,3,'1-2',2,'07:15','08:35',11,2,3),(134,'MPL-3330681',9,2,'3-4',2,'08:35','09:50',11,2,3),(135,'MPL-5779834',15,5,'5-6',2,'10:05','11:25',11,2,3),(136,'MPL-346273',6,7,'7-8',2,'11:25','12:40',11,2,3),(137,'MPL-6023285',6,7,'1-2',2,'07:15','08:35',12,2,3),(138,'MPL-6821947',14,3,'3-4',2,'08:35','09:50',12,2,3),(139,'MPL-1847467',42,2,'5-6',2,'10:05','11:25',12,2,3),(140,'MPL-188859',15,5,'7-8',2,'11:25','12:40',12,2,3),(141,'MPL-785504',11,10,'1-3',2,'07:15','09:15',13,2,3),(142,'MPL-2169073',41,7,'4-5',2,'09:15','10:45',13,2,3),(143,'MPL-8206234',42,2,'6-8',2,'10:45','12:40',13,2,3),(144,'MPL-4968593',7,9,'1-3',3,'07:15','09:15',9,2,3),(145,'MPL-1112165',6,7,'4-5',3,'09:15','10:45',9,2,3),(146,'MPL-648244',12,1,'6-8',3,'10:45','12:40',9,2,3),(147,'MPL-7490735',8,6,'1-3',3,'07:15','09:15',10,2,3),(148,'MPL-8051336',10,8,'4-6',3,'09:15','10:45',10,2,3),(149,'MPL-6183774',9,2,'7-8',3,'11:25','12:40',10,2,3),(150,'MPL-779516',14,3,'1-2',3,'07:15','08:35',11,2,3),(151,'MPL-7298357',9,2,'3-5',3,'08:35','10:45',11,2,3),(152,'MPL-1705167',8,6,'6-8',3,'10:45','12:40',11,2,3),(153,'MPL-9820788',43,1,'1-3',3,'07:15','09:15',12,2,3),(154,'MPL-332902',8,6,'4-6',3,'09:15','11:25',12,2,3),(155,'MPL-333568',6,7,'7-8',3,'11:25','12:40',12,2,3),(156,'MPL-2084005',42,2,'1-2',3,'07:15','08:35',13,2,3),(157,'MPL-5733984',41,7,'3-4',3,'08:35','09:50',13,2,3),(158,'MPL-6804042',14,3,'5-6',3,'10:05','11:25',13,2,3),(159,'MPL-930351',8,6,'7-8',3,'11:25','12:40',13,2,3),(161,'MPL-8336408',15,5,'1-2',4,'07:15','08:35',9,2,3),(162,'MPL-6924512',14,3,'3-4',4,'08:35','09:50',9,2,3),(163,'MPL-791072',9,2,'5-6',4,'10:05','11:25',9,2,3),(164,'MPL-1200526',6,7,'7-8',4,'11:25','12:40',9,2,3),(165,'MPL-3520443',9,2,'1-3',4,'07:15','09:15',10,2,3),(166,'MPL-254096',14,3,'4-4',4,'09:15','09:50',10,2,3),(167,'MPL-240704',15,5,'5-6',4,'10:05','11:25',10,2,3),(168,'MPL-4340258',8,6,'7-8',4,'11:25','12:40',10,2,3),(169,'MPL-3118281',12,1,'1-3',4,'07:15','09:15',11,2,3),(170,'MPL-4331458',11,10,'4-6',4,'09:15','11:25',11,2,3),(171,'MPL-5371654',6,7,'7-8',4,'11:25','12:40',11,2,3),(172,'MPL-928894',11,10,'1-3',4,'07:15','09:15',12,2,3),(173,'MPL-9722493',8,6,'4-5',4,'09:15','10:45',12,2,3),(174,'MPL-5408037',43,1,'6-8',4,'10:45','12:40',12,2,3),(175,'MPL-668023',43,1,'1-3',4,'07:15','09:15',13,2,3),(176,'MPL-1152382',10,8,'4-6',4,'09:15','11:25',13,2,3),(177,'MPL-55545',15,5,'7-8',4,'11:25','12:40',13,2,3),(178,'MPL-7604895',11,10,'1-3',5,'07:15','09:15',9,2,3),(179,'MPL-0601692',12,1,'4-6',5,'09:30','11:30',9,2,3),(180,'MPL-3630369',12,1,'1-3',5,'07:15','09:15',10,2,3),(181,'MPL-463091',11,10,'4-6',5,'09:30','11:30',10,2,3),(182,'MPL-7754557',8,6,'1-3',5,'07:15','09:15',11,2,3),(183,'MPL-650777',10,8,'4-6',5,'09:30','11:30',11,2,3),(184,'MPL-0959477',10,8,'1-3',5,'07:15','09:15',12,2,3),(185,'MPL-1841729',7,9,'4-6',5,'09:30','11:30',12,2,3),(186,'MPL-7605772',7,9,'1-3',5,'07:15','09:15',13,2,3),(187,'MPL-262811',43,1,'4-6',5,'09:30','11:30',13,2,3),(188,'MPL-0955887',9,2,'5-6',1,'11:25','12:55',9,1,2);
/*!40000 ALTER TABLE `master_jadwal_mengajar` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `master_jam_mengajar`
--

DROP TABLE IF EXISTS `master_jam_mengajar`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `master_jam_mengajar` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `jam` varchar(32) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=14 DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `master_jam_mengajar`
--

LOCK TABLES `master_jam_mengajar` WRITE;
/*!40000 ALTER TABLE `master_jam_mengajar` DISABLE KEYS */;
INSERT INTO `master_jam_mengajar` VALUES (1,'07:00'),(2,'07:15'),(3,'07:30'),(4,'07:45'),(5,'08:00'),(6,'08:30'),(7,'09:00'),(8,'09:30'),(9,'10:00'),(10,'10:30'),(11,'11:00'),(12,'11:30'),(13,'12:00');
/*!40000 ALTER TABLE `master_jam_mengajar` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `master_kelas`
--

DROP TABLE IF EXISTS `master_kelas`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `master_kelas` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `kelas` varchar(16) NOT NULL,
  `jml_laki` int(11) DEFAULT NULL,
  `jml_perempuan` int(11) DEFAULT NULL,
  `jml_seluruh` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=30 DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `master_kelas`
--

LOCK TABLES `master_kelas` WRITE;
/*!40000 ALTER TABLE `master_kelas` DISABLE KEYS */;
INSERT INTO `master_kelas` VALUES (9,'VIII-1',2,3,5),(10,'VIII-2',2,3,5),(11,'VIII-3',2,3,5),(12,'VIII-4',2,3,5),(13,'VIII-5',3,2,5);
/*!40000 ALTER TABLE `master_kelas` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `master_kepsek`
--

DROP TABLE IF EXISTS `master_kepsek`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `master_kepsek` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `guru_id` int(11) DEFAULT NULL,
  `status` varchar(2) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `guru_id` (`guru_id`),
  CONSTRAINT `master_kepsek_ibfk_1` FOREIGN KEY (`guru_id`) REFERENCES `detail_guru` (`user_id`) ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=26 DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `master_kepsek`
--

LOCK TABLES `master_kepsek` WRITE;
/*!40000 ALTER TABLE `master_kepsek` DISABLE KEYS */;
INSERT INTO `master_kepsek` VALUES (25,44,'1');
/*!40000 ALTER TABLE `master_kepsek` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `master_mapel`
--

DROP TABLE IF EXISTS `master_mapel`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `master_mapel` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `mapel` varchar(64) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=20 DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `master_mapel`
--

LOCK TABLES `master_mapel` WRITE;
/*!40000 ALTER TABLE `master_mapel` DISABLE KEYS */;
INSERT INTO `master_mapel` VALUES (1,'Bahasa Indonesia'),(2,'Matematika'),(3,'Bahasa Inggris'),(4,'Seni Budaya'),(5,'Prakarya'),(6,'Ilmu Pengetahuan Alam'),(7,'Ilmu Pengetahuan Sosial'),(8,'Pendidikan Agama Islam'),(9,'Pendidikan Kewarganegaraan'),(10,'Pendidikan Jasmani, Olahraga, dan Kesehatan');
/*!40000 ALTER TABLE `master_mapel` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `master_nama_bulan`
--

DROP TABLE IF EXISTS `master_nama_bulan`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `master_nama_bulan` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `nama_bulan` varchar(32) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=14 DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `master_nama_bulan`
--

LOCK TABLES `master_nama_bulan` WRITE;
/*!40000 ALTER TABLE `master_nama_bulan` DISABLE KEYS */;
INSERT INTO `master_nama_bulan` VALUES (1,'januari'),(2,'februari'),(3,'maret'),(4,'april'),(5,'mei'),(6,'juni'),(7,'juli'),(8,'agustus'),(9,'september'),(10,'oktober'),(11,'november'),(12,'desember');
/*!40000 ALTER TABLE `master_nama_bulan` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `master_semester`
--

DROP TABLE IF EXISTS `master_semester`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `master_semester` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `semester` varchar(32) NOT NULL,
  `is_active` varchar(1) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `master_semester`
--

LOCK TABLES `master_semester` WRITE;
/*!40000 ALTER TABLE `master_semester` DISABLE KEYS */;
INSERT INTO `master_semester` VALUES (1,'genap','0'),(2,'ganjil','1');
/*!40000 ALTER TABLE `master_semester` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `master_tahun`
--

DROP TABLE IF EXISTS `master_tahun`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `master_tahun` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `tahun` varchar(4) NOT NULL,
  `status` varchar(6) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `tahun` (`tahun`)
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `master_tahun`
--

LOCK TABLES `master_tahun` WRITE;
/*!40000 ALTER TABLE `master_tahun` DISABLE KEYS */;
INSERT INTO `master_tahun` VALUES (4,'2021','0'),(7,'2022','1'),(8,'2023','1');
/*!40000 ALTER TABLE `master_tahun` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `master_tahun_ajaran`
--

DROP TABLE IF EXISTS `master_tahun_ajaran`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `master_tahun_ajaran` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `th_ajaran` varchar(32) NOT NULL,
  `is_active` varchar(1) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `master_tahun_ajaran`
--

LOCK TABLES `master_tahun_ajaran` WRITE;
/*!40000 ALTER TABLE `master_tahun_ajaran` DISABLE KEYS */;
INSERT INTO `master_tahun_ajaran` VALUES (1,'2021-2022','0'),(2,'2022-2023','0'),(3,'2023-2024','1');
/*!40000 ALTER TABLE `master_tahun_ajaran` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `master_wali_kelas`
--

DROP TABLE IF EXISTS `master_wali_kelas`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `master_wali_kelas` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `guru_id` int(11) DEFAULT NULL,
  `kelas_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `guru_id` (`guru_id`),
  KEY `kelas_id` (`kelas_id`),
  CONSTRAINT `master_wali_kelas_ibfk_1` FOREIGN KEY (`kelas_id`) REFERENCES `master_kelas` (`id`),
  CONSTRAINT `master_wali_kelas_ibfk_2` FOREIGN KEY (`guru_id`) REFERENCES `detail_guru` (`user_id`)
) ENGINE=InnoDB AUTO_INCREMENT=13 DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `master_wali_kelas`
--

LOCK TABLES `master_wali_kelas` WRITE;
/*!40000 ALTER TABLE `master_wali_kelas` DISABLE KEYS */;
INSERT INTO `master_wali_kelas` VALUES (1,7,9),(2,8,11),(3,10,13),(4,12,10),(5,13,12);
/*!40000 ALTER TABLE `master_wali_kelas` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2023-11-07 11:24:09
