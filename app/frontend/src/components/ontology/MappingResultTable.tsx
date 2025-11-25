/**
 * 매핑 결과 테이블 컴포넌트
 * 온톨로지 매핑 결과를 테이블로 표시
 */

import { Table, Tag } from 'antd';
import type { ColumnsType } from 'antd/es/table';

interface MappingResult {
  [key: string]: any;
  filename?: string;
  mapped_class?: string;
  confidence?: number;
  method?: string;
}

interface MappingResultTableProps {
  /** 매핑 결과 데이터 */
  data: Array<Record<string, any>>;
  /** 로딩 상태 */
  loading?: boolean;
}

const MappingResultTable = ({ data, loading }: MappingResultTableProps) => {
  // 데이터가 비어있으면 빈 테이블 표시
  if (!data || data.length === 0) {
    return (
      <Table
        dataSource={[]}
        columns={[]}
        loading={loading}
        locale={{ emptyText: '매핑 결과가 없습니다.' }}
      />
    );
  }

  // 첫 번째 행의 키를 기반으로 컬럼 생성
  const firstRow = data[0];
  const columns: ColumnsType<MappingResult> = Object.keys(firstRow).map(
    (key) => {
      // 특정 키에 대한 특별한 렌더링
      if (key.toLowerCase().includes('confidence') || key.toLowerCase().includes('score')) {
        return {
          title: key,
          dataIndex: key,
          key: key,
          sorter: (a: MappingResult, b: MappingResult) => {
            const aVal = Number(a[key]) || 0;
            const bVal = Number(b[key]) || 0;
            return aVal - bVal;
          },
          render: (value: any) => {
            const numValue = Number(value);
            if (isNaN(numValue)) return value;
            const color = numValue >= 0.8 ? 'green' : numValue >= 0.5 ? 'orange' : 'red';
            return <Tag color={color}>{numValue.toFixed(3)}</Tag>;
          },
        };
      }

      if (key.toLowerCase().includes('method') || key.toLowerCase().includes('type')) {
        return {
          title: key,
          dataIndex: key,
          key: key,
          render: (value: any) => <Tag>{String(value)}</Tag>,
        };
      }

      return {
        title: key,
        dataIndex: key,
        key: key,
        sorter: (a: MappingResult, b: MappingResult) => {
          const aVal = String(a[key] || '');
          const bVal = String(b[key] || '');
          return aVal.localeCompare(bVal);
        },
      };
    }
  );

  return (
    <Table
      dataSource={data.map((row, index) => ({ ...row, key: index }))}
      columns={columns}
      loading={loading}
      pagination={{
        pageSize: 10,
        showSizeChanger: true,
        showTotal: (total) => `총 ${total}개`,
      }}
      scroll={{ x: 'max-content' }}
    />
  );
};

export default MappingResultTable;

