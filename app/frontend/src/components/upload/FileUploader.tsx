/**
 * 파일 업로더 컴포넌트
 * 드래그 앤 드롭 파일 업로드 지원
 */

import { useState } from 'react';
import { Upload, message } from 'antd';
import { InboxOutlined } from '@ant-design/icons';
import type { UploadFile, UploadProps } from 'antd';

const { Dragger } = Upload;

interface FileUploaderProps {
  /** 파일 변경 핸들러 */
  onChange?: (file: File | null) => void;
  /** 허용된 파일 타입 */
  accept?: string;
  /** 최대 파일 크기 (MB) */
  maxSize?: number;
  /** 업로드 가능 여부 */
  disabled?: boolean;
}

const FileUploader = ({
  onChange,
  accept = '.csv,.json,.xlsx,.xls',
  maxSize = 500,
  disabled = false,
}: FileUploaderProps) => {
  const [fileList, setFileList] = useState<UploadFile[]>([]);

  const props: UploadProps = {
    name: 'file',
    multiple: false,
    accept,
    disabled,
    fileList,
    beforeUpload: (file) => {
      // 파일 크기 검증
      const isLtMaxSize = file.size / 1024 / 1024 < maxSize;
      if (!isLtMaxSize) {
        message.error(`파일 크기는 ${maxSize}MB 이하여야 합니다.`);
        return Upload.LIST_IGNORE;
      }

      // 파일 타입 검증
      const fileExtension = file.name.split('.').pop()?.toLowerCase();
      const allowedExtensions = ['csv', 'json', 'xlsx', 'xls'];
      if (!fileExtension || !allowedExtensions.includes(fileExtension)) {
        message.error('CSV, JSON, Excel 파일만 업로드할 수 있습니다.');
        return Upload.LIST_IGNORE;
      }

      setFileList([file]);
      onChange?.(file);
      return false; // 자동 업로드 방지
    },
    onRemove: () => {
      setFileList([]);
      onChange?.(null);
    },
    onChange: (info) => {
      setFileList(info.fileList);
    },
  };

  return (
    <Dragger {...props}>
      <p className="ant-upload-drag-icon">
        <InboxOutlined />
      </p>
      <p className="ant-upload-text">클릭하거나 파일을 드래그하여 업로드</p>
      <p className="ant-upload-hint">
        CSV, JSON, Excel 파일을 업로드할 수 있습니다. (최대 {maxSize}MB)
      </p>
    </Dragger>
  );
};

export default FileUploader;

