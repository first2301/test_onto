/**
 * RDF Graph 뷰어 컴포넌트
 * Turtle 형식의 RDF Graph를 표시하고 다운로드
 */

import { useState } from 'react';
import { Card, Button, Space, message } from 'antd';
import { CopyOutlined, DownloadOutlined } from '@ant-design/icons';

interface RDFGraphViewerProps {
  /** RDF Graph (Turtle 형식) */
  graph: string;
  /** 제목 */
  title?: string;
}

const RDFGraphViewer = ({ graph, title = 'RDF Graph (Turtle)' }: RDFGraphViewerProps) => {
  const [copied, setCopied] = useState(false);

  const handleCopy = async () => {
    try {
      await navigator.clipboard.writeText(graph);
      setCopied(true);
      message.success('클립보드에 복사되었습니다.');
      setTimeout(() => setCopied(false), 2000);
    } catch (error) {
      message.error('복사에 실패했습니다.');
    }
  };

  const handleDownload = () => {
    const blob = new Blob([graph], { type: 'text/turtle' });
    const url = URL.createObjectURL(blob);
    const link = document.createElement('a');
    link.href = url;
    link.download = `ontology_${new Date().getTime()}.ttl`;
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
    URL.revokeObjectURL(url);
    message.success('파일이 다운로드되었습니다.');
  };

  return (
    <Card
      title={title}
      extra={
        <Space>
          <Button
            icon={<CopyOutlined />}
            onClick={handleCopy}
            disabled={!graph}
          >
            {copied ? '복사됨' : '복사'}
          </Button>
          <Button
            type="primary"
            icon={<DownloadOutlined />}
            onClick={handleDownload}
            disabled={!graph}
          >
            다운로드 (.ttl)
          </Button>
        </Space>
      }
    >
      {graph ? (
        <pre
          style={{
            backgroundColor: '#f5f5f5',
            padding: 16,
            borderRadius: 4,
            overflow: 'auto',
            maxHeight: 600,
            fontSize: 12,
            fontFamily: 'monospace',
            whiteSpace: 'pre-wrap',
            wordBreak: 'break-word',
          }}
        >
          {graph}
        </pre>
      ) : (
        <div style={{ textAlign: 'center', color: '#999', padding: 40 }}>
          RDF Graph 데이터가 없습니다.
        </div>
      )}
    </Card>
  );
};

export default RDFGraphViewer;

