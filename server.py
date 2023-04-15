import uvicorn

from src.app import cors

if __name__ == "__main__":
    uvicorn.run(cors, host="0.0.0.0", port=8000)
