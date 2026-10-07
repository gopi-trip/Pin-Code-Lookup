from pydantic import BaseModel, field_validator

class PincodeRequest(BaseModel):
    pincode:str

    #Checking if Pincode is exactly 6 digits
    @field_validator("pincode")
    @classmethod
    def validate_pincode(cls,value):
        if len(value)!=6 or not value.isdigit():
            raise ValueError("Pincode must be exactly 6 digits")
        return value

class LocationResponse(BaseModel):
    pincode:str
    city:str
    state:str
    district:str

class BulkPincodeRequests(BaseModel):
    pincodes:list[str]

    @field_validator("pincodes")
    @classmethod
    def validate_pincodes(cls,values):
        if(len(values) == 0):
            raise ValueError("Provide atleast one pincode")
        if(len(values) > 20):
            raise ValueError("Maximum 20 pincodes allowed per request")

        for code in values:
            if len(code)!=6 or not code.isdigit():
                raise ValueError("Pincode: {code} must be exactly 6 digits") 
        return values

class BulkRequestResponse(BaseModel):
    status:str = "Success"
    found:int
    not_found:int
    result: list[LocationResponse]
    missing: list[str]