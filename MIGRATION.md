# Python 3.x Migration Guide

Questa guida fornisce i passaggi dettagliati per migrare pypbald da Python 2.7 a Python 3.x (consigliato: Python 3.9-3.11).

## Analisi Pre-Migrazione

### Problemi Identificati
- ✅ **Complessità BASSA**: Il progetto è ben strutturato e utilizza poche dipendenze
- 📊 **Impatto limitato**: ~25 file Python da aggiornare
- 🔧 **Modifiche principali**: Import, print statements, dictionary methods

### Raccomandazione Python Version
- **Python 3.9**: Stabile, LTS fino ottobre 2025
- **Python 3.10**: Migliori error messages, match-case syntax  
- **Python 3.11**: Performance boost +25%, ottimo per network processing

## Piano di Migrazione

### Fase 1: Preparazione Ambiente

```bash
# 1. Creare branch dedicato
git checkout -b python3-migration

# 2. Backup del branch corrente
git tag python2-backup

# 3. Verificare Python 3.x installato
python3 --version  # Deve essere 3.9+

# 4. Installare tool di migrazione
pip3 install 2to3
```

### Fase 2: Aggiornamento Dependencies

**Prima della migrazione, verificare disponibilità:**

```bash
# Verificare dpkt per Python 3
pip3 install dpkt

# Verificare MySQL connector
pip3 install mysql-connector-python

# Alternative per py2exe
pip3 install pyinstaller
```

### Fase 3: Migrazione Automatica con 2to3

```bash
cd trunk/src

# Backup dei file originali
find . -name "*.py" -exec cp {} {}.py2bak \;

# Eseguire conversione automatica
2to3 -w -n --print-function .

# Verificare i cambiamenti
git diff
```

### Fase 4: Correzioni Manuali Specifiche

#### 4.1 ConfigParser Import

**File: `trunk/src/PBA.py`**
```python
# PRIMA (Python 2)
import ConfigParser

# DOPO (Python 3)
import configparser
```

**Aggiornare anche l'utilizzo:**
```python
# PRIMA
config = ConfigParser.RawConfigParser()

# DOPO  
config = configparser.RawConfigParser()
```

#### 4.2 Dictionary has_key() Method

**Files da modificare:**
- `trunk/src/pypbald/records/PBARecordARPRequest.py:34`
- `trunk/src/pypbald/backend/PBABackend.py:82,94`
- `trunk/src/pypbald/records/PBARecordNBDS.py:34`

```python
# PRIMA (Python 2)
if backend.getsummaryarp().has_key(hash_value):

# DOPO (Python 3)
if hash_value in backend.getsummaryarp():
```

#### 4.3 Print Statements → Print Functions

**Files principali:**
- `trunk/src/pypbald/parsing/PBAParser.py` (molte occorrenze)
- `trunk/src/pypbald/sniffing/PBASniffer.py`
- `trunk/src/pypbald/backend/PBABackend.py`

```python
# PRIMA (Python 2)
print 'listening on %s: %s' % (self._pc.name, self._pc.filter)
print hexlify(udp_packet.data)

# DOPO (Python 3)
print('listening on %s: %s' % (self._pc.name, self._pc.filter))
print(hexlify(udp_packet.data))
```

### Fase 5: Aggiornamento Build System

#### 5.1 Sostituire py2exe con PyInstaller

**File: `trunk/src/setup.py`**

```python
# PRIMA (Python 2 + py2exe)
import os
from distutils.core import setup
from shutil import rmtree

setup(console=['main.py'],
      options = {"py2exe": {"dist_dir": os.path.join("..", "dist")}})
rmtree('build')
```

**DOPO (Python 3 + PyInstaller):**

```python
# Nuovo setup.py per Python 3
from setuptools import setup, find_packages

setup(
    name="pypbald",
    version="2.0.0",
    author="Giovanni Novelli",
    author_email="giovanni.novelli@gmail.com",
    description="Python network analysis tool for ARP and NBD packets",
    packages=find_packages(),
    python_requires=">=3.9",
    install_requires=[
        "dpkt>=1.9.0",
        "mysql-connector-python>=8.0.0",
    ],
    entry_points={
        'console_scripts': [
            'pypbald=main:main',
        ],
    },
)
```

**Nuovo script di build:**

```bash
# Nuovo build.bat (o build.sh per Linux)
#!/bin/bash
cd src
pyinstaller --onefile --console main.py --name pypbald --distpath ../dist
```

