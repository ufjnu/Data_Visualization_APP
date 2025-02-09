import React, { useState } from "react";
import { Upload, Button } from "antd";
import { UploadOutlined } from "@ant-design/icons";

const FileUpload = ({ uiController }) => {
  const [file, setFile] = useState(null);
  const [fileName, setFileName] = useState("No file selected");

  // 处理文件选择
  const uploadProps = {
    beforeUpload: (file) => {
      console.log("File selected:", file.name); // 调试信息
      setFile(file);
      setFileName(file.name);
      return false; // 阻止自动上传
    },
    onRemove: () => {
      console.log("File removed"); // 调试信息
      setFile(null);
      setFileName("No file selected");
    },
    showUploadList: false,
  };

  // 确保 uiController 存在
  if (!uiController || !uiController.modifyData) {
    console.error("Error: uiController is undefined or missing modifyData method in FileUpload!");
    return null;
  }

  // 处理文件上传
  const handleUpload = async () => {
  if (!file) {
    alert("Please select a file first!");
    return;
  }

  console.log("Uploading file:", file.name);

  const formData = new FormData();
  formData.append("file", file);

  try {
    const data = await uiController.modifyData("http://127.0.0.1:8000/data/upload/", "POST", formData);

    if (data) {
      uiController.currentDatasetId = data.id;  // ✅ 更新当前 datasetId
      console.log("Upload successful, dataset ID:", data.id);
      setFileName(data.name);
      alert(`File uploaded successfully! Dataset ID: ${data.id}`);
    } else {
      alert("Upload failed. Please try again.");
    }
  } catch (error) {
    console.error("Upload error:", error);
    alert("Upload failed. Please try again.");
  }
};


  return (
    <div style={{ display: "flex", alignItems: "center", gap: "12px" }}>
      {/* 文件名 */}
      <span style={{ minWidth: "150px", whiteSpace: "nowrap", overflow: "hidden", textOverflow: "ellipsis" }}>
        {fileName}
      </span>

      {/* 选择文件按钮 */}
      <Upload {...uploadProps} maxCount={1}>
        <Button type="primary" icon={<UploadOutlined />}>Select File</Button>
      </Upload>

      {/* 上传按钮 */}
      <Button type="primary" onClick={handleUpload} disabled={!file}>
        Upload
      </Button>
    </div>
  );
};

export default FileUpload;
