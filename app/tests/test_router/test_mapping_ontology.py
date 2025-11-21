"""
온톨로지 매핑 라우터 테스트
HTTP 엔드포인트 동작 검증
"""

import pytest
from fastapi import status
from fastapi.testclient import TestClient


def test_build_hybrid_ontology_endpoint_success(client: TestClient, sample_ontology_classes: list[str]):
    """하이브리드 온톨로지 구축 엔드포인트 성공 테스트"""
    request_data = {
        "ontology_classes": sample_ontology_classes[:2],  # 2개만 사용
        "model_name": "sentence-transformers/all-MiniLM-L6-v2"
    }
    
    response = client.post("/api/v1/build_hybrid_ontology", json=request_data)
    
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert "message" in data
    assert "mapping_df" in data
    assert "g" in data
    assert isinstance(data["mapping_df"], list)
    assert isinstance(data["g"], str)


def test_build_hybrid_ontology_endpoint_without_model_name(client: TestClient, sample_ontology_classes: list[str]):
    """모델명 없이 하이브리드 온톨로지 구축 테스트 (기본값 사용)"""
    request_data = {
        "ontology_classes": sample_ontology_classes[:1]
    }
    
    response = client.post("/api/v1/build_hybrid_ontology", json=request_data)
    
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert "message" in data


def test_build_hybrid_ontology_endpoint_empty_classes(client: TestClient):
    """빈 온톨로지 클래스 리스트 테스트 (검증 실패 예상)"""
    request_data = {
        "ontology_classes": []
    }
    
    response = client.post("/api/v1/build_hybrid_ontology", json=request_data)
    
    # Pydantic 검증 실패로 422 에러 예상
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_CONTENT


def test_get_hybrid_ontology_endpoint(client: TestClient):
    """온톨로지 조회 엔드포인트 테스트"""
    ontology_id = "test_ontology_123"
    
    response = client.get("/api/v1/get_hybrid_ontology", params={"ontology_id": ontology_id})
    
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert "message" in data
    assert "ontology_id" in data
    assert data["ontology_id"] == ontology_id


def test_get_hybrid_ontology_endpoint_missing_param(client: TestClient):
    """온톨로지 조회 엔드포인트 - 필수 파라미터 누락 테스트"""
    response = client.get("/api/v1/get_hybrid_ontology")
    
    # 필수 파라미터 누락으로 422 에러 예상
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_CONTENT

