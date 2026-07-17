"""
Thunder AI — System/Automation API Routes
"""
from fastapi import APIRouter
from pydantic import BaseModel
from automation.windows_control import (
    shutdown_pc, restart_pc, lock_pc, sleep_pc, cancel_shutdown,
    volume_up, volume_down, mute_volume,
    open_app, close_app, open_website, search_google, search_youtube,
    create_folder, delete_path, list_folder
)

router = APIRouter(prefix="/api/system", tags=["system"])


class AppRequest(BaseModel):
    name: str

class PathRequest(BaseModel):
    path: str

class SearchRequest(BaseModel):
    query: str


@router.post("/shutdown")
def shutdown():
    return {"result": shutdown_pc()}

@router.post("/restart")
def restart():
    return {"result": restart_pc()}

@router.post("/lock")
def lock():
    return {"result": lock_pc()}

@router.post("/sleep")
def sleep():
    return {"result": sleep_pc()}

@router.post("/volume/up")
def vol_up():
    return {"result": volume_up()}

@router.post("/volume/down")
def vol_down():
    return {"result": volume_down()}

@router.post("/volume/mute")
def vol_mute():
    return {"result": mute_volume()}

@router.post("/app/open")
def app_open(req: AppRequest):
    return {"result": open_app(req.name)}

@router.post("/app/close")
def app_close(req: AppRequest):
    return {"result": close_app(req.name)}

@router.post("/browser/open")
def browser_open(req: PathRequest):
    return {"result": open_website(req.path)}

@router.post("/browser/google")
def browser_google(req: SearchRequest):
    return {"result": search_google(req.query)}

@router.post("/browser/youtube")
def browser_youtube(req: SearchRequest):
    return {"result": search_youtube(req.query)}

@router.post("/folder/create")
def folder_create(req: PathRequest):
    return {"result": create_folder(req.path)}

@router.post("/folder/delete")
def folder_delete(req: PathRequest):
    return {"result": delete_path(req.path)}

@router.get("/folder/list")
def folder_list(path: str = "."):
    return {"result": list_folder(path)}
