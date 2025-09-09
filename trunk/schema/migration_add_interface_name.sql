-- Migration script to add interface_name field to all relevant tables
-- This allows tracking which network interface received each packet

-- Set SQL mode to allow zero dates (for compatibility)
SET sql_mode = 'ALLOW_INVALID_DATES';

-- Add interface_name to pba_arp table
ALTER TABLE `pba_arp` 
ADD COLUMN `interface_name` varchar(20) NOT NULL DEFAULT '' AFTER `src_ip`;

-- Add interface_name to pba_arp_raw table  
ALTER TABLE `pba_arp_raw`
ADD COLUMN `interface_name` varchar(20) NOT NULL DEFAULT '' AFTER `hash`;

-- Add interface_name to pba_arp_summary table
ALTER TABLE `pba_arp_summary`
ADD COLUMN `interface_name` varchar(20) NOT NULL DEFAULT '' AFTER `src_ip`;

-- Add interface_name to pba_nbds table
ALTER TABLE `pba_nbds`
ADD COLUMN `interface_name` varchar(20) NOT NULL DEFAULT '' AFTER `src_ip`;

-- Add interface_name to pba_nbds_raw table
ALTER TABLE `pba_nbds_raw`
ADD COLUMN `interface_name` varchar(20) NOT NULL DEFAULT '' AFTER `hash`;

-- Add interface_name to pba_nbds_summary table
ALTER TABLE `pba_nbds_summary`
ADD COLUMN `interface_name` varchar(20) NOT NULL DEFAULT '' AFTER `src_ip`;

-- Update views to include interface_name

-- Drop and recreate pba_arp_report view
DROP VIEW IF EXISTS `pba_arp_report`;
CREATE VIEW `pba_arp_report` AS
SELECT  `pba_arp_summary`.`src_mac` AS `src_mac`,
        `pba_arp_summary`.`src_ip` AS `src_ip`,
        `pba_arp_summary`.`interface_name` AS `interface_name`,
        `pba_arp_summary`.`count` AS `count`,
        `pba_arp_summary`.`first_seen` AS `first_seen`,
        `pba_arp_summary`.`last_seen` AS `last_seen`
FROM `pba_arp_summary`
ORDER BY `pba_arp_summary`.`count` DESC;

-- Drop and recreate pba_nbds_report view
DROP VIEW IF EXISTS `pba_nbds_report`;
CREATE VIEW `pba_nbds_report` AS
SELECT  `pba_nbds_summary`.`src_mac` AS `src_mac`,
        `pba_nbds_summary`.`src_ip` AS `src_ip`,
        `pba_nbds_summary`.`interface_name` AS `interface_name`,
        `pba_nbds_summary`.`dst_ip` AS `dst_ip`,
        `pba_nbds_summary`.`src_netbios_name` AS `src_netbios_name`,
        `pba_nbds_summary`.`dst_netbios_name` AS `dst_netbios_name`,
        `pba_nbds_summary`.`count` AS `count`,
        `pba_nbds_summary`.`first_seen` AS `first_seen`,
        `pba_nbds_summary`.`last_seen` AS `last_seen`
FROM `pba_nbds_summary`
ORDER BY `pba_nbds_summary`.`count` DESC;