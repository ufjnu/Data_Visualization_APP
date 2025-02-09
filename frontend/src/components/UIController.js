import ModalController from './modal/ModalController';
import GraphManager from './graph/GraphManager';
import GraphWindowController from './graph/GraphWindowController';
import ToolManager from './tool/ToolManager';
import LogManager from "./log/LogManager";
import DatasetManager from "./file/DatasetManager";
import TableManager from "./table/TableManager";

class UIController {
  constructor() {
    this.datasetManager = new DatasetManager();
    this.tableManager = new TableManager(this.datasetManager);
    this.modalController = new ModalController(); // Manages modal windows
    this.graphManager = new GraphManager(); // Manages graph creation and modification
    this.graphWindowController = new GraphWindowController(this.graphManager); // Manages graph windows
    this.toolManager = new ToolManager(); // Manages UI tools
    this.logManager = new LogManager(); // 确保 logManager 全局可用
    this.currentDatasetId = null; // 追踪当前数据集
  }


  /**
   * 获取数据（如文件列表、下载文件等）
   * @param {string} url - 请求的 API 地址
   * @returns {Promise<any>} - 返回服务器的响应数据
   */
  async fetchData(url) {
    console.log("Fetching data from:", url);
    try {
      const response = await fetch(url);
      if (!response.ok) {
        throw new Error(`Failed to fetch data from ${url}`);
      }

      // 判断是 JSON 还是文件
      const contentType = response.headers.get("content-type");
      if (contentType.includes("application/json")) {
        const data = await response.json();
        console.log("Fetched JSON data:", data);
        return data;
      } else {
        const blob = await response.blob();
        console.log("Fetched file:", url);
        return blob;
      }
    } catch (error) {
      console.error("Error fetching data:", error);
      return null;
    }
  }

  /**
   * 改变数据（如上传、删除文件）
   * @param {string} url - API 地址
   * @param {string} method - HTTP 方法（"POST"、"PUT"、"DELETE"）
   * @param {FormData | object} body - 请求的 body 数据（FormData 或 JSON）
   * @returns {Promise<any>} - 返回服务器响应数据
   */
  async modifyData(url, method, body = null) {
    console.log(`Modifying data: ${method} ${url}`, body);

    const options = {
      method,
      headers: {},
    };

    // 处理 FormData（用于文件上传）
    if (body instanceof FormData) {
      options.body = body;
    } else if (body) {
      options.body = JSON.stringify(body);
      options.headers["Content-Type"] = "application/json";
    }

    try {
      const response = await fetch(url, options);
      const data = await response.json();
      console.log("Modify response:", data);

      if (data.error) {
        throw new Error(`Error from server: ${data.error}`);
      }

      return data;
    } catch (error) {
      console.error("Modify operation failed:", error);
      return null;
    }
  }


  handleUserAction(action) {
    switch (action.type) {
      case 'OPEN_MODAL':
        this.modalController.openModal(action.modalType, action.data);
        break;
      case 'CLOSE_MODAL':
        this.modalController.closeModal();
        break;
      case 'OPEN_GRAPH_WINDOW':
        this.graphWindowController.openGraphWindow(action.graphData);
        break;
      case 'CLOSE_GRAPH_WINDOW':
        this.graphWindowController.closeGraphWindow(action.windowId);
        break;
      case 'DISPLAY_ERROR':
        alert(`Error: ${action.errorDetails}`);
        break;
      case 'DISPATCH_REQUEST':
        console.log('Dispatching request to backend:', action);
        break;

      {/*来自NewGraphModal的Action，注意这里的参数还没写完*/}
      case 'CREATE_GRAPH':
        this.graphManager.createGraph(action.type);
        this.graphWindowController.openGraphWindow();
        break;
      default:
        console.warn('Unhandled action:', action);
    }
  }

  setModalController(modalController) {
    this.modalController = modalController;
  }

  setGraphWindowController(graphWindowController) {
    this.graphWindowController = graphWindowController;
  }

  setGraphManager(graphManager) {
    this.graphManager = graphManager;
  }

  setToolManager(toolManager) {
    this.toolManager = toolManager;
  }

  setImageDisplayArea(imageDisplayArea) {
    this.imageDisplayArea = imageDisplayArea;
  }

  getGraphManager() {
    return this.graphManager;
  }

  getModalController() {
    return this.modalController;
  }

  getGraphWindowController() {
    return this.graphWindowController;
  }

  getToolManager() {
    return this.toolManager;
  }


  getImageDisplayArea() {
    return this.imageDisplayArea;
  }

  openGraphWindow(graphId) {
    return this.graphWindowController.openGraphWindowById(graphId);
  }

  closeGraphWindow(windowId) {
    return this.graphWindowController.closeGraphWindow(windowId);
  }

  getGraphWindows() {
    return this.graphWindowController.getGraphWindows();
  }

  getLogManager() {
    return this.logManager;
  }

}

export default UIController;
