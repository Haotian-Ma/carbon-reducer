<template>
  <div class="classifier-container">
    <!-- Drag & Drop Area -->
    <div
      class="upload-area"
      :class="{ 'is-dragover': isDragover, 'has-preview': previewUrl }"
      @dragover.prevent="handleDragOver"
      @dragleave.prevent="isDragover = false"
      @drop.prevent="handleDrop"
      @click="triggerFileInput"
    >
      <input
        ref="fileInput"
        type="file"
        accept="image/*"
        class="file-input"
        @change="handleFileChange"
      />
      
      <div v-if="!previewUrl" class="upload-prompt">
        <p class="instruction">Drag & drop your image here</p>
        <p class="sub-instruction">or click to browse files</p>
      </div>
      
      <div v-else class="preview-container">
        <img :src="previewUrl" alt="Preview" class="preview-image" />
        <button class="clear-btn" @click.stop="clearSelection">
          ×
        </button>
      </div>
    </div>

    <!-- Action buttons -->
    <div class="action-buttons">
      <button
        class="predict-btn"
        :disabled="!selectedFile || isLoading"
        @click="submitImage"
      >
        <span v-if="!isLoading">Analyze Image</span>
        <span v-else class="spinner">Processing...</span>
      </button>
      
      <button
        v-if="previewUrl"
        class="secondary-btn"
        @click="clearSelection"
        :disabled="isLoading"
      >
        Reset
      </button>
    </div>

    <!-- Results display -->
    <div v-if="result" class="results-card">
      <h3 class="results-title">Analysis Results</h3>
      
      <div class="results-grid">
        <div class="result-item">
          <span class="result-label">Class:</span>
          <span class="result-value">{{ result.class }}</span>
        </div>
        <div class="result-item">
          <span class="result-label">Confidence:</span>
          <span class="result-value">
            {{ (result.confidence * 100).toFixed(1) }}%
            <div class="confidence-bar-container">
              <div 
                class="confidence-bar" 
                :style="{ width: result.confidence * 100 + '%' }"
              ></div>
            </div>
          </span>
        </div>
      </div>
      
      <div v-if="result.recyclingInfo" class="recycling-tip">
        <p>{{ result.recyclingInfo }}</p>
      </div>
    </div>

    <!-- Error message display -->
    <div v-if="errorMessage" class="error-message">
      <p>{{ errorMessage }}</p>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import axios from 'axios';
const API_BASE_URL = import.meta.env.VITE_API_BASE_URL
const selectedFile = ref(null);
const previewUrl = ref('');
const result = ref(null);
const isLoading = ref(false);
const isDragover = ref(false);
const errorMessage = ref('');
const fileInput = ref(null);

const handleFileChange = (e) => {
  errorMessage.value = '';
  const file = e.target.files[0];
  processSelectedFile(file);
};

const handleDragOver = () => {
  isDragover.value = true;
};

const handleDrop = (e) => {
  isDragover.value = false;
  errorMessage.value = '';
  const file = e.dataTransfer.files[0];
  
  if (!file) return;
  
  if (!file.type.startsWith('image/')) {
    errorMessage.value = 'Please upload an image file (JPEG, PNG, etc.)';
    return;
  }
  
  processSelectedFile(file);
};

const processSelectedFile = (file) => {
  if (!file) return;
  
  // Validate file size (max 5MB)
  if (file.size > 5 * 1024 * 1024) {
    errorMessage.value = 'Image size should be less than 5MB';
    return;
  }
  
  selectedFile.value = file;
  previewUrl.value = URL.createObjectURL(file);
  result.value = null;
};

const triggerFileInput = () => {
  fileInput.value.click();
};

const clearSelection = () => {
  selectedFile.value = null;
  previewUrl.value = '';
  result.value = null;
  errorMessage.value = '';
  fileInput.value.value = '';
};

const submitImage = async () => {
  if (!selectedFile.value || isLoading.value) return;
  
  isLoading.value = true;
  errorMessage.value = '';
  result.value = null;
  
  const formData = new FormData();
  formData.append('file', selectedFile.value);
  
  try {
    const response = await axios.post(`${API_BASE_URL}/api/predict`, formData, {
      headers: {
        'Content-Type': 'multipart/form-data'
      },
      timeout: 30000
    });
    
    result.value = response.data;
    
    // Add recycling info based on classification
    if (result.value.class === 'recyclable') {
      result.value.recyclingInfo = 'This item can be recycled in your blue bin.';
    } else if (result.value.class === 'hazardous') {
      result.value.recyclingInfo = 'This item requires special disposal. Please check local guidelines.';
    }
    
  } catch (error) {
    console.error('Prediction error:', error);
    errorMessage.value = error.response?.data?.message || 
                        error.message || 
                        'Failed to analyze image. Please try again.';
  } finally {
    isLoading.value = false;
  }
};
</script>

