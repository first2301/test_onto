"""
규칙 기반 매핑 모듈
키워드 사전을 활용한 고신뢰도 매핑 전략
"""

import re
from typing import List, Optional, Tuple


class RuleBasedMapper:
    """고신뢰도 키워드 기반 규칙 매핑"""
    
    def __init__(self):
        # 도메인별 키워드 사전 (실무에서 도메인 지식 반영)
        self.keyword_rules = {
            "Injection_Molding_Machine": [
                "injection", "molding", "moulding", "plastic", "inj", "사출"
            ],
            "Welding_Robot": [
                "welding", "welder", "weld", "robot", "용접"
            ],
            "Industrial_Pump": [
                "pump", "펌프", "pressure"
            ],
            "CNC_Machine": [
                "cnc", "machining", "nc", "가공"
            ],
            "Conveyor_Belt": [
                "conveyor", "belt", "컨베이어", "transport"
            ],
            "Motor": [
                "motor", "curr", "current", "voltage", "volt", "모터"
            ],
            "Melting_Machine": [
                "melting", "melt", "molten", "주석", "주석기",
            ]
        }
    
    def preprocess_text(self, text: str) -> str:
        """텍스트 전처리 (규칙 매칭용)"""
        text = text.lower()
        text = re.sub(r'[^a-z0-9\s]', ' ', text)
        text = re.sub(r'\s+', ' ', text).strip()
        return text
    
    def match_by_keywords(self, filename: str) -> Optional[Tuple[str, float]]:
        """키워드 기반 매칭 (고신뢰도)"""
        clean_name = self.preprocess_filename(filename)
        words = clean_name.split()
        
        best_match = None
        best_score = 0.0
        
        for class_name, keywords in self.keyword_rules.items():
            matches = sum(1 for kw in keywords if kw in clean_name or any(kw in word for word in words))
            if matches > 0:
                # 매칭된 키워드 수에 비례한 점수
                score = min(0.95, 0.7 + (matches * 0.1))
                if score > best_score:
                    best_score = score
                    best_match = class_name
        
        return (best_match, best_score) if best_match else None
    
    def preprocess_filename(self, fname: str) -> str:
        """파일명 전처리"""
        name = fname.replace('.csv', '').replace('.CSV', '')
        name = re.sub(r'[_\-\d]', ' ', name)
        return name.lower().strip()