#### 5.2 Aggiornamento Documentation

**File: `trunk/doc.bat`**

```bash
# PRIMA
python c:\Python25\Scripts\pydoctor --add-package src

# DOPO (opzioni moderne)
# Opzione 1: pdoc3
pip3 install pdoc3
pdoc3 --html --output-dir ../docs src

# Opzione 2: Sphinx
pip3 install sphinx
sphinx-quickstart docs
```

### Fase 6: Testing e Validazione

#### 6.1 Test di Sintassi

```bash
cd trunk/src
python3 -m py_compile main.py
python3 -m py_compile PBA.py

# Test ricorsivo di tutti i file
find . -name "*.py" -exec python3 -m py_compile {} \;
```

#### 6.2 Test Funzionali

```bash
# 1. Test configurazione
cd trunk/src
python3 -c "from PBA import PBA; pba = PBA(); print('Config OK')"

# 2. Test database connection (se DB disponibile)
python3 -c "
from pypbald.backend.PBABackend import PBABackend
from PBA import PBA
pba = PBA()
backend = PBABackend(pba)
print('Database OK')
"

# 3. Test completo (con permessi admin per network sniffing)
sudo python3 main.py
```

### Fase 7: Aggiornamento Configurazione

**File: `trunk/pypbald.config`**
- ✅ **Nessuna modifica richiesta** - Il formato rimane compatibile

**File: `trunk/schema/pba.sql`**
- ✅ **Nessuna modifica richiesta** - MySQL schema indipendente da Python

### Fase 8: Finalizzazione

```bash
# 1. Rimuovere backup files
find . -name "*.py2bak" -delete

# 2. Aggiornare requirements (creare nuovo file)
echo "dpkt>=1.9.0" > requirements.txt
echo "mysql-connector-python>=8.0.0" >> requirements.txt
echo "pyinstaller>=4.0" >> requirements.txt

# 3. Test finale
python3 main.py --help  # Se implementato
sudo python3 main.py    # Test completo

# 4. Commit delle modifiche
git add .
git commit -m "Migrate to Python 3.x

- Convert ConfigParser to configparser
- Replace has_key() with in operator  
- Convert print statements to functions
- Update build system from py2exe to PyInstaller
- Add Python 3.x requirements.txt

🤖 Generated with Claude Code"
```

## Troubleshooting

### Problemi Comuni

**1. ImportError: No module named 'ConfigParser'**
```bash
# Soluzione: Verificare import corretto
grep -r "ConfigParser" . 
# Deve essere "configparser" (lowercase)
```

**2. dpkt compatibility issues**
```bash
# Soluzione: Aggiornare dpkt
pip3 install --upgrade dpkt>=1.9.0
```

**3. MySQL connection errors**
```bash
# Soluzione: Installare connector Python 3
pip3 uninstall mysql-python  # Rimuovere versione Python 2
pip3 install mysql-connector-python
```

**4. Network permissions**
```bash
# Soluzione: Eseguire con privilegi admin
sudo python3 main.py
# Oppure configurare capabilities
sudo setcap cap_net_raw+ep /usr/bin/python3
```

## Rollback Plan

Se la migrazione presenta problemi:

```bash
# 1. Tornare al branch originale
git checkout master

# 2. Oppure usare il tag di backup
git checkout python2-backup

# 3. Oppure ripristinare file specifici
find . -name "*.py2bak" -exec bash -c 'mv "$1" "${1%.py2bak}"' _ {} \;
```

## Post-Migrazione

### Benefici Ottenuti
- ✅ **Sicurezza**: Supporto security patches attivo
- ✅ **Performance**: Miglioramento prestazioni 15-25%
- ✅ **Maintenance**: Accesso a librerie moderne  
- ✅ **Future-proof**: Supporto garantito fino 2027+ 

### Aggiornamenti Raccomandati
- Considerare async/await per network I/O (future enhancement)
- Migrare a f-strings per string formatting
- Implementare type hints per migliore maintainability
- Aggiungere pytest per testing automatizzato

## Timeline Stimato

- **Preparazione**: 2-4 ore
- **Migrazione automatica**: 1 ora  
- **Correzioni manuali**: 4-6 ore
- **Testing**: 2-4 ore
- **Documentazione**: 1 ora

**Totale: 2-3 giorni lavorativi**