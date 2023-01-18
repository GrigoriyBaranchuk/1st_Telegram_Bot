import json


def open_json():
    """
    return json format of our database list of dicts
    """
    with open('db.json', mode='r') as f:
        return json.load(f)


def add_user_to_db(dct: dict):
    """
    add users instance in our database db.json
     pk = message.from_user.id
     spreadsheetID = id of google sheet
     first_name = message.from_user.first_name
     """
    db = open_json()
    db.append(dct)
    with open('db.json', mode='w') as f:
        json.dump(db, f, indent=4)


def user_spreadsheetId(message):
    """return unique id of google sheet of user with exact id = user_id"""
    user_id = str(message.from_user.id)
    db = open_json()
    for inst in db:
        if user_id == inst["pk"]:
            return inst["spreadsheetId"]


