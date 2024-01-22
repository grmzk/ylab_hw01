from fastapi import FastAPI

from menus.router import router as router_menus

app = FastAPI(title="Menu Management")

app.include_router(router_menus)
