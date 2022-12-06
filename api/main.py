from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.auth import router as auth_router
from api.users import router as user_router
from api.opts import router as otp_router
from .utils.dbUtil import database

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    # FastAPI doc related to allow_origin (to avoid CORS issues):
    # "It's also possible to declare the list as "*" (a "wildcard") to say that all are allowed.
    # But that will only allow certain types of communication, excluding everything that involves
    # credentials: Cookies, Authorization headers like those used with Bearer Tokens, etc.
    # So, for everything to work correctly, it's better to specify explicitly the allowed origins."
    # => Workarround: use allow_origin_regex
    # Source: https://github.com/tiangolo/fastapi/issues/133#issuecomment-646985050
    allow_origin_regex="https?://.*",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"],
)


@app.on_event("startup")
async def startup():
    await database.connect()


@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()


@app.get("/")
async def index():
    return "hello"


app.include_router(auth_router.router, tags=["Auth"])
app.include_router(user_router.router, tags=["User"])
app.include_router(otp_router.router, tags=["OTP"])
