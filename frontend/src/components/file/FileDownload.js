import React, { useState } from "react";
import { Button, Modal, Select } from "antd";
import { DownloadOutlined } from "@ant-design/icons";

const FileDownload = ({ uiController }) => {
  const [downloadFormat, setDownloadFormat] = useState("csv");

  // 确保 uiController 存在，避免 undefined 错误
  if (!uiController || !uiController.fetchData || !uiController.getModalController) {
    console.error("Error: uiController is missing fetchData or getModalController in FileDownload!");
    return null;
  }

  // 处理文件下载 记得改路径
  const handleDownload = async () => {
    console.log("Starting file download:", downloadFormat);

    // 关闭 Modal
    uiController.getModalController().closeModal();

    try {
      const blob = await uiController.fetchData(`http://127.0.0.1:8000/api/download?format=${downloadFormat}`);

      if (blob) {
        console.log("File download successful:", downloadFormat);
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement("a");
        a.href = url;
        a.download = `dataset.${downloadFormat}`;
        document.body.appendChild(a);
        a.click();
        window.URL.revokeObjectURL(url);
        alert("Download started!");
      } else {
        alert("Download failed. Please try again.");
      }
    } catch (error) {
      console.error("Download error:", error);
      alert("Download failed. Please try again.");
    }
  };

  return (
    <div style={{ display: "flex", alignItems: "center", gap: "12px" }}>
      {/* 下载按钮 */}
      <Button
        icon={<DownloadOutlined />}
        onClick={() => uiController.getModalController().openModal("download", { format: "csv" })}
      >
        Download File
      </Button>

      {/* 选择文件格式的 Modal */}
      <Modal
        title="Select Download Format"
        visible={uiController.getModalController().isModalActive("download")}
        onOk={handleDownload}
        onCancel={() => uiController.getModalController().closeModal()}
      >
        <Select
          defaultValue="csv"
          style={{ width: "100%" }}
          onChange={(value) => setDownloadFormat(value)}
        >
          <Select.Option value="csv">CSV</Select.Option>
          <Select.Option value="json">JSON</Select.Option>
          <Select.Option value="xlsx">Excel</Select.Option>
        </Select>
      </Modal>
    </div>
  );
};

export default FileDownload;
