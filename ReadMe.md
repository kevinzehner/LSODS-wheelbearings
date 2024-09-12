# CV Boots Catalogue Application

## Overview

This project is a Wheelbearing Catalogue Application developed using Python and Pyside. The application is designed to aid a company during an exhibition in Germany. It allows staff to confirm the availability of parts based on specific vehicle data provided by customers. The application uses a series of dropdowns to filter available parts and displays relevant information in an organized manner.

## Features

- **Dropdown Menus**: Users can select vehicle manufacturer, model, engine size, mark series, drive type, position, and transmission to filter available parts.
- **Search Functionality**: Based on the selected criteria, the application searches the database for available parts and displays them.
- **Image Display**: Most parts have an image of a diagram included, although it is missing on some. 
- **Results Layout**: Results are displayed in a grid layout, with each part's size and number presented.

## Installation

### Prerequisites

- Python 3.12
- PyQt5
- SQLite3

### Setting Up the Environment

1. **Clone the Repository:**

   ```sh
   git clone https://github.com/kevinzehner/python-boot-catalogue.git
   cd python-boot-catalogue
   ```

2. **Create a Virtual Environment:**

   ```sh
   python3 -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
   ```

3. **Install Dependencies:**

   ```sh
   pip install -r requirements.txt
   ```

4. **Set Up the Database:**
   Ensure that the `boots.db` database file is in the root directory of the project.

5. **Create Indexes for Faster Search:**
   ```sh
   python -c "from create_indexes import create_indexes; create_indexes('boots.db')"
   ```

## Running the Application

1. **Run the Application:**
   ```sh
   python main.py
   ```
   The application window will open, displaying the dropdown menus for selecting the vehicle data.

## Usage

1. **Select Vehicle Data:** Use the dropdown menus to select the vehicle manufacturer, model, engine size, mark series, drive type, position, and transmission.
2. **Search for Parts:** Click the "Search" button to find available parts based on the selected criteria.
3. **View Results:** The results will be displayed in a grid layout, showing part numbers, sizes, and images.

## Known Issues

- Ensure the database file `boots.db` is present in the root directory of the application.
- If the application is slow, verify that the indexes have been created on the database.
- attempted to package the application using PyInstaller but was unable to open the packaged application. This issue is still unresolved.

## Contributing

1. Fork the repository.
2. Create a new branch (`git checkout -b feature-branch`).
3. Commit your changes (`git commit -am 'Add new feature'`).
4. Push to the branch (`git push origin feature-branch`).
5. Create a new Pull Request.

## License

This project is licensed under the MIT License. See the LICENSE file for details.

If you have any questions or need further assistance, please contact Kevin Zehner.
