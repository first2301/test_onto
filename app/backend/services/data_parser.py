"""
데이터 파서 모듈
다양한 형식의 데이터 파일을 파싱하여 관계 데이터 추출
"""

import logging
import polars as pl
from typing import List, Dict, Any, Optional
from io import BytesIO

logger = logging.getLogger(__name__)


class DataParser:
    """데이터 파서 기본 클래스"""
    
    def parse(self, file_content: bytes, file_name: str) -> pl.DataFrame:
        """
        파일 내용을 파싱하여 DataFrame으로 변환
        
        Args:
            file_content: 파일 내용 (bytes)
            file_name: 파일명
            
        Returns:
            DataFrame: 파싱된 데이터
        """
        raise NotImplementedError("Subclass must implement parse method")


class CSVParser(DataParser):
    """CSV 파일 파서"""
    
    def parse(self, file_content: bytes, file_name: str) -> pl.DataFrame:
        """
        CSV 파일 파싱
        
        Args:
            file_content: CSV 파일 내용 (bytes)
            file_name: 파일명
            
        Returns:
            DataFrame: 파싱된 데이터
        """
        try:
            # UTF-8 인코딩 시도
            try:
                content_str = file_content.decode('utf-8')
            except UnicodeDecodeError:
                # UTF-8 실패 시 CP949 (한글) 시도
                content_str = file_content.decode('cp949')
            
            # StringIO로 변환하여 polars로 읽기
            from io import StringIO
            df = pl.read_csv(StringIO(content_str))
            
            logger.info(f"CSV 파일 파싱 완료: {file_name}, {len(df)}개 행, {len(df.columns)}개 컬럼")
            return df
            
        except Exception as e:
            logger.error(f"CSV 파일 파싱 실패: {file_name}, {str(e)}", exc_info=True)
            raise ValueError(f"CSV 파일 파싱 중 오류가 발생했습니다: {str(e)}")


class JSONParser(DataParser):
    """JSON 파일 파서"""
    
    def parse(self, file_content: bytes, file_name: str) -> pl.DataFrame:
        """
        JSON 파일 파싱
        
        Args:
            file_content: JSON 파일 내용 (bytes)
            file_name: 파일명
            
        Returns:
            DataFrame: 파싱된 데이터
        """
        try:
            import json
            
            content_str = file_content.decode('utf-8')
            data = json.loads(content_str)
            
            # 리스트인 경우
            if isinstance(data, list):
                df = pl.DataFrame(data)
            # 딕셔너리인 경우
            elif isinstance(data, dict):
                # 중첩된 구조 처리
                if any(isinstance(v, (list, dict)) for v in data.values()):
                    # 첫 번째 키의 리스트를 사용
                    for key, value in data.items():
                        if isinstance(value, list):
                            df = pl.DataFrame(value)
                            break
                    else:
                        df = pl.DataFrame([data])
                else:
                    df = pl.DataFrame([data])
            else:
                raise ValueError("지원하지 않는 JSON 형식입니다.")
            
            logger.info(f"JSON 파일 파싱 완료: {file_name}, {len(df)}개 행, {len(df.columns)}개 컬럼")
            return df
            
        except Exception as e:
            logger.error(f"JSON 파일 파싱 실패: {file_name}, {str(e)}", exc_info=True)
            raise ValueError(f"JSON 파일 파싱 중 오류가 발생했습니다: {str(e)}")


class ExcelParser(DataParser):
    """Excel 파일 파서"""
    
    def parse(self, file_content: bytes, file_name: str, sheet_name: Optional[str] = None) -> pl.DataFrame:
        """
        Excel 파일 파싱
        
        Args:
            file_content: Excel 파일 내용 (bytes)
            file_name: 파일명
            sheet_name: 시트명 (None이면 첫 번째 시트)
            
        Returns:
            DataFrame: 파싱된 데이터
        """
        try:
            # polars는 Excel을 직접 지원하지 않으므로 pandas로 읽은 후 변환
            import pandas as pd
            df_pd = pd.read_excel(BytesIO(file_content), sheet_name=sheet_name)
            
            # 여러 시트인 경우 첫 번째 시트 사용
            if isinstance(df_pd, dict):
                df_pd = list(df_pd.values())[0]
            
            # pandas DataFrame을 polars DataFrame으로 변환
            df = pl.from_pandas(df_pd)
            
            logger.info(f"Excel 파일 파싱 완료: {file_name}, {len(df)}개 행, {len(df.columns)}개 컬럼")
            return df
            
        except Exception as e:
            logger.error(f"Excel 파일 파싱 실패: {file_name}, {str(e)}", exc_info=True)
            raise ValueError(f"Excel 파일 파싱 중 오류가 발생했습니다: {str(e)}")


def get_parser(file_type: str) -> DataParser:
    """
    파일 타입에 맞는 파서 반환
    
    Args:
        file_type: 파일 타입 (csv, json, excel)
        
    Returns:
        DataParser: 파서 인스턴스
    """
    file_type_lower = file_type.lower()
    
    if file_type_lower == 'csv':
        return CSVParser()
    elif file_type_lower == 'json':
        return JSONParser()
    elif file_type_lower == 'excel' or file_type_lower in ['xlsx', 'xls']:
        return ExcelParser()
    else:
        raise ValueError(f"지원하지 않는 파일 타입입니다: {file_type}")

