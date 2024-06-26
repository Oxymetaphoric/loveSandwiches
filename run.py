

import gspread
from google.oauth2.service_account import Credentials
from pprint import pprint

SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
    ]

CREDS = Credentials.from_service_account_file('creds.json')
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open('love_sandwiches')

sales = SHEET.worksheet('sales')

data = sales.get_all_values()


def get_sales_data():
    while True:
        print("please enter sales data from the last market: ")
        print("Data should be six numbers, seperated by commas.")
        print("Example: 10,20,30,40,50,60")
              
    
        data_str = input("Enter your data here: ")
        sales_data = data_str.split(",")
        if validate_data(sales_data):
            print("Data is valid!")
            break
    
    return sales_data

def validate_data(values):
    try:
        [int(value) for value in values] 
        if len(values) != 6:
            raise ValueError(
                f'exactly 6 values required, you provided {len(values)}'
            )
    except ValueError as e:
        print(f"Invalid data: {e}, please try again.\n")
        return False

    return True

def update_worksheet(sheet, data):
    worksheet = SHEET.worksheet(sheet)
    print(f"Updating {worksheet.title}...\n")
    worksheet.append_row(data)
    print(f"{worksheet.title} worksheet updated successfully!\n")

def calculate_surplus_data(sales_row):
    print("Calculating surplus data...\n")
    stock = SHEET.worksheet("stock").get_all_values()
    stock_row = stock[-1]

    surplus_data = []
    for stock, sales in zip(stock_row, sales_row):
        surplus = int(stock) - sales
        surplus_data.append(surplus)

    return surplus_data

def get_last_five_sales():
    sales = SHEET.worksheet("sales")
    columns = []
    for ind in range(1,7):
        column = sales.col_values(ind)
        columns.append(column[-5:])
    
    return columns

def calculate_stock_data(data):
    print("Calculating stock data...\n")
    new_stock_data = []
    
    for column in data: 
        int_column = [int(num) for num in column]
        average = sum(int_column)/len(int_column)
        stock_num = average * 1.1
        
        new_stock_data.append(int(stock_num))

    return new_stock_data
        
def get_stock_values():

    pass
    return dictionary

def main():
    data = get_sales_data()
    sales_data = [int(num) for num in data]
    update_worksheet("sales", sales_data)
    surplus_data = calculate_surplus_data(sales_data)
    update_worksheet("surplus", surplus_data)
    sales_columns = get_last_five_sales()
    stock_data = calculate_stock_data(sales_columns)
    update_worksheet("stock", stock_data)

print("Welcome to Love sandwiches Data Automation")
main()
