import logging
import asyncio
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.router.mapping_ontology import router as mapping_ontology_router
from backend.router.data_upload import router as data_upload_router

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
    
    try:
        # 필요한 초기화 작업이 있다면 여기에 추가
        # 예: 저장소 초기화 확인 (이미 모듈 레벨에서 초기화되므로 선택사항)
        from backend.services.ontology_storage import get_ontology_storage
        storage = get_ontology_storage()
        logger.info("Ontology storage initialized")
        
    except Exception as e:
        # Startup 단계의 예외는 즉시 raise
        logger.error(f"Error during application startup: {str(e)}", exc_info=True)
        raise
    
    # yield: 서버 실행 (startup 성공 후에만 실행)
    try:
        yield
    except asyncio.CancelledError:
        # 서버 종료 요청 시 발생하는 정상적인 에러
        # shutdown 단계이므로 로깅만 하고 raise하지 않음
        logger.info("Shutting down application...")
    except Exception as e:
        # shutdown 단계의 예외는 로깅만 하고 raise하지 않음
        # FastAPI의 정상적인 shutdown 프로세스를 방해하지 않기 위함
        logger.warning(f"Error during application shutdown: {str(e)}", exc_info=True)
    finally:
        # 정리 작업 (필요시)
        try:
            logger.info("Application shutdown complete")
        except Exception as e:
            # finally 블록의 예외도 로깅만 함
            logger.warning(f"Error in shutdown cleanup: {str(e)}", exc_info=True)


app = FastAPI(lifespan=lifespan)

# CORS 미들웨어 추가
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # 프론트엔드 주소
    allow_credentials=True,
    allow_methods=["*"],  # 모든 HTTP 메서드 허용 (GET, POST, OPTIONS 등)
    allow_headers=["*"],  # 모든 헤더 허용
)

app.include_router(mapping_ontology_router)
app.include_router(data_upload_router)

@app.get("/")
def read_root():
    return {"message": "FastAPI is running"}