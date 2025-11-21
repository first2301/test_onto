"""
온톨로지 구축 모듈
하이브리드 매핑 결과를 기반으로 RDF 온톨로지 구축
"""

import os
import urllib.parse
import pandas as pd
from rdflib import Graph, Literal, RDF, Namespace, XSD
from typing import List

from backend.services.ontology_services.config import BASE_URI, FACT_URI, DEFAULT_MODEL
from backend.services.ontology_services.hybrid_mapper import HybridMapper
from backend.services.ontology_services.config import INPUT_DATA_FOLDER, OUTPUT_DATA_FOLDER, OUTPUT_FILE


def build_hybrid_ontology(
    ontology_classes: List[str],
    model_name: str = DEFAULT_MODEL
):
    """
    하이브리드 접근법으로 온톨로지 구축 (파일명만 사용)
    
    Args:
        input_folder: CSV 파일이 있는 폴더
        ontology_classes: 표준 온톨로지 클래스 리스트
        output_file: 출력 TTL 파일명
        model_name: SentenceTransformer 모델명
    
    Returns:
        tuple: (매핑 결과 DataFrame, RDF Graph)
    """
    print("하이브리드 온톨로지 구축을 시작합니다...")
    
    # 네임스페이스 설정
    META = Namespace(BASE_URI)
    FACT = Namespace(FACT_URI)
    g = Graph()
    g.bind("meta", META)
    g.bind("fact", FACT)
    
    # 하이브리드 매퍼 초기화
    mapper = HybridMapper(ontology_classes, model_name)
    
    # 폴더 내 파일 탐색
    if not os.path.exists(INPUT_DATA_FOLDER):
        os.makedirs(INPUT_DATA_FOLDER)
        print(f"   [안내] '{INPUT_DATA_FOLDER}' 폴더가 생성되었습니다.")
        # 빈 DataFrame과 Graph 반환
        return pd.DataFrame(), g
    
    files = [f for f in os.listdir(INPUT_DATA_FOLDER) if f.endswith((".csv", ".CSV"))]
    
    if not files:
        print(f"   [경고] '{INPUT_DATA_FOLDER}' 폴더에 CSV 파일이 없습니다.")
        # 빈 DataFrame과 Graph 반환
        return pd.DataFrame(), g
    
    # 하이브리드 매핑 수행 (파일명만 사용)
    mapping_df = mapper.map_files(files)
    
    print("\n📊 매핑 결과:")
    print(mapping_df.to_string(index=False))
    
    # 온톨로지 구축 (파일명과 온톨로지 클래스만 매핑)
    for _, row in mapping_df.iterrows():
        filename = row['Filename']
        mapped_class = row['Mapped_Class']
        confidence = row['Confidence']
        method = row['Method']
        
        if mapped_class == "Unclassified":
            print(f"   ⚠️  {filename}: 매핑 실패 (수동 검토 필요)")
            continue
        
        # URI 생성
        dataset_name = os.path.splitext(filename)[0]
        dataset_uri = FACT[urllib.parse.quote(dataset_name)]
        class_uri = FACT[urllib.parse.quote(mapped_class)]
        
        # 데이터셋 객체 생성 (파일명과 온톨로지 클래스만)
        # g.add((dataset_uri, RDF.type, META.Dataset))
        # g.add((dataset_uri, META.hasFileName, Literal(filename)))
        
        # 클래스 매핑
        g.add((dataset_uri, FACT.isDataOf, class_uri))
        
        print(f"   ✅ {filename} → {mapped_class} ({method}, confidence: {confidence:.2f})")
    
    # 결과 저장
    if len(mapping_df) > 0:  # 파일이 있을 때만 저장
        # 출력 디렉토리 생성 (없으면)
        if not os.path.exists(OUTPUT_DATA_FOLDER):
            os.makedirs(OUTPUT_DATA_FOLDER, exist_ok=True)
            print(f"   [안내] '{OUTPUT_DATA_FOLDER}' 폴더가 생성되었습니다.")
        
        output_path = os.path.join(OUTPUT_DATA_FOLDER, OUTPUT_FILE)
        g.serialize(destination=output_path, format="turtle")
        print(f"\n✅ 온톨로지 구축 완료! ({output_path})")
        
        # 통계 출력
        method_counts = mapping_df['Method'].value_counts()
        print("\n📈 매핑 방법 통계:")
        for method, count in method_counts.items():
            print(f"   {method}: {count}개")
    
    return mapping_df, g

