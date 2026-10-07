from fastapi import FastAPI
from exception import (
    PinCodeNotFoundError,
    InvalidPinCodeError,
    pincode_not_found_handler,
    invalid_pincode_handler
)
from data import pincode_data
from models import (
    PincodeRequest,
    BulkPincodeRequests,
    LocationResponse,
    BulkRequestResponse
)

app = FastAPI(
    title="Pin Code Lookup API",
    description="Auto-fill the city and state of Indian Pincode during checkout"
)

# Register your custom exception handler
app.add_exception_handler(PinCodeNotFoundError,pincode_not_found_handler)
app.add_exception_handler(InvalidPinCodeError,invalid_pincode_handler)

@app.get("/")
def root():
    return {
        "Message":"Pincode Lookup"
    }

@app.get("/pincode/{id}",response_model=LocationResponse)
def lookup_pincode(id:str):
    if(len(id) != 6 or not id.isdigit()):
        raise InvalidPinCodeError(id,"Pincode must be exactly 6 digits")

    if id not in pincode_data:
        raise PinCodeNotFoundError(id)

    return pincode_data[id]

@app.post("/pincode/bulk",response_model=BulkRequestResponse)
def bulk_lookup(request:BulkPincodeRequests):
    res = []
    missing = []

    for code in request.pincodes:
        if(code in pincode_data):
            res.append(pincode_data[code])
        else:
            missing.append(code)

    return BulkRequestResponse(
        status="Success",
        found=len(res),
        not_found=len(missing),
        result=res,
        missing=missing
    )