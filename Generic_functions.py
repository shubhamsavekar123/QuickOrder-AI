import re

def get_session_id(session_id:str):
    match = re.search(r"/sessions/(.*?)/contexts", session_id)
    if match:
        return match.group(1)

    return ""

def get_order_str(food_item:dict):
    return ", ".join([f"{int(value)} {key}" for key, value in food_item.items()])