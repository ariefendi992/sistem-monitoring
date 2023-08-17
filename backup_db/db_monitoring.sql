-- phpMyAdmin SQL Dump
-- version 5.2.0
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Aug 17, 2023 at 10:39 PM
-- Server version: 10.4.25-MariaDB
-- PHP Version: 7.4.30

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `db_monitoring`
--

-- --------------------------------------------------------

--
-- Table structure for table `alembic_version`
--

CREATE TABLE `alembic_version` (
  `version_num` varchar(32) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `alembic_version`
--

INSERT INTO `alembic_version` (`version_num`) VALUES
('734cfb5c95db');

-- --------------------------------------------------------

--
-- Table structure for table `auth_status_user_login`
--

CREATE TABLE `auth_status_user_login` (
  `id` varchar(36) NOT NULL,
  `user_login_id` int(11) DEFAULT NULL,
  `status_login` tinyint(1) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `auth_status_user_login`
--

INSERT INTO `auth_status_user_login` (`id`, `user_login_id`, `status_login`) VALUES
('34411d51-16e0-4639-8358-cdc47f868e54', 21, 0),
('42efb905-f0fe-4d6a-8f05-b9323594478c', 20, 0),
('bdbf5fb2-3b8d-49dd-8f19-8ab20acc87a6', 16, 1),
('ff3c3643-e739-4c4e-8b5a-9497c45bf3c4', 19, 0);

-- --------------------------------------------------------

--
-- Table structure for table `auth_token_block`
--

CREATE TABLE `auth_token_block` (
  `id` int(11) NOT NULL,
  `jti` varchar(36) NOT NULL,
  `created_at` datetime NOT NULL,
  `user_id` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `auth_token_block`
--

INSERT INTO `auth_token_block` (`id`, `jti`, `created_at`, `user_id`) VALUES
(24, 'bf9dce7f-751c-4ac8-a9f2-55163fabc429', '2023-05-11 00:09:13', NULL),
(25, 'e9879307-b48d-45a0-8f10-a9d94ea8b8dc', '2023-05-17 12:53:56', NULL),
(26, 'c6d4d132-d242-4704-8ccf-89221a8fe103', '2023-05-17 12:54:16', NULL),
(27, '676f1550-d666-4179-ab0f-c0f849523010', '2023-05-17 12:54:22', NULL),
(28, '5f4b8ba8-59ef-4ce2-a200-f8d4c4852050', '2023-05-17 12:54:38', NULL),
(29, '360dc288-9918-47b9-9bfa-f3d4c7d69b18', '2023-05-18 11:48:06', NULL),
(30, '4a1e497d-7de9-4ba6-9560-70ec7d90744d', '2023-05-18 11:54:07', NULL),
(31, 'dbe7b656-b4f5-4d9f-9014-0e906cf4d5f0', '2023-05-18 11:55:44', NULL),
(32, '466b6187-9374-435e-83e7-977c1c0f03fc', '2023-05-18 11:57:25', NULL),
(33, 'f709b1aa-4a83-4d5e-a7e2-107023695014', '2023-05-18 11:58:14', NULL),
(34, 'b17de407-15b9-47e3-b47f-4d13a216d757', '2023-05-18 11:58:30', NULL),
(35, '9db40ff5-c604-40d4-a993-866b6b8c7c0e', '2023-05-18 11:58:35', NULL),
(36, 'ed9dff05-2c85-445a-b6fe-4a484f71cd3d', '2023-05-18 11:59:09', NULL),
(37, '4e442020-7fb8-4ece-b202-c7b2adb24456', '2023-05-18 11:59:25', NULL),
(38, '279613e2-6aed-4581-8e83-e8e010054058', '2023-05-18 12:00:30', NULL),
(39, '527c79b3-6f69-4be8-ba7e-c56c611e110c', '2023-05-18 12:01:06', NULL),
(40, '24ac3450-aabf-459a-b0a1-77be7c77e74b', '2023-05-18 12:01:58', NULL),
(41, 'b082ded3-c283-466b-adcc-83144551eccb', '2023-05-18 12:02:33', NULL),
(42, 'abd2aa40-cc90-419e-b804-1781eda36b7b', '2023-05-18 12:03:10', NULL),
(43, 'e39351a6-8a6c-4179-ae11-b7bb84c84671', '2023-05-18 12:03:49', NULL),
(44, 'e05544b9-436b-4e7f-95f2-69d62e36a87e', '2023-05-18 20:57:12', NULL),
(45, 'c7a30bb5-2209-439f-9b53-58a039ab11b6', '2023-05-19 02:35:59', NULL),
(46, '081ae796-518d-4e4f-bfe7-f8591ac695b4', '2023-05-22 18:02:44', NULL),
(47, '677193f6-2b0b-4a66-a066-74214e6e0ab5', '2023-05-22 18:05:20', NULL),
(48, '770fb65e-c1e5-4ab7-882e-66b8b3acfb03', '2023-05-22 18:09:54', NULL),
(49, 'fe7aaa3c-1436-456e-8684-ac457171d76e', '2023-05-22 19:41:43', NULL),
(50, '22c45ee0-cba2-4021-bfeb-98591724f6f2', '2023-05-22 19:42:20', NULL),
(51, '6c3ca347-1694-4be1-be8e-437376802970', '2023-05-22 19:49:06', NULL),
(52, '8d9c4489-c063-45d4-a97e-f4e4740e292b', '2023-05-22 20:28:32', NULL),
(53, 'aa6e50c7-b86b-4f28-9e66-309e9da17bc8', '2023-05-22 20:29:06', NULL),
(54, '55d62083-d0df-40dd-b82d-895ca101a8dc', '2023-05-22 20:30:47', NULL),
(55, '989ccaef-8454-4146-bfed-ee928b977429', '2023-05-22 20:31:02', NULL),
(56, 'a9ffff5e-3c0f-412b-907f-ffbec86b2f8f', '2023-05-24 01:08:58', NULL),
(57, '093a04b8-b895-424d-9fa1-2a509128af98', '2023-05-24 03:42:07', NULL),
(58, '9ac34cd4-ebfa-4a77-a929-0fa08ad3ee39', '2023-05-24 04:08:40', NULL),
(59, 'c620ca54-8722-453c-9b01-d31270f9c03e', '2023-05-24 04:24:24', NULL),
(60, '6523fdf9-33f3-44cb-8196-ce26eb47160a', '2023-05-24 04:24:37', NULL),
(61, '0c3cc12a-ea84-4af9-a453-7f1b917de21e', '2023-05-24 06:47:44', NULL),
(62, '113a1643-d2e2-45b1-946b-b9c067dcfd23', '2023-05-24 08:44:47', NULL),
(63, 'b31875e9-e25f-4713-ba96-c4d0367ff288', '2023-05-24 10:07:42', NULL),
(64, 'c5f37fea-d9d4-4852-9440-d36389498cc9', '2023-05-26 00:39:48', NULL),
(65, '07f95494-adbc-450a-82b2-c28b50b7d8d1', '2023-05-26 04:40:07', NULL),
(66, '50493186-f7ef-4712-a0c9-74d5d2146127', '2023-05-27 02:54:07', NULL),
(67, '37f11258-a4dd-4c35-a218-f90f38d70c9d', '2023-06-01 20:11:22', NULL),
(68, 'd328faf3-70cb-4b3b-88c9-bf71a81178bf', '2023-06-01 20:13:31', NULL),
(69, '94560b8a-567b-4274-9a8b-025db9f69b06', '2023-06-03 14:37:14', NULL),
(70, '0850e40e-0c48-48c6-849b-1a877f7635ee', '2023-06-03 16:14:11', NULL),
(71, '94484bca-9d66-4766-a297-df9ee015dabd', '2023-06-03 16:14:23', NULL),
(72, 'cdffb4c0-0d77-4f38-bc27-c17f5fc2fd0d', '2023-06-03 19:21:23', NULL),
(73, 'a40e07ba-b0d7-4460-ad11-75ecb120ae9b', '2023-06-03 19:22:55', NULL),
(74, 'e5b6149b-7db8-414e-a676-19e917c02ce4', '2023-06-03 19:23:03', NULL),
(75, '4bc80592-d48a-49bc-953f-aff9c872182f', '2023-06-03 19:38:48', NULL),
(76, '91007f9a-cbe6-43a8-80d5-082f58ec22cb', '2023-06-03 20:12:38', NULL),
(77, '98310e14-25ad-47d6-8b61-249344ec239b', '2023-06-03 20:14:09', NULL),
(78, 'e451c354-9109-48d2-93c1-0cefe32be6ab', '2023-06-03 20:14:30', NULL),
(79, 'cbebcab5-f561-405b-9ca5-89204dd59bb4', '2023-06-03 20:14:58', NULL),
(80, '56fa658d-1da3-43c5-bb9b-9c887b0f6ae1', '2023-06-03 20:16:19', NULL),
(81, '842d6657-09f3-4eca-b952-6b2885136f76', '2023-06-03 20:34:01', NULL),
(82, '8b26b39a-ec83-4f42-8c10-d457c380408e', '2023-06-03 20:35:26', NULL),
(83, '673228d4-482c-4502-b834-3a089592803a', '2023-06-03 20:35:48', NULL),
(84, 'c6cbed34-1133-41e6-b731-fce6a0951feb', '2023-06-03 20:36:03', NULL),
(85, '132cc5cf-2c2b-4f3f-a699-de1a1802c15e', '2023-06-03 20:36:21', NULL),
(86, '017ea4ca-3a42-4ec0-9cc4-9a7637d65832', '2023-06-03 20:36:46', NULL),
(87, 'fab2d537-dfb2-4dc8-9db5-3a6463db4385', '2023-06-03 20:38:09', NULL),
(88, '8fe27224-3895-4be6-939e-e08c08dffbdc', '2023-06-03 20:38:30', NULL),
(89, 'bd70bac5-0b13-4652-abe9-798866a47bca', '2023-06-03 20:38:48', NULL),
(90, '0e8428e0-460b-4ecc-8e30-8f3ff13c8748', '2023-06-03 20:39:16', NULL),
(91, '780b0de1-4276-4cc9-bcb1-c96f88bdc531', '2023-06-03 20:41:12', NULL),
(92, '1243eb04-bf28-4c17-813a-5f43bc3bee76', '2023-06-03 20:41:54', NULL),
(93, '4b9b6159-0c98-4b7b-ba1e-3f6c52a34050', '2023-06-03 20:42:27', NULL),
(94, '985a4a78-b0eb-42ef-a3e2-8be757a06eec', '2023-06-03 20:42:34', NULL),
(95, '3f738b63-eb92-4852-82fb-db85e5ef3607', '2023-06-03 20:42:59', NULL),
(96, '5e1d048a-d7ef-4779-8d3a-76e0c815550a', '2023-06-03 20:43:42', NULL),
(97, '2d9d0014-7b0a-4e0f-a2f5-aa6e57b2cb2d', '2023-06-03 20:43:58', NULL),
(98, '5d49f77b-7217-447a-985c-4344f5f1f73e', '2023-06-03 21:58:14', NULL),
(99, '7f4cfb81-b728-4a4f-bf0f-3df1e8dda2e8', '2023-06-03 21:59:14', NULL),
(100, 'a502ae02-acec-4688-9d23-bddf042ccdfd', '2023-06-03 22:00:13', NULL),
(101, '1e63087c-6ae9-4462-af20-7ceb6ea15ce7', '2023-06-03 22:00:42', NULL),
(102, '153c27ad-f1f5-427a-9bca-0d923a96c1f1', '2023-06-03 22:07:23', NULL),
(103, '69a3e438-1fa0-4d3d-8fda-440f39e2116c', '2023-06-03 22:08:29', NULL),
(104, 'e0b1fc14-c233-4392-9f6c-cd93c13ab00c', '2023-06-03 22:09:38', NULL),
(105, 'bd230674-a5ce-4c0b-9efd-2afad97cd5a1', '2023-06-03 22:11:10', NULL),
(106, '9d67af8b-82a6-4cd9-a9eb-9fc207dd9b87', '2023-06-03 22:14:44', NULL),
(107, 'b0f3695b-c4d8-4af6-a2a1-a38e9f3624e3', '2023-06-03 22:15:13', NULL),
(108, 'bca4e850-f945-466a-81b3-d1e2ad74e9a8', '2023-06-04 11:52:42', NULL),
(109, 'bcb8f4ad-3dd1-48fb-9d24-693bc1cd76ed', '2023-06-04 15:11:34', NULL),
(110, '2e086061-d7f1-4688-8153-063b17d41a2a', '2023-06-04 18:37:06', NULL),
(111, '82a2f145-e5ef-40bb-bb02-f7058033f4e7', '2023-06-04 21:03:59', NULL),
(112, '7f9d6eb4-eb12-495e-8da3-893ed95a07fe', '2023-06-05 01:05:39', NULL),
(113, '368e9413-a087-4c9a-a403-399ebae87f4e', '2023-06-06 03:16:04', NULL),
(114, 'a56bc8f0-7e85-4d84-921c-e22f5b058aac', '2023-06-07 14:13:26', NULL),
(115, '22eb04dd-16f1-4fac-b6cf-8f99f5e0c210', '2023-06-09 01:37:37', NULL),
(116, 'bbd74339-e136-437f-a8a2-8b6671d90856', '2023-06-09 01:51:42', NULL),
(117, '1768fde2-b618-43be-bd34-8bf293bc34eb', '2023-06-09 01:52:18', NULL),
(118, 'e1097b11-1552-4a2e-b4dc-68a42feeed42', '2023-06-09 01:55:56', NULL),
(119, '817a47c2-1c7d-44ef-94b9-2d5bc8268a74', '2023-06-09 07:14:33', NULL),
(120, 'f717a717-a92a-4963-bcda-c10e1fd9b0ef', '2023-06-09 07:17:22', NULL),
(121, 'f948bd72-7227-4d31-ba85-4fe098a93d5b', '2023-06-09 08:38:09', NULL),
(122, '3dda02fd-6b3b-47c3-8b9a-e1d0c383e67e', '2023-06-09 08:39:01', NULL),
(123, 'ba3b37b3-6083-4f66-8d17-ee75cd850f55', '2023-06-09 20:42:11', NULL),
(124, '59d499f0-782b-4701-b043-70b2a9fe7360', '2023-06-09 20:50:18', NULL),
(125, '2facfaf1-445b-4950-8860-54ff057489d4', '2023-06-10 13:40:23', NULL),
(126, '5d5ad99f-6a7d-470c-aa0f-0c78616361a6', '2023-06-10 23:20:13', NULL),
(127, 'd3b349a4-6ef1-4185-9866-220012422318', '2023-06-13 23:40:01', NULL),
(128, 'fe7d8a34-8ed2-4d08-af16-44c49f319887', '2023-06-13 23:42:36', NULL),
(129, 'e8098a2e-e184-4cc5-aa7b-83979ad93c3b', '2023-06-14 15:27:42', NULL),
(130, 'c5a27e8c-3b85-4a44-952b-1a6afe5e3f46', '2023-06-14 16:07:21', NULL),
(131, 'b5d36d08-fd3d-4e4c-8833-daad17a759f0', '2023-06-14 16:07:44', NULL),
(132, '369bd37b-66e2-4de9-b50a-45c9901dab85', '2023-06-16 20:53:10', NULL),
(133, '974bbd8d-ed47-4ca3-86d8-bb7591f65c6c', '2023-07-07 00:22:26', NULL),
(134, '0a525a68-a458-4929-8d52-8124a7674d3c', '2023-07-07 00:55:01', NULL),
(135, '6dab9bbf-e0fe-4f5f-a323-7e0027aa15d2', '2023-07-06 00:56:46', NULL),
(136, 'dc3aac8b-1efa-4155-a2ed-cc4433facf3c', '2023-07-07 02:28:55', NULL);

-- --------------------------------------------------------

--
-- Table structure for table `auth_user`
--

CREATE TABLE `auth_user` (
  `id` int(11) NOT NULL,
  `username` varchar(128) NOT NULL,
  `password` varchar(256) NOT NULL,
  `group` varchar(128) NOT NULL,
  `join_date` datetime DEFAULT NULL,
  `update_date` datetime DEFAULT NULL,
  `is_active` varchar(2) NOT NULL,
  `user_last_login` datetime DEFAULT NULL,
  `user_logout` datetime DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `auth_user`
--

INSERT INTO `auth_user` (`id`, `username`, `password`, `group`, `join_date`, `update_date`, `is_active`, `user_last_login`, `user_logout`) VALUES
(5, 'admin', 'pbkdf2:sha256:260000$ppQCAb9XeA0ySjUp$ec7695e8ca5c83fdf7a3a7198862af70c31cadce3a3b96287fd65e2555bc9826', 'admin', '2022-11-21 08:59:26', NULL, '1', '2022-12-12 11:58:38', NULL),
(6, '196606271996022001', 'pbkdf2:sha256:260000$NS1yfMhyPjaf792v$19ecfb1c7a645732ee6c0767128b282763629ecf4b8a03f770dcca2d3cee5d95', 'guru', '2022-11-23 10:45:46', '2023-01-04 19:36:16', '1', '2023-05-24 08:43:00', NULL),
(7, '196204141987032019', 'pbkdf2:sha256:260000$MMeaDwSNRQ3ARN4U$e44985c1d72630be619674e95c137060cb16ae3d1d3c43f3dcdea8f0b8957cbd', 'guru', '2022-11-23 11:08:44', NULL, '1', '2023-06-01 20:11:12', '2023-06-01 20:11:22'),
(8, '196910171992032008', 'pbkdf2:sha256:260000$e3HYbX7VHSGCtjhd$513d24d883d654425540fe9982e4dbe546d29bb08251aa73cabb5fb1f13bff0d', 'guru', '2022-11-23 11:08:44', NULL, '1', '2023-06-07 13:55:21', '2023-06-07 14:13:26'),
(9, '196501021987032021', 'pbkdf2:sha256:260000$ciDiGmznZ6r9LyqS$57b7487d7f19b9b918c94358c91de9afac0cef2c907af4da0752dd48b6072245', 'guru', '2022-11-23 11:08:44', NULL, '1', NULL, NULL),
(10, '196905041998022004', 'pbkdf2:sha256:260000$5CCTPpKEwU4uxlek$1e036fd3e8a23aba35d8057445c3a41a77e91098cc264c5d446182943c8bf79b', 'guru', '2022-11-23 11:08:44', NULL, '1', NULL, NULL),
(11, '198512072011011008', 'pbkdf2:sha256:260000$7x53OC52o0UTJopc$eeda5256c88e04eaf2ed9eeb0babb6937007a3583a6af81c7d32d31a45d7db49', 'guru', '2022-11-23 11:08:44', NULL, '1', '2023-05-23 15:00:31', '2023-05-24 01:08:58'),
(12, '197209152000032003', 'pbkdf2:sha256:260000$ARFmTsYoMDqWj6ad$0c06f0c7fc0652906caaf0c6d21d22d4c03b46c39d9dac30622c406f6c851b3e', 'guru', '2022-11-23 11:08:44', NULL, '1', '2022-12-30 21:52:36', NULL),
(13, '197008182006042000', 'pbkdf2:sha256:260000$5iJn2hLZzxofDs27$abf40d5b69774e87cb2ca22b685280269695e39cfec43895403647b5e40d8666', 'guru', '2022-11-23 11:08:44', NULL, '1', '2023-05-24 06:38:43', '2023-05-24 06:47:44'),
(14, '197008182006042008', 'pbkdf2:sha256:260000$yV565KKXayH4cvjP$de6cb43b94ad125f04be9667652e43109db405600d205c6b6c0128f2a1340d85', 'guru', '2022-11-23 11:08:44', NULL, '1', '2023-05-24 06:48:00', '2023-05-24 08:44:47'),
(15, '196701221995122001', 'pbkdf2:sha256:260000$TRNddbol1pvrXoFk$914ff1b2d7fa445ef6aef3df9a887aefb3c234599418acd1d3965ed68f8f230b', 'guru', '2022-11-23 11:08:44', '2022-11-23 11:47:21', '1', '2023-05-24 00:27:53', NULL),
(16, '0094755743', 'pbkdf2:sha256:260000$ML9TPvjwvoRkXRlc$2ac7283adc7e2b23210aa4cc815891f760cd7288c45fb92ca7f2f087b75b003c', 'siswa', '2022-11-23 11:31:51', NULL, '1', '2023-07-10 09:48:25', '2023-07-07 02:28:55'),
(17, '0099789908', 'pbkdf2:sha256:260000$IxrgSpm1OdaIRHiw$07b40cf46bd1bccc9e5fb37f05f2de2fcfc0b5e23902181a3ac7bafac38c4045', 'siswa', '2022-11-23 11:31:51', NULL, '1', '2023-05-05 20:57:02', '2023-05-05 17:10:17'),
(18, '0094125167', 'pbkdf2:sha256:260000$XiEMZ3lc84rxmSNg$5547334703162b6d5de070e528bda10cefb54c1d89065ade98e80810e5622db2', 'siswa', '2022-11-23 11:31:51', NULL, '1', '2023-04-03 17:58:09', NULL),
(19, '0095787926', 'pbkdf2:sha256:260000$JTRY49t1Ldzu55kr$d6460b91f9e943fece13de1e894c6544a6a642b142b192edc670477e9fc0a5d3', 'siswa', '2022-11-23 11:31:51', NULL, '1', '2023-05-17 12:54:34', '2023-05-17 12:54:38'),
(20, '0085321166', 'pbkdf2:sha256:260000$72p1lOU3A4KG9Uc2$72a55d99071debe3833a857d3a8c1be9ead96587b74adbee12c497dd871abe55', 'siswa', '2022-11-23 11:31:51', '2023-01-02 15:34:22', '1', '2023-05-18 11:48:02', '2023-05-18 11:48:06'),
(21, '0096991422', 'pbkdf2:sha256:260000$h3fqF2lWUhcL6Cf4$4c2f1714a947969eea806afc551de8a2ee41a51b3269c172144901e3a87ae66e', 'siswa', '2022-11-23 11:31:51', NULL, '1', '2023-06-13 23:42:38', '2023-06-14 15:27:42'),
(22, '0082803614', 'pbkdf2:sha256:260000$QJHf5FUGh55IGbB0$42718f61c621dc341516ba04fc3f455d789064eaeff17f06556314d1aec24dd4', 'siswa', '2022-11-23 11:31:51', NULL, '1', NULL, NULL),
(23, '0081227491', 'pbkdf2:sha256:260000$rdn8mzlaaRTY4NOP$043dc8641b48ad01d4fe0865bb1d63c77eaa2e475e1c56f242010bd85b15f97f', 'siswa', '2022-11-23 11:31:51', NULL, '1', NULL, NULL),
(24, '0084835186', 'pbkdf2:sha256:260000$52kFS3XISmvOzgAr$aad75485875917b109c501b76eb69f95696003dbe21db4c7f3ae102d63f24ce0', 'siswa', '2022-11-23 11:31:51', NULL, '1', NULL, NULL),
(25, '0095267997', 'pbkdf2:sha256:260000$gZodkTyvH5gnho4h$2c5eb6a9be688d53af8efae986493a1b86cf1f62e4f87710b49484bc958fefa0', 'siswa', '2022-11-23 11:31:51', NULL, '1', NULL, NULL),
(26, '0086737425', 'pbkdf2:sha256:260000$V0rgIzgrlMVjonrc$83d96778abe92ae8b56e8abe80c220f81c9febf9713cb2fc6a7a725388d415b0', 'siswa', '2022-11-23 11:31:51', NULL, '1', NULL, NULL),
(27, '0088283893', 'pbkdf2:sha256:260000$ziJz2NHvmkU50TvG$1480e329fe8b85f4bf2956f47ff411cfb5aa06d90c38efed65c34a86eb595f96', 'siswa', '2022-11-23 11:31:51', NULL, '1', NULL, NULL),
(28, '0098182346', 'pbkdf2:sha256:260000$5JCO14IKtRK1ko1v$1beabc030166114030395b3f8d012f8f0f5792dbcd668cff5d496e6298d63c27', 'siswa', '2022-11-23 11:31:51', NULL, '1', NULL, NULL),
(29, '0096041815', 'pbkdf2:sha256:260000$AnEY9J7FmVPzcWll$ac102a317ea0684961ed1e0bbac15dc3567b493af21e45ef437303cd8ef3c11e', 'siswa', '2022-11-23 11:31:51', NULL, '1', NULL, NULL),
(30, '0097282248', 'pbkdf2:sha256:260000$rJHbrYsXaPv7S3L8$4dc317566a9ae65963763e3259f8299516ed42e9abf912d1b3078895357f7284', 'siswa', '2022-11-23 11:31:51', NULL, '1', NULL, NULL),
(31, '0099049864', 'pbkdf2:sha256:260000$ooA2Wg5ZfbPKG5OS$08e060ae798530c488a6838dde29d3b6ea2349a13bc21d744f87ff6f35ea141a', 'siswa', '2022-11-23 11:31:51', NULL, '1', '2023-03-29 02:01:39', NULL),
(32, '0071412829', 'pbkdf2:sha256:260000$rZ9HEEPohgO8fC9j$4a07f87a2126af570d1f2e98874bfb2a6bee43570dc61f85a715c8b193ef2406', 'siswa', '2022-11-23 11:31:51', NULL, '1', '2022-11-23 12:06:34', NULL),
(33, '0083083027', 'pbkdf2:sha256:260000$obSCRkge0aCgToLi$68d66ec4019e5b5591bfaa21cba5370a2009b878b0c50817df3cdcb07d6833fc', 'siswa', '2022-12-01 00:18:15', NULL, '1', NULL, NULL),
(34, '0099631922', 'pbkdf2:sha256:260000$up3QPN9hgOSj6Z67$c53daca0c82c704c8d5295b4765bfa22bfba667f12b42689001f6cf8f48a5f83', 'siswa', '2022-12-01 00:18:15', NULL, '1', NULL, NULL),
(35, '0095459342', 'pbkdf2:sha256:260000$gYDnabg5ky8XHn8v$554f6856c28572550019c64f00789bc75a03221f52cef31ec4822a525dad6d26', 'siswa', '2022-12-01 00:18:15', NULL, '1', NULL, NULL),
(36, '0091604225', 'pbkdf2:sha256:260000$rBBOl2DoD7PBpocT$47985d62393ffd6671d37785ad18469624d9e3f53994cca81269315022bd4dfa', 'siswa', '2022-12-01 00:18:15', NULL, '1', NULL, NULL),
(37, '0091746861', 'pbkdf2:sha256:260000$dEmD4yWdFE0JmcHo$0d2a8e6fff9e28c961b5b0a6ea8c7dacf093d320464d33d354cd7f918eabf10a', 'siswa', '2022-12-21 21:01:38', NULL, '1', NULL, NULL),
(38, '0094595250', 'pbkdf2:sha256:260000$Zs5NouVQmGciuPlf$24ab81a22cc9aafd3e2e422ce53c97b873f8154b0b54edaf9ea5461241807884', 'siswa', '2022-12-21 21:01:38', NULL, '1', NULL, NULL),
(39, '0087800776', 'pbkdf2:sha256:260000$3DNixgIqHpUbXTfw$e20bf32b2686bb8c960105f20c6d3409cce46562564cb85453f332336088777e', 'siswa', '2022-12-21 21:01:38', NULL, '1', NULL, NULL),
(40, '0096678822', 'pbkdf2:sha256:260000$4FFtcbqrQdjSZK8f$4513c3c7e2507c6a3cd79f26915a0c4c2c01975c023a741f1c5b4550b1cb7d89', 'siswa', '2022-12-21 21:01:38', NULL, '1', NULL, NULL),
(41, '197312221999032007', 'pbkdf2:sha256:260000$cKqtj4FgvVUBfQQc$92e34e373800f6c9c1fb8c157e8e3ebd2d6f9bf3e6d5a5a50b31b48bdebaeee6', 'guru', '2023-01-03 19:34:33', NULL, '1', '2023-06-14 15:28:14', '2023-06-14 16:07:21'),
(42, '198109122009022008', 'pbkdf2:sha256:260000$Ey4gA0RLQ95t7eDY$57a4397769588a3eae028250728faca20f360fa6f682c79dc1e0024870ba830d', 'guru', '2023-01-03 19:34:33', NULL, '1', NULL, NULL),
(43, '196312311988032109', 'pbkdf2:sha256:260000$lkvfeYneHJ1NSsCQ$514f4531f96788ca5f6ec9089a72c71b50cbf41f603c342b3e2c53303abb8c55', 'guru', '2023-01-03 19:34:33', NULL, '1', NULL, NULL),
(44, '196512311989032117', 'pbkdf2:sha256:260000$u2aFy7r2VgYZ0k4u$27bb5858363ec031fedd3df4673093fb416c7782ea86f657dcf3bfce27d8da04', 'guru', '2023-01-03 23:23:19', NULL, '1', NULL, NULL),
(45, '196509141991032011', 'pbkdf2:sha256:260000$0RMyU05XqAkihPtL$540bea8f04bdc3a8fa537225c8978f68001d59831a7c53d923041d18c428244c', 'bk', '2023-01-03 23:23:19', NULL, '1', '2023-08-17 20:52:43', NULL);

-- --------------------------------------------------------

--
-- Table structure for table `data_absensi`
--

CREATE TABLE `data_absensi` (
  `id` int(11) NOT NULL,
  `mengajar_id` int(11) DEFAULT NULL,
  `siswa_id` int(11) DEFAULT NULL,
  `tgl_absen` date DEFAULT NULL,
  `ket` varchar(16) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `data_absensi`
--

INSERT INTO `data_absensi` (`id`, `mengajar_id`, `siswa_id`, `tgl_absen`, `ket`) VALUES
(594, 50, 16, '2022-11-01', 'H'),
(595, 50, 17, '2022-11-01', 'H'),
(596, 50, 18, '2022-11-01', 'H'),
(597, 50, 19, '2022-11-01', 'H'),
(598, 50, 20, '2022-11-01', 'H'),
(599, 50, 16, '2022-11-03', 'H'),
(600, 50, 17, '2022-11-03', 'I'),
(601, 50, 18, '2022-11-03', 'H'),
(602, 50, 19, '2022-11-03', 'H'),
(603, 50, 20, '2022-11-03', 'S'),
(604, 50, 16, '2022-11-08', 'A'),
(605, 50, 17, '2022-11-08', 'H'),
(606, 50, 18, '2022-11-08', 'H'),
(607, 50, 19, '2022-11-08', 'H'),
(608, 50, 20, '2022-11-08', 'S'),
(609, 81, 16, '2022-11-10', 'S'),
(610, 81, 17, '2022-11-10', 'H'),
(611, 81, 18, '2022-11-10', 'A'),
(612, 81, 19, '2022-11-10', 'H'),
(613, 81, 20, '2022-11-10', 'H'),
(614, 81, 16, '2022-11-15', 'H'),
(615, 81, 17, '2022-11-15', 'H'),
(616, 81, 18, '2022-11-15', 'H'),
(617, 81, 19, '2022-11-15', 'H'),
(618, 81, 20, '2022-11-15', 'H'),
(619, 81, 16, '2022-11-17', 'H'),
(620, 81, 17, '2022-11-17', 'H'),
(621, 81, 18, '2022-11-17', 'S'),
(622, 81, 19, '2022-11-17', 'H'),
(623, 81, 20, '2022-11-17', 'H'),
(624, 50, 16, '2022-11-22', 'S'),
(625, 50, 17, '2022-11-22', 'H'),
(626, 50, 18, '2022-11-22', 'H'),
(627, 50, 19, '2022-11-22', 'A'),
(628, 50, 20, '2022-11-22', 'I'),
(629, 50, 16, '2022-11-24', 'H'),
(630, 50, 17, '2022-11-24', 'H'),
(631, 50, 18, '2022-11-24', 'H'),
(632, 50, 19, '2022-11-24', 'H'),
(633, 50, 20, '2022-11-24', 'H'),
(634, 50, 16, '2022-11-29', 'H'),
(635, 50, 17, '2022-11-29', 'H'),
(636, 50, 18, '2022-11-29', 'H'),
(637, 50, 19, '2022-11-29', 'H'),
(638, 50, 20, '2022-11-29', 'H'),
(641, 182, 19, '2023-06-02', 'A'),
(642, 157, 28, '2023-06-14', 'H'),
(643, 178, 16, '2023-07-07', 'H'),
(644, 178, 17, '2023-07-07', 'H'),
(645, 178, 18, '2023-07-07', 'H'),
(646, 178, 19, '2023-07-07', 'H'),
(647, 178, 20, '2023-07-07', 'H'),
(648, 181, 21, '2023-07-07', 'H'),
(649, 181, 22, '2023-07-07', 'H'),
(650, 181, 23, '2023-07-07', 'H'),
(651, 181, 24, '2023-07-07', 'H'),
(652, 181, 25, '2023-07-07', 'H'),
(653, 180, 21, '2023-07-07', 'H'),
(654, 180, 22, '2023-07-07', 'H'),
(655, 180, 23, '2023-07-07', 'H'),
(656, 180, 24, '2023-07-07', 'H'),
(657, 180, 25, '2023-07-07', 'H'),
(658, 179, 16, '2023-07-07', 'H'),
(659, 179, 17, '2023-07-07', 'H'),
(660, 179, 18, '2023-07-07', 'H'),
(661, 179, 19, '2023-07-07', 'H'),
(662, 179, 20, '2023-07-07', 'H'),
(663, 178, 16, '2023-06-30', 'H'),
(664, 178, 17, '2023-06-30', 'H'),
(665, 178, 18, '2023-06-30', 'H'),
(666, 178, 19, '2023-06-30', 'H'),
(667, 178, 20, '2023-06-30', 'H'),
(668, 181, 21, '2023-06-30', 'H'),
(669, 181, 22, '2023-06-30', 'H'),
(670, 181, 23, '2023-06-30', 'H'),
(671, 181, 24, '2023-06-30', 'H'),
(672, 181, 25, '2023-06-30', 'H'),
(673, 180, 21, '2023-06-30', 'H'),
(674, 180, 22, '2023-06-30', 'H'),
(675, 180, 23, '2023-06-30', 'H'),
(676, 180, 24, '2023-06-30', 'H'),
(677, 180, 25, '2023-06-30', 'H'),
(678, 179, 16, '2023-06-30', 'H'),
(679, 179, 17, '2023-06-30', 'H'),
(680, 179, 18, '2023-06-30', 'H'),
(681, 179, 19, '2023-06-30', 'H'),
(682, 179, 20, '2023-06-30', 'H'),
(683, 164, 16, '2023-07-06', 'H'),
(684, 164, 17, '2023-07-06', 'H'),
(685, 164, 18, '2023-07-06', 'H'),
(686, 164, 19, '2023-07-06', 'H'),
(687, 164, 20, '2023-07-06', 'H'),
(688, 171, 26, '2023-07-06', 'H'),
(689, 171, 27, '2023-07-06', 'H'),
(690, 171, 28, '2023-07-06', 'H'),
(691, 171, 29, '2023-07-06', 'H'),
(692, 171, 30, '2023-07-06', 'H'),
(693, 178, 16, '2023-06-23', 'H'),
(694, 178, 17, '2023-06-23', 'H'),
(695, 178, 18, '2023-06-23', 'S'),
(696, 178, 19, '2023-06-23', 'H'),
(697, 178, 20, '2023-06-23', 'H'),
(698, 181, 21, '2023-06-23', 'S'),
(699, 181, 22, '2023-06-23', 'H'),
(700, 181, 23, '2023-06-23', 'S'),
(701, 181, 24, '2023-06-23', 'I'),
(702, 181, 25, '2023-06-23', 'A');

-- --------------------------------------------------------

--
-- Table structure for table `data_jenis_pelanggaran`
--

CREATE TABLE `data_jenis_pelanggaran` (
  `id` int(11) NOT NULL,
  `jenis_pelanggaran` text DEFAULT NULL,
  `status` varchar(64) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `data_jenis_pelanggaran`
--

INSERT INTO `data_jenis_pelanggaran` (`id`, `jenis_pelanggaran`, `status`) VALUES
(4, 'Bolos', '1'),
(5, 'Baju tidak rapi', '1'),
(6, 'Berkelahi', '1'),
(7, 'Terlambat', '1'),
(8, 'Rambut gondrong', '1'),
(9, 'Tidur di kelas', '1'),
(10, 'Membawa Senjata Tajam', '1'),
(11, 'Miras', '1');

-- --------------------------------------------------------

--
-- Table structure for table `data_pelanggaran`
--

CREATE TABLE `data_pelanggaran` (
  `id` int(11) NOT NULL,
  `siswa_id` int(11) DEFAULT NULL,
  `jenis_pelanggaran_id` int(11) DEFAULT NULL,
  `note` text DEFAULT NULL,
  `tgl_report` date NOT NULL,
  `status` varchar(128) DEFAULT NULL,
  `guru_id` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `data_pelanggaran`
--

INSERT INTO `data_pelanggaran` (`id`, `siswa_id`, `jenis_pelanggaran_id`, `note`, `tgl_report`, `status`, `guru_id`) VALUES
(36, 16, 7, 'Tidak mengikuti upacara', '2023-08-17', 'Pelanggaran Ke-1', NULL);

-- --------------------------------------------------------

--
-- Table structure for table `data_pembinaan`
--

CREATE TABLE `data_pembinaan` (
  `id` int(11) NOT NULL,
  `bina` int(11) DEFAULT NULL,
  `tgl_bina` date NOT NULL,
  `pelanggaran_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Table structure for table `data_sub_tata_tertib1`
--

CREATE TABLE `data_sub_tata_tertib1` (
  `id` int(11) NOT NULL,
  `tata_tertib` varchar(255) DEFAULT NULL,
  `t_tertib_id` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `data_sub_tata_tertib1`
--

INSERT INTO `data_sub_tata_tertib1` (`id`, `tata_tertib`, `t_tertib_id`) VALUES
(3, 'Wajib berada dilingkungan sekolah jam 07.15 wita dan pelajaran dimulai jam 07.30 wita', 1),
(4, 'Wajib mengikuti upacara bendera setiap hari senin / upacara hari besar nasional yang diadakan oleh sekolah dengan berpakaian seragam sesuai ketentuan sekolah.', 1),
(5, 'Wajib mengerjakan tugas pembelajaran dari masing-masing guru dengan tepat waktu ', 1),
(6, 'Siswa yang terlambat akan diedukasi oleh guru BK.', 1),
(7, 'Wajib berpakaian seragam sekolah dengan ketentuan sebagai berikut :', 1),
(8, 'Wajib mengikuti kegiatan Ekstrakurikuler (minimal 1 kegiatan Ekstrakurikuler)', 1),
(9, 'Wajib menjaga ketenangan belajar baik dikelas, perpustakaan, laboratorium maupun ditempat lain dilingkungan sekolah.', 1),
(10, 'Wajib menjaga nama baik sekolah baik didalam maupun diluar sekolah.', 1),
(11, 'Wajib menghormati sesama warga sekolah (Kepala sekolah,Guru, Karyawan dan Siswa) ', 1),
(12, 'Membeli makanan waktu jam pelajaran / bergerombol di warung / kantin.', 2),
(13, 'Membuang sampah tidak pada tempatnya (5)', 2),
(14, 'Berhias yang berlebihan, memakai aksesories bagi peserta didik putri', 2),
(15, 'Rambut gondrong / disemir berwarna / tidak rapi (dicukur rapi 1 cm).', 2),
(16, 'Mencoret-coret tembok, pintu, jendela, meja dan kursi', 2),
(17, 'Membolos / meninggalkan sekolah tanpa izin.', 2),
(18, 'Membawa buku, majalah, VCD, dan gambar porno', 2),
(19, 'Membawa kendaraan bermotor di lingkungan sekolah', 2),
(20, 'Membawa dan merokok di lingkungan sekolah dan sekitarnya', 2),
(21, 'Berkelahi / main hakim sendiri / mengancam', 2),
(22, 'Merusak sarana prasarana sekolah', 2),
(23, 'Mencuri / memeras.', 2),
(24, 'Membawa, mengancam dan melukai dengan senjata tajam dan sejenisnya.\r\n\r\n', 2);

-- --------------------------------------------------------

--
-- Table structure for table `data_sub_tata_tertib2`
--

CREATE TABLE `data_sub_tata_tertib2` (
  `id` int(11) NOT NULL,
  `sub1_id` int(11) DEFAULT NULL,
  `tata_tertib` varchar(255) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `data_sub_tata_tertib2`
--

INSERT INTO `data_sub_tata_tertib2` (`id`, `sub1_id`, `tata_tertib`) VALUES
(1, 7, 'Senin: berpakaian putih biru, berdasi, badge osis dan identitas sekolah lengkap, sepatu hitam, berkaos kaki putih setengah lutut, dan ikat pinggang hitam.'),
(2, 7, 'Selasa: berpakaian seragam batik kotak coklat, sepatu hitam, berkaos kaki putih setengah lutut, dan ikat pinggang hitam.'),
(3, 7, 'Rabu:  berpakaian seragam rompi hijau, sepatu hitam, berkaos kaki putih setengah lutut, dan ikat pinggang hitam.'),
(5, 7, 'Kamis: berpakaian seragam batik kota, sepatu hitam, berkaos kaki putih setengah lutut, dan ikat pinggang hitam.'),
(6, 7, 'Jumat: berpakaian  Pramuka, sepatu hitam, berkaos kaki hitam setengah lutut, dan ikat pinggang hitam.');

-- --------------------------------------------------------

--
-- Table structure for table `data_tata_tertib`
--

CREATE TABLE `data_tata_tertib` (
  `id` int(11) NOT NULL,
  `tata_tertib` varchar(128) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `data_tata_tertib`
--

INSERT INTO `data_tata_tertib` (`id`, `tata_tertib`) VALUES
(1, 'Kewajiban – kewajiban peserta didik:'),
(2, 'Dalam kegiatan sehari-hari di sekolah, setiap peserta didik dilarang melakukan hal-hal sebagai berikut:');

-- --------------------------------------------------------

--
-- Table structure for table `data_teks`
--

CREATE TABLE `data_teks` (
  `id` int(11) NOT NULL,
  `teks` text DEFAULT NULL,
  `ket` varchar(128) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `data_teks`
--

INSERT INTO `data_teks` (`id`, `teks`, `ket`) VALUES
(2, 'Berdasarkan hasil keputusan rapat dan musyawarah perwakilan kelas\npengurus OSIS serta Dewan Guru. Maka setiap peserta didik yang\ntidak mengindahkan tata tertib sekolah akan diberikan sanksi\nberdasarkan aturan yang sudah disepakati.\n<strong>Tata tertib ini berlaku selama peserta didik belajar\ndilingkungan SMP Negeri 2 Makassar.</strong>', 'bk');

-- --------------------------------------------------------

--
-- Table structure for table `detail_admin`
--

CREATE TABLE `detail_admin` (
  `id` int(11) NOT NULL,
  `first_name` varchar(128) NOT NULL,
  `last_name` varchar(128) NOT NULL,
  `gender` varchar(32) DEFAULT NULL,
  `alamat` varchar(128) DEFAULT NULL,
  `user_id` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `detail_admin`
--

INSERT INTO `detail_admin` (`id`, `first_name`, `last_name`, `gender`, `alamat`, `user_id`) VALUES
(2, 'ADMIN', 'Sajalah', 'laki-laki', NULL, 5);

-- --------------------------------------------------------

--
-- Table structure for table `detail_guru`
--

CREATE TABLE `detail_guru` (
  `id` int(11) NOT NULL,
  `first_name` varchar(128) NOT NULL,
  `last_name` varchar(128) NOT NULL,
  `gender` varchar(32) NOT NULL,
  `agama` varchar(32) DEFAULT NULL,
  `alamat` varchar(256) DEFAULT NULL,
  `telp` varchar(16) DEFAULT NULL,
  `user_id` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `detail_guru`
--

INSERT INTO `detail_guru` (`id`, `first_name`, `last_name`, `gender`, `agama`, `alamat`, `telp`, `user_id`) VALUES
(1, 'Dra.', 'Rosmawati', 'perempuan', 'islam', '', '', 6),
(2, 'Dra.', 'Haslinda', 'perempuan', 'islam', '', '', 7),
(3, 'Harnidah,', 'S.Pd.', 'Perempuan', 'Islam', 'Makassar', '08123535222222', 8),
(4, 'Hj.', 'St. Nurbaya, S.Pd., M.Pd.', 'perempuan', 'islam', '', '', 9),
(5, 'Hj.', 'Suriani, S.Ag.', 'perempuan', 'islam', '', '', 10),
(6, 'Ruslan', 'Talebe, S.Pd.', 'laki-laki', 'islam', '', '', 11),
(7, 'Rahmini,', 'S.Pd., M.MPd', 'perempuan', 'islam', '', '', 12),
(8, 'Mariyani', 'Mannya, S.Pd.', 'perempuan', 'islam', '', '', 13),
(9, 'Hj.', 'Sahiah, S.Pd', 'perempuan', 'islam', '', '', 14),
(10, 'Sahabuddin,', 'S.Pd.', 'laki-laki', 'islam', 'Makassar', '', 15),
(11, 'Enny,', 'S.Pd, M.Pd.', 'perempuan', 'islam', '', '', 41),
(12, 'Herlina,', 'S.Pd.', 'perempuan', 'islam', '', '', 42),
(13, 'Nuraeny', 'Palesang, S.Pd.', 'perempuan', 'islam', '', '', 43),
(14, 'Andi', 'Muliati, S.Pd., M.Pd.', 'perempuan', 'islam', '', '', 44),
(15, 'Septri', 'Tangke, S.Pd.', 'perempuan', 'kristen', '', '', 45);

-- --------------------------------------------------------

--
-- Table structure for table `detail_siswa`
--

CREATE TABLE `detail_siswa` (
  `id` int(11) NOT NULL,
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
  `kelas_id` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `detail_siswa`
--

INSERT INTO `detail_siswa` (`id`, `first_name`, `last_name`, `gender`, `tempat_lahir`, `tgl_lahir`, `agama`, `nama_ortu_or_wali`, `no_telp`, `alamat`, `qr_code`, `pic`, `user_id`, `kelas_id`) VALUES
(5, 'Ar', 'Rijal Dhaffa Nugraha', 'laki-laki', NULL, NULL, 'islam', NULL, '', NULL, 'VIII-1_rijal_3fb661f3f82b97dec979e77d66abf644.png', '', 16, 9),
(6, 'ALISYAH', 'PUTRI RAMADHANI', 'perempuan', NULL, NULL, 'islam', NULL, '', NULL, 'VIII-1_alisyah_90dc225705eeaeb5abb97227413647fa.png', NULL, 17, 9),
(7, 'ANANDA', 'PUTRI AURELIA AKBAR', 'perempuan', NULL, NULL, 'islam', NULL, '', NULL, 'VIII-1_ananda_48ddf3afe6e410cbeca3ad26d07d393a.png', 'VIII-1_ananda_a4370751a9e2d430fbc2146479f8d579.jpg', 18, 9),
(8, 'RHIFQI', 'ASHRAF SHANDY', 'laki-laki', NULL, NULL, 'islam', NULL, '', NULL, 'VIII-1_rhifqi_a80b09af269cd4d0691b5a7efc0833e0.png', NULL, 19, 9),
(9, 'Salsabila', 'Azisah Az Zahra', 'perempuan', NULL, NULL, 'islam', NULL, '', NULL, 'VIII-1_salsabila_1fc49a06f936cdc6ee3b10f1ccead8a3.png', NULL, 20, 9),
(10, 'A.', 'ZHIL ZHILLAH ANUGRAH TANDIARI', 'perempuan', NULL, NULL, 'islam', NULL, '', NULL, 'VIII-2_zhil_dd1cb5affc968d080340660d82a0c7d7.png', NULL, 21, 10),
(11, 'ADZKIYAH', 'ADELIAH', 'perempuan', NULL, NULL, 'islam', NULL, '', NULL, 'VIII-2_adzkiyah_dd1b9da82be2cd5725f675ff0f4bf7b6.png', NULL, 22, 10),
(12, 'M.', 'Dede Irza Saputra', 'laki-laki', NULL, NULL, 'islam', NULL, '', NULL, NULL, NULL, 23, 10),
(13, 'Lingga', 'Gwen Safitri', 'perempuan', NULL, NULL, 'islam', NULL, '', NULL, NULL, NULL, 24, 10),
(14, 'RAFA', 'PUTRA RAMADHAN. A', 'laki-laki', NULL, NULL, 'islam', NULL, '', NULL, NULL, NULL, 25, 10),
(15, 'Ahmad', 'Fachri Al Farabi', 'laki-laki', NULL, NULL, 'islam', NULL, '', NULL, 'VIII-3_ahmad_b9d2adcdc32768ecb2c6349191572ee4.png', 'VIII-3_ahmad_d7bcd6ca8898ecce74bd88f3da556876.jpeg', 26, 11),
(16, 'ALIKA', 'ZAYRAH DWI SEPTIA K', 'perempuan', NULL, NULL, 'islam', NULL, '', NULL, NULL, NULL, 27, 11),
(17, 'Aqyla', 'Utami Putri Patriot', 'perempuan', NULL, NULL, 'islam', NULL, '', NULL, NULL, NULL, 28, 11),
(18, 'BIMA', 'SASTRANEGARA ARY PUTRA', 'laki-laki', NULL, NULL, 'islam', NULL, '', NULL, NULL, NULL, 29, 11),
(19, 'Sitti', 'Adelia Mukarramah Munafr', 'perempuan', NULL, NULL, 'islam', NULL, '', NULL, 'VIII-3_sitti_e45ca191eefb3a31625c5a63bd5ce75d.png', NULL, 30, 11),
(20, 'A.', 'AYU APRILIA', 'perempuan', NULL, NULL, 'islam', NULL, '', NULL, NULL, NULL, 31, 12),
(21, 'Andi', 'Irgi', 'laki-laki', NULL, NULL, 'islam', NULL, '', NULL, NULL, NULL, 32, 13),
(22, 'AHMAD', 'AL FAHREZI', 'laki-laki', NULL, NULL, 'islam', NULL, '', NULL, NULL, NULL, 33, 12),
(23, 'Andi', 'Wafiqah Raidah Khamilah', 'perempuan', NULL, NULL, 'islam', NULL, '', NULL, NULL, NULL, 34, 12),
(24, 'Muh.', 'Rifqy Athaillah Hamran', 'laki-laki', NULL, NULL, 'islam', NULL, '', NULL, NULL, NULL, 35, 12),
(25, 'SARIFA', 'ALIFIYAH ISWANDI', 'perempuan', NULL, NULL, 'islam', NULL, '', NULL, NULL, NULL, 36, 12),
(26, 'Andini', 'Nur Rahmania', 'perempuan', NULL, NULL, 'islam', NULL, '', NULL, NULL, NULL, 37, 13),
(27, 'Fadlan', 'Nurrahman', 'laki-laki', NULL, NULL, 'islam', NULL, '', NULL, NULL, NULL, 38, 13),
(28, 'MUH.', 'SUPOMO GUNTUR IRWAN', 'laki-laki', NULL, NULL, 'islam', NULL, '', NULL, 'VIII-5_muh._a7ede22697d2bed31570d31af1793f91.png', NULL, 39, 13),
(29, 'Nur', 'Aini Indira Rihaz', 'perempuan', NULL, NULL, 'islam', NULL, '', NULL, NULL, NULL, 40, 13);

-- --------------------------------------------------------

--
-- Table structure for table `master_guru_bk`
--

CREATE TABLE `master_guru_bk` (
  `id` int(11) NOT NULL,
  `guru_id` int(11) DEFAULT NULL,
  `status` varchar(1) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `master_guru_bk`
--

INSERT INTO `master_guru_bk` (`id`, `guru_id`, `status`) VALUES
(1, 45, '1');

-- --------------------------------------------------------

--
-- Table structure for table `master_hari`
--

CREATE TABLE `master_hari` (
  `id` int(11) NOT NULL,
  `hari` varchar(32) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `master_hari`
--

INSERT INTO `master_hari` (`id`, `hari`) VALUES
(1, 'senin'),
(2, 'selasa'),
(3, 'rabu'),
(4, 'kamis'),
(5, 'jumat'),
(7, 'sabtu');

-- --------------------------------------------------------

--
-- Table structure for table `master_jadwal_mengajar`
--

CREATE TABLE `master_jadwal_mengajar` (
  `id` int(11) NOT NULL,
  `kode_mengajar` varchar(32) NOT NULL,
  `guru_id` int(11) DEFAULT NULL,
  `mapel_id` int(11) DEFAULT NULL,
  `jam_ke` varchar(6) DEFAULT NULL,
  `hari_id` int(11) DEFAULT NULL,
  `jam_mulai` varchar(12) DEFAULT NULL,
  `jam_selesai` varchar(12) DEFAULT NULL,
  `kelas_id` int(11) DEFAULT NULL,
  `semester_id` int(11) DEFAULT NULL,
  `tahun_ajaran_id` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `master_jadwal_mengajar`
--

INSERT INTO `master_jadwal_mengajar` (`id`, `kode_mengajar`, `guru_id`, `mapel_id`, `jam_ke`, `hari_id`, `jam_mulai`, `jam_selesai`, `kelas_id`, `semester_id`, `tahun_ajaran_id`) VALUES
(33, 'MPL-955566', 9, 2, '1-3', 1, '07:30', '09:30', 9, 1, 2),
(34, 'MPL-642394', 14, 3, '4-5', 1, '09:30', '11:00', 9, 1, 2),
(35, 'MPL-2049658', 8, 6, '6-8', 1, '11:00', '12:55', 9, 1, 2),
(36, 'MPL-649138', 8, 6, '1-3', 1, '07:30', '09:30', 10, 1, 2),
(37, 'MPL-8917823', 15, 5, '4-5', 1, '09:30', '11:00', 10, 1, 2),
(38, 'MPL-2699945', 12, 1, '6-8', 1, '11:00', '12:55', 10, 1, 2),
(39, 'MPL-9091926', 12, 1, '1-2', 1, '07:30', '08:50', 11, 1, 2),
(40, 'MPL-0855632', 15, 5, '3', 1, '08:50', '09:30', 11, 1, 2),
(41, 'MPL-496497', 10, 8, '4-6', 1, '09:30', '11:40', 11, 1, 2),
(42, 'MPL-1266716', 14, 3, '7-8', 1, '11:40', '12:55', 11, 1, 2),
(43, 'MPL-4209483', 13, 4, '1-3', 1, '07:30', '09:30', 12, 1, 2),
(44, 'MPL-7297764', 42, 2, '4-5', 1, '09:30', '11:00', 12, 1, 2),
(45, 'MPL-2787924', 43, 1, '6-8', 1, '11:00', '12:55', 12, 1, 2),
(46, 'MPL-964149', 14, 3, '1-2', 1, '07:30', '08:50', 13, 1, 2),
(47, 'MPL-935434', 43, 1, '3-5', 1, '08:50', '11:00', 13, 1, 2),
(48, 'MPL-7705064', 13, 4, '6-8', 1, '11:00', '12:55', 13, 1, 2),
(49, 'MPL-769659', 13, 4, '1-3', 2, '07:15', '09:15', 9, 1, 2),
(50, 'MPL-4828076', 41, 7, '4-5', 2, '09:15', '10:45', 9, 1, 2),
(51, 'MPL-971107', 10, 8, '6-8', 2, '10:45', '12:40', 9, 1, 2),
(52, 'MPL-624748', 8, 6, '1-2', 2, '07:15', '08:35', 10, 1, 2),
(53, 'MPL-9747136', 10, 8, '3-5', 2, '08:35', '10:45', 10, 1, 2),
(54, 'MPL-5785005', 12, 1, '6-8', 2, '10:45', '12:40', 10, 1, 2),
(55, 'MPL-3774605', 9, 2, '1-3', 2, '07:15', '09:15', 11, 1, 2),
(56, 'MPL-4230661', 13, 4, '4-6', 2, '09:15', '11:25', 11, 1, 2),
(57, 'MPL-2690954', 41, 7, '7-8', 2, '11:25', '12:40', 11, 1, 2),
(58, 'MPL-3618176', 6, 7, '1-2', 2, '07:15', '08:35', 12, 1, 2),
(59, 'MPL-6286607', 8, 6, '3-5', 2, '08:35', '10:45', 12, 1, 2),
(60, 'MPL-2728553', 42, 2, '6-8', 2, '10:45', '12:40', 12, 1, 2),
(61, 'MPL-2372444', 11, 10, '1-3', 2, '07:15', '09:15', 13, 1, 2),
(62, 'MPL-4727843', 6, 7, '4-5', 2, '09:15', '10:45', 13, 1, 2),
(63, 'MPL-145499', 8, 6, '6-8', 2, '10:45', '12:40', 13, 1, 2),
(64, 'MPL-0572498', 12, 1, '1-3', 3, '07:15', '09:15', 9, 1, 2),
(65, 'MPL-9665446', 8, 6, '4-5', 3, '09:15', '10:45', 9, 1, 2),
(66, 'MPL-1854267', 7, 9, '6-8', 3, '10:45', '12:40', 9, 1, 2),
(67, 'MPL-3523862', 13, 4, '1-3', 3, '07:15', '09:15', 10, 1, 2),
(68, 'MPL-7090046', 11, 10, '4-6', 3, '09:15', '11:25', 10, 1, 2),
(69, 'MPL-553489', 14, 3, '7-8', 3, '11:25', '12:40', 10, 1, 2),
(70, 'MPL-9910965', 8, 6, '1-3', 3, '07:15', '09:15', 11, 1, 2),
(71, 'MPL-7209883', 12, 1, '4-5', 3, '09:15', '10:45', 11, 1, 2),
(72, 'MPL-8258874', 15, 5, '6', 3, '10:45', '11:25', 11, 1, 2),
(73, 'MPL-030209', 9, 2, '7-8', 3, '11:25', '12:40', 11, 1, 2),
(74, 'MPL-8716755', 7, 9, '1-3', 3, '07:15', '09:15', 12, 1, 2),
(75, 'MPL-3001113', 14, 3, '4-5', 3, '09:15', '10:45', 12, 1, 2),
(76, 'MPL-9592643', 10, 8, '6-8', 3, '10:45', '12:40', 12, 1, 2),
(77, 'MPL-8577526', 42, 2, '1-2', 3, '07:15', '08:35', 13, 1, 2),
(78, 'MPL-6703382', 15, 5, '3-4', 3, '08:35', '09:50', 13, 1, 2),
(79, 'MPL-10255', 6, 7, '5-6', 3, '10:05', '11:25', 13, 1, 2),
(80, 'MPL-079401', 8, 6, '7-8', 3, '11:25', '12:40', 13, 1, 2),
(81, 'MPL-5040846', 41, 7, '1-2', 4, '07:15', '08:35', 9, 1, 2),
(82, 'MPL-2512572', 9, 2, '3-4', 4, '08:35', '09:50', 9, 1, 2),
(83, 'MPL-33468', 15, 5, '5-6', 4, '10:05', '11:25', 9, 1, 2),
(84, 'MPL-6281545', 14, 3, '7-8', 4, '11:25', '12:40', 9, 1, 2),
(85, 'MPL-069096', 7, 9, '1-3', 4, '07:15', '09:15', 10, 1, 2),
(86, 'MPL-3795192', 6, 7, '4-5', 4, '09:15', '10:45', 10, 1, 2),
(87, 'MPL-9334261', 9, 2, '6-8', 4, '10:45', '12:40', 10, 1, 2),
(88, 'MPL-7867444', 11, 10, '1-3', 4, '07:15', '09:15', 11, 1, 2),
(89, 'MPL-363804', 12, 1, '4-5', 4, '09:15', '10:45', 11, 1, 2),
(90, 'MPL-9890945', 7, 9, '6-8', 4, '10:45', '12:40', 11, 1, 2),
(91, 'MPL-2045546', 43, 1, '1-3', 4, '07:15', '09:15', 12, 1, 2),
(92, 'MPL-832374', 11, 10, '4-6', 4, '09:15', '11:25', 12, 1, 2),
(93, 'MPL-9587512', 6, 7, '7-8', 4, '11:25', '12:40', 12, 1, 2),
(94, 'MPL-9440625', 10, 8, '1-3', 4, '07:15', '09:15', 13, 1, 2),
(95, 'MPL-2316525', 14, 3, '4-5', 4, '09:15', '10:45', 13, 1, 2),
(96, 'MPL-889407', 42, 2, '6-8', 4, '10:45', '12:40', 13, 1, 2),
(97, 'MPL-5329022', 12, 1, '1-3', 5, '07:15', '09:15', 9, 1, 2),
(98, 'MPL-6249998', 11, 10, '4-6', 5, '09:15', '11:30', 9, 1, 2),
(99, 'MPL-364484', 9, 2, '1-2', 5, '07:15', '08:35', 10, 1, 2),
(100, 'MPL-4111667', 41, 7, '3-4', 5, '08:35', '10:10', 10, 1, 2),
(101, 'MPL-7619693', 14, 3, '5-6', 5, '10:10', '11:30', 10, 1, 2),
(102, 'MPL-1705787', 14, 3, '1-2', 5, '07:15', '08:35', 11, 1, 2),
(103, 'MPL-1095114', 8, 6, '3-4', 5, '08:35', '10:10', 11, 1, 2),
(104, 'MPL-8916461', 41, 7, '5-6', 5, '10:10', '11:30', 11, 1, 2),
(105, 'MPL-8990536', 8, 6, '1-2', 5, '07:15', '08:35', 12, 1, 2),
(106, 'MPL-9599771', 14, 3, '3-4', 5, '08:35', '10:10', 12, 1, 2),
(107, 'MPL-1323905', 15, 5, '5-6', 5, '10:10', '11:30', 12, 1, 2),
(108, 'MPL-668466', 43, 1, '1-3', 5, '07:15', '09:15', 13, 1, 2),
(109, 'MPL-028389', 7, 9, '4-6', 5, '09:15', '11:30', 13, 1, 2),
(112, 'MPL-755727', 8, 6, '1-3', 1, '07:30', '09:30', 9, 2, 2),
(113, 'MPL-435962', 14, 3, '4-5', 1, '09:30', '11:00', 9, 2, 2),
(115, 'MPL-6679351', 6, 7, '1-2', 1, '07:30', '08:50', 10, 2, 2),
(116, 'MPL-8708794', 12, 1, '3-5', 1, '08:50', '11:00', 10, 2, 2),
(117, 'MPL-2415986', 14, 3, '6-8', 1, '11:00', '12:55', 10, 2, 2),
(118, 'MPL-3027883', 13, 4, '1-3', 1, '07:30', '09:30', 11, 2, 2),
(119, 'MPL-6737182', 8, 6, '3-5', 1, '09:30', '11:00', 11, 2, 2),
(120, 'MPL-6186533', 12, 1, '6-8', 1, '11:00', '12:55', 11, 2, 2),
(121, 'MPL-5969248', 42, 2, '1-3', 1, '07:30', '09:30', 12, 2, 2),
(122, 'MPL-605567', 43, 1, '4-5', 1, '09:30', '11:00', 12, 2, 2),
(123, 'MPL-2748168', 13, 4, '6-8', 1, '11:00', '12:55', 12, 2, 2),
(124, 'MPL-833579', 14, 3, '1-2', 1, '07:30', '08:50', 13, 2, 2),
(125, 'MPL-0531113', 13, 4, '3-5', 1, '08:50', '11:00', 13, 2, 2),
(126, 'MPL-5996518', 8, 6, '6-8', 1, '11:00', '12:55', 13, 2, 2),
(127, 'MPL-0325942', 8, 6, '1-2', 2, '07:15', '08:35', 9, 2, 2),
(128, 'MPL-2878656', 10, 8, '3-5', 2, '08:35', '10:45', 9, 2, 2),
(129, 'MPL-6375954', 13, 4, '6-8', 2, '10:45', '12:40', 9, 2, 2),
(130, 'MPL-6180506', 13, 4, '1-3', 2, '07:15', '09:15', 10, 2, 2),
(131, 'MPL-3506382', 6, 7, '4-5', 2, '09:15', '10:45', 10, 2, 2),
(132, 'MPL-1222904', 7, 9, '6-8', 2, '10:45', '12:40', 10, 2, 2),
(133, 'MPL-0286024', 14, 3, '1-2', 2, '07:15', '08:35', 11, 2, 2),
(134, 'MPL-3330681', 9, 2, '3-4', 2, '08:35', '09:50', 11, 2, 2),
(135, 'MPL-5779834', 15, 5, '5-6', 2, '10:05', '11:25', 11, 2, 2),
(136, 'MPL-346273', 6, 7, '7-8', 2, '11:25', '12:40', 11, 2, 2),
(137, 'MPL-6023285', 6, 7, '1-2', 2, '07:15', '08:35', 12, 2, 2),
(138, 'MPL-6821947', 14, 3, '3-4', 2, '08:35', '09:50', 12, 2, 2),
(139, 'MPL-1847467', 42, 2, '5-6', 2, '10:05', '11:25', 12, 2, 2),
(140, 'MPL-188859', 15, 5, '7-8', 2, '11:25', '12:40', 12, 2, 2),
(141, 'MPL-785504', 11, 10, '1-3', 2, '07:15', '09:15', 13, 2, 2),
(142, 'MPL-2169073', 41, 7, '4-5', 2, '09:15', '10:45', 13, 2, 2),
(143, 'MPL-8206234', 42, 2, '6-8', 2, '10:45', '12:40', 13, 2, 2),
(144, 'MPL-4968593', 7, 9, '1-3', 3, '07:15', '09:15', 9, 2, 2),
(145, 'MPL-1112165', 6, 7, '4-5', 3, '09:15', '10:45', 9, 2, 2),
(146, 'MPL-648244', 12, 1, '6-8', 3, '10:45', '12:40', 9, 2, 2),
(147, 'MPL-7490735', 8, 6, '1-3', 3, '07:15', '09:15', 10, 2, 2),
(148, 'MPL-8051336', 10, 8, '4-6', 3, '09:15', '10:45', 10, 2, 2),
(149, 'MPL-6183774', 9, 2, '7-8', 3, '11:25', '12:40', 10, 2, 2),
(150, 'MPL-779516', 14, 3, '1-2', 3, '07:15', '08:35', 11, 2, 2),
(151, 'MPL-7298357', 9, 2, '3-5', 3, '08:35', '10:45', 11, 2, 2),
(152, 'MPL-1705167', 8, 6, '6-8', 3, '10:45', '12:40', 11, 2, 2),
(153, 'MPL-9820788', 43, 1, '1-3', 3, '07:15', '09:15', 12, 2, 2),
(154, 'MPL-332902', 8, 6, '4-6', 3, '09:15', '11:25', 12, 2, 2),
(155, 'MPL-333568', 6, 7, '7-8', 3, '11:25', '12:40', 12, 2, 2),
(156, 'MPL-2084005', 42, 2, '1-2', 3, '07:15', '08:35', 13, 2, 2),
(157, 'MPL-5733984', 41, 7, '3-4', 3, '08:35', '09:50', 13, 2, 2),
(158, 'MPL-6804042', 14, 3, '5-6', 3, '10:05', '11:25', 13, 2, 2),
(159, 'MPL-930351', 8, 6, '7-8', 3, '11:25', '12:40', 13, 2, 2),
(161, 'MPL-8336408', 15, 5, '1-2', 4, '07:15', '08:35', 9, 2, 2),
(162, 'MPL-6924512', 14, 3, '3-4', 4, '08:35', '09:50', 9, 2, 2),
(163, 'MPL-791072', 9, 2, '5-6', 4, '10:05', '11:25', 9, 2, 2),
(164, 'MPL-1200526', 6, 7, '7-8', 4, '11:25', '12:40', 9, 2, 2),
(165, 'MPL-3520443', 9, 2, '1-3', 4, '07:15', '09:15', 10, 2, 2),
(166, 'MPL-254096', 14, 3, '4-4', 4, '09:15', '09:50', 10, 2, 2),
(167, 'MPL-240704', 15, 5, '5-6', 4, '10:05', '11:25', 10, 2, 2),
(168, 'MPL-4340258', 8, 6, '7-8', 4, '11:25', '12:40', 10, 2, 2),
(169, 'MPL-3118281', 12, 1, '1-3', 4, '07:15', '09:15', 11, 2, 2),
(170, 'MPL-4331458', 11, 10, '4-6', 4, '09:15', '11:25', 11, 2, 2),
(171, 'MPL-5371654', 6, 7, '7-8', 4, '11:25', '12:40', 11, 2, 2),
(172, 'MPL-928894', 11, 10, '1-3', 4, '07:15', '09:15', 12, 2, 2),
(173, 'MPL-9722493', 8, 6, '4-5', 4, '09:15', '10:45', 12, 2, 2),
(174, 'MPL-5408037', 43, 1, '6-8', 4, '10:45', '12:40', 12, 2, 2),
(175, 'MPL-668023', 43, 1, '1-3', 4, '07:15', '09:15', 13, 2, 2),
(176, 'MPL-1152382', 10, 8, '4-6', 4, '09:15', '11:25', 13, 2, 2),
(177, 'MPL-55545', 15, 5, '7-8', 4, '11:25', '12:40', 13, 2, 2),
(178, 'MPL-7604895', 11, 10, '1-3', 5, '07:15', '09:15', 9, 2, 2),
(179, 'MPL-0601692', 12, 1, '4-6', 5, '09:30', '11:30', 9, 2, 2),
(180, 'MPL-3630369', 12, 1, '1-3', 5, '07:15', '09:15', 10, 2, 2),
(181, 'MPL-463091', 11, 10, '4-6', 5, '09:30', '11:30', 10, 2, 2),
(182, 'MPL-7754557', 8, 6, '1-3', 5, '07:15', '09:15', 11, 2, 2),
(183, 'MPL-650777', 10, 8, '4-6', 5, '09:30', '11:30', 11, 2, 2),
(184, 'MPL-0959477', 10, 8, '1-3', 5, '07:15', '09:15', 12, 2, 2),
(185, 'MPL-1841729', 7, 9, '4-6', 5, '09:30', '11:30', 12, 2, 2),
(186, 'MPL-7605772', 7, 9, '1-3', 5, '07:15', '09:15', 13, 2, 2),
(187, 'MPL-262811', 43, 1, '4-6', 5, '09:30', '11:30', 13, 2, 2),
(188, 'MPL-0955887', 9, 2, '5-6', 1, '11:25', '12:55', 9, 1, 2);

-- --------------------------------------------------------

--
-- Table structure for table `master_jam_mengajar`
--

CREATE TABLE `master_jam_mengajar` (
  `id` int(11) NOT NULL,
  `jam` varchar(32) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `master_jam_mengajar`
--

INSERT INTO `master_jam_mengajar` (`id`, `jam`) VALUES
(1, '07:00'),
(2, '07:15'),
(3, '07:30'),
(4, '07:45'),
(5, '08:00'),
(6, '08:30'),
(7, '09:00'),
(8, '09:30'),
(9, '10:00'),
(10, '10:30'),
(11, '11:00'),
(12, '11:30'),
(13, '12:00');

-- --------------------------------------------------------

--
-- Table structure for table `master_kelas`
--

CREATE TABLE `master_kelas` (
  `id` int(11) NOT NULL,
  `kelas` varchar(16) NOT NULL,
  `jml_laki` int(11) DEFAULT NULL,
  `jml_perempuan` int(11) DEFAULT NULL,
  `jml_seluruh` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `master_kelas`
--

INSERT INTO `master_kelas` (`id`, `kelas`, `jml_laki`, `jml_perempuan`, `jml_seluruh`) VALUES
(9, 'VIII-1', 2, 3, 5),
(10, 'VIII-2', 2, 3, 5),
(11, 'VIII-3', 2, 3, 5),
(12, 'VIII-4', 2, 3, 5),
(13, 'VIII-5', 3, 2, 5);

-- --------------------------------------------------------

--
-- Table structure for table `master_kepsek`
--

CREATE TABLE `master_kepsek` (
  `id` int(11) NOT NULL,
  `guru_id` int(11) DEFAULT NULL,
  `status` varchar(2) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `master_kepsek`
--

INSERT INTO `master_kepsek` (`id`, `guru_id`, `status`) VALUES
(1, 44, '1');

-- --------------------------------------------------------

--
-- Table structure for table `master_mapel`
--

CREATE TABLE `master_mapel` (
  `id` int(11) NOT NULL,
  `mapel` varchar(64) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `master_mapel`
--

INSERT INTO `master_mapel` (`id`, `mapel`) VALUES
(1, 'Bahasa Indonesia '),
(2, 'Matematika'),
(3, 'Bahasa Inggris'),
(4, 'Seni Budaya'),
(5, 'Prakarya'),
(6, 'Ilmu Pengetahuan Alam'),
(7, 'Ilmu Pengetahuan Sosial'),
(8, 'Pendidikan Agama Islam'),
(9, 'Pendidikan Kewarganegaraan'),
(10, 'Pendidikan Jasmani, Olahraga, dan Kesehatan');

-- --------------------------------------------------------

--
-- Table structure for table `master_nama_bulan`
--

CREATE TABLE `master_nama_bulan` (
  `id` int(11) NOT NULL,
  `nama_bulan` varchar(32) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `master_nama_bulan`
--

INSERT INTO `master_nama_bulan` (`id`, `nama_bulan`) VALUES
(1, 'januari'),
(2, 'februari'),
(3, 'maret'),
(4, 'april'),
(5, 'mei'),
(6, 'juni'),
(7, 'juli'),
(8, 'agustus'),
(9, 'september'),
(10, 'oktober'),
(11, 'november'),
(12, 'desember');

-- --------------------------------------------------------

--
-- Table structure for table `master_semester`
--

CREATE TABLE `master_semester` (
  `id` int(11) NOT NULL,
  `semester` varchar(32) NOT NULL,
  `is_active` varchar(1) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `master_semester`
--

INSERT INTO `master_semester` (`id`, `semester`, `is_active`) VALUES
(1, 'ganjil', '0'),
(2, 'genap', '1');

-- --------------------------------------------------------

--
-- Table structure for table `master_tahun`
--

CREATE TABLE `master_tahun` (
  `id` int(11) NOT NULL,
  `tahun` varchar(4) NOT NULL,
  `status` varchar(6) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `master_tahun`
--

INSERT INTO `master_tahun` (`id`, `tahun`, `status`) VALUES
(4, '2021', '0'),
(7, '2022', '1'),
(8, '2023', '1');

-- --------------------------------------------------------

--
-- Table structure for table `master_tahun_ajaran`
--

CREATE TABLE `master_tahun_ajaran` (
  `id` int(11) NOT NULL,
  `th_ajaran` varchar(32) NOT NULL,
  `is_active` varchar(1) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `master_tahun_ajaran`
--

INSERT INTO `master_tahun_ajaran` (`id`, `th_ajaran`, `is_active`) VALUES
(1, '2021-2022', '0'),
(2, '2022-2023', '1'),
(3, '2023-2024', '0');

-- --------------------------------------------------------

--
-- Table structure for table `master_wali_kelas`
--

CREATE TABLE `master_wali_kelas` (
  `id` int(11) NOT NULL,
  `guru_id` int(11) DEFAULT NULL,
  `kelas_id` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `master_wali_kelas`
--

INSERT INTO `master_wali_kelas` (`id`, `guru_id`, `kelas_id`) VALUES
(1, 7, 9),
(2, 8, 11),
(3, 10, 13),
(4, 12, 10),
(5, 13, 12);

--
-- Indexes for dumped tables
--

--
-- Indexes for table `alembic_version`
--
ALTER TABLE `alembic_version`
  ADD PRIMARY KEY (`version_num`);

--
-- Indexes for table `auth_status_user_login`
--
ALTER TABLE `auth_status_user_login`
  ADD PRIMARY KEY (`id`),
  ADD KEY `user_login_id` (`user_login_id`);

--
-- Indexes for table `auth_token_block`
--
ALTER TABLE `auth_token_block`
  ADD PRIMARY KEY (`id`),
  ADD KEY `user_id` (`user_id`),
  ADD KEY `ix_auth_token_block_jti` (`jti`);

--
-- Indexes for table `auth_user`
--
ALTER TABLE `auth_user`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `data_absensi`
--
ALTER TABLE `data_absensi`
  ADD PRIMARY KEY (`id`),
  ADD KEY `mengajar_id` (`mengajar_id`),
  ADD KEY `siswa_id` (`siswa_id`);

--
-- Indexes for table `data_jenis_pelanggaran`
--
ALTER TABLE `data_jenis_pelanggaran`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `data_pelanggaran`
--
ALTER TABLE `data_pelanggaran`
  ADD PRIMARY KEY (`id`),
  ADD KEY `jenis_pelanggaran_id` (`jenis_pelanggaran_id`),
  ADD KEY `siswa_id` (`siswa_id`),
  ADD KEY `guru_id` (`guru_id`);

--
-- Indexes for table `data_pembinaan`
--
ALTER TABLE `data_pembinaan`
  ADD PRIMARY KEY (`id`),
  ADD KEY `pelanggaran_id` (`pelanggaran_id`);

--
-- Indexes for table `data_sub_tata_tertib1`
--
ALTER TABLE `data_sub_tata_tertib1`
  ADD PRIMARY KEY (`id`),
  ADD KEY `t_tertib_id` (`t_tertib_id`);

--
-- Indexes for table `data_sub_tata_tertib2`
--
ALTER TABLE `data_sub_tata_tertib2`
  ADD PRIMARY KEY (`id`),
  ADD KEY `sub1_id` (`sub1_id`);

--
-- Indexes for table `data_tata_tertib`
--
ALTER TABLE `data_tata_tertib`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `data_teks`
--
ALTER TABLE `data_teks`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `detail_admin`
--
ALTER TABLE `detail_admin`
  ADD PRIMARY KEY (`id`),
  ADD KEY `user_id` (`user_id`);

--
-- Indexes for table `detail_guru`
--
ALTER TABLE `detail_guru`
  ADD PRIMARY KEY (`id`),
  ADD KEY `user_id` (`user_id`);

--
-- Indexes for table `detail_siswa`
--
ALTER TABLE `detail_siswa`
  ADD PRIMARY KEY (`id`),
  ADD KEY `kelas_id` (`kelas_id`),
  ADD KEY `user_id` (`user_id`);

--
-- Indexes for table `master_guru_bk`
--
ALTER TABLE `master_guru_bk`
  ADD PRIMARY KEY (`id`),
  ADD KEY `guru_id` (`guru_id`);

--
-- Indexes for table `master_hari`
--
ALTER TABLE `master_hari`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `master_jadwal_mengajar`
--
ALTER TABLE `master_jadwal_mengajar`
  ADD PRIMARY KEY (`id`),
  ADD KEY `guru_id` (`guru_id`),
  ADD KEY `hari_id` (`hari_id`),
  ADD KEY `kelas_id` (`kelas_id`),
  ADD KEY `mapel_id` (`mapel_id`),
  ADD KEY `semester_id` (`semester_id`),
  ADD KEY `tahun_ajaran_id` (`tahun_ajaran_id`);

--
-- Indexes for table `master_jam_mengajar`
--
ALTER TABLE `master_jam_mengajar`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `master_kelas`
--
ALTER TABLE `master_kelas`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `master_kepsek`
--
ALTER TABLE `master_kepsek`
  ADD PRIMARY KEY (`id`),
  ADD KEY `guru_id` (`guru_id`);

--
-- Indexes for table `master_mapel`
--
ALTER TABLE `master_mapel`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `master_nama_bulan`
--
ALTER TABLE `master_nama_bulan`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `master_semester`
--
ALTER TABLE `master_semester`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `master_tahun`
--
ALTER TABLE `master_tahun`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `tahun` (`tahun`);

--
-- Indexes for table `master_tahun_ajaran`
--
ALTER TABLE `master_tahun_ajaran`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `master_wali_kelas`
--
ALTER TABLE `master_wali_kelas`
  ADD PRIMARY KEY (`id`),
  ADD KEY `guru_id` (`guru_id`),
  ADD KEY `kelas_id` (`kelas_id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `auth_token_block`
--
ALTER TABLE `auth_token_block`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=137;

--
-- AUTO_INCREMENT for table `auth_user`
--
ALTER TABLE `auth_user`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=46;

--
-- AUTO_INCREMENT for table `data_absensi`
--
ALTER TABLE `data_absensi`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=703;

--
-- AUTO_INCREMENT for table `data_jenis_pelanggaran`
--
ALTER TABLE `data_jenis_pelanggaran`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=12;

--
-- AUTO_INCREMENT for table `data_pelanggaran`
--
ALTER TABLE `data_pelanggaran`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=37;

--
-- AUTO_INCREMENT for table `data_pembinaan`
--
ALTER TABLE `data_pembinaan`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;

--
-- AUTO_INCREMENT for table `data_sub_tata_tertib1`
--
ALTER TABLE `data_sub_tata_tertib1`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=25;

--
-- AUTO_INCREMENT for table `data_sub_tata_tertib2`
--
ALTER TABLE `data_sub_tata_tertib2`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=7;

--
-- AUTO_INCREMENT for table `data_tata_tertib`
--
ALTER TABLE `data_tata_tertib`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT for table `data_teks`
--
ALTER TABLE `data_teks`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT for table `detail_admin`
--
ALTER TABLE `detail_admin`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT for table `detail_guru`
--
ALTER TABLE `detail_guru`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=16;

--
-- AUTO_INCREMENT for table `detail_siswa`
--
ALTER TABLE `detail_siswa`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=30;

--
-- AUTO_INCREMENT for table `master_guru_bk`
--
ALTER TABLE `master_guru_bk`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT for table `master_hari`
--
ALTER TABLE `master_hari`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=8;

--
-- AUTO_INCREMENT for table `master_jadwal_mengajar`
--
ALTER TABLE `master_jadwal_mengajar`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=189;

--
-- AUTO_INCREMENT for table `master_jam_mengajar`
--
ALTER TABLE `master_jam_mengajar`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=14;

--
-- AUTO_INCREMENT for table `master_kelas`
--
ALTER TABLE `master_kelas`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=18;

--
-- AUTO_INCREMENT for table `master_kepsek`
--
ALTER TABLE `master_kepsek`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- AUTO_INCREMENT for table `master_mapel`
--
ALTER TABLE `master_mapel`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=11;

--
-- AUTO_INCREMENT for table `master_nama_bulan`
--
ALTER TABLE `master_nama_bulan`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=14;

--
-- AUTO_INCREMENT for table `master_semester`
--
ALTER TABLE `master_semester`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT for table `master_tahun`
--
ALTER TABLE `master_tahun`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=9;

--
-- AUTO_INCREMENT for table `master_tahun_ajaran`
--
ALTER TABLE `master_tahun_ajaran`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT for table `master_wali_kelas`
--
ALTER TABLE `master_wali_kelas`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `auth_status_user_login`
--
ALTER TABLE `auth_status_user_login`
  ADD CONSTRAINT `auth_status_user_login_ibfk_1` FOREIGN KEY (`user_login_id`) REFERENCES `auth_user` (`id`) ON DELETE CASCADE;

--
-- Constraints for table `auth_token_block`
--
ALTER TABLE `auth_token_block`
  ADD CONSTRAINT `auth_token_block_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Constraints for table `data_absensi`
--
ALTER TABLE `data_absensi`
  ADD CONSTRAINT `data_absensi_ibfk_1` FOREIGN KEY (`mengajar_id`) REFERENCES `master_jadwal_mengajar` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `data_absensi_ibfk_2` FOREIGN KEY (`siswa_id`) REFERENCES `detail_siswa` (`user_id`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Constraints for table `data_pelanggaran`
--
ALTER TABLE `data_pelanggaran`
  ADD CONSTRAINT `data_pelanggaran_ibfk_4` FOREIGN KEY (`guru_id`) REFERENCES `detail_guru` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `data_pelanggaran_ibfk_5` FOREIGN KEY (`jenis_pelanggaran_id`) REFERENCES `data_jenis_pelanggaran` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `data_pelanggaran_ibfk_6` FOREIGN KEY (`siswa_id`) REFERENCES `detail_siswa` (`user_id`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Constraints for table `data_pembinaan`
--
ALTER TABLE `data_pembinaan`
  ADD CONSTRAINT `data_pembinaan_ibfk_1` FOREIGN KEY (`pelanggaran_id`) REFERENCES `data_pelanggaran` (`id`);

--
-- Constraints for table `data_sub_tata_tertib1`
--
ALTER TABLE `data_sub_tata_tertib1`
  ADD CONSTRAINT `data_sub_tata_tertib1_ibfk_1` FOREIGN KEY (`t_tertib_id`) REFERENCES `data_tata_tertib` (`id`);

--
-- Constraints for table `data_sub_tata_tertib2`
--
ALTER TABLE `data_sub_tata_tertib2`
  ADD CONSTRAINT `data_sub_tata_tertib2_ibfk_1` FOREIGN KEY (`sub1_id`) REFERENCES `data_sub_tata_tertib1` (`id`);

--
-- Constraints for table `detail_admin`
--
ALTER TABLE `detail_admin`
  ADD CONSTRAINT `detail_admin_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`) ON DELETE CASCADE;

--
-- Constraints for table `detail_guru`
--
ALTER TABLE `detail_guru`
  ADD CONSTRAINT `detail_guru_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Constraints for table `detail_siswa`
--
ALTER TABLE `detail_siswa`
  ADD CONSTRAINT `detail_siswa_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `detail_siswa_ibfk_2` FOREIGN KEY (`kelas_id`) REFERENCES `master_kelas` (`id`);

--
-- Constraints for table `master_guru_bk`
--
ALTER TABLE `master_guru_bk`
  ADD CONSTRAINT `master_guru_bk_ibfk_1` FOREIGN KEY (`guru_id`) REFERENCES `detail_guru` (`user_id`) ON UPDATE CASCADE;

--
-- Constraints for table `master_jadwal_mengajar`
--
ALTER TABLE `master_jadwal_mengajar`
  ADD CONSTRAINT `master_jadwal_mengajar_ibfk_1` FOREIGN KEY (`tahun_ajaran_id`) REFERENCES `master_tahun_ajaran` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `master_jadwal_mengajar_ibfk_2` FOREIGN KEY (`mapel_id`) REFERENCES `master_mapel` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `master_jadwal_mengajar_ibfk_3` FOREIGN KEY (`kelas_id`) REFERENCES `master_kelas` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `master_jadwal_mengajar_ibfk_4` FOREIGN KEY (`hari_id`) REFERENCES `master_hari` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `master_jadwal_mengajar_ibfk_5` FOREIGN KEY (`guru_id`) REFERENCES `detail_guru` (`user_id`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `master_jadwal_mengajar_ibfk_6` FOREIGN KEY (`semester_id`) REFERENCES `master_semester` (`id`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Constraints for table `master_kepsek`
--
ALTER TABLE `master_kepsek`
  ADD CONSTRAINT `master_kepsek_ibfk_1` FOREIGN KEY (`guru_id`) REFERENCES `detail_guru` (`user_id`) ON UPDATE CASCADE;

--
-- Constraints for table `master_wali_kelas`
--
ALTER TABLE `master_wali_kelas`
  ADD CONSTRAINT `master_wali_kelas_ibfk_1` FOREIGN KEY (`kelas_id`) REFERENCES `master_kelas` (`id`),
  ADD CONSTRAINT `master_wali_kelas_ibfk_2` FOREIGN KEY (`guru_id`) REFERENCES `detail_guru` (`user_id`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
