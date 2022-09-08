import pygsheets
path = 'golden-toolbox-361815-e80359fa3e91.json'

gc = pygsheets.authorize(service_account_file=path)
#gc.create('apartments')
sh = gc.open('apartments')
wk1 = sh.sheet1
wk1.clear()
wk1.insert_rows(0, number=1, values=['Title', 'Pict_url', 'City', 'Beds', 'Description', 'Price', 'Currency', 'Date'])

def write_google_sheet(values):
    cells = wk1.get_all_values(include_tailing_empty_rows=False, include_tailing_empty=False, returnas='matrix')
    last_row = len(cells)
    wk1.insert_rows(last_row, number=1, values=values)



