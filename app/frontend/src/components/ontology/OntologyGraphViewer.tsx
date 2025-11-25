/**
 * 온톨로지 그래프 뷰어 컴포넌트
 * Force-directed graph를 사용한 인터랙티브 시각화
 */

import { useMemo, useState } from 'react';
import ForceGraph2D from 'react-force-graph-2d';
import type { OntologyGraphNode, OntologyGraphEdge } from '../../types/ontology';

interface OntologyGraphViewerProps {
  /** 노드 목록 */
  nodes: OntologyGraphNode[];
  /** 엣지 목록 */
  edges: OntologyGraphEdge[];
  /** 그래프 높이 */
  height?: number;
}

// CSS 변수를 사용한 모던한 색상 팔레트
const getCssVariable = (varName: string, fallback: string = ''): string => {
  if (typeof window === 'undefined') return fallback;
  try {
    const value = getComputedStyle(document.documentElement).getPropertyValue(varName).trim();
    return value || fallback;
  } catch {
    return fallback;
  }
};

// 관계 타입별 색상 매핑 함수 (런타임에 CSS 변수 읽기)
const getRelationColor = (relationName: string): string => {
  const colorMap: Record<string, { var: string; fallback: string }> = {
    'isDataOf': { var: '--graph-edge-isDataOf', fallback: '#6366F1' },
    'hasPart': { var: '--graph-edge-hasPart', fallback: '#10B981' },
    'relatedTo': { var: '--graph-edge-relatedTo', fallback: '#F59E0B' },
    'dependsOn': { var: '--graph-edge-dependsOn', fallback: '#EF4444' },
  };
  
  const config = colorMap[relationName];
  return config ? getCssVariable(config.var, config.fallback) : getCssVariable('--graph-edge-default', '#CBD5E1');
};

// 관계 타입별 라벨 매핑
const RELATION_LABELS: Record<string, string> = {
  'isDataOf': 'isDataOf (데이터 → 클래스)',
  'hasPart': 'hasPart (전체 → 부분)',
  'relatedTo': 'relatedTo (관련 관계)',
  'dependsOn': 'dependsOn (의존 관계)',
};

