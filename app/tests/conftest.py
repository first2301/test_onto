"""
전역 pytest 설정 및 fixtures
모든 테스트에서 공통으로 사용하는 fixtures 정의
"""

import pytest
from pathlib import Path
from fastapi.testclient import TestClient
from backend.main import app


@pytest.fixture(scope="session")
def test_data_dir() -> Path:
    """테스트 데이터 디렉토리 경로"""
    return Path(__file__).parent / "test_data"


@pytest.fixture
def client() -> TestClient:
    """FastAPI 테스트 클라이언트"""
    return TestClient(app)


@pytest.fixture
def sample_ontology_classes() -> list[str]:
    """샘플 온톨로지 클래스 리스트"""
    return [
        "Injection_Molding_Machine",
        "Welding_Robot",
        "CNC_Machine",
        "Industrial_Pump"
    ]

