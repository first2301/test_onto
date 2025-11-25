"""
데이터 업로드 라우터
파일 업로드 및 온톨로지 관계 추가 처리
"""

import logging
from fastapi import APIRouter, UploadFile, File, Form, HTTPException, status, Depends
from typing import Optional, List
from backend.dependencies.services import get_ontology_service
from backend.services.ontology_service import OntologyService
from backend.services.data_upload_service import DataUploadService
from backend.schmas.ontology_schma import UploadDataResponse
from backend.services.ontology_services.config import DEFAULT_MODEL

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/v1", tags=["data_upload"])

# 업로드 서비스 인스턴스
_upload_service = DataUploadService()

# 최대 파일 크기 제한 (500MB)
MAX_FILE_SIZE = 500 * 1024 * 1024  # 500MB in bytes


@router.post("/upload_data", response_model=UploadDataResponse)
async def upload_data_endpoint(
    file: UploadFile = File(..., description="업로드할 파일"),
    ontology_classes: str = Form(..., description="온톨로지 클래스 목록 (쉼표로 구분)"),
    ontology_id: Optional[str] = Form(None, description="기존 온톨로지 ID (선택사항)"),
    relation_type: str = Form("isDataOf", description="관계 타입"),
    source_column: Optional[str] = Form(None, description="소스 컬럼명 (선택사항)"),
    target_column: Optional[str] = Form(None, description="타겟 컬럼명 (선택사항)"),
    model_name: str = Form(DEFAULT_MODEL, description="모델명"),
    service: OntologyService = Depends(get_ontology_service)
):
    """
    데이터 파일 업로드 및 온톨로지 관계 추가
    매핑은 자동으로 처리됩니다: 타겟 컬럼이 있으면 직접 매핑, 없으면 파일명 기반 하이브리드 매핑 사용
    
    Args:
        file: 업로드할 파일
        ontology_classes: 온톨로지 클래스 목록 (쉼표로 구분)
        ontology_id: 기존 온톨로지 ID (선택사항)
        relation_type: 관계 타입
        source_column: 소스 컬럼명 (선택사항)
        target_column: 타겟 컬럼명 (선택사항, 있으면 직접 매핑 사용)
        model_name: 모델명
        service: 온톨로지 서비스 (의존성 주입)
        
    Returns:
        UploadDataResponse: 업로드 결과
    """
    try:
        # 파일 타입 확인
        file_type = _get_file_type(file.filename)
        if not file_type:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="지원하지 않는 파일 형식입니다. (CSV, JSON, Excel만 지원)"
            )
        
        # 파일 내용 읽기
        file_content = await file.read()
        
        # 파일 크기 검증
        file_size = len(file_content)
        if file_size > MAX_FILE_SIZE:
            raise HTTPException(
                status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
                detail=f"파일 크기는 {MAX_FILE_SIZE / 1024 / 1024}MB 이하여야 합니다. 현재 파일 크기: {file_size / 1024 / 1024:.2f}MB"
            )
        
        logger.info(f"파일 크기 검증 통과: {file_size / 1024 / 1024:.2f}MB")
        
        # 온톨로지 클래스 파싱
        classes_list = [cls.strip() for cls in ontology_classes.split(",") if cls.strip()]
        if not classes_list:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="온톨로지 클래스가 필요합니다."
            )
        
        logger.info(f"데이터 업로드 요청: 파일={file.filename}, 타입={file_type}, 클래스={len(classes_list)}개")
        
        # 업로드 서비스 호출
        result = _upload_service.upload_and_build_ontology(
            file_content=file_content,
            file_name=file.filename,
            file_type=file_type,
            ontology_classes=classes_list,
            ontology_id=ontology_id,
            relation_type=relation_type,
            source_column=source_column,
            target_column=target_column,
            model_name=model_name
        )
        
        logger.info(f"데이터 업로드 완료: ontology_id={result.ontology_id}, 관계={result.relations_added}개")
        
        return result
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(
            f"데이터 업로드 실패: {str(e)}",
            exc_info=True
        )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"데이터 업로드 중 오류가 발생했습니다: {str(e)}"
        )


def _get_file_type(filename: str) -> Optional[str]:
    """
    파일명에서 파일 타입 추출
    
    Args:
        filename: 파일명
        
    Returns:
        Optional[str]: 파일 타입 (csv, json, excel) 또는 None
    """
    if not filename:
        return None
    
    filename_lower = filename.lower()
    
    if filename_lower.endswith('.csv'):
        return 'csv'
    elif filename_lower.endswith('.json'):
        return 'json'
    elif filename_lower.endswith(('.xlsx', '.xls')):
        return 'excel'
    else:
        return None

