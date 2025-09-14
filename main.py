from fastapi import FastAPI, Request

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
    session_id = generic_helper.extract_session_id(output_contexts[0]["name"])

    intent_handler_dict = {
        'order.add - context: ongoing-order': add_to_order,
        'order.remove - context: ongoing-order': remove_from_order,
        'order.complete - context: ongoing-order': complete_order,
        'track.order - context: ongoing-tracking': track_order
    }

    if intent == "track order - context: ongoing-tracking":
        return JSONResponse(content={
            "fulfillmentText": f"Received =={intent}== in the backend"
        }

    return intent_handler_dict[intent](parameters, session_id)

# venv\Scripts\activate
#  uvicorn main:app --reload
# tunnel pass:92.40.212.121