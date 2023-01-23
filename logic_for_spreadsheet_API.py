import gspread
from logic import now_date



"""'turnkey-aleph-372212-94f79b4408eb.json'"""
path = 'service_account.json'


def create_table(gs, name: str) -> str:
    """create table for new user with name = message.from_user.first_name
    return an unique spreadsheet id for Google table """
    sh = gs.create(name)
    sh.share('baranchukoff@gmail.com', perm_type='user', role='writer')
    worksheet = sh.get_worksheet(0)
    # TODO change 'Проснулся', 'Уснул', to loop with range
    worksheet.update('B1:W1', [['Проснулся', 'Уснул', 'Проснулся', 'Уснул', 'Проснулся', 'Уснул', 'Проснулся', 'Уснул',
                                'Проснулся', 'Уснул', 'Проснулся', 'Уснул', 'Проснулся', 'Уснул']])
    spreadsheetId = sh.id
    return spreadsheetId


def upload_cell(gs, users_table: str, row: int, column: int, data):
    """upload data in users table in first sheet in cell with address(row, column)"""

    sh = gs.open_by_key(users_table)
    worksheet = sh.get_worksheet(0)
    worksheet.update_cell(row, column, data)


def check_is_full(gs, users_table: str, row: int, column: int) -> bool:
    """if some value in cell empty - return True
    """

    sh = gs.open_by_key(users_table)
    worksheet = sh.get_worksheet(0)

    if worksheet.cell(row, column).value:
        return True
    else:
        return False


def table(gs, users_table: str):
    """return instance of spreadsheet where users_table - is id of spreadsheet"""

    sh = gs.open_by_key(users_table)
    return sh


def create_new_day(gs, user_table):
    row = 2
    column = 1
    user_table = table(gs, user_table)
    # worksheet = user_table.get_worksheet(0)

    if now_date() in user_table.get_worksheet(0).col_values(1):
        pass
    else:
        while check_is_full(users_table=user_table.id, row=row, column=column):
            row += 1
        else:
            upload_cell(users_table=user_table.id, row=row, column=column, data=now_date())




