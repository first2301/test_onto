/**
 * 온톨로지 클래스 입력 컴포넌트
 * 다중 선택 가능한 입력 필드
 */

import { useState } from 'react';
import { Select, Tag, Input, Typography } from 'antd';
import type { SelectProps } from 'antd';

const { Option } = Select;
const { Text } = Typography;

interface OntologyClassInputProps {
  /** 선택된 클래스 목록 */
  value?: string[];
  /** 값 변경 핸들러 */
  onChange?: (value: string[]) => void;
  /** 기본 제공 클래스 목록 */
  defaultClasses?: string[];
}

// 기본 제공 온톨로지 클래스 목록
const DEFAULT_ONTOLOGY_CLASSES = [
  'Injection_Molding_Machine',
  'Welding_Robot',
  'CNC_Machine',
  'Industrial_Pump',
  'Conveyor_Belt',
  'Motor',
  'Melting_Machine',
];

const OntologyClassInput = ({
  value = [],
  onChange,
  defaultClasses = DEFAULT_ONTOLOGY_CLASSES,
}: OntologyClassInputProps) => {
  const [inputValue, setInputValue] = useState('');

  const handleChange = (selectedValues: string[]) => {
    onChange?.(selectedValues);
  };

  // 입력값 검증 및 정규화
  const validateAndNormalize = (input: string): string | null => {
    // 공백 제거
    const trimmed = input.trim();
    
    // 빈 문자열 체크
    if (!trimmed) {
      return null;
    }
    
    // 최소/최대 길이 체크
    if (trimmed.length < 2) {
      return null; // 너무 짧음
    }
    if (trimmed.length > 50) {
      return null; // 너무 김
    }
    
    // 유효한 문자만 허용 (영문, 숫자, 언더스코어, 하이픈)
    // 단, 첫 글자는 영문자 또는 언더스코어만 허용
    const validPattern = /^[A-Za-z_][A-Za-z0-9_-]*$/;
    if (!validPattern.test(trimmed)) {
      return null; // 유효하지 않은 문자 포함
    }
    
    return trimmed;
  };

  const handleInputConfirm = () => {
    const normalized = validateAndNormalize(inputValue);
    if (normalized && !value.includes(normalized)) {
      onChange?.([...value, normalized]);
      setInputValue('');
    } else if (inputValue.trim()) {
      // 검증 실패 시 입력값만 초기화 (사용자에게 피드백은 시각적으로 제공)
      setInputValue('');
    }
  };

  const tagRender: SelectProps['tagRender'] = (props) => {
    const { label, closable, onClose } = props;
    return (
      <Tag
        closable={closable}
        onClose={onClose}
        style={{ marginRight: 3 }}
      >
        {label}
      </Tag>
    );
  };

  return (
    <div>
      <Select
        mode="tags"
        value={value}
        onChange={handleChange}
        placeholder="온톨로지 클래스를 입력하거나 선택하세요"
        style={{ width: '100%' }}
        tagRender={tagRender}
        dropdownRender={(menu) => (
          <>
            {menu}
            <div style={{ padding: '8px', borderTop: '1px solid #f0f0f0' }}>
              <Input
                value={inputValue}
                placeholder="새 클래스 입력 후 Enter (영문, 숫자, _, - 만 허용)"
                onChange={(e) => setInputValue(e.target.value)}
                onPressEnter={handleInputConfirm}
                onBlur={handleInputConfirm}
                status={inputValue && !validateAndNormalize(inputValue) ? 'error' : ''}
              />
              <Text type="secondary" style={{ fontSize: 11, display: 'block', marginTop: 4 }}>
                💡 직접 입력하거나 드롭다운에서 선택하세요. 클래스명은 영문자로 시작해야 합니다.
              </Text>
            </div>
          </>
        )}
      >
        {defaultClasses.map((className) => (
          <Option key={className} value={className}>
            {className}
          </Option>
        ))}
      </Select>
      <Text type="secondary" style={{ fontSize: 12, display: 'block', marginTop: 4 }}>
        {value.length > 0 ? `선택된 클래스: ${value.length}개` : '최소 1개 이상의 온톨로지 클래스를 입력해주세요.'}
      </Text>
    </div>
  );
};

export default OntologyClassInput;

