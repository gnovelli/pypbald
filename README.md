# pypbald

**pypbald** is a Python application designed for managing network configurations and handling backend, parsing, logging, and sniffing tasks using the Singleton pattern.

## Table of Contents

- [Requirements](#requirements)
- [Installation](#installation)
- [Usage](#usage)
- [Project Structure](#project-structure)
- [Configuration](#configuration)
- [Database](#database)
- [Useful Scripts](#useful-scripts)
- [Author](#author)
- [License](#license)

---

## Requirements

- **Python 2.7** (the project may require updates to work with Python 3)
- Required modules:
  - `ConfigParser`
  - Custom modules included in the project (`PBABackend`, `PBALogger`, `PBAParser`, `PBASniffer`)

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/gnovelli/pypbald.git
   cd pypbald/trunk/src
   ```

2. Install the package using `setup.py`:

   ```bash
   python setup.py install
   ```

## Usage

Run the application using the `main.py` script:

```bash
python main.py
```

The application uses the `pypbald.config` configuration file located in the `trunk` folder.

## Project Structure

The repository structure is organized as follows:

```
pypbald/
│
└── trunk/
    ├── build.bat              # Build script (Windows)
    ├── doc.bat                # Documentation generation script (Windows)
    ├── nbproject/             # NetBeans configuration folder
    ├── pypbald.config         # Main configuration file
    ├── run.bat                # Script to run the application (Windows)
    ├── schema/
    │   └── pba.sql            # SQL script for database creation
    └── src/
        ├── pypbald/
        │   ├── backend/       # Backend-related classes
        │   ├── logging/       # Logging-related classes
        │   ├── parsing/       # Parsing-related classes
        │   ├── records/       # Record management classes
        │   ├── sniffing/      # Sniffing-related classes
        │   ├── PBASingleton.py  # Singleton pattern implementation
        │   └── __init__.py    # Module initialization file
        │
        ├── PBA.py             # Main PBA class for configuration management
        ├── __init__.py        # Module initialization file
        ├── main.py            # Main entry point of the application
        └── setup.py           # Package installation script
```

### Description of Folders and Files

- **`src/pypbald/`**: Contains core components for the project:
  - **`backend/`**: Manages backend operations and database interactions.
  - **`logging/`**: Handles logging functionality.
  - **`parsing/`**: Contains parsing classes for processing input data.
  - **`records/`**: Manages record-keeping functionalities.
  - **`sniffing/`**: Handles network sniffing tasks.
  - **`PBASingleton.py`**: Implements the Singleton pattern for shared configurations.
  - **`__init__.py`**: Initializes the `pypbald` module.

- **`pypbald.config`**: Configuration file for setting logging, database, and filters.

- **Batch Scripts**:
  - **`build.bat`**: Script for building the project.
  - **`doc.bat`**: Script for generating documentation.
  - **`run.bat`**: Script for running the program.

- **`schema/`**:
- **`pba.sql`**: [SQL script to create the database structure used by the application](DATA_MODEL.md).

## Configuration

The `pypbald.config` file contains the main settings. Example configuration:

```ini
[global]
debug = true
filter = some_filter
log_filename = pypbald.log

[localdb]
username = user
password = pass
database = localdb
detail = true
raw = false
```

## Database

The `schema/pba.sql` file contains the database schema used by **pypbald**. Example command to create the database:

```bash
mysql -u username -p database_name < schema/pba.sql
```

## Useful Scripts

- **Build the Project**:

  ```bash
  ./build.bat
  ```

- **Generate Documentation**:

  ```bash
  ./doc.bat
  ```

- **Run the Application**:

  ```bash
  ./run.bat
  ```

## Author

**Giovanni Novelli, Ph.D.**  
Email: [giovanni.novelli@gmail.com](mailto:giovanni.novelli@gmail.com)

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.

---

If you need further information or encounter any issues, feel free to open an **Issue** on [GitHub Issues](https://github.com/gnovelli/pypbald/issues).
