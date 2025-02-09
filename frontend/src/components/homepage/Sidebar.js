import React, { useState } from "react";
import { Layout, Menu, Modal } from "antd";
import {
  BarChartOutlined,
  DatabaseOutlined,
  FileTextOutlined,
  TableOutlined,
  SettingOutlined,
  SlidersOutlined,
} from "@ant-design/icons";
import DimReductionModal from "../modal/DimReductionModal";
import modalController from "../modal/ModalController";
import NewGraphModal from "../modal/NewGraphModal";
import ReplicaManagerModal from "../modal/ReplicaManagerModal";

const { Sider } = Layout;
const { SubMenu } = Menu;

const Sidebar = ({ uiController, setShowGraph, setShowData, setShowLog, showGraph, showData, showLog }) => {
  // 直接管理窗口开关 这些开闭不用经过uicontroller 下面的工具需要uicontroller，也需要注册工具类
  const [openKeys, setOpenKeys] = useState([]); // 控制展开菜单
  const [newGraphModalVisible, setNewGraphModalVisible] = useState(false);
  const [dimReductionModalVisible, setDimReductionModalVisible] = useState(false);
  const [replicasModalVisible, setReplicasModalVisible] = useState(false);

    // ✅ 获取当前数据集 ID
  const datasetId = uiController.currentDatasetId;
  console.log("📌 Current datasetId:", datasetId);

  const handleOpenChange = (keys) => {
    setOpenKeys(keys);
  };

  return (
    <Sider width={220} style={{ background: "#fff" }}>
      <Menu
        mode="inline"
        openKeys={openKeys}
        onOpenChange={handleOpenChange}
        defaultSelectedKeys={["graphOverview"]}
        style={{ height: "100%", borderRight: 0 }}
      >
        {/* 窗口开关（Graph / DataTable / Log） */}
        <Menu.Item
          key="toggleGraph"
          icon={<BarChartOutlined />}
          onClick={() => setShowGraph(!showGraph)}
        >
          {showGraph ? "Close Graph Window" : "Open Graph Window"}
        </Menu.Item>

        <Menu.Item
          key="toggleDataTable"
          icon={<TableOutlined />}
          onClick={() => setShowData(!showData)}
        >
          {showData ? "Close Data Table" : "Open Data Table"}
        </Menu.Item>

        <Menu.Item
          key="toggleLog"
          icon={<FileTextOutlined />}
          onClick={() => setShowLog(!showLog)}
        >
          {showLog ? "Close Log Window" : "Open Log Window"}
        </Menu.Item>

        <Menu.Item//修改中 文件管理
          key="dataCopyManagement"
          icon={<SettingOutlined />}
          onClick={() => setReplicasModalVisible(true)}
        >
          Data Copy Management
        </Menu.Item>

        {/* Graph Manager */}
        <SubMenu key="graphManager" icon={<BarChartOutlined />} title="Graph Manager">
          <Menu.Item key="newGraph" onClick={() => setNewGraphModalVisible(true)}>
            New Graph
          </Menu.Item>
        </SubMenu>

        {/* Data Processing */}
        <SubMenu key="dataProcessing" icon={<BarChartOutlined />} title="Data Processing">
          <Menu.Item key="dimReduction" onClick={() => setDimReductionModalVisible(true)}>
            Dimensionality Reduction
          </Menu.Item>
        </SubMenu>
      </Menu>




      {/* modal将来要移动到别处 可能是放在modalmanager里 manager是组件 controller是逻辑*/}
      {/* 新建 Graph 的 Modal */}
      <NewGraphModal
        visible={newGraphModalVisible}
        onCancel={() => setNewGraphModalVisible(false)}
        uiController={uiController}
      />


      {/* 降维 Modal */}
       <DimReductionModal
           title="Dimensionality Reduction"
           visible={dimReductionModalVisible}
           onCancel={() => setDimReductionModalVisible(false)}
           onClose={() => setDimReductionModalVisible(false)}
           onUpdateDataset={(newData) => console.log("Updated dataset:", newData)}
           logAction={(log) => console.log("Log:", log)}
       />

       {/* data copy manage Modal */}
       <ReplicaManagerModal
           visible={replicasModalVisible}
           onClose={() => setReplicasModalVisible(false)}
           uiController={uiController}
           datasetId={datasetId}
       />

    </Sider>
  );
};

export default Sidebar;
