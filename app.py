import os
import uuid
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import cowsay

app = FastAPI(
    docs_url="/",
    title="Cowsay API",
    description="A simple API to generate cowsay messages."
)

# Ensure the output directory exists
OUTPUT_DIR = "outputs"
os.makedirs(OUTPUT_DIR, exist_ok=True)

class NameRequest(BaseModel):
    name: str

@app.post("/generate/{name}")
async def generate_cowsay(name: str):
    try:
        # Generate a hex UUID
        file_uuid = uuid.uuid4().hex
        
        # Create the output file path
        output_path = os.path.join(OUTPUT_DIR, f"{file_uuid}.txt")
        
        # Generate cowsay message
        cowsay_message = cowsay.get_output_string("cow", f"Hello, {name}!")
        
        # Write the message to the file
        with open(output_path, 'w') as f:
            f.write(cowsay_message)
        
        return {"uuid": file_uuid}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
