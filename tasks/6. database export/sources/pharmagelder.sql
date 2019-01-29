-- phpMyAdmin SQL Dump
-- version 4.7.0
-- https://www.phpmyadmin.net/
--
-- Host: localhost
-- Erstellungszeit: 29. Jan 2019 um 14:19
-- Server-Version: 10.1.21-MariaDB
-- PHP-Version: 7.1.2

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET AUTOCOMMIT = 0;
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Datenbank: `pharmagelder`
--

-- --------------------------------------------------------

--
-- Tabellenstruktur für Tabelle `accumulation`
--

CREATE TABLE `accumulation` (
  `acc_id` int(11) NOT NULL,
  `acc_fk_pharma` int(11) NOT NULL,
  `acc_year` int(11) NOT NULL,
  `acc_donations_grants` double DEFAULT NULL,
  `acc_sponsorship` double DEFAULT NULL,
  `acc_registration_fees` double DEFAULT NULL,
  `acc_travel_accommodation` double DEFAULT NULL,
  `acc_fees` double DEFAULT NULL,
  `acc_related_expenses` double DEFAULT NULL,
  `acc_total` double NOT NULL,
  `acc_type` varchar(5) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Tabellenstruktur für Tabelle `pharma`
--

CREATE TABLE `pharma` (
  `pha_id` int(11) NOT NULL,
  `pha_name` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Tabellenstruktur für Tabelle `pharma_source`
--

CREATE TABLE `pharma_source` (
  `phf_id` int(11) NOT NULL,
  `phf_fk_pharma` int(11) NOT NULL,
  `phf_source` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Tabellenstruktur für Tabelle `recipient`
--

CREATE TABLE `recipient` (
  `rec_id` int(11) NOT NULL,
  `rec_name` varchar(255) NOT NULL,
  `rec_address` varchar(255) DEFAULT NULL,
  `rec_location` varchar(255) DEFAULT NULL,
  `rec_plz` varchar(8) DEFAULT NULL,
  `rec_plz_shaddow` varchar(255) DEFAULT NULL,
  `rec_country` varchar(3) NOT NULL,
  `rec_uci` varchar(255) NOT NULL,
  `rec_type` varchar(3) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Tabellenstruktur für Tabelle `transaction`
--

CREATE TABLE `transaction` (
  `tra_id` int(11) NOT NULL,
  `tra_fk_pharma` int(11) NOT NULL,
  `tra_fk_recipient` int(11) NOT NULL,
  `tra_year` int(4) NOT NULL,
  `tra_donations_grants` double DEFAULT NULL,
  `tra_sponsorship` double DEFAULT NULL,
  `tra_registration_fees` double DEFAULT NULL,
  `tra_travel_accommodation` double DEFAULT NULL,
  `tra_fees` double DEFAULT NULL,
  `tra_related_expenses` double DEFAULT NULL,
  `tra_total` double DEFAULT NULL,
  `tra_name_original` varchar(255) DEFAULT NULL,
  `tra_location_original` varchar(255) DEFAULT NULL,
  `tra_address_original` varchar(255) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Indizes der exportierten Tabellen
--

--
-- Indizes für die Tabelle `accumulation`
--
ALTER TABLE `accumulation`
  ADD PRIMARY KEY (`acc_id`),
  ADD KEY `acc_fk_pharma` (`acc_fk_pharma`);

--
-- Indizes für die Tabelle `pharma`
--
ALTER TABLE `pharma`
  ADD PRIMARY KEY (`pha_id`);

--
-- Indizes für die Tabelle `pharma_source`
--
ALTER TABLE `pharma_source`
  ADD PRIMARY KEY (`phf_id`),
  ADD KEY `phf_fk_pharma` (`phf_fk_pharma`);

--
-- Indizes für die Tabelle `recipient`
--
ALTER TABLE `recipient`
  ADD PRIMARY KEY (`rec_id`);

--
-- Indizes für die Tabelle `transaction`
--
ALTER TABLE `transaction`
  ADD PRIMARY KEY (`tra_id`),
  ADD KEY `tra_fk_pharma` (`tra_fk_pharma`),
  ADD KEY `tra_fk_recipient` (`tra_fk_recipient`);

--
-- AUTO_INCREMENT für exportierte Tabellen
--

--
-- AUTO_INCREMENT für Tabelle `accumulation`
--
ALTER TABLE `accumulation`
  MODIFY `acc_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=169;
--
-- AUTO_INCREMENT für Tabelle `pharma`
--
ALTER TABLE `pharma`
  MODIFY `pha_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=57;
--
-- AUTO_INCREMENT für Tabelle `pharma_source`
--
ALTER TABLE `pharma_source`
  MODIFY `phf_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=57;
--
-- AUTO_INCREMENT für Tabelle `recipient`
--
ALTER TABLE `recipient`
  MODIFY `rec_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6286;
--
-- AUTO_INCREMENT für Tabelle `transaction`
--
ALTER TABLE `transaction`
  MODIFY `tra_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=10486;
--
-- Constraints der exportierten Tabellen
--

--
-- Constraints der Tabelle `accumulation`
--
ALTER TABLE `accumulation`
  ADD CONSTRAINT `accumulation_ibfk_1` FOREIGN KEY (`acc_fk_pharma`) REFERENCES `pharma` (`pha_id`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Constraints der Tabelle `pharma_source`
--
ALTER TABLE `pharma_source`
  ADD CONSTRAINT `pharma_source_ibfk_1` FOREIGN KEY (`phf_fk_pharma`) REFERENCES `pharma` (`pha_id`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Constraints der Tabelle `transaction`
--
ALTER TABLE `transaction`
  ADD CONSTRAINT `transaction_ibfk_1` FOREIGN KEY (`tra_fk_pharma`) REFERENCES `pharma` (`pha_id`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `transaction_ibfk_2` FOREIGN KEY (`tra_fk_recipient`) REFERENCES `recipient` (`rec_id`) ON DELETE CASCADE ON UPDATE CASCADE;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
