import os
import uuid
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import cowsay
import requests
import hashlib
from fastapi.logger import logger
import logging

# Configure logging before creating the app
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

# Set up the logger explicitly
logger = logging.getLogger("cowsay_api")
logger.setLevel(logging.INFO)

app = FastAPI(
    docs_url="/",
    title="Cowsay API",
    description="A simple API to generate cowsay messages."
)

RSTUF_SERVER = os.getenv("CS_RSTUF_SERVER", "http://rstuf-rstuf-api.rstuf.svc.cluster.local")
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
        file_name = f"{file_uuid}.txt"
        
        # Create the output file path
        output_path = os.path.join(OUTPUT_DIR, file_name)
        
        # Generate cowsay message
        cowsay_message = cowsay.get_output_string("cow", f"Hello, {name}!")
        
        # Write the message to the file
        sha256_hash = hashlib.sha256(cowsay_message.encode()).hexdigest()

        # Compute length
        length = len(cowsay_message.encode())        
        with open(output_path, 'w') as f:
            f.write(cowsay_message)
        
        payload = {
            "artifacts": [
                {
                    "info": {
                        "hashes": {
                            "sha256": sha256_hash
                        },
                        "length": length
                    },
                    "path": file_name
                }
            ]
        }
        response = requests.post(f"{RSTUF_SERVER}/api/v1/artifacts/", json=payload)
        logger.info(f"Response from RSTUF: {response.status_code}")
        logger.info(f"Response from RSTUF: {response.text}")
        return {"uuid": file_uuid}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
