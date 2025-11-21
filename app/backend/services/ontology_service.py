"""
온톨로지 서비스 레이어
비즈니스 로직 및 데이터 변환 처리
"""

import logging
from typing import List, Dict, Any
from backend.services.ontology_services.ontology_builder import build_hybrid_ontology
from backend.services.ontology_services.config import DEFAULT_MODEL
from backend.schmas.ontology_schma import (
    BuildHybridOntologyRequest,
    BuildHybridOntologyResponse,
    GetHybridOntologyResponse
)

logger = logging.getLogger(__name__)


class OntologyService:
    """온톨로지 관련 비즈니스 로직 처리"""
    
    def build_hybrid_ontology(self, request: BuildHybridOntologyRequest) -> BuildHybridOntologyResponse:
        """
        하이브리드 온톨로지 구축
        
        Args:
            request: 구축 요청 스키마
            
        Returns:
            BuildHybridOntologyResponse: 구축 결과
        """
        try:
            # 기본값 처리 (비즈니스 로직)
            model_name = request.model_name or DEFAULT_MODEL
            logger.debug(f"모델명: {model_name}, 온톨로지 클래스 수: {len(request.ontology_classes)}")
            
            # 비즈니스 로직 호출
            logger.debug("온톨로지 구축 함수 호출 시작")
            mapping_df, g = build_hybrid_ontology(
                request.ontology_classes,
                model_name
            )
            logger.debug(f"매핑 결과: {len(mapping_df)}개 행, RDF Graph: {len(g)}개 트리플")
            
            # 데이터 변환 (비즈니스 로직)
            logger.debug("DataFrame을 딕셔너리로 변환 중...")
            mapping_dict = mapping_df.to_dict(orient="records")
            logger.debug(f"변환 완료: {len(mapping_dict)}개 레코드")
            
            logger.debug("RDF Graph를 Turtle 형식으로 직렬화 중...")
            graph_turtle = g.serialize(format="turtle")  # RDFLib 7.x는 이미 문자열 반환
            logger.debug(f"직렬화 완료: {len(graph_turtle)} 문자")
            
            # 응답 객체 생성
            logger.debug("응답 객체 생성 중...")
            response = BuildHybridOntologyResponse(
                message="온톨로지 구축 완료",
                mapping_df=mapping_dict,
                g=graph_turtle
            )
            logger.info(f"온톨로지 구축 성공: {len(mapping_dict)}개 매핑")
            return response
            
        except Exception as e:
            logger.error(
                f"온톨로지 구축 중 오류 발생: {str(e)}",
                exc_info=True,
                extra={
                    "model_name": request.model_name or DEFAULT_MODEL,
                    "ontology_classes_count": len(request.ontology_classes)
                }
            )
            raise
    
    def get_hybrid_ontology(self, ontology_id: str) -> GetHybridOntologyResponse:
        """
        온톨로지 조회
        
        Args:
            ontology_id: 온톨로지 ID
            
        Returns:
            GetHybridOntologyResponse: 조회 결과
            
        Note:
            TODO: 실제 조회 로직 구현 필요
        """
        return GetHybridOntologyResponse(
            message="하이브리드 온톨로지 조회 완료",
            ontology_id=ontology_id
        )

