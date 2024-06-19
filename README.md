# WebScraper

WebScraper is a Python-based web scraping tool designed to extract temperature data from a specified website. The script uses Selenium for browser automation to navigate through the website, select options, and collect temperature data for various districts over a specified range of years and months.

## Features

- Automated browser control using Selenium.
- Extraction of temperature data for different districts, months, and years.
- Option to select country, district, and date range interactively.
- Saves the scraped data into an Excel file.

## Requirements

- Python 3.7 or higher
- Google Chrome browser
- ChromeDriver corresponding to your Chrome version
- Selenium
- Pandas

## Installation

1. **Clone the repository:**

    ```bash
    git clone https://github.com/yourusername/webscraper.git
    cd webscraper
    ```

2. **Install the required Python packages:**

    ```bash
    pip install -r requirements.txt
    ```

3. **Download and set up ChromeDriver:**

    - Download ChromeDriver from [here](https://sites.google.com/a/chromium.org/chromedriver/downloads).
    - Ensure the `chromedriver.exe` is placed in the project directory or specify its path in the script.

## Usage

1. **Run the script:**

    ```bash
    python webscraper.py
    ```

2. **Follow the prompts:**

    - The script will prompt you to select a country from a displayed list.
    - Enter the start and end years for the data you want to scrape (between 1997 and 2024).
    - The script will then automatically navigate through the website, select the necessary options, and scrape the temperature data.

3. **Output:**

    - The scraped data will be saved in an Excel file named `temperature_data.xlsx` in the project directory.

## Code Structure

- `WebScraper`: The main class that handles all the web scraping operations.
    - `__init__(self, url)`: Initializes the WebScraper instance with the given URL and sets up the Selenium WebDriver.
    - `get_country(self)`: Retrieves the list of countries from the website.
    - `show_client_message_get_id(self)`: Displays the country list and prompts the user to select a country.
    - `get_districts(self)`: Retrieves the list of districts for the selected country.
    - `get_month(self)`: Retrieves the list of months.
    - `get_year(self)`: Prompts the user to input the start and end years for data collection.
    - `get_temperature(self)`: Scrapes temperature data for the selected districts, years, and months.
    - `save_info(self)`: Saves the collected data into an Excel file.
    - `close_browser(self)`: Closes the Selenium WebDriver.
    - `main()`: The main function to execute the web scraping process.

## Contributing

If you wish to contribute to this project, please follow these steps:

1. Fork the repository.
2. Create a new branch for your feature or bug fix.
3. Commit your changes and push to the new branch.
4. Create a pull request describing your changes.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Contact

For any questions or suggestions, feel free to open an issue or contact the repository owner.

---

*Note: Ensure you comply with the website's terms of service and robots.txt file before scraping data.*
