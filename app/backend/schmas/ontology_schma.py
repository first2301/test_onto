from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any


# ============================================================================
# 온톨로지 구축 응답 스키마
# ============================================================================
# 참고: BuildHybridOntologyRequest는 제거되었습니다.
# 온톨로지 구축은 데이터 업로드 기능을 통해 수행됩니다.

class BuildHybridOntologyResponse(BaseModel):
    """하이브리드 온톨로지 구축 응답 스키마"""
    
    message: str = Field(..., description="응답 메시지")
    ontology_id: str = Field(..., description="생성된 온톨로지 ID")
    mapping_df: List[Dict[str, Any]] = Field(..., description="매핑 결과 DataFrame")
    g: str = Field(..., description="RDF Graph (Turtle 형식)")


# ============================================================================
# 온톨로지 조회 요청/응답 스키마
# ============================================================================

class GetHybridOntologyRequest(BaseModel):
    """온톨로지 조회 요청 스키마"""
    
    ontology_id: str = Field(..., description="온톨로지 ID")


class GetHybridOntologyResponse(BaseModel):
    """온톨로지 조회 응답 스키마"""
    
    message: str = Field(..., description="응답 메시지")
    ontology_id: str = Field(..., description="온톨로지 ID")
    created_at: str = Field(..., description="생성일시")
    ontology_classes: List[str] = Field(..., description="온톨로지 클래스 목록")
    mapping_count: int = Field(..., description="매핑 개수")
    mapping_df: List[Dict[str, Any]] = Field(..., description="매핑 결과 DataFrame")
    g: str = Field(..., description="RDF Graph (Turtle 형식)")


# ============================================================================
# 온톨로지 목록 조회 스키마
# ============================================================================

class OntologyListItem(BaseModel):
    """온톨로지 목록 아이템 스키마"""
    
    ontology_id: str = Field(..., description="온톨로지 ID")
    created_at: str = Field(..., description="생성일시")
    ontology_classes: List[str] = Field(..., description="온톨로지 클래스 목록")
    mapping_count: int = Field(..., description="매핑 개수")


class ListOntologiesResponse(BaseModel):
    """온톨로지 목록 조회 응답 스키마"""
    
    message: str = Field(..., description="응답 메시지")
    total: int = Field(..., description="전체 개수")
    ontologies: List[OntologyListItem] = Field(..., description="온톨로지 목록")


# ============================================================================
# 온톨로지 그래프 스키마
# ============================================================================

class OntologyGraphNode(BaseModel):
    """그래프 노드 스키마"""
    
    id: str = Field(..., description="노드 ID")
    label: str = Field(..., description="노드 라벨")
    type: str = Field(..., description="노드 타입 (class, dataset)")


class OntologyGraphEdge(BaseModel):
    """그래프 엣지 스키마"""
    
    source: str = Field(..., description="시작 노드 ID")
    target: str = Field(..., description="종료 노드 ID")
    relation: str = Field(..., description="관계 타입")


class OntologyGraphResponse(BaseModel):
    """온톨로지 그래프 응답 스키마"""
    
    message: str = Field(..., description="응답 메시지")
    ontology_id: str = Field(..., description="온톨로지 ID")
    nodes: List[OntologyGraphNode] = Field(..., description="노드 목록")
    edges: List[OntologyGraphEdge] = Field(..., description="엣지 목록")


# ============================================================================
# 데이터 업로드 스키마
# ============================================================================

class UploadDataResponse(BaseModel):
    """데이터 업로드 응답 스키마"""
    
    message: str = Field(..., description="응답 메시지")
    ontology_id: str = Field(..., description="온톨로지 ID (기존 또는 새로 생성)")
    file_name: str = Field(..., description="업로드된 파일명")
    file_size: int = Field(..., description="파일 크기 (bytes)")
    records_processed: int = Field(..., description="처리된 레코드 수")
    relations_added: int = Field(..., description="추가된 관계 수")
    mapping_df: List[Dict[str, Any]] = Field(..., description="매핑 결과 DataFrame")
    g: str = Field(..., description="RDF Graph (Turtle 형식)")