<style scoped>
.classifier-container {
  max-width: 500px;
  margin: 2rem auto;
  padding: 1.5rem;
  background-color: #fff;
  border-radius: 12px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
  font-family: 'Segoe UI', system-ui, sans-serif;
}

.upload-area {
  position: relative;
  width: 100%;
  height: 250px;
  border: 2px dashed #d1d5db;
  border-radius: 10px;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: all 0.3s ease;
  background-color: #f9fafb;
  overflow: hidden;
}

.upload-area.is-dragover {
  border-color: #3b82f6;
  background-color: #eff6ff;
}

.upload-area.has-preview {
  border-style: solid;
  border-color: #e5e7eb;
  background-color: #fff;
}

.upload-prompt {
  text-align: center;
  padding: 1rem;
}

.instruction {
  font-size: 1.1rem;
  font-weight: 500;
  color: #374151;
  margin-bottom: 0.25rem;
}

.sub-instruction {
  font-size: 0.9rem;
  color: #6b7280;
}

.preview-container {
  position: relative;
  width: 100%;
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
}

.preview-image {
  max-width: 100%;
  max-height: 100%;
  object-fit: contain;
  border-radius: 6px;
}

.clear-btn {
  position: absolute;
  top: 0.5rem;
  right: 0.5rem;
  width: 32px;
  height: 32px;
  border-radius: 50%;
  background-color: rgba(0, 0, 0, 0.6);
  color: white;
  display: flex;
  align-items: center;
  justify-content: center;
  border: none;
  cursor: pointer;
  transition: background-color 0.2s;
  font-size: 1.2rem;
  line-height: 1;
}

.clear-btn:hover {
  background-color: rgba(0, 0, 0, 0.8);
}

.file-input {
  display: none;
}

.action-buttons {
  display: flex;
  gap: 0.75rem;
  margin-top: 1.5rem;
  justify-content: center;
}

.predict-btn, .secondary-btn {
  padding: 0.75rem 1.5rem;
  border-radius: 8px;
  font-weight: 500;
  font-size: 0.95rem;
  cursor: pointer;
  transition: all 0.2s;
  border: none;
}

.predict-btn {
  background-color: #3b82f6;
  color: white;
}

.predict-btn:hover:not(:disabled) {
  background-color: #2563eb;
}

.predict-btn:disabled {
  background-color: #bfdbfe;
  cursor: not-allowed;
}

.secondary-btn {
  background-color: #f3f4f6;
  color: #4b5563;
}

.secondary-btn:hover:not(:disabled) {
  background-color: #e5e7eb;
}

.spinner {
  display: inline-block;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

.results-card {
  margin-top: 1.5rem;
  padding: 1.25rem;
  background-color: #f8fafc;
  border-radius: 10px;
  border: 1px solid #e2e8f0;
}

.results-title {
  font-size: 1.1rem;
  color: #1e293b;
  margin-bottom: 1rem;
  padding-bottom: 0.5rem;
  border-bottom: 1px solid #e2e8f0;
}

.results-grid {
  display: grid;
  grid-template-columns: max-content 1fr;
  gap: 0.75rem 1rem;
}

.result-item {
  display: contents;
}

.result-label {
  font-weight: 500;
  color: #475569;
}

.result-value {
  color: #1e293b;
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.confidence-bar-container {
  width: 100px;
  height: 6px;
  background-color: #e5e7eb;
  border-radius: 3px;
  overflow: hidden;
}

.confidence-bar {
  height: 100%;
  background-color: #3b82f6;
  border-radius: 3px;
  transition: width 0.3s ease;
}

.recycling-tip {
  margin-top: 1rem;
  padding: 0.75rem;
  background-color: #ecfdf5;
  border-radius: 8px;
  border-left: 4px solid #10b981;
}

.recycling-tip p {
  margin: 0;
  color: #065f46;
  font-size: 0.9rem;
}

.error-message {
  margin-top: 1rem;
  padding: 0.75rem;
  background-color: #fef2f2;
  border-radius: 8px;
  border-left: 4px solid #ef4444;
}

.error-message p {
  margin: 0;
  color: #b91c1c;
  font-size: 0.9rem;
}

/* Responsive adjustments */
@media (max-width: 640px) {
  .classifier-container {
    padding: 1rem;
    margin: 1rem auto;
  }
  
  .upload-area {
    height: 200px;
  }
  
  .action-buttons {
    flex-direction: column;
  }
  
  .predict-btn, .secondary-btn {
    width: 100%;
  }
}
</style>