"""
유틸리티 함수 모듈
ID 생성, 파일명 전처리 등 공통 유틸리티 함수
"""

import hashlib
import os
from typing import Optional


def generate_dataset_id(
    filename: str, 
    mapped_class: str, 
    file_path: Optional[str] = None
) -> str:
    """
    데이터셋 ID 생성 (실무 권장 방식)
    
    Args:
        filename: 파일명
        mapped_class: 매핑된 클래스명
        file_path: 파일 경로 (선택)
    
    Returns:
        고유한 데이터셋 ID
    """
    file_base = os.path.splitext(filename)[0]
    class_prefix = mapped_class.lower().replace('_', '-')
    
    # 파일명 + 클래스 기반 해시
    content = f"{file_base}_{class_prefix}"
    if file_path and os.path.exists(file_path):
        # 파일 내용 기반 해시 추가 (더 정확한 고유성)
        with open(file_path, 'rb') as f:
            file_hash = hashlib.sha256(f.read()).hexdigest()[:8]
        content = f"{content}_{file_hash}"
    
    hash_id = hashlib.sha256(content.encode()).hexdigest()[:8]
    
    # 형식: {class_prefix}/{file_base}_{hash_id}
    dataset_id = f"{class_prefix}/{file_base}_{hash_id}"
    return dataset_id


def sanitize_filename_for_uri(filename: str) -> str:
    """
    URI에 사용할 수 있도록 파일명 정제
    
    Args:
        filename: 원본 파일명
    
    Returns:
        URI-safe 파일명
    """
    # 확장자 제거
    name = os.path.splitext(filename)[0]
    # 특수문자를 언더스코어로 변환
    name = name.replace(' ', '_').replace('-', '_')
    return name

