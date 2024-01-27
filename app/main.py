from fastapi import FastAPI

from menus.router import router as router_menus

app = FastAPI(title="Menu Management",
              docs_url='/api/docs',
              redoc_url='/api/redoc',
              openapi_url='/api/openapi.json')

app.include_router(router_menus)
