"""
시맨틱 매핑 모듈
임베딩 기반 시맨틱 유사도 매핑 전략
"""

import pandas as pd
from sentence_transformers import SentenceTransformer, util
from typing import List


class SemanticMapper:
    """임베딩 기반 시맨틱 매핑"""
    
    def __init__(self, model_name: str = 'sentence-transformers/all-MiniLM-L6-v2'):
        self.model = SentenceTransformer(model_name)
    
    def preprocess_filename(self, fname: str) -> str:
        """파일명 전처리 (시맨틱 매칭용)"""
        name = fname.replace('.csv', '').replace('_', ' ').replace('-', ' ')
        return name.strip()
    
    def map_semantic(self, files: List[str], classes: List[str]) -> pd.DataFrame:
        """시맨틱 매핑 수행"""
        clean_names = [self.preprocess_filename(f) for f in files]
        embeddings_files = self.model.encode(clean_names)
        embeddings_classes = self.model.encode(classes)
        
        scores = util.cos_sim(embeddings_files, embeddings_classes)
        
        results = []
        for i, fname in enumerate(files):
            best_idx = scores[i].argmax().item()
            best_score = scores[i][best_idx].item()
            best_class = classes[best_idx]
            
            results.append({
                "Filename": fname,
                "Interpreted_As": clean_names[i],
                "Mapped_Class": best_class,
                "Confidence": round(best_score, 3)
            })
        
        return pd.DataFrame(results)

