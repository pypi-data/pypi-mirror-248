from fastapi import FastAPI, Request
from fastapi.encoders import jsonable_encoder
from fastapi.middleware.cors import CORSMiddleware
from starlette.responses import JSONResponse

from openaoe.backend.api.route_minimax import router as minimax_router
from openaoe.backend.api.route_openai import router as openai_router
from openaoe.backend.api.route_baidu import router as baidu_router
from openaoe.backend.api.route_google import router as google_router
from openaoe.backend.api.route_claude import router as claude_router
from openaoe.backend.api.route_xunfei import router as xunfei_router
from openaoe.backend.util.log import log
from openaoe.backend.job.jobs import start_jobs

from openaoe.backend.util.exception import OpenAIException, is_openai_key_limited
from openaoe.backend.util.request_info import set_request_keys_need_rotate
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

# control doc
if os.getenv("DOCS_ON") == "1":
    app = FastAPI(title="alles-apin APIs playground",
                  swagger_ui_parameters={"tryItOutEnabled": True, "defaultModelsExpandDepth": -1},
                  openapi_version='3.0.0', servers=[{"url": "https://openxlab.org.cn/gw/alles-apin-hub"}],
                  root_path="/gw/alles-apin-hub", root_path_in_servers=False,
                  description='<br><br>Only minimal parameters'
                               '<br><br>Detail info please check https://aicarrier.feishu.cn/docx/CjINdK211oHzLKxXFUhcyb4Xnsd')
else:
    app = FastAPI(openapi_url=None, redoc_url=None)


base_dir = app_abs_path()  # 获取当前脚本所在的目录
print(base_dir)
STATIC_RESOURCE_DIR = os.path.join(base_dir, "frontend/dist")  # 静态文件所在的目录
CSS_PATH_LIB = f"{STATIC_RESOURCE_DIR}/assets"
IMG_PATH_LIB = f"{STATIC_RESOURCE_DIR}/assets"
JS_PATH_LIB = f"{STATIC_RESOURCE_DIR}/js"
path = img_out_path()
OUT_IMG_PATH_LIB = f"{path}"

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


# if os.getenv("INFER_STORE_ENABLED", "0").casefold() == "1":
#     app.add_middleware(CollectMiddleware)

# add middlewares
# api-key统一管理中间件
# app.add_middleware(ApiKeyDetermineMiddleware)
# 接口健康访问记录中间件
# app.add_middleware(HealthRecordMiddleware)
# app.add_middleware(AuthMiddleware)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# add routers
app.include_router(minimax_router, prefix=f"/{API_VER}/minimax")
app.include_router(openai_router, prefix=f"/{API_VER}/openai")
app.include_router(baidu_router, prefix=f"/{API_VER}/baidu")
app.include_router(google_router, prefix=f"/{API_VER}/google")
app.include_router(claude_router, prefix=f"/{API_VER}/claude")
app.include_router(xunfei_router, prefix=f"/{API_VER}/xunfei")


@app.exception_handler(OpenAIException)
# 统一处理openai请求时的异常，对于需要轮转的key，设置轮转标记（在后续middleware中统一处理)
async def openai_exceptioxn_handler(request: Request, exc: OpenAIException):
    logger.warning(f"{exc}")
    is_limited, reason = is_openai_key_limited(exc.model, exc.error)
    if is_limited:
        set_request_keys_need_rotate(request, exc.api_key, reason, exc.res_headers)

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
    # start_jobs()
    # os.system("gunicorn main:app -w 1 -k uvicorn.workers.UvicornWorker --preload --bind 0.0.0.0:10029 -t 1800 "
    #           "--max-requests 50")
    # # todo debug
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
