# import os

import aiohttp
# from fastapi_cachette import Cachette
from fastapi import FastAPI, Response #, Depends
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
from fastapi.requests import Request
from fastapi.staticfiles import StaticFiles
from pybadges import badge
# from pydantic import BaseModel

from .b64 import software_logos

"""
ENV = os.environ
MONGO_HOST = ENV.get("MONGO_HOST")
MONGO_PORT = ENV.get("MONGO_HOST")
MONGO_USER = ENV.get("MONGO_HOST")
MONGO_PASS = ENV.get("MONGO_HOST")

if MONGO_HOST is None or MONGO_PORT is None:
    raise ConnectionError(
        "MONGO_HOST and MONGO_PORT is Required. Please set to Environmental Variables."
    )

class Payload(BaseModel):
  key: str
  value: str
"""

app = FastAPI(
    title="FedBadges",
    version="0.1.0",
    description="Badge Generator for ActivityPub Servers.",
    openapi_url=None,
    redoc_url=None,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

"""
@Cachette.load_config
def get_cachette_config():
    return [
        ("backend", "mongodb"),
        (
            "mongodb_url",
            f"mongodb://{MONGO_USER}:{MONGO_PASS}@{MONGO_HOST}:{MONGO_PORT}",
        ),
        ("ttl", "3600")
    ]
"""

@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    context = {
        "request": request
    }
    return templates.TemplateResponse("index.html", context)

@app.get("/followers")
async def followers(response: Response, username: str, host: str=None, software: str = "activitypub"):
    response.headers["X-Robots-Tag"] = "noimageai"
    head = {
        "Accept": "application/activity+json",
        "User-Agent": "FediBadges (https://github.com/sonyakun/fedibadges)",
    }
    if host is None:
        b = badge(left_text="Followers", right_text="host is Required", right_color="#FF4949")
        return HTMLResponse(content=b, status_code=200, media_type="image/svg+xml")
    elif username is None:
        b = badge(left_text="Followers", right_text="username is Required", right_color="#FF4949")
        return HTMLResponse(content=b, status_code=200, media_type="image/svg+xml")
    if software_logos.get(software.lower()) is None:
        logo = software_logos.get("activitypub")
    else:
        logo = software_logos.get(software.lower())
    if host.startswith("http://") or host.startswith("https://"):
        b = badge(left_text="Followers", right_text="Error", right_color="#FF4949")
        return HTMLResponse(content=b, status_code=200, media_type="image/svg+xml")
    async with aiohttp.ClientSession() as session:
        async with session.get(
            f"https://{host}/.well-known/webfinger?resource=acct:{username}@{host}",
            headers=head,
        ) as wf_resp:
            if wf_resp.status == 404:
                b = badge(
                    left_text="Followers", right_text="Not Found", right_color="#FF4949"
                )
                return HTMLResponse(
                    content=b, status_code=200, media_type="image/svg+xml"
                )
            wf_resp = await wf_resp.json()
            url = None
            for link in wf_resp["links"]:
                if link["rel"] == "self":
                    url = link["href"]
                    break
            if url is None:
                b = badge(
                    left_text="Followers", right_text="Error", right_color="#FF4949"
                )
                return HTMLResponse(
                    content=b, status_code=200, media_type="image/svg+xml"
                )
        async with session.get(url + "/followers", headers=head) as resp:
            if resp.status == 200:
                resp = await resp.json()
                follower_count = str(resp["totalItems"])
            elif resp.status == 403:
                follower_count = "unknown"
            else:
                b = badge(
                    left_text="Followers",
                    right_text="Error",
                    right_color="#FF4949",
                    logo=logo["b64"],
                )
                return HTMLResponse(
                    content=b, status_code=200, media_type="image/svg+xml"
                )
    b = badge(
        left_text="Followers",
        right_text=follower_count,
        right_color=logo["color"],
        logo=logo["b64"],
    )
    return HTMLResponse(content=b, status_code=200, media_type="image/svg+xml")

@app.get("/posts")
async def posts(response: Response, username: str=None, host: str=None, software: str = "activitypub"):
    response.headers["X-Robots-Tag"] = "noimageai"
    if host is None:
        b = badge(left_text="Followers", right_text="host is Required", right_color="#FF4949")
        return HTMLResponse(content=b, status_code=200, media_type="image/svg+xml")
    elif username is None:
        b = badge(left_text="Followers", right_text="username is Required", right_color="#FF4949")
        return HTMLResponse(content=b, status_code=200, media_type="image/svg+xml")
    if software.lower() == "misskey":
        text = "Notes"
    elif software.lower() == "mastodon":
        text = "Toots"
    else:
        text = "Posts"

    head = {
        "Accept": "application/activity+json",
        "User-Agent": "FediBadges (https://github.com/sonyakun/fedibadges)",
    }
    if software_logos.get(software.lower()) is None:
        logo = software_logos.get("activitypub")
    else:
        logo = software_logos.get(software.lower())
    if host.startswith("http://") or host.startswith("https://"):
        b = badge(left_text="Total " + text, right_text="Host is Unknown", right_color="#FF4949")
        return HTMLResponse(content=b, status_code=200, media_type="image/svg+xml")
    async with aiohttp.ClientSession() as session:
        async with session.get(
            f"https://{host}/.well-known/webfinger?resource=acct:{username}@{host}",
            headers=head,
        ) as wf_resp:
            if wf_resp.status == 404:
                b = badge(
                    left_text="Total " + text, right_text="Not Found", right_color="#FF4949"
                )
                return HTMLResponse(
                    content=b, status_code=200, media_type="image/svg+xml"
                )
            wf_resp = await wf_resp.json()
            url = None
            for link in wf_resp["links"]:
                if link["rel"] == "self":
                    url = link["href"]
                    break
            if url is None:
                b = badge(
                    left_text="Total " + text, right_text="Internal Error", right_color="#FF4949"
                )
                return HTMLResponse(
                    content=b, status_code=200, media_type="image/svg+xml"
                )
        async with session.get(url + "/outbox", headers=head) as resp:
            if resp.status == 200:
                resp = await resp.json()
                post_count = str(resp["totalItems"])
            elif resp.status == 403:
                post_count = "unknown"
            else:
                b = badge(
                    left_text="Total " + text,
                    right_text="Internal Error",
                    right_color="#FF4949",
                    logo=logo["b64"],
                )
                return HTMLResponse(
                    content=b, status_code=200, media_type="image/svg+xml"
                )

    b = badge(
        left_text="Total " + text,
        right_text=post_count,
        right_color=logo["color"],
        logo=logo["b64"],
    )
    return HTMLResponse(content=b, status_code=200, media_type="image/svg+xml")