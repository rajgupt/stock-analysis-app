# Stock Analysis App

This is a Streamlit application for analyzing stock market data. The application connects to an SQLite database to retrieve and display market trends and prices.

## Project Structure

- `src/app.py`: Main entry point of the Streamlit application.
- `src/data/market_data.db`: SQLite database containing market data.
- `src/utils/database.py`: Functions for connecting to the database and querying data.
- `src/components/charts.py`: Functions for creating visualizations of the data.
- `requirements.txt`: Lists the dependencies required for the project.
- `.gitignore`: Specifies files and directories to be ignored by Git.

## Setup Instructions

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd stock-analysis-app
   ```

2. Install the required packages:
   ```bash
   pip install -r requirements.txt
   ```

3. Run the Streamlit app:
   ```bash
   streamlit run src/app.py
   ```

4. Open your web browser and navigate to `http://localhost:8501` to view the application.

## License

This project is licensed under the MIT License.