# BHTOM-scripts

This project automates the process of preparing, filtering and uploading astronomical data from ROTUZ to the BHTOM system.

## How it works

The core logic is handled by `main.py`. You pass the path to a folder containing the data you want to process. The script then performs the following operations:

1. **Unpacking**  
   All `.gz` files in the specified directory are automatically unzipped [`unzip_files.sh`].

2. **File Processing**  
   Each file is processed individually:
   - The script checks whether any astronomical objects are detected in the image ['stars_detection.py'].
   - The photometric filter is extracted from the filename ['filter.py'].
   - A log entry is created, including a timestamp, object name, filename and detection status ['logs.py'].

3. **Uploading to BHTOM**  
   If the file contains detectable objects, it is sent to the BHTOM system via the API ['upload_files.py'].
