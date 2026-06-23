import mysql.connector
global cnx



cnx = mysql.connector.connect(
    host="localhost",
    user="root",
    password = "Shubh@m123",
    database="pandeyji_eatery"
)


def get_order_id():
    cursor = cnx.cursor()
    query = "select max(order_id) from orders"
    cursor.execute(query)
    result = cursor.fetchone()[0]
    cursor.close()

    if result is None:
        return 1
    else:
        return result+1

def insert_order_item(food_item, quantity, order_id):
    try:
        cursor = cnx.cursor()

        # Calling the stored procedure
        cursor.callproc('insert_order_item', (food_item, quantity, order_id))

        # Committing the changes
        cnx.commit()

        # Closing the cursor
        cursor.close()

        print("Order item inserted successfully!")

        return 1

    except mysql.connector.Error as err:
        print(f"Error inserting order item: {err}")

        # Rollback changes if necessary
        cnx.rollback()

        return -1

    except Exception as e:
        print(f"An error occurred: {e}")
        # Rollback changes if necessary
        cnx.rollback()

        return -1


def get_total_order_price(order_id):
    cursor = cnx.cursor()
    query = f"select get_total_order_price({order_id})"
    cursor.execute(query)
    result = cursor.fetchone()[0]
    cursor.close()
    return result


def insert_order_tracking(order_id,status):
    cursor = cnx.cursor()
    insert_query = "insert into order_tracking (order_id,status) values (%s,%s)"
    cursor.execute(insert_query,(order_id,status))
    cnx.commit()
    cursor.close()


def get_order_status(order_id:int):
    if not cnx.is_connected():
        cnx.reconnect()

    cursor = cnx.cursor()

    query = "SELECT status FROM order_tracking WHERE order_id = %s"
    cursor.execute(query,(order_id,))

    result = cursor.fetchone()

    cursor.close()
    # cnx.close()

    if result:
        return result[0]
    else:
        return None


