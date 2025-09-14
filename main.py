from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
import db_helper

app = FastAPI()

@app.get("/") # GET request to root URL
async def root():
    return {"message": "Hello World"}


@app.post("/")
async def handle_request(request: Request):
    # Retrieve the JSON data from the request
    payload = await request.json()

    # Extract the necessary information from the payload
    # based on the structure of the WebhookRequest from Dialogflow
    intent = payload['queryResult']['intent']['displayName']
    parameters = payload['queryResult']['parameters']
    output_contexts = payload['queryResult']['outputContexts']
    # session_id = generic_helper.extract_session_id(output_contexts[0]["name"])

    # intent_handler_dict = {
    #     'order.add - context: ongoing-order': add_to_order,
    #     'order.remove - context: ongoing-order': remove_from_order,
    #     'order.complete - context: ongoing-order': complete_order,
    #     'track.order - context: ongoing-tracking': track_order
    # }

    if intent == "track.order - context: ongoing-tracking":
        return track_order(parameters)

    # return intent_handler_dict[intent](parameters, session_id)

def track_order(parameters: dict):

    order_id = parameters['order_id']

    order_status = db_helper.get_order_status(order_id)

    if order_status:
        fulfillment_text = f"The order status for order id: {order_id} is: {order_status}"
    else:
        fulfillment_text = f"No order found with order id: {order_id}"

    return JSONResponse(content={
        "fulfillmentText": fulfillment_text

    })
# venv\Scripts\activate
#  uvicorn main:app --reload