const OntologyGraphViewer = ({
  nodes,
  edges,
  height = 600,
}: OntologyGraphViewerProps) => {
  const [hoveredNode, setHoveredNode] = useState<string | null>(null);
  const [hoveredLink, setHoveredLink] = useState<any | null>(null);

  // 그래프 데이터 변환
  const graphData = useMemo(() => {
    return {
      nodes: nodes.map((node) => ({
        id: node.id,
        name: node.label,
        type: node.type,
      })),
      links: edges.map((edge) => ({
        source: edge.source,
        target: edge.target,
        relation: edge.relation,
      })),
    };
  }, [nodes, edges]);

  // 노드 색상 결정 (균형잡힌 색상, 과도한 강조 방지)
  const getNodeColor = (node: any) => {
    const isHovered = hoveredNode === node.id;
    
    // 호버 시 약간만 밝게 (과도하지 않게)
    if (node.type === 'class') {
      return isHovered 
        ? getCssVariable('--graph-node-class-hover') || '#7C3AED'
        : getCssVariable('--graph-node-class') || '#6366F1';
    } else if (node.type === 'dataset') {
      return isHovered
        ? getCssVariable('--graph-node-dataset-hover') || '#059669'
        : getCssVariable('--graph-node-dataset') || '#10B981';
    }
    return isHovered
      ? getCssVariable('--graph-node-default-hover') || '#CBD5E1'
      : getCssVariable('--graph-node-default') || '#94A3B8';
  };

  // 노드 크기 결정 (작은 동그라미로 명확하게 표현, 1.5배 작게)
  const getNodeSize = (node: any) => {
    // 연결된 엣지 수에 따라 크기 조정 (작은 크기 유지)
    const linkCount = edges.filter(
      (e) => e.source === node.id || e.target === node.id
    ).length;
    // 기본 크기 4px, 최대 8px로 제한 (기존의 1.5배 작게)
    return Math.max(4, Math.min(8, 4 + linkCount * 0.67));
  };

  // 관계 타입별 엣지 색상 결정 (모던한 색상)
  const getLinkColor = (link: any) => {
    const relation = link.relation || '';
    // 관계 타입에서 실제 관계명 추출 (URI에서 마지막 부분만)
    const relationName = relation.split('#').pop()?.split('/').pop() || relation;
    return getRelationColor(relationName);
  };
  
  // 엣지 두께 결정 (균형잡힌 두께)
  const getLinkWidth = (link: any) => {
    // 호버 시 약간만 두껍게 (과도하지 않게)
    if (hoveredLink && (hoveredLink.source === link.source && hoveredLink.target === link.target)) {
      return 2.5;
    }
    return 1.5;
  };

  // 그래프에 나타나는 고유한 관계 타입 목록 추출
  const uniqueRelations = useMemo(() => {
    const relationSet = new Set<string>();
    const validRelations = ['isDataOf', 'hasPart', 'relatedTo', 'dependsOn'];
    edges.forEach((edge) => {
      const relation = edge.relation || '';
      const relationName = relation.split('#').pop()?.split('/').pop() || relation;
      if (relationName && validRelations.includes(relationName)) {
        relationSet.add(relationName);
      }
    });
    return Array.from(relationSet).sort();
  }, [edges]);

  if (nodes.length === 0) {
    return (
      <div
        style={{
          height,
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center',
          backgroundColor: getCssVariable('--bg-tertiary') || '#F1F5F9',
          borderRadius: 12,
          color: getCssVariable('--text-tertiary') || '#94A3B8',
          border: `1px solid ${getCssVariable('--graph-border') || 'rgba(0, 0, 0, 0.08)'}`,
        }}
      >
        표시할 그래프 데이터가 없습니다.
      </div>
    );
  }

  return (
    <div
      style={{
        border: `1px solid ${getCssVariable('--graph-border') || 'rgba(0, 0, 0, 0.08)'}`,
        borderRadius: 12,
        overflow: 'hidden',
        backgroundColor: getCssVariable('--graph-bg') || '#FFFFFF',
        boxShadow: getCssVariable('--graph-shadow') || '0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06)',
      }}
    >
      <ForceGraph2D
        graphData={graphData}
        nodeLabel={(node: any) => `${node.name} (${node.type})`}
        nodeColor={getNodeColor}
        nodeVal={getNodeSize}
        nodeCanvasObject={(node: any, ctx: CanvasRenderingContext2D, globalScale: number) => {
          // 노드 크기와 색상 계산
          const nodeSize = getNodeSize(node);
          const nodeColor = getNodeColor(node);
          
          // 노드 원형 그리기
          ctx.beginPath();
          ctx.arc(node.x, node.y, nodeSize, 0, 2 * Math.PI);
          ctx.fillStyle = nodeColor;
          ctx.fill();
          
          // 흰색 테두리로 명확성 향상 (노드 크기에 비례하여 작게)
          ctx.strokeStyle = '#FFFFFF';
          ctx.lineWidth = 1;
          ctx.stroke();
          
          // 텍스트 레이블 (노드 오른쪽에 배치, 1.5배 작게)
          const label = node.name || '';
          ctx.font = `${5}px -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif`;
          ctx.fillStyle = getCssVariable('--text-primary') || '#1E293B';
          ctx.textAlign = 'left';
          ctx.textBaseline = 'middle';
          ctx.fillText(label, node.x + nodeSize + 3, node.y);
        }}
        linkLabel={(link: any) => {
          const relation = link.relation || '';
          const relationName = relation.split('#').pop()?.split('/').pop() || relation;
          return RELATION_LABELS[relationName] || relation;
        }}
        linkDirectionalArrowLength={0}
        linkDirectionalArrowWidth={0}
        linkColor={getLinkColor}
        linkWidth={getLinkWidth}
        linkOpacity={0.5}
        width={800}
        height={height}
        cooldownTicks={100}
        onNodeHover={(node: any) => {
          setHoveredNode(node ? node.id : null);
        }}
        onLinkHover={(link: any) => {
          setHoveredLink(link);
        }}
        onNodeClick={(node: any) => {
          console.log('Node clicked:', node);
        }}
      />
      <div
        style={{
          padding: '12px 16px',
          backgroundColor: getCssVariable('--graph-legend-bg') || '#F8FAFC',
          borderTop: `1px solid ${getCssVariable('--graph-border') || 'rgba(0, 0, 0, 0.08)'}`,
          fontSize: 12,
          color: getCssVariable('--text-secondary') || '#64748B',
        }}
      >
        <div style={{ display: 'flex', gap: 16, alignItems: 'center', flexWrap: 'wrap' }}>
          {/* 노드 타입 범례 */}
          <div style={{ display: 'flex', gap: 12, alignItems: 'center' }}>
            <div style={{ display: 'flex', alignItems: 'center', gap: 6 }}>
              <span
                style={{
                  display: 'inline-block',
                  width: 12,
                  height: 12,
                  backgroundColor: getCssVariable('--graph-node-class') || '#6366F1',
                  borderRadius: '50%',
                }}
              />
              <span style={{ fontWeight: 400 }}>클래스</span>
            </div>
            <div style={{ display: 'flex', alignItems: 'center', gap: 6 }}>
              <span
                style={{
                  display: 'inline-block',
                  width: 12,
                  height: 12,
                  backgroundColor: getCssVariable('--graph-node-dataset') || '#10B981',
                  borderRadius: '50%',
                }}
              />
              <span style={{ fontWeight: 400 }}>데이터셋</span>
            </div>
          </div>

          {/* 관계 타입 범례 */}
          {uniqueRelations.length > 0 && (
            <div style={{ 
              display: 'flex', 
              gap: 12, 
              alignItems: 'center', 
              marginLeft: 4, 
              paddingLeft: 16, 
              borderLeft: `1px solid ${getCssVariable('--graph-border') || 'rgba(0, 0, 0, 0.08)'}` 
            }}>
              {uniqueRelations.map((relation) => (
                <div key={relation} style={{ display: 'flex', alignItems: 'center', gap: 6 }}>
                  <span
                    style={{
                      display: 'inline-block',
                      width: 18,
                      height: 2,
                      backgroundColor: getRelationColor(relation),
                      borderRadius: 1,
                      verticalAlign: 'middle',
                    }}
                  />
                  <span style={{ fontWeight: 400, fontSize: 11 }}>
                    {RELATION_LABELS[relation] || relation}
                  </span>
                </div>
              ))}
            </div>
          )}

          <div style={{ 
            marginLeft: 'auto', 
            fontWeight: 400,
            fontSize: 11,
            color: getCssVariable('--text-secondary') || '#64748B',
          }}>
            노드 {nodes.length}개 · 엣지 {edges.length}개
          </div>
        </div>
      </div>
    </div>
  );
};

export default OntologyGraphViewer;

