"""
설정 관리 모듈
온톨로지 매핑 및 구축에 사용되는 설정값들을 중앙 관리
"""

# 신뢰도 임계값 설정
HIGH_CONFIDENCE = 0.7
MEDIUM_CONFIDENCE = 0.4
LOW_CONFIDENCE = 0.0

# 네임스페이스 URI 설정
BASE_URI = "http://factory.org/meta/"
FACT_URI = "http://factory.org/"

# 기본 모델 설정
DEFAULT_MODEL = 'sentence-transformers/all-MiniLM-L6-v2'

INPUT_DATA_FOLDER = "backend/data/ontology_input_data"
OUTPUT_DATA_FOLDER = "backend/data/ontology_output"
OUTPUT_FILE = "metadata_ontology.ttl"