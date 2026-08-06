# N100 Financial Intelligence

This project is a Streamlit application designed for financial analysis and stock screening. It provides users with various tools to analyze stocks, view financial trends, and access reports.

## Project Structure

```
N100-Financial-Intelligence
├── src
│   ├── dashboard
│   │   ├── app.py                # Main entry point for the Streamlit application
│   │   └── pages
│   │       ├── home.py           # Home page of the application
│   │       ├── profile.py        # User profile page
│   │       ├── screener.py       # Stock screener functionality
│   │       ├── peers.py          # Peers page
│   │       ├── trends.py         # Trends page
│   │       ├── sectors.py        # Sectors page
│   │       ├── capital.py        # Capital page
│   │       └── reports.py        # Reports page
│   └── utils
│       └── db.py                 # SQL helper functions for database interaction
├── requirements.txt               # Project dependencies
└── README.md                      # Project documentation
```

## Installation

To run this project, you need to have Python installed on your machine. You can install the required dependencies using pip:

```bash
pip install -r requirements.txt
```

## Running the Application

To start the Streamlit application, use the following command:

```bash
streamlit run src/dashboard/app.py
```

## Features

- **Stock Screener**: Filter stocks based on various financial metrics such as ROE, Debt/Equity ratio, and Net Profit Margin.
- **User Profile**: View and manage user-specific information.
- **Financial Trends**: Analyze trends in financial data over time.
- **Sector Analysis**: Explore different sectors and their performance.
- **Capital Management**: Tools for managing capital investments.
- **Reports**: Generate and view financial reports.

## Contributing

Contributions are welcome! Please feel free to submit a pull request or open an issue for any suggestions or improvements.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.