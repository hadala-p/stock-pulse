<template>
  <div class="modal-overlay" @click.self="close">
    <div class="modal-content">
      <div class="modal-header">
        <h5 class="modal-title">Add New Prediction</h5>
        <button type="button" class="btn-close" @click="close"></button>
      </div>
      <div class="modal-body">
        <div
            class="drag-drop-area"
            @dragover.prevent
            @drop.prevent="handleFileDrop"
            @click="triggerFileInput"
        >
          <p>Drag and drop the file here or click to select a file</p>
          <input
              type="file"
              ref="fileInputRef"
              @change="handleFileChange"
              style="display: none;"
          />
        </div>
      </div>
      <div class="modal-footer">
        <button type="button" class="btn btn-secondary" @click="close">
          Close
        </button>
      </div>
    </div>
  </div>
</template>

<script>
import { ref } from 'vue';

export default {
  name: 'AddPredictionModal',
  emits: ['close', 'new-stock'],
  setup(props, { emit }) {
    const fileInputRef = ref(null);

    const triggerFileInput = () => {
      fileInputRef.value.click();
    };

    const handleFileDrop = (event) => {
      const files = event.dataTransfer.files;
      handleFile(files[0]);
    };

    const handleFileChange = (event) => {
      const files = event.target.files;
      handleFile(files[0]);
    };

    const handleFile = (file) => {
      const reader = new FileReader();
      reader.onload = (e) => {
        try {
          const json = JSON.parse(e.target.result);
          validateFile(json);
        } catch (error) {
          alert('Incorrect JSON file.');
        }
      };
      reader.readAsText(file);
    };

    const validateFile = (json) => {
      if (
          typeof json === 'object' &&
          json !== null &&
          'companyName' in json &&
          'baseData' in json &&
          Array.isArray(json.baseData)
      ) {
        const newStock = {
          id: json.companyName,
          name: json.companyName,
          change: 0,
          image: null,
          baseData: json.baseData,
        };
        emit('new-stock', newStock);
        close();
      } else {
        alert(
            'Invalid format. The JSON file should contain the keys "companyName" (string) and "baseData" (array).'
        );
      }
    };

    const close = () => {
      emit('close');
    };

    return {
      fileInputRef,
      triggerFileInput,
      handleFileDrop,
      handleFileChange,
      close,
    };
  },
};
</script>

<style scoped>
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1050;
}

.modal-content {
  background-color: white;
  border-radius: 0.3rem;
  width: 80%;
  max-width: 600px;
  max-height: 90%;
  overflow-y: auto;
  position: relative;
  padding: 1rem;
}

.modal-header,
.modal-footer {
  display: flex;
  justify-content: flex-end;
  align-items: center;
}

.modal-header .modal-title {
  flex: 1;
  margin: 0;
  text-align: left;
}

.modal-footer {
  justify-content: flex-end;
}

.btn-close {
  background: transparent;
  border: none;
  font-size: 1.5rem;
  line-height: 1;
  cursor: pointer;
}

.drag-drop-area {
  border: 0.1rem dashed #ced4da;
  border-radius: 0.3rem;
  padding: 2.5rem;
  text-align: center;
  cursor: pointer;
  transition: background-color 0.3s;
}

.drag-drop-area:hover {
  background-color: #f8f9fa;
}

.drag-drop-area p {
  margin: 0;
  font-size: 1.2rem;
  color: #6c757d;
}
</style>
