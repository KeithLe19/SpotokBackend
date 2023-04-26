import os
from dotenv import load_dotenv
from app import app

if __name__ == "__main__":
    load_dotenv()
    app.run(host='0.0.0.0', port=int(os.getenv("PORT") or 5000))
