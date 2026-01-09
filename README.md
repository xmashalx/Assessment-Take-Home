# Book Data Processing Pipeline

This project implements a data pipeline for processing raw book data, generating insights, and creating visualizations.

## Pipeline Overview

The pipeline consists of three main stages:

1. **Data Processing**: Raw CSV files from the `data/` folder are cleaned and transformed into a standardized format
2. **Data Analysis**: The processed data is analyzed to generate visual insights saved to the `visuals/` directory
3. **Keyword Extraction**: Key terms are extracted from book titles and visualized

```
data/RAW_DATA_*.csv → process_raw_data.py → data/processed_data.csv
                                                    ↓
                                          analyse_processed_data.py → visuals/*.png
                                                    ↓
                                          get_keywords.py → visuals/keywords_chart.png
```

## Prerequisites

### Installing Python

This project requires Python 3.8 or higher.

**macOS/Linux:**
```bash
# Check if Python is installed
python3 --version

# If not installed, on macOS use Homebrew:
brew install python3


### Installing pip

pip usually comes with Python 3. Verify installation:

```bash
pip3 --version
```

If pip is not installed:
```bash
python3 -m ensurepip --upgrade
```

## Installation

1. Clone or download this repository

2. Navigate to the project directory:
```bash
cd Assessment-Take-Home-main
```

3. Install required dependencies:
```bash
pip3 install -r requirements.txt
```

## Usage

### 1. Process Raw Data

The `process_raw_data.py` script cleans and standardizes raw book data files.

**What it does:**
- Removes unnecessary columns and duplicate index columns
- Drops rows with missing book titles or authors
- Reformats rating values (converts European decimal format to standard)
- Cleans the ratings column (removes backticks)
- Converts data types to appropriate formats
- Merges author information from the `authors.db` database
- Renames columns to standardized names
- Outputs cleaned data to `data/processed_data.csv`

**Run the script:**
```bash
python3 process_raw_data.py data/RAW_DATA_X.csv
```

Or with the short flag:
```bash
python3 process_raw_data.py -f data/RAW_DATA_X.csv
```

### 2. Analyze Processed Data

The `analyse_processed_data.py` script generates visual insights from the processed data.

**What it does:**
- Loads `data/processed_data.csv`
- Adds a decade column for temporal analysis
- Creates a pie chart showing the proportion of novels by decade
- Creates a bar chart showing the top 10 most-rated authors
- Creates a line graph of the number of romance novels released over the years
- Saves both charts as PNG files to the `visuals/` directory

**Run the script:**
```bash
python3 analyse_processed_data.py
```

**Output:**
- `visuals/decade_distribution.png` - Pie chart of books by decade
- `visuals/top_authors.png` - Bar chart of top 10 authors by total ratings
- `visuals/release_trends_over_time.png` - line graph of number of books released over the years

### 3. Extract Keywords

The `get_keywords.py` script extracts and visualizes common keywords from book titles.

**What it does:**
- Loads `data/processed_data.csv`
- Extracts keywords from book titles
- Counts keyword frequency
- Creates a bar chart of the most common keywords
- Saves the visualization to the `visuals/` directory

**Run the script:**
```bash
python3 get_keywords.py
```

**Output:**
- `visuals/keywords_chart.png` - Bar chart of top keywords from book titles


## Running Tests

To verify the data processing functions work correctly:

```bash
pytest test_process_raw_data.py
```

Or for verbose output:
```bash
pytest test_process_raw_data.py -v
```

## Dependencies

Key libraries used in this project:
- **pandas**: Data manipulation and analysis
- **altair**: Declarative statistical visualization
- **sqlite3**: Database operations (built-in)
- **pytest**: Testing framework

See `requirements.txt` for the complete list with versions.

## Troubleshooting

**Issue: Database not found**

Ensure the `authors.db` file exists in the project root. If missing you may need to move into the project root.
