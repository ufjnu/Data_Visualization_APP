class ModalController {
  constructor() {
    this.modalActive = false;
    this.activeModal = null;
    this.data = null;
  }

  openModal(modalType, data = null) {
    this.modalActive = true;
    this.activeModal = modalType;
    this.data = data;
    console.log(`Opened modal: ${modalType}`, data);
  }

  closeModal() {
    this.modalActive = false;
    this.activeModal = null;
    this.data = null;
    console.log('Closed modal');
  }

  updateModalData(newData) {
    if (this.modalActive) {
      this.data = newData;
      console.log('Updated modal data:', newData);
    } else {
      console.warn('Cannot update modal data. No modal is active.');
    }
  }

  isModalActive(modalType) {
    return this.modalActive && this.activeModal === modalType;
  }

  getActiveModal() {
    return this.activeModal;
  }

  getModalData() {
    return this.data;
  }
}

export default ModalController;
