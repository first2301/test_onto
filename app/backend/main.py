import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI
from backend.router.mapping_ontology import router as mapping_ontology_router

# 로깅 설정
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """애플리케이션 시작/종료 이벤트 처리"""
    # Startup
    logger.info("Starting application...")
    yield
    # Shutdown
    logger.info("Shutting down application...")


app = FastAPI(lifespan=lifespan)

app.include_router(mapping_ontology_router)

@app.get("/")
def read_root():
    return {"message": "FastAPI is running"}