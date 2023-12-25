# URL Marshall

## Overview

The **URL Marshall** script takes a list of URLs as input, parses them, and generates a list of unique endpoint URLs by progressively removing path components from each original URL.

### Prerequisites

Make sure you have Python installed on your system.

### Installation

No specific installation is required.

### How to Run

1. Install Pip Package
    ```bash
   pip install url_marshall
    ```

2. Run the script with the required arguments:

    ```bash
   urlmarshal -l path/to/input.txt -o path/to/output.txt
    ```
 - `-l` or `--list`: Path to the input file containing a list of URLs.
 - `-o` or `--output`: Path to the output file where the unique endpoint URLs will be stored.
    
       
### Using in programs
```python 
from url_marshall import url_marshall
input_file = "path/to/input.txt"
output_file = "path/to/output.txt"

url_marshall(input_file, output_file)
```




    

