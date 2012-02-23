SET SQL_MODE="NO_AUTO_VALUE_ON_ZERO";
--
-- Database: `pba`
--

-- --------------------------------------------------------

--
-- table `pba_arp`
--

DROP TABLE IF EXISTS `pba_arp`;
CREATE TABLE IF NOT EXISTS `pba_arp` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `hash` varchar(50) CHARACTER SET utf8 COLLATE utf8_turkish_ci NOT NULL,
  `thetime` datetime NOT NULL,
  `src_mac` text COLLATE utf8_unicode_ci NOT NULL,
  `src_ip` text COLLATE utf8_unicode_ci NOT NULL,
  `first_timestamp` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `last_timestamp` timestamp NOT NULL DEFAULT '0000-00-00 00:00:00',
  `count` int(11) NOT NULL DEFAULT '0',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci COMMENT='NBDS LOG' AUTO_INCREMENT=1 ;

-- --------------------------------------------------------

--
-- table `pba_arp_raw`
--

DROP TABLE IF EXISTS `pba_arp_raw`;
CREATE TABLE IF NOT EXISTS `pba_arp_raw` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `hash` varchar(50) COLLATE utf8_unicode_ci NOT NULL,
  `raw` text COLLATE utf8_unicode_ci NOT NULL,
  `timestamp` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci AUTO_INCREMENT=1 ;

-- --------------------------------------------------------

--
-- table `pba_arp_summary`
--

DROP TABLE IF EXISTS `pba_arp_summary`;
CREATE TABLE IF NOT EXISTS `pba_arp_summary` (
  `src_mac` text COLLATE utf8_unicode_ci NOT NULL,
  `src_ip` text COLLATE utf8_unicode_ci NOT NULL,
  `count` int(11) NOT NULL DEFAULT '1',
  `first_seen` datetime DEFAULT NULL,
  `last_seen` datetime DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

-- --------------------------------------------------------

--
-- table `pba_nbds`
--

DROP TABLE IF EXISTS `pba_nbds`;
CREATE TABLE IF NOT EXISTS `pba_nbds` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `hash` varchar(50) CHARACTER SET utf8 COLLATE utf8_turkish_ci NOT NULL,
  `thetime` datetime NOT NULL,
  `src_mac` text COLLATE utf8_unicode_ci NOT NULL,
  `src_ip` text COLLATE utf8_unicode_ci NOT NULL,
  `dst_ip` text COLLATE utf8_unicode_ci NOT NULL,
  `src_netbios_name` text COLLATE utf8_unicode_ci NOT NULL,
  `src_netbios_name_hex` text COLLATE utf8_unicode_ci NOT NULL,
  `src_netbios_name_encoded` text COLLATE utf8_unicode_ci NOT NULL,
  `dst_netbios_name` text COLLATE utf8_unicode_ci NOT NULL,
  `dst_netbios_name_hex` text COLLATE utf8_unicode_ci NOT NULL,
  `dst_netbios_name_encoded` text COLLATE utf8_unicode_ci NOT NULL,
  `first_timestamp` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `last_timestamp` timestamp NOT NULL DEFAULT '0000-00-00 00:00:00',
  `count` int(11) NOT NULL DEFAULT '0',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci COMMENT='NBDS LOG' AUTO_INCREMENT=1 ;

-- --------------------------------------------------------

--
-- table `pba_nbds_raw`
--

DROP TABLE IF EXISTS `pba_nbds_raw`;
CREATE TABLE IF NOT EXISTS `pba_nbds_raw` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `hash` varchar(50) COLLATE utf8_unicode_ci NOT NULL,
  `raw` text COLLATE utf8_unicode_ci NOT NULL,
  `timestamp` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci AUTO_INCREMENT=1 ;

-- --------------------------------------------------------

--
-- table `pba_nbds_summary`
--

DROP TABLE IF EXISTS `pba_nbds_summary`;
CREATE TABLE IF NOT EXISTS `pba_nbds_summary` (
  `src_mac` text COLLATE utf8_unicode_ci NOT NULL,
  `src_ip` text COLLATE utf8_unicode_ci NOT NULL,
  `dst_ip` text COLLATE utf8_unicode_ci NOT NULL,
  `src_netbios_name` text COLLATE utf8_unicode_ci NOT NULL,
  `src_netbios_name_encoded` text COLLATE utf8_unicode_ci NOT NULL,
  `dst_netbios_name` text COLLATE utf8_unicode_ci NOT NULL,
  `dst_netbios_name_encoded` text COLLATE utf8_unicode_ci NOT NULL,
  `count` int(11) NOT NULL DEFAULT '1',
  `first_seen` datetime DEFAULT NULL,
  `last_seen` datetime DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;


-- --------------------------------------------------------

--
-- view `pba_nbds_groups`
--
DROP VIEW IF EXISTS `pba_nbds_groups`;
CREATE VIEW `pba_nbds_groups` AS
SELECT DISTINCT `pba_nbds_summary`.`dst_netbios_name` AS `gruppo`,
                count(`pba_nbds_summary`.`src_netbios_name`) AS `macchine`
FROM `pba_nbds_summary`
GROUP BY `pba_nbds_summary`.`dst_netbios_name`
ORDER BY count(`pba_nbds_summary`.`src_netbios_name`) DESC;

-- --------------------------------------------------------

--
-- view `pba_arp_report`
--
DROP VIEW IF EXISTS `pba_arp_report`;
CREATE VIEW `pba_arp_report` AS
SELECT  `pba_arp_summary`.`src_mac` AS `src_mac`,
        `pba_arp_summary`.`src_ip` AS `src_ip`,
        `pba_arp_summary`.`count` AS `count`,
        `pba_arp_summary`.`first_seen` AS `first_seen`,
        `pba_arp_summary`.`last_seen` AS `last_seen`
FROM `pba_arp_summary`
ORDER BY `pba_arp_summary`.`count` DESC;

-- --------------------------------------------------------

--
-- view `pba_nbds_report`
--
DROP VIEW IF EXISTS `pba_nbds_report`;
CREATE VIEW `pba_nbds_report` AS
SELECT  `pba_nbds_summary`.`src_mac` AS `src_mac`,
        `pba_nbds_summary`.`src_ip` AS `src_ip`,
        `pba_nbds_summary`.`dst_ip` AS `dst_ip`,
        `pba_nbds_summary`.`src_netbios_name` AS `src_netbios_name`,
        `pba_nbds_summary`.`dst_netbios_name` AS `dst_netbios_name`,
        `pba_nbds_summary`.`count` AS `count`,
        `pba_nbds_summary`.`first_seen` AS `first_seen`,
        `pba_nbds_summary`.`last_seen` AS `last_seen`
FROM `pba_nbds_summary`
ORDER BY `pba_nbds_summary`.`count` DESC;
