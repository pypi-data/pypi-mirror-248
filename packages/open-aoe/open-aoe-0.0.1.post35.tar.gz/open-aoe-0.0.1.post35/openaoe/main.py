from fastapi import FastAPI, Request
from fastapi.encoders import jsonable_encoder
from fastapi.middleware.cors import CORSMiddleware
from starlette.responses import JSONResponse

from openaoe.backend.api.route_minimax import router as minimax_router
from openaoe.backend.api.route_openai import router as openai_router
from openaoe.backend.api.route_google import router as google_router
from openaoe.backend.api.route_claude import router as claude_router
from openaoe.backend.api.route_xunfei import router as xunfei_router
from openaoe.backend.util.log import log

from openaoe.backend.util.exception import OpenAIException, is_openai_key_limited
from openaoe.backend.model.dto.ReturnBase import ReturnBase

from fastapi.responses import FileResponse
from starlette.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from openaoe.backend.config.biz_config import app_abs_path, img_out_path
from openaoe.backend.util.str_util import safe_join
import os



logger = log(__name__)
# define global variable
API_VER = 'v1'
base_dir = app_abs_path()  # 获取当前脚本所在的目录
print(base_dir)
STATIC_RESOURCE_DIR = os.path.join(base_dir, "frontend/dist")  # 静态文件所在的目录
CSS_PATH_LIB = f"{STATIC_RESOURCE_DIR}/assets"
IMG_PATH_LIB = f"{STATIC_RESOURCE_DIR}/assets"
JS_PATH_LIB = f"{STATIC_RESOURCE_DIR}/js"
path = img_out_path()
OUT_IMG_PATH_LIB = f"{path}"

app = FastAPI()

app.mount("/static", StaticFiles(directory=STATIC_RESOURCE_DIR), name="static")

@app.get("/", response_class=HTMLResponse)
@app.get("/home", response_class=HTMLResponse)
async def server():
    return FileResponse(f"{STATIC_RESOURCE_DIR}/index.html")


@app.get("/assets/css/{path:path}")
async def build_resource(path: str):
    build_file = safe_join(CSS_PATH_LIB, path)
    return FileResponse(build_file)


@app.get("/{path:path}")
async def build_resource(path: str):
    static_file = safe_join(STATIC_RESOURCE_DIR, path)
    return FileResponse(static_file)


# add middlewares here if need
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# add api routers
app.include_router(minimax_router, prefix=f"/{API_VER}/minimax")
app.include_router(openai_router, prefix=f"/{API_VER}/openai")
app.include_router(google_router, prefix=f"/{API_VER}/google")
app.include_router(claude_router, prefix=f"/{API_VER}/claude")
app.include_router(xunfei_router, prefix=f"/{API_VER}/xunfei")


@app.exception_handler(OpenAIException)
# 统一处理openai请求时的异常，对于需要轮转的key，设置轮转标记（在后续middleware中统一处理)
async def openai_exceptioxn_handler(request: Request, exc: OpenAIException):
    logger.warning(f"{exc}")
    is_limited, reason = is_openai_key_limited(exc.model, exc.error)
    if is_limited:
        logger.info("is limited")

    if 'stream' in request.url.path:
        return
    return JSONResponse(
        status_code=200,
        content=jsonable_encoder(ReturnBase(
            msg="error",
            msgCode="-1",
            data=str(exc.error)
        )))


def main():
    import uvicorn
    uvicorn.run(
        app,
        host='0.0.0.0',
        port=10029,
        timeout_keep_alive=600,
        workers=1
    )


if __name__ == "__main__":
    main()
