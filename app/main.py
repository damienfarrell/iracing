import logging
import requests
from fastapi import FastAPI, Form, Request, status, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from .data import fetch_session_data, parse_data, import_race_data
from .auth import encode_password, authenticate
from .config import EMAIL, PASSWORD, SUBSESSION_URL
from . import schemas

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

app = FastAPI()

origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def index_page(request: Request):
    return {"Status": "Server is running"}

@app.post("/races", status_code=status.HTTP_201_CREATED, response_model=schemas.RaceDataResponse)
def race_info(
    session_id: int = Form(...),
    passcode: int = Form(...)
):
    try:
        # Validate input using Pydantic model
        race_data = schemas.RaceDataInput(session_id=session_id, passcode=passcode)

        if race_data.passcode != 123454321:
            logging.warning(f"Incorrect passcode: {race_data.passcode}")
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect passcode")
        
        pw_value_to_submit = encode_password(EMAIL, PASSWORD)
        sso_cookie_value, auth_token = authenticate(EMAIL, pw_value_to_submit)
        session = requests.Session()
        session.cookies.update({
            "irsso_membersv2": sso_cookie_value,
            "authtoken_members": f'{{"authtoken":{{"authcode":"{auth_token}","email":"{EMAIL}"}}}}'
        })
        
        session_url = f'{SUBSESSION_URL}{race_data.session_id}'
        response_data = fetch_session_data(session, session_url)
        parsed_data = parse_data(response_data)
        import_race_data(parsed_data)

        return {"session_id": race_data.session_id, "session_name": response_data["session_name"], "status": "success"}

    except HTTPException as he:
        logging.error(f"HTTP error occurred: {he.detail}")
        raise
    except requests.RequestException as re:
        logging.error(f"Request exception occurred: {re}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to fetch session data")
    except Exception as e:
        logging.error(f"Failed to import race data: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to import race data")