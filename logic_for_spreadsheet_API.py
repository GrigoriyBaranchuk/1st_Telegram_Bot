import gspread
"""'turnkey-aleph-372212-94f79b4408eb.json'"""


def create_table(name: str) -> str:
    """create table for new user with name = message.from_user.first_name
    return an unique spreadsheet id for Google table """
    gs = gspread.service_account()
    sh = gs.create(name)
    sh.share('baranchukoff@gmail.com', perm_type='user', role='writer')
    worksheet = sh.get_worksheet(0)
    # TODO change 'Проснулся', 'Уснул', to loop with range
    worksheet.update('B1:W1', [['Проснулся', 'Уснул', 'Проснулся', 'Уснул', 'Проснулся', 'Уснул', 'Проснулся', 'Уснул',
                                'Проснулся', 'Уснул', 'Проснулся', 'Уснул', 'Проснулся', 'Уснул']])
    spreadsheetId = sh.id
    return spreadsheetId


def upload_cell(users_table: str, row: int, column: int, data):
    """upload data in users table in first sheet in cell with address(row, column)"""
    gs = gspread.service_account()
    sh = gs.open_by_key(users_table)
    worksheet = sh.get_worksheet(0)
    worksheet.update_cell(row, column, data)


def check_is_full(users_table: str, row: int, column: int) -> bool:
    """if some value in cell empty - return True
    """
    gs = gspread.service_account()
    sh = gs.open_by_key(users_table)
    worksheet = sh.get_worksheet(0)

    if worksheet.cell(row, column).value:
        return True
    else:
        return False


def table(users_table: str):
    """return instance of spreadsheet where users_table - is id of spreadsheet"""
    gs = gspread.service_account()
    sh = gs.open_by_key(users_table)
    return sh




