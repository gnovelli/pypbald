# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

pypbald is a Python 2.7 network analysis tool that captures and analyzes ARP (Address Resolution Protocol) and NBD (Network Block Device) packets. The application uses a Singleton pattern for configuration management and includes database storage for both detailed and raw packet data.

## Common Development Commands

**Run the application:**
```bash
cd trunk/src
python main.py
```

**Build executable (Windows):**
```bash
cd trunk
./build.bat
# Or manually: cd src && python setup.py py2exe
```

**Generate documentation:**
```bash
cd trunk
./doc.bat
# Or manually: python c:\Python25\Scripts\pydoctor --add-package src
```

**Database setup:**
```bash
mysql -u username -p database_name < trunk/schema/pba.sql
```

## Architecture

**Core Components (Singleton Pattern):**
- `PBA` (trunk/src/PBA.py): Main orchestrator class that inherits from PBASingleton
- `PBASingleton` (trunk/src/pypbald/PBASingleton.py): Singleton pattern implementation

**Key Modules:**
- `backend/`: Database operations and storage (local/remote MySQL)
- `sniffing/`: Network packet capture using filters 
- `parsing/`: Packet parsing and analysis
- `logging/`: Application logging
- `records/`: Data structures for ARP and NBDS records

**Data Flow:**
1. PBA reads configuration from `trunk/pypbald.config`
2. Initializes backend (databases), logger, parser, and sniffer
3. Sniffer captures packets using configurable filters
4. Parser processes packets into structured records
5. Backend stores both summary and raw data in MySQL tables

## Configuration

**Main config file:** `trunk/pypbald.config`
- Global settings: debug mode, packet filters, log filename
- Local database: MySQL connection details, storage options
- Remote database: Optional remote MySQL storage

**Important settings:**
- `filter`: Network packet filter (e.g., "broadcast and ((udp and src port 138) or arp)")
- `detail`/`raw`: Control what data gets stored in databases

## Database Schema

**Core tables (see DATA_MODEL.md):**
- `pba_arp`: Summarized ARP data with timestamps and counts
- `pba_arp_raw`: Raw ARP packet data
- `pba_arp_summary`: Aggregated ARP statistics
- `pba_nbds`: Network Block Device records

**Key fields:**
- All tables use `hash` fields for linking related data
- Automatic timestamp tracking with `first_timestamp`/`last_timestamp`
- Count fields track packet frequency

## Working Directory

Always work from `trunk/src/` when running Python commands. The configuration file is read relative to this location (`../pypbald.config`).