import sys
import re
import pandas as pd
import warnings

# Function definitions
def reshuffler(messed_up_date):
    date_pattern = re.compile(r'([0-9]{1,2})/([0-9]{1,2})/([0-9]{4})')
    month, day, year = date_pattern.search(messed_up_date).group(1, 2, 3)
    if len(month) == 1:
        month = '0' + month
    if len(day) == 1:
        day = '0' + day
    return '-'.join([year, month, day])

if __name__ == '__main__':

    html_file = sys.argv[1]
    filename = html_file[:-5]

    # Read table into memory, rely on pandas magic
    origin = pd.read_html(html_file)

    # Unpack table from list
    table = origin[0]

    # Select columns of interest
    keep_cols = ['State', 'Branching Restrictivness Index', 'Effective Date']
    target = table[keep_cols]

    # Reshuffle format of date column (keeping them as strings)
    dates_origin = target['Effective Date'].to_list()
    with warnings.catch_warnings():
        warnings.simplefilter('ignore')
        target.loc[:, 'Effective Date'] = list(map(reshuffler, dates_origin))

    # Dump result to a CSV file
    target.to_csv('./' + filename + '.csv', index=False)
