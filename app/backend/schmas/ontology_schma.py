from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any


# ============================================================================
# 온톨로지 구축 요청/응답 스키마
# ============================================================================

class BuildHybridOntologyRequest(BaseModel):
    """하이브리드 온톨로지 구축 요청 스키마"""
    
    ontology_classes: List[str] = Field(
        ...,
        description="표준 온톨로지 클래스 리스트",
        min_length=1,
        json_schema_extra={
            "example": ["Injection_Molding_Machine", "Welding_Robot", "CNC_Machine"]
        }
    )
    model_name: Optional[str] = Field(
        default=None,
        description="SentenceTransformer 모델명",
        json_schema_extra={
            "example": "sentence-transformers/all-MiniLM-L6-v2"
        }
    )


class BuildHybridOntologyResponse(BaseModel):
    """하이브리드 온톨로지 구축 응답 스키마"""
    
    message: str = Field(..., description="응답 메시지")
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

