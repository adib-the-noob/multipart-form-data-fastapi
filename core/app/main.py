from fastapi import FastAPI, staticfiles
from routers import (
    auth,
    profile,
)


app = FastAPI()

app.mount("/media", staticfiles.StaticFiles(directory="media"), name="media")

# routers
app.include_router(auth.router)
app.include_router(profile.router)


@app.get("/health")
async def health():
    return {"status": "ok"}
