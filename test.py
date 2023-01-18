# import gspread
#
# gs = gspread.service_account()
# sh = gs.open_by_key("1VSgq2V8Y733EcuFLZE_hNeIZlPeIdYmg3iMYY9fvVAI")
#
# worksheet = sh.get_worksheet(0)
# worksheet.update('A2:L2', [['Встал', 'Встал', 'Встал', 'Встал', 'Встал']])
# print(worksheet.get('1:1'))
#
# cell = worksheet.find("Встал")
# print(cell.__dict__)
#
#
#
# sh = gs.create('My_test')
# sh.share('baranchukoff@gmail.com', perm_type='user', role='writer')
# import pdb
# pdb.set_trace()
# worksheet = sh.get_worksheet(0)
# worksheet.update_cell(1, 2, 'Bingo!')


from logic import now_time
from time import sleep

a = now_time()
print(a)
sleep(60)
b = now_time()
print(b)
print(b < a)



