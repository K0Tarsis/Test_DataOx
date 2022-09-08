# Test_DataOx
The goal was to parse the data from this page "https://www.kijiji.ca/b-apartments-condos/city-of-toronto/c37l1700273".
The data was saved to Postgresql using peewee. Also, using pygsheets, it is saved in Google Sheets.
All dependencies are recorded in the requirements.txt file. To install use comand "pip install -r requirements.txt" in your virtual environment.

Launching occurs through a file pars.py, to prevent ban, pagination occurs with a certain interval and sequentially.
The database connection parameters are stored in the models.py, settings for connection to the google sheets in the pygsheet.py file

Data stored: Title, Picture url, City, Beds, Description, Price and currency is separated, Date.
