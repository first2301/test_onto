"""
서비스 의존성 주입 함수들
각 서비스의 싱글톤 인스턴스를 관리
"""

from backend.services.ontology_service import OntologyService

# 싱글톤 인스턴스
_ontology_service: OntologyService | None = None


def get_ontology_service() -> OntologyService:
    """
    온톨로지 서비스 인스턴스 가져오기 (싱글톤 패턴)
    
    Returns:
        OntologyService: 온톨로지 서비스 싱글톤 인스턴스
    """
    global _ontology_service
    if _ontology_service is None:
        _ontology_service = OntologyService()
    return _ontology_service

