from pydantic import BaseModel, field_validator

class PincodeRequest(BaseModel):
    pincode: str

    #pincode must of exactly 6 digits and only digits
    @field_validator('pincode')
    def validate_pincode(cls, value):
        if not value.isdigit() or len(value) != 6:
            raise ValueError('Pincode must be a 6-digit number.')
        return value


class locationResponse(BaseModel):
    pincode: str
    city: str
    state: str
    district: str

class BulkRequest(BaseModel):
    pincodes: list[str]

    @field_validator("pincodes")
    @classmethod
    def validate_pincodes(cls, value):
        if len(value) == 0:
            raise ValueError("Pincodes list cannot be empty.")
        if len(value) > 20:
            raise ValueError("Pincodes list cannot contain more than 20 items.")

        for code in value:
            if not code.isdigit() or len(code) != 6:
                raise ValueError(f"Pincode '{code}' must be a 6-digit number.")


class BulkResponse(BaseModel):
   status: str = "success"
   found: int
   not_found: int
   results: list[locationResponse]
   missing: list[str]
