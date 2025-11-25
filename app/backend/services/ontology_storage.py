"""
온톨로지 저장소
생성된 온톨로지 메타데이터를 메모리에 저장
"""

import logging
from datetime import datetime
from typing import Dict, Optional, List
from backend.schmas.ontology_schma import BuildHybridOntologyResponse

logger = logging.getLogger(__name__)


class OntologyStorage:
    """온톨로지 메타데이터 저장소 (메모리 기반)"""
    
    def __init__(self):
        """저장소 초기화"""
        self._storage: Dict[str, Dict] = {}
        logger.info("온톨로지 저장소 초기화 완료")
    
    def save(self, response: BuildHybridOntologyResponse, ontology_classes: List[str]) -> None:
        """
        온톨로지 저장
        
        Args:
            response: 구축 응답 객체
            ontology_classes: 사용된 온톨로지 클래스 목록
        """
        ontology_id = response.ontology_id
        
        self._storage[ontology_id] = {
            "ontology_id": ontology_id,
            "created_at": datetime.now().isoformat(),
            "ontology_classes": ontology_classes,
            "mapping_count": len(response.mapping_df),
            "rdf_graph": response.g,
            "mapping_df": response.mapping_df,
            "message": response.message,
        }
        
        logger.info(f"온톨로지 저장 완료: ID={ontology_id}, 매핑={len(response.mapping_df)}개")
    
    def get(self, ontology_id: str) -> Optional[Dict]:
        """
        온톨로지 조회
        
        Args:
            ontology_id: 온톨로지 ID
            
        Returns:
            온톨로지 메타데이터 또는 None
        """
        return self._storage.get(ontology_id)
    
    def list_all(self) -> List[Dict]:
        """
        모든 온톨로지 목록 조회
        
        Returns:
            온톨로지 목록 (생성일시 역순 정렬)
        """
        ontologies = list(self._storage.values())
        # 생성일시 역순 정렬 (최신순)
        ontologies.sort(key=lambda x: x["created_at"], reverse=True)
        return ontologies
    
    def delete(self, ontology_id: str) -> bool:
        """
        온톨로지 삭제
        
        Args:
            ontology_id: 온톨로지 ID
            
        Returns:
            삭제 성공 여부
        """
        if ontology_id in self._storage:
            del self._storage[ontology_id]
            logger.info(f"온톨로지 삭제 완료: ID={ontology_id}")
            return True
        return False
    
    def count(self) -> int:
        """
        저장된 온톨로지 개수
        
        Returns:
            온톨로지 개수
        """
        return len(self._storage)


# 전역 저장소 인스턴스
_ontology_storage = OntologyStorage()


def get_ontology_storage() -> OntologyStorage:
    """
    온톨로지 저장소 인스턴스 반환
    
    Returns:
        OntologyStorage 인스턴스
    """
    return _ontology_storage

