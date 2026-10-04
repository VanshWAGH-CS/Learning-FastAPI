from pydantic import BaseModel, Field

class Contract(BaseModel):
    id: str = Field(..., alias="_id")
    title: str
    content: str
    created_at: str
    updated_at: str
    page_count: int
    word_count: int
    status: str = "uploaded"  # Default status when a contract is created


    def model_dump_init(self, __context):
        if not self.upload_date:
            self.upload_date = datetime.utcnow().isoformat()