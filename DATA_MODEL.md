# Data Model Documentation for pypbald

## Overview

This document outlines the database schema used in the **pypbald** project. The schema consists of several tables designed to store information related to ARP (Address Resolution Protocol) and Network Block Devices (NBDs). The database uses the **InnoDB** engine with UTF-8 character encoding.

---

## Tables

### 1. `pba_arp`

Stores ARP log information.

| Column            | Type          | Constraints                            | Description                        |
|-------------------|---------------|----------------------------------------|------------------------------------|
| `id`              | `int(11)`     | Primary Key, Auto-Increment            | Unique identifier for the record   |
| `hash`            | `varchar(50)` | NOT NULL                               | Hash value representing the entry  |
| `thetime`         | `datetime`    | NOT NULL                               | Timestamp of the ARP event         |
| `src_mac`         | `text`        | NOT NULL                               | Source MAC address                 |
| `src_ip`          | `text`        | NOT NULL                               | Source IP address                  |
| `first_timestamp` | `timestamp`   | NOT NULL, Default: `CURRENT_TIMESTAMP` | First recorded timestamp           |
| `last_timestamp`  | `timestamp`   | Default: `'0000-00-00 00:00:00'`      | Last recorded timestamp            |
| `count`           | `int(11)`     | NOT NULL, Default: `0`                 | Number of occurrences              |

**Comment**: *NBDS LOG*

---

### 2. `pba_arp_raw`

Stores raw ARP log data.

| Column       | Type          | Constraints                            | Description                          |
|--------------|---------------|----------------------------------------|--------------------------------------|
| `id`        | `int(11)`     | Primary Key, Auto-Increment            | Unique identifier for the record     |
| `hash`      | `varchar(50)` | NOT NULL                               | Hash value representing the entry    |
| `raw`       | `text`        | NOT NULL                               | Raw ARP log data                     |
| `timestamp` | `timestamp`   | NOT NULL, Default: `CURRENT_TIMESTAMP` | Time the raw data was recorded       |

---

### 3. `pba_arp_summary`

Stores summarized ARP log information.

| Column        | Type          | Constraints                  | Description                          |
|---------------|---------------|------------------------------|--------------------------------------|
| `src_mac`    | `text`        | NOT NULL                     | Source MAC address                   |
| `src_ip`     | `text`        | NOT NULL                     | Source IP address                    |
| `count`      | `int(11)`     | NOT NULL, Default: `1`       | Number of occurrences                |
| `first_seen` | `datetime`    |                              | First time the entry was seen        |
| `last_seen`  | `datetime`    |                              | Last time the entry was seen         |

---

### 4. `pba_nbds`

Stores Network Block Device (NBD) log information.

| Column     | Type          | Constraints                  | Description                        |
|------------|---------------|------------------------------|------------------------------------|
| `id`      | `int(11)`     | Primary Key, Auto-Increment  | Unique identifier for the record   |
| `hash`    | `varchar(50)` | NOT NULL                     | Hash value representing the entry  |
| `thetime` | `datetime`    | NOT NULL                     | Timestamp of the NBD event         |

---

## Relationships

- **`pba_arp`** and **`pba_arp_raw`**:
  - Both tables use a `hash` field to link summarized and raw ARP data.

- **`pba_arp_summary`**:
  - Aggregates data from **`pba_arp`** based on `src_mac` and `src_ip`.

---

## Notes

- **Encoding**: All tables use UTF-8 encoding with `utf8_unicode_ci` collation.
- **Engine**: The tables use the **InnoDB** engine, which supports transactions and foreign key constraints.
- **Timestamps**: Fields like `first_timestamp` and `timestamp` use default values for automatic time recording.

This data model supports efficient storage and retrieval of network-related data, facilitating logging, analysis, and summary operations within the **pypbald** application.
