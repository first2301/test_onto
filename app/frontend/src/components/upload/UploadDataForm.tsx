/**
 * 데이터 업로드 폼 컴포넌트
 * 파일 업로드 및 온톨로지 설정
 */

import { useState } from 'react';
import { Form, Button, Select, Space, Divider } from 'antd';
import FileUploader from './FileUploader';
import OntologyClassInput from '../ontology/OntologyClassInput';
import type { UploadDataResponse } from '../../types/ontology';

interface UploadDataFormProps {
  /** 제출 핸들러 */
  onSubmit: (params: {
    file: File;
    ontologyClasses: string[];
    options: {
      ontologyId?: string;
      relationType?: string;
      modelName?: string;
    };
  }) => void;
  /** 로딩 상태 */
  loading?: boolean;
  /** 기존 온톨로지 목록 (선택사항) */
  existingOntologies?: Array<{ id: string; label: string }>;
}

// 관계 타입 옵션
const RELATION_TYPE_OPTIONS = [
  { label: 'isDataOf (데이터 → 클래스)', value: 'isDataOf' },
  { label: 'hasPart (전체 → 부분)', value: 'hasPart' },
  { label: 'relatedTo (관련 관계)', value: 'relatedTo' },
  { label: 'dependsOn (의존 관계)', value: 'dependsOn' },
];

const UploadDataForm = ({
  onSubmit,
  loading,
  existingOntologies = [],
}: UploadDataFormProps) => {
  const [form] = Form.useForm();
  const [selectedFile, setSelectedFile] = useState<File | null>(null);

  const handleSubmit = (values: any) => {
    if (!selectedFile) {
      return;
    }

    const options: {
      ontologyId?: string;
      relationType?: string;
      modelName?: string;
    } = {};

    if (values.ontology_id) {
      options.ontologyId = values.ontology_id;
    }
    if (values.relation_type) {
      options.relationType = values.relation_type;
    }
    if (values.model_name) {
      options.modelName = values.model_name;
    }

    onSubmit({
      file: selectedFile,
      ontologyClasses: values.ontology_classes || [],
      options,
    });
  };

  return (
    <Form
      form={form}
      layout="vertical"
      onFinish={handleSubmit}
      initialValues={{
        ontology_classes: [],
        relation_type: 'isDataOf',
      }}
    >
      <Form.Item
        name="file"
        label="데이터 파일"
        rules={[
          {
            required: true,
            validator: () => {
              if (!selectedFile) {
                return Promise.reject(new Error('파일을 선택해주세요.'));
              }
              return Promise.resolve();
            },
          },
        ]}
      >
        <FileUploader
          onChange={(file) => setSelectedFile(file)}
          disabled={loading}
          maxSize={500}
        />
      </Form.Item>

      <Divider />

      <Form.Item
        name="ontology_classes"
        label="온톨로지 클래스"
        rules={[
          {
            required: true,
            message: '최소 1개 이상의 온톨로지 클래스를 입력해주세요.',
          },
        ]}
      >
        <OntologyClassInput />
      </Form.Item>

      {existingOntologies.length > 0 && (
        <Form.Item
          name="ontology_id"
          label="기존 온톨로지에 추가 (선택사항)"
          tooltip="기존 온톨로지 ID를 선택하면 해당 온톨로지에 관계가 추가됩니다."
        >
          <Select
            placeholder="온톨로지를 선택하세요 (선택하지 않으면 새로 생성)"
            allowClear
            showSearch
            optionFilterProp="label"
            options={existingOntologies.map((ont) => ({
              label: ont.label,
              value: ont.id,
            }))}
          />
        </Form.Item>
      )}

      <Form.Item
        name="relation_type"
        label="관계 타입"
        tooltip="데이터 간의 관계 타입을 선택하세요."
      >
        <Select options={RELATION_TYPE_OPTIONS} />
      </Form.Item>

      <Form.Item>
        <Space>
          <Button type="primary" htmlType="submit" loading={loading} size="large">
            데이터 업로드 및 온톨로지 구축
          </Button>
          <Button
            onClick={() => {
              form.resetFields();
              setSelectedFile(null);
            }}
            size="large"
            disabled={loading}
          >
            초기화
          </Button>
        </Space>
      </Form.Item>
    </Form>
  );
};

export default UploadDataForm;

