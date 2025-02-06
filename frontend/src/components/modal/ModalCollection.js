import React from "react";
import { Modal, Select, Progress, Button } from "antd";

const ModalCollection = ({ uiController }) => {
  const modalController = uiController.getModalController();
  const modalData = modalController.getModalData();

  return (
    <>
      {/* 下载文件的 Modal */}
      <Modal
        title="Select Download Format"
        visible={modalController.isModalActive("download")}
        onOk={() => {
          modalController.closeModal();
          uiController.downloadFile(modalData?.format || "csv");
        }}
        onCancel={() => modalController.closeModal()}
      >
        <Select
          defaultValue={modalData?.format || "csv"}
          style={{ width: "100%" }}
          onChange={(value) => modalData.format = value}
        >
          <Select.Option value="csv">CSV</Select.Option>
          <Select.Option value="json">JSON</Select.Option>
          <Select.Option value="xlsx">Excel</Select.Option>
        </Select>
      </Modal>

      {/* 上传进度的 Modal */}
      <Modal
        title="Uploading File"
        visible={modalController.isModalActive("uploadProgress")}
        footer={null}
        closable={false}
      >
        <Progress percent={modalData?.progress || 0} />
      </Modal>

      {/* 删除确认的 Modal */}
      <Modal
        title="Confirm Deletion"
        visible={modalController.isModalActive("deleteConfirmation")}
        onOk={() => {
          modalController.closeModal();
          modalData?.onConfirm();
        }}
        onCancel={() => modalController.closeModal()}
      >
        <p>{modalData?.message || "Are you sure you want to delete this item?"}</p>
      </Modal>
    </>
  );
};

export default ModalCollection;
