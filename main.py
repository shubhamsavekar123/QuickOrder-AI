
from fastapi import FastAPI
from fastapi import Request
from fastapi.responses import JSONResponse
from starlette import status
import db
import Generic_functions

app = FastAPI()

inprogress_orders = {}
@app.post("/")



async def handle_request(request: Request):
    payload = await request.json()

    intent = payload["queryResult"]["intent"]["displayName"]
    parameters = payload["queryResult"]["parameters"]
    output_contexts = payload["queryResult"]["outputContexts"]
    session_id = Generic_functions.get_session_id(output_contexts[0]['name'])

    if intent == "track.order-context":
        return track_order(parameters,session_id)
    elif intent == "order.complete":
        return complete_order(parameters,session_id)
    elif intent == "order.add":
        return add_order(parameters,session_id)
    elif intent == "order.remove":
        return remove_order(parameters,session_id)
    else:
        return None






def add_order(parameters:dict,session_id):
    food_item = parameters["Food-item"]
    number = parameters["number"]

    if len(food_item) != len(number):
        fulfillment_text = f"Please specify the exactly number of food items"
    else:
        new_food_dict = dict(zip(food_item, number))

        if session_id not in inprogress_orders:
            inprogress_orders[session_id] = new_food_dict
        else:
            current_food_dict = inprogress_orders[session_id]
            current_food_dict.update(new_food_dict)
            inprogress_orders[session_id] = current_food_dict

        order_str = Generic_functions.get_order_str(inprogress_orders[session_id])
        fulfillment_text = f"So far you have {order_str}. Do you want to add more food?"
    return JSONResponse(content={
        "fulfillmentText": fulfillment_text
    })

def track_order(parameters:dict,session_id):
    order_id = int(parameters["number"][0])
    order_status = db.get_order_status(order_id)
    if order_status:
        fulfillment_text = f"The order status of {order_id} is : {order_status}"
    else:
        fulfillment_text = f"The order status of {order_id} is : Not found"
    return JSONResponse(content={
        "fulfillmentText": fulfillment_text
    })

def remove_order(parameters:dict,session_id):
    if session_id not in inprogress_orders:
        return JSONResponse(content={
            "fulfillmentText" : f"I am having some trouble in finding your order.Sorry! please place a new order"
        })
    else:
        current_items = inprogress_orders[session_id]
        food_item = parameters["food-item"]

        removed_items = []
        no_removed_items = []

        for item in food_item:
            if item not in current_items:
                no_removed_items.append(item)
            else:
                removed_items.append(item)
                del current_items[item]


        if len(removed_items) > 0:
            fulfillment_text = f"Removed {",".join(removed_items)} from your order"
        if len(no_removed_items) > 0:
            fulfillment_text = f"Your current order does not have {",".join(no_removed_items)} food items "

        if len(current_items.keys()) == 0:
            fulfillment_text += f"Your order is empty!"
        else:
            order_str = Generic_functions.get_order_str(current_items)
            fulfillment_text += f"Here is what left in your order: {order_str}"

    return JSONResponse(content={
        "fulfillmentText": fulfillment_text
    })

def complete_order(parameters:dict,session_id):
    if session_id not in inprogress_orders:
        fulfillment_text = f"I am having some trouble in placing your order.Sorry! but please place a new order"
    else:
        order = inprogress_orders[session_id]
        order_id = save_to_db(order)

        if order_id == -1:
            fulfillment_text = f"Sorry, I couldn't process your order due to a backend error. "\
                                f"Please try again later."
        else:
            order_total = db.get_total_order_price(order_id)
            fulfillment_text = f"Awesome. We have placed your order. " \
                               f"Here is your order id {order_id} and total order price is {order_total}"
        del inprogress_orders[session_id]
    return JSONResponse(content={
        "fulfillmentText": fulfillment_text
    })


def save_to_db(order:dict):
    order_id = db.get_order_id()
    for food_item,quantity in order.items():
        rcode = db.insert_order_item(
            food_item,
            quantity,
            order_id
        )
        if rcode == -1:
            return -1
    db.insert_order_tracking(order_id,"in progress")

    return order_id
