# Finance-Assistant

## Overview

SmartInvest Assistant is an advanced AI-driven financial analysis platform built using OpenAI's Generative AI. It enhances traditional language models by integrating real-time financial APIs, retrieval-augmented generation (RAG) from curated datasets.

## Key Functionalities

* **Real-Time Financial Metrics:** Integrates Polygon.io API for up-to-date stock and financial data retrieval.
* **Retrieval-Augmented Generation (RAG):** Utilizes a curated Fortune 500 dataset to provide accurate and context-specific responses.


## Technical Details

### Core Components

* **File Search (RAG):** Efficiently accesses the 2024 Fortune 500 PDF for accurate company information.
* **Function Calling:** Employs Polygon.io API calls dynamically for various financial metrics such as revenue, profit margins, and stock prices.

### Tech Stack

* Python 3.8+
* OpenAI Assistants API
* Polygon.io API
* Jupyter Notebooks

## Installation

### Prerequisites

* Python 3.8 or newer
* API keys from OpenAI and Polygon.io

### Setup Instructions

```bash
git clone [your-repository-url]
cd SmartInvest
pip install -r requirements.txt
```

### Running the Assistant

1. Configure your `.env` file with your API keys.
2. Start Jupyter Notebook:

```bash
jupyter notebook Assistant_V13.ipynb
```

## Project Structure

```
SmartInvest/
├── data/
│   └── fortune500_2024.pdf
├── Assistant_V13.ipynb  # Main notebook containing assistant logic
├── requirements.txt     # Python dependencies
└── README.md
```

## Usage Examples

* **Revenue Comparison:** "Compare 2024 revenue between Apple and Microsoft."
* **Stock Quality Analysis:** "Evaluate Apple's stock using recent financial metrics."

## Contributions

Contributions and suggestions are welcome. Please create pull requests or issues as necessary.

## Acknowledgements

* OpenAI API
* Polygon.io API
* Fortune 500 data source
  
<img width="635" alt="Screenshot 2025-05-25 at 12 41 12" src="https://github.com/user-attachments/assets/aa5b9660-5c05-471c-a52c-cce68a78e3ff" />


