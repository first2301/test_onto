"""
온톨로지 매핑 라우터
HTTP 요청/응답 처리만 담당
"""

import logging
from fastapi import APIRouter, HTTPException, status, Depends
from backend.dependencies.services import get_ontology_service
from backend.services.ontology_service import OntologyService
from backend.schmas.ontology_schma import (
    BuildHybridOntologyRequest,
    BuildHybridOntologyResponse,
    GetHybridOntologyResponse
)

logger = logging.getLogger(__name__)


router = APIRouter(prefix="/api/v1", tags=["mapping_ontology"])


@router.post("/build_hybrid_ontology", response_model=BuildHybridOntologyResponse)
async def build_hybrid_ontology_endpoint(
    request: BuildHybridOntologyRequest,
    service: OntologyService = Depends(get_ontology_service)
):
    """
    하이브리드 온톨로지 구축
    
    Args:
        request: 구축 요청
        service: 온톨로지 서비스 (의존성 주입)
        
    Returns:
        BuildHybridOntologyResponse: 구축 결과
    """
    try:
        logger.info(f"하이브리드 온톨로지 구축 요청: {len(request.ontology_classes)}개 클래스")
        result = service.build_hybrid_ontology(request)
        logger.info(f"하이브리드 온톨로지 구축 완료: {len(result.mapping_df)}개 매핑")
        return result
    except Exception as e:
        logger.error(
            f"하이브리드 온톨로지 구축 실패: {str(e)}",
            exc_info=True,
            extra={
                "ontology_classes_count": len(request.ontology_classes) if request else 0,
                "model_name": request.model_name if request else None
            }
        )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"온톨로지 구축 중 오류가 발생했습니다: {str(e)}"
        )


@router.get("/get_hybrid_ontology", response_model=GetHybridOntologyResponse)
async def get_hybrid_ontology_endpoint(
    ontology_id: str,
    service: OntologyService = Depends(get_ontology_service)
):
    """
    온톨로지 조회
    
    Args:
        ontology_id: 온톨로지 ID
        service: 온톨로지 서비스 (의존성 주입)
        
    Returns:
        GetHybridOntologyResponse: 조회 결과
    """
    try:
        logger.info(f"온톨로지 조회 요청: ontology_id={ontology_id}")
        result = service.get_hybrid_ontology(ontology_id)
        logger.info(f"온톨로지 조회 완료: ontology_id={ontology_id}")
        return result
    except Exception as e:
        logger.error(
            f"온톨로지 조회 실패: ontology_id={ontology_id}, error={str(e)}",
            exc_info=True
        )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"온톨로지 조회 중 오류가 발생했습니다: {str(e)}"
        )