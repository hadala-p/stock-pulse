<template>
  <div class="modal-overlay" @click.self="close">
    <div class="modal-content">
      <div class="modal-header">
        <h5 class="modal-title">Predict new data</h5>
        <button type="button" class="btn-close" @click="close"></button>
      </div>
      <div class="modal-body">
        <input class="form-control" v-model="companyName" placeholder="Company name" /><br/>
        <div
            :class="['drag-drop-area', { 'file-dropped': fileDropped }]"
            @dragover.prevent
            @drop.prevent="handleFileDrop"
            @click="triggerFileInput"
        >
          <p :class="{ 'file-dropped': fileDropped }">Drag and drop the file here or click to select a file</p>
          <input
              type="file"
              ref="fileInputRef"
              @change="handleFileChange"
              style="display: none;"
          />
        </div>
      </div>
      <br/>
      <div class="modal-footer">
        <button type="button" class="btn btn-primary" @click="upload">
          Upload
        </button>
        <button type="button" class="btn btn-secondary" @click="close">
          Close
        </button>
      </div>
    </div>
  </div>
</template>

<script>
import { ref } from 'vue';
const apiURL = process.env.VUE_APP_BACKEND_URL;
const axios = require('axios');

export default {
  name: 'AddPredictionModal',
  emits: ['close', 'new-stock'],
  setup(props, { emit }) {
    const fileInputRef = ref(null);
    const companyName = ref('');
    const file = ref(null);
    const fileDropped = ref(false);

    const triggerFileInput = () => {
      fileInputRef.value.click();
    };

    const handleFileDrop = (event) => {
      if (fileDropped.value === true) {
        return;
      }
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
      file.value = file;
    };

    const validateFile = (json) => {
      if (
          typeof json === 'object' &&
          json !== null &&
          Array.isArray(json)
      ) {
        fileDropped.value = true; 
        file.value = json;
      } else {
        fileDropped.value = false;
        alert('Invalid format. The JSON file should contain the data array');
      }
    };

    const close = () => {
      emit('close');
    };

    const upload = () => 
    {
      if (file.value === null) {
        alert('Please select a file.');
        return;
      }
      
      if (companyName.value === '') {
        alert('Please enter the company name.');
        return;
      }

      let jsonToUpload = {
        companyName: companyName.value,
        predictionStartOffset: 0,
        predictionDays: 30,
        baseData: file.value,
      };

      axios({
            method: 'post',
            url: `${apiURL}/prediction/post`,
            data: jsonToUpload,
            headers: {
              "Content-Type": "application/json",
              Authorization: `${localStorage.getItem('token')}`
            }
        }).then(response => {
            if (response.status !== 200) 
            {
              close();
              alert('Error uploading prediction');
              return;
            }
            
            close();
            emit('new-stock');
        }).catch((err) => {
          close();
          alert(`Error uploading prediction: ${err}`);
          return;
        });
    };

    return {
      fileInputRef,
      triggerFileInput,
      handleFileDrop,
      handleFileChange,
      close,
      upload,
      companyName,
      fileDropped,
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

.drag-drop-area.file-dropped {
  background-color: #b5f3c4;
}
.drag-drop-area.file-dropped>p {
  transition: 0.5s;
  font-size: 0rem;
}
</style>
