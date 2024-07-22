-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Jul 22, 2024 at 04:20 PM
-- Server version: 10.4.32-MariaDB
-- PHP Version: 8.0.30

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `church_reports`
--

-- --------------------------------------------------------

--
-- Table structure for table `church_reports`
--

CREATE TABLE `church_reports` (
  `id` varchar(255) NOT NULL,
  `ministry_year` varchar(255) DEFAULT NULL,
  `month` varchar(255) DEFAULT NULL,
  `zone` varchar(255) DEFAULT NULL,
  `region` varchar(255) DEFAULT NULL,
  `num_groups` int(11) DEFAULT NULL,
  `num_achieved_1m_copies` int(11) DEFAULT NULL,
  `num_hit_500k_copies` int(11) DEFAULT NULL,
  `num_hit_250k_copies` int(11) DEFAULT NULL,
  `num_hit_100k` int(11) DEFAULT NULL,
  `wonder_alerts` int(11) DEFAULT NULL,
  `sytk_alerts` int(11) DEFAULT NULL,
  `rrm` int(11) DEFAULT NULL,
  `total_copies_distribution` int(11) DEFAULT NULL,
  `num_souls_won` int(11) DEFAULT NULL,
  `num_rhapsody_outreaches` int(11) DEFAULT NULL,
  `rhapsody_cells` int(11) DEFAULT NULL,
  `num_new_churches` int(11) DEFAULT NULL,
  `num_partners_enlisted` int(11) DEFAULT NULL,
  `num_lingual_cells` int(11) DEFAULT NULL,
  `num_language_churches` int(11) DEFAULT NULL,
  `num_languages_sponsored` int(11) DEFAULT NULL,
  `num_distribution_centers` int(11) DEFAULT NULL,
  `num_prayer_programs` int(11) DEFAULT NULL,
  `num_external_ministers` int(11) DEFAULT NULL,
  `num_i_seed_daily` int(11) DEFAULT NULL,
  `num_language_ambassadors` int(11) DEFAULT NULL,
  `full_name` varchar(255) DEFAULT NULL,
  `submission_timestamp` varchar(255) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `church_reports`
--

INSERT INTO `church_reports` (`id`, `ministry_year`, `month`, `zone`, `region`, `num_groups`, `num_achieved_1m_copies`, `num_hit_500k_copies`, `num_hit_250k_copies`, `num_hit_100k`, `wonder_alerts`, `sytk_alerts`, `rrm`, `total_copies_distribution`, `num_souls_won`, `num_rhapsody_outreaches`, `rhapsody_cells`, `num_new_churches`, `num_partners_enlisted`, `num_lingual_cells`, `num_language_churches`, `num_languages_sponsored`, `num_distribution_centers`, `num_prayer_programs`, `num_external_ministers`, `num_i_seed_daily`, `num_language_ambassadors`, `full_name`, `submission_timestamp`) VALUES
('GPD2024-0001', '2024', 'March', 'Lagos Sub Zone C', 'Region 6', 12, 12, 12, 12, 21, 21, 21, 21, 21, 21, 12, 212, 12, 21, 21, 21, 21, 21, 21, 21, 12, 12, 'cece', '2024-07-10 17:48:30');

-- --------------------------------------------------------

--
-- Table structure for table `id_tracker`
--

CREATE TABLE `id_tracker` (
  `year` varchar(255) NOT NULL,
  `last_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `id_tracker`
--

INSERT INTO `id_tracker` (`year`, `last_id`) VALUES
('2023', 5),
('2024', 1);

-- --------------------------------------------------------

--
-- Table structure for table `users`
--

CREATE TABLE `users` (
  `username` varchar(255) NOT NULL,
  `password` varbinary(255) NOT NULL,
  `full_name` varchar(255) NOT NULL,
  `region` varchar(255) NOT NULL,
  `zone` varchar(255) NOT NULL,
  `privileges` varchar(255) DEFAULT 'View Reports,Submit Reports,Manage Reports'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `users`
--

INSERT INTO `users` (`username`, `password`, `full_name`, `region`, `zone`, `privileges`) VALUES
('cece', 0x2432622431322455513937643378414d767675324370686863314a6865594d49486a516c3238686452442f54394b384a37414d626b4b466176733879, 'cece', 'Region 6', 'Lagos Sub Zone C', 'View Reports,Submit Reports,Manage Reports'),
('max', 0x243279243130247350432e2f41345079563670504e6c7734436f5042757957746c6c4f6d6c4470346d357a4e7637322e71525362464a335247717853, 'max', 'Lagos Zone 6', 'Lagos Sub-Zone C', 'View Reports,Submit Reports,Manage Reports'),
('maxwellvn', 0x24326224313224754564542f71626474707356476736563667795a6a7567564b38392e487a61623430363950584c49576e68536335666d7854356c71, 'jay jay', 'Region 1', 'SA Zone 1', 'View Reports,Submit Reports,Manage Reports');

-- --------------------------------------------------------

--
-- Table structure for table `zones`
--

CREATE TABLE `zones` (
  `id` int(11) NOT NULL,
  `region` varchar(255) NOT NULL,
  `zone` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `zones`
--

INSERT INTO `zones` (`id`, `region`, `zone`) VALUES
(1, 'Region 1', 'SA Zone 1'),
(2, 'Region 1', 'Cape Town Zone 1'),
(3, 'Region 1', 'SA Zone 5'),
(4, 'Region 1', 'Cape Town Zone 2'),
(5, 'Region 1', 'SA Zone 2'),
(6, 'Region 1', 'BLW Southern Africa Region'),
(7, 'Region 1', 'Middle East Asia'),
(8, 'Region 1', 'CE India'),
(9, 'Region 1', 'SA Zone 3'),
(10, 'Region 1', 'Durban'),
(11, 'Region 1', 'BLW Asia & North Africa Region'),
(12, 'Region 2', 'UK Zone 3 Region 2'),
(13, 'Region 2', 'CE Amsterdam DSP'),
(14, 'Region 2', 'BLW Europe Region'),
(15, 'Region 2', 'Western Europe Zone 4'),
(16, 'Region 2', 'UK Zone 3 Region 1'),
(17, 'Region 2', 'USA Zone 2 Region 1'),
(18, 'Region 2', 'Eastern Europe'),
(19, 'Region 2', 'Australia Zone'),
(20, 'Region 2', 'Toronto Zone'),
(21, 'Region 2', 'Western Europe Zone 2'),
(22, 'Region 2', 'USA Zone 1 Region 2/Pacific Islands Region/New Zealand'),
(23, 'Region 2', 'USA Region 3'),
(24, 'Region 2', 'BLW Canada Sub-Region'),
(25, 'Region 2', 'Western Europe Zone 3'),
(26, 'Region 2', 'Dallas Zone USA Region 2'),
(27, 'Region 2', 'UK Zone 4 Region 1'),
(28, 'Region 2', 'Western Europe Zone 1'),
(29, 'Region 2', 'UK Zone 1 (Region 2)'),
(30, 'Region 2', 'UK Zone 2 Region 1'),
(31, 'Region 2', 'UK Zone 1 Region 1'),
(32, 'Region 2', 'USA Zone 1 Region 1'),
(33, 'Region 2', 'BLW USA Region 2'),
(34, 'Region 2', 'Ottawa Zone'),
(35, 'Region 2', 'UK Zone 4 Region 2'),
(36, 'Region 2', 'Quebec Zone'),
(37, 'Region 2', 'BLW USA Region 1'),
(38, 'Region 3', 'Kenya Zone'),
(39, 'Region 3', 'Lagos Zone 1'),
(40, 'Region 3', 'EWCA Zone 4'),
(41, 'Region 3', 'CE Chad'),
(42, 'Region 3', 'EWCA Zone 2'),
(43, 'Region 3', 'Ministry Center Warri'),
(44, 'Region 3', 'Mid-West Zone'),
(45, 'Region 3', 'South West Zone 2'),
(46, 'Region 3', 'South West Zone 1'),
(47, 'Region 3', 'Lagos Zone 4'),
(48, 'Region 3', 'Ibadan Zone 1'),
(49, 'Region 3', 'Ibadan Zone 2'),
(50, 'Region 3', 'Accra Zone'),
(51, 'Region 3', 'South West Zone 3'),
(52, 'Region 3', 'EWCA Zone 5'),
(53, 'Region 3', 'EWCA Zone 3'),
(54, 'Region 3', 'MC Abeokuta'),
(55, 'Region 3', 'EWCA Zone 6'),
(56, 'Region 4', 'Abuja Zone 2'),
(57, 'Region 4', 'CELVZ'),
(58, 'Region 4', 'Lagos Zone 2'),
(59, 'Region 4', 'South South Zone 3'),
(60, 'Region 4', 'South-South Zone 2'),
(61, 'Region 4', 'Lagos Zone 3'),
(62, 'Region 4', 'EWCA Zone 1'),
(63, 'Region 4', 'South-South Zone 1'),
(64, 'Region 4', 'DSC Sub Zone Warri'),
(65, 'Region 4', 'Ministry Center Abuja'),
(66, 'Region 4', 'Ministry Center Calabar'),
(67, 'Region 5', 'Middle Belt Region Zone 2'),
(68, 'Region 5', 'North East Zone 1'),
(69, 'Region 5', 'PH Zone 1'),
(70, 'Region 5', 'Lagos Zone 6'),
(71, 'Region 5', 'Lagos Sub Zone B'),
(72, 'Region 5', 'Middle Belt Region Zone 1'),
(73, 'Region 5', 'PH Zone 3'),
(74, 'Region 5', 'Lagos Sub Zone A'),
(75, 'Region 5', 'South West Zone 5'),
(76, 'Region 5', 'Onitsha Zone'),
(77, 'Region 5', 'Abuja Zone'),
(78, 'Region 5', 'PH Zone 2'),
(79, 'Region 5', 'North West Zone 2'),
(80, 'Region 5', 'Lagos Zone 5'),
(81, 'Region 5', 'Northwest Zone 1'),
(82, 'Region 5', 'Ministry Center Ibadan'),
(83, 'Region 5', 'South West Zone 4'),
(84, 'Region 5', 'North Central Zone 1'),
(85, 'Region 5', 'North Central Zone 2'),
(86, 'Region 6', 'Lagos Sub Zone C'),
(87, 'Region 6', 'Benin Zone 2'),
(88, 'Region 6', 'Aba Zone'),
(89, 'Region 6', 'Benin Zone 1'),
(90, 'Region 6', 'Loveworld Church Zone'),
(91, 'Region 6', 'South East Zone 1'),
(92, 'Region 6', 'BLW West Africa Region'),
(93, 'Region 6', 'BLW East & Central Africa Region'),
(94, 'Region 6', 'South East Zone 3'),
(95, 'Region 6', 'Edo North & Central'),
(96, 'Region 6', 'BLW Nigeria Region');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `church_reports`
--
ALTER TABLE `church_reports`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `id_tracker`
--
ALTER TABLE `id_tracker`
  ADD PRIMARY KEY (`year`);

--
-- Indexes for table `users`
--
ALTER TABLE `users`
  ADD PRIMARY KEY (`username`);

--
-- Indexes for table `zones`
--
ALTER TABLE `zones`
  ADD PRIMARY KEY (`id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `zones`
--
ALTER TABLE `zones`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=97;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
