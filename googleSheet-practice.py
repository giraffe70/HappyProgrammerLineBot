import gspread
from oauth2client.service_account import ServiceAccountCredentials
scope=['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name('HappyProgrammer.json',scope)

client = gspread.authorize(creds)

LineBotSheet = client.open('happy programmer')
usersSheet = LineBotSheet.worksheet('users')

#寫入
#update_cell(row,col)
usersSheet.update_cell(1, 1, 'Roy')
usersSheet.update_cell(2, 1, 'Audio')

#讀值
print(usersSheet.cell(1,1).value)

#搜尋
cell = usersSheet.find('Audio')
print(cell.row,cell.col)