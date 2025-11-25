/**
 * 에러 메시지 컴포넌트
 * Ant Design Alert 컴포넌트를 사용한 에러 표시
 */

import { Alert } from 'antd';

interface ErrorMessageProps {
  /** 에러 메시지 */
  message: string;
  /** 에러 설명 (선택사항) */
  description?: string;
  /** 닫기 버튼 표시 여부 */
  closable?: boolean;
  /** 닫기 이벤트 핸들러 */
  onClose?: () => void;
}

const ErrorMessage = ({
  message,
  description,
  closable = true,
  onClose,
}: ErrorMessageProps) => {
  return (
    <Alert
      message={message}
      description={description}
      type="error"
      showIcon
      closable={closable}
      onClose={onClose}
      style={{ marginBottom: 16 }}
    />
  );
};

export default ErrorMessage;

