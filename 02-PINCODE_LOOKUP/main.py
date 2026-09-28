from fastapi import FastAPI
from exceptions import (
    PincodeNotFoundException,
    PincodeInvalidException,
    InvalidPincodeError,
    invalid_pincode_handler,
    pincode_not_found_handler,
)
from models import PincodeRequest, locationResponse, BulkRequest, BulkResponse
from data import get_location_by_pincode, get_locations_by_pincodes

app = FastAPI(
    title="Pincode Lookup API",
    description="A simple API to lookup details of a pincode.",
    version="1.0.0",
)

#register your custom exception handlers
app.add_exception_handler(PincodeNotFoundException, pincode_not_found_handler)
app.add_exception_handler(PincodeInvalidException, invalid_pincode_handler)





@app.get("/")
def read():
    return {"message": "Welcome to the Pincode Lookup API!"}


@app.get("/pincode/{code}", response_model=locationResponse)
def lookup_pincode(code: str):
    # Your implementation here
    if(len(code) != 6 or not code.isdigit()):
        raise InvalidPincodeError(code, "Pincode must be a 6-digit number.")

    if get_location_by_pincode(code) is None:
        raise PincodeNotFoundException(code)

    return get_location_by_pincode(code)


@app.post("/pincode/bulk", response_model=BulkResponse)
def lookup_bulk_pincode(request: BulkRequest):
    # Your implementation here
    results = []
    missing = []

    for code in request.pincodes:
        location = get_location_by_pincode(code)
        if location is not None:
            results.append(location)
        else:
            missing.append(code)

    return BulkResponse(found=results, missing=missing)
        