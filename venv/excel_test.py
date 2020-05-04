from openpyxl import Workbook
#
# workbook = Workbook()
# sheet = workbook.active
#
# sheet["A1"] = "hello"
# sheet["B1"] = "world!"
#
# workbook.save(filename="hello_world.xlsx")

# from openpyxl import load_workbook
# workbook = load_workbook(filename="COVID.xlsx")
# print(workbook.sheetnames)
# sheet = workbook.active
#
# print(sheet["C3"].value)

# import pandas lib as pd
import pandas as pd

# only read specific columns from an excel file

# print(dataframe)

# require_cols = [0, 4, 5, 6]
# dataframe1 = pd.read_excel('COVID.xlsx', usecols=require_cols, index=False)
# print(dataframe1)




# dataframe = pd.read_excel('COVID.xlsx')
# print(dataframe)
#
# require_cols = [0, 4, 5, 6]
# dataframe1 = pd.read_excel('COVID.xlsx', usecols=require_cols, index=False)
# print(dataframe1)

dataframe = pd.read_excel('pub_numbers.xlsx')
dataframe.to_csv (r'pubs_numbers.csv', index = False, header=True)

