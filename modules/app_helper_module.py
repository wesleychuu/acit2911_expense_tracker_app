from modules.expense_module import *

def data_to_dict(data_tup: tuple) -> dict:
    return {
        "name": data_tup[2],
        "date": data_tup[3],
        "category": data_tup[4],
        "amount": data_tup[5],
        "eid": data_tup[0],
    }

def get_pie_data(conn, uid: int) -> dict:
    categories = get_user_categories(conn, uid)
   
    total_category_exp = []
    for cat in categories:
        total_category_exp.append(
            get_total_expenses_by_category(conn, uid, cat)
        )
    
    pie_data = {"Category": "Amount"}
    for i, cat in enumerate(categories):
        pie_data[cat] = total_category_exp[i]
        
    return pie_data


def check_session(uid:int) -> bool:
    logged_in = False

    if uid:
        logged_in = True

    return logged_in