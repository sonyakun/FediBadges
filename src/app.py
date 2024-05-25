# import os

import aiohttp
# from fastapi_cachette import Cachette
import uvicorn
from fastapi import FastAPI #, Depends
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from pybadges import badge
import uvicorn
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
    description="Mastodon/Misskey Badge Generator",
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

@app.get("/followers")
async def followers(username: str, host: str, software: str = "activitypub"):
    head = {
        "Accept": "application/activity+json",
        "User-Agent": "FediBadges (https://github.com/sonyakun/fedibadges)",
    }
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
async def posts(username: str, host: str, software: str = "activitypub"):
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