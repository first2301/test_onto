"""
온톨로지 매핑 라우터
HTTP 요청/응답 처리만 담당
"""

import logging
from fastapi import APIRouter, HTTPException, status, Depends, Query
from backend.dependencies.services import get_ontology_service
from backend.services.ontology_service import OntologyService
from backend.schmas.ontology_schma import (
    GetHybridOntologyResponse,
    ListOntologiesResponse,
    OntologyGraphResponse,
)

logger = logging.getLogger(__name__)


router = APIRouter(prefix="/api/v1", tags=["mapping_ontology"])


@router.get("/get_hybrid_ontology", response_model=GetHybridOntologyResponse)
async def get_hybrid_ontology_endpoint(
    ontology_id: str = Query(..., description="온톨로지 ID"),
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


@router.get("/list_ontologies", response_model=ListOntologiesResponse)
async def list_ontologies_endpoint(
    service: OntologyService = Depends(get_ontology_service)
):
    """
    온톨로지 목록 조회
    
    Args:
        service: 온톨로지 서비스 (의존성 주입)
        
    Returns:
        ListOntologiesResponse: 목록 조회 결과
    """
    try:
        logger.info("온톨로지 목록 조회 요청")
        result = service.list_ontologies()
        logger.info(f"온톨로지 목록 조회 완료: {result.total}개")
        return result
    except Exception as e:
        logger.error(
            f"온톨로지 목록 조회 실패: {str(e)}",
            exc_info=True
        )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"온톨로지 목록 조회 중 오류가 발생했습니다: {str(e)}"
        )


@router.get("/get_ontology_graph/{ontology_id}", response_model=OntologyGraphResponse)
async def get_ontology_graph_endpoint(
    ontology_id: str,
    service: OntologyService = Depends(get_ontology_service)
):
    """
    온톨로지 그래프 데이터 조회
    
    Args:
        ontology_id: 온톨로지 ID
        service: 온톨로지 서비스 (의존성 주입)
        
    Returns:
        OntologyGraphResponse: 그래프 데이터
    """
    try:
        logger.info(f"온톨로지 그래프 조회 요청: ontology_id={ontology_id}")
        result = service.get_ontology_graph(ontology_id)
        logger.info(f"온톨로지 그래프 조회 완료: ontology_id={ontology_id}, 노드={len(result.nodes)}개, 엣지={len(result.edges)}개")
        return result
    except Exception as e:
        logger.error(
            f"온톨로지 그래프 조회 실패: ontology_id={ontology_id}, error={str(e)}",
            exc_info=True
        )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"온톨로지 그래프 조회 중 오류가 발생했습니다: {str(e)}"
        )


@router.get("/get_merged_ontology_graph", response_model=OntologyGraphResponse)
async def get_merged_ontology_graph_endpoint(
    service: OntologyService = Depends(get_ontology_service)
):
    """
    모든 온톨로지를 통합한 그래프 데이터 조회
    
    Args:
        service: 온톨로지 서비스 (의존성 주입)
        
    Returns:
        OntologyGraphResponse: 통합된 그래프 데이터
    """
    try:
        logger.info("통합 온톨로지 그래프 조회 요청")
        result = service.get_merged_ontology_graph()
        logger.info(f"통합 온톨로지 그래프 조회 완료: 노드={len(result.nodes)}개, 엣지={len(result.edges)}개")
        return result
    except Exception as e:
        logger.error(
            f"통합 온톨로지 그래프 조회 실패: {str(e)}",
            exc_info=True
        )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"통합 온톨로지 그래프 조회 중 오류가 발생했습니다: {str(e)}"
        )