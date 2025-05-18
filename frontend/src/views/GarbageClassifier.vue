<template>
  <div class="classifier-container">
    <div class="classifier-card">
      <div class="card-header">
        <h2><i class="fas fa-recycle me-2"></i>Garbage Classifier</h2>
        <p class="subtitle">Upload an image to identify waste type</p>
      </div>

      <div class="upload-section">
        <div class="file-drop-area" @dragover.prevent="dragover = true" @dragleave.prevent="dragover = false"
          @drop.prevent="onFileDrop" :class="{ 'active-dropzone': dragover }">
          <input type="file" accept="image/*" @change="onFileChange" id="file-input" class="file-input" />

          <div v-if="!previewUrl" class="upload-prompt">
            <i class="fas fa-cloud-upload-alt upload-icon"></i>
            <p>Drag and drop an image or <label for="file-input" class="file-label">browse</label></p>
            <p class="upload-hint">Supported formats: JPG, PNG, JPEG</p>
          </div>

          <div v-else class="image-preview-container">
            <img :src="previewUrl" alt="Preview" class="image-preview" />
            <button class="change-image-btn" @click="resetImage">
              <i class="fas fa-redo-alt me-1"></i> Change image
            </button>
          </div>
        </div>

        <button class="predict-btn" :disabled="!file || loading" @click="upload" v-if="file && !result">
          <i class="fas fa-search me-2"></i>
          {{ loading ? 'Analyzing...' : 'Identify Waste Type' }}
          <span v-if="loading" class="spinner-border spinner-border-sm ms-2" role="status"></span>
        </button>
      </div>

      <div v-if="error" class="error-message">
        <i class="fas fa-exclamation-circle me-2"></i>{{ error }}
      </div>

      <div v-if="result" class="result-section">
        <div class="result-header">
          <div class="result-badge" :class="getWasteTypeClass(result.class)">
            {{ result.class }}
          </div>
          <div class="confidence-meter">
            <div class="confidence-label">Confidence:</div>
            <div class="progress">
              <div class="progress-bar" role="progressbar" :style="{ width: `${result.confidence * 100}%` }">
                {{ (result.confidence * 100).toFixed(0) }}%
              </div>
            </div>
          </div>
        </div>

        <div class="waste-instructions">
          <h3>How to dispose of {{ result.class }}</h3>
          <div class="instruction-content" v-html="getWasteInstructions(result.class)"></div>
        </div>

        <button class="classify-another-btn" @click="resetAll">
          <i class="fas fa-redo me-2"></i>Classify Another Item
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import axios from 'axios'

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL;
const file = ref(null)
const previewUrl = ref('')
const loading = ref(false)
const error = ref('')
const result = ref(null)
const dragover = ref(false)

/**
 * Handler when the user selects a file.
 */
function onFileChange(e) {
  error.value = ''
  result.value = null
  file.value = e.target.files[0] || null
  if (file.value) {
    previewUrl.value = URL.createObjectURL(file.value)
  }
}

/**
 * Handler for drag and drop file upload
 */
function onFileDrop(e) {
  dragover.value = false
  const droppedFile = e.dataTransfer.files[0]
  if (droppedFile && droppedFile.type.match('image.*')) {
    error.value = ''
    result.value = null
    file.value = droppedFile
    previewUrl.value = URL.createObjectURL(droppedFile)
  } else {
    error.value = 'Please drop an image file'
  }
}

/**
 * Reset the image selection
 */
function resetImage() {
  file.value = null
  previewUrl.value = ''
  result.value = null
  error.value = ''
}

/**
 * Reset everything to start over
 */
function resetAll() {
  resetImage()
}

/**
 * Uploads the selected image to the backend and retrieves prediction.
 */
async function upload() {
  if (!file.value) return
  loading.value = true
  error.value = ''
  result.value = null

  const form = new FormData()
  form.append('file', file.value)

  try {
    const res = await axios.post(`${API_BASE_URL}/api/predict`, form, {
      headers: { 'Content-Type': 'multipart/form-data' },
      timeout: 60000
    })
    result.value = res.data
  } catch (e) {
    // Prefer backend-provided error message
    error.value = e.response?.data?.error
      || e.message
      || 'An unexpected error occurred'
  } finally {
    loading.value = false
  }
}

/**
 * Returns CSS class based on waste type
 */
function getWasteTypeClass(wasteType) {
  const typeClasses = {
    'glass': 'badge-glass',
    'paper': 'badge-paper',
    'cardboard': 'badge-cardboard',
    'plastic': 'badge-plastic',
    'metal': 'badge-metal',
    'trash': 'badge-trash'
  }

  // Convert to lowercase for case-insensitive matching
  const lowerType = wasteType.toLowerCase();
  return typeClasses[lowerType] || 'badge-default'
}

/**
 * Returns disposal instructions for each waste type
 */
function getWasteInstructions(wasteType) {
  // Convert to lowercase for case-insensitive matching
  const lowerType = wasteType.toLowerCase();

  const instructions = {
    'glass': `
      <ul>
        <li>Rinse containers thoroughly to remove food and liquid residues</li>
        <li>Remove any non-glass components (lids, corks, metal rings)</li>
        <li>Sort by color if required by your local recycling program</li>
        <li>Place in dedicated glass recycling bins (often green or white)</li>
        <li>Do not mix with other recyclables as broken glass can contaminate other materials</li>
        <li>Note that window glass, mirrors, and cookware glass generally cannot be recycled with containers</li>
      </ul>
    `,
    'paper': `
      <ul>
        <li>Keep paper clean and dry - wet or soiled paper usually cannot be recycled</li>
        <li>Remove plastic wrapping, tape, and metal fasteners</li>
        <li>Separate glossy magazines from regular paper if required locally</li>
        <li>Shredded paper should be contained in a paper bag marked "shredded paper"</li>
        <li>Place in blue recycling bins or paper-specific collection points</li>
        <li>Consider reusing or repurposing clean paper before recycling</li>
      </ul>
    `,
    'cardboard': `
      <ul>
        <li>Break down and flatten all boxes to save space</li>
        <li>Remove all packaging materials (foam, plastic, etc.)</li>
        <li>Remove any tape, labels, and staples if possible</li>
        <li>Keep cardboard dry and clean - greasy pizza boxes should go in compost or trash</li>
        <li>Bundle large quantities with twine or place in larger cardboard containers</li>
        <li>Place in blue recycling bins or cardboard-specific collection points</li>
      </ul>
    `,
    'plastic': `
      <ul>
        <li>Check the recycling number (1-7) inside the triangle symbol</li>
        <li>Rinse containers to remove food residue and liquids</li>
        <li>Remove lids, caps, and labels when possible</li>
        <li>Crush containers to save space in recycling bins</li>
        <li>Place in blue recycling bins or plastic-specific collection points</li>
        <li>Note that some municipalities only accept certain types of plastic - check local guidelines</li>
      </ul>
    `,
    'metal': `
      <ul>
        <li>Rinse cans and containers to remove food and liquid residue</li>
        <li>Remove paper labels when possible</li>
        <li>Crush aluminum cans to save space (if required by your recycling program)</li>
        <li>Small metal items like bottle caps can be collected inside a metal can</li>
        <li>Place in blue recycling bins or metal-specific collection points</li>
        <li>Larger metal items may require special handling or drop-off at scrap yards</li>
      </ul>
    `,
    'trash': `
      <ul>
        <li>Place in general waste containers or black bins</li>
        <li>Seal items that might leak or create odors in closed bags</li>
        <li>Double-check if any components could be recycled before disposal</li>
        <li>Consider if the item could be donated or repurposed instead</li>
        <li>Follow local regulations for waste disposal</li>
        <li>Reduce general waste by choosing recyclable or compostable alternatives when possible</li>
      </ul>
    `
  }

  return instructions[lowerType] || '<p>No specific instructions available for this waste type.</p>'
}
</script>

<style scoped>
.classifier-container {
  display: flex;
  justify-content: center;
  align-items: center;
  padding: 2rem;
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
  width: 100%;
  max-width: 100%;
  box-sizing: border-box;
}

.classifier-card {
  width: 100%;
  max-width: 900px;

  min-width: 600px;

  border-radius: 16px;
  box-shadow: 0 8px 30px rgba(0, 0, 0, 0.12);
  background-color: #fff;
  overflow: hidden;
}

.card-header {
  background: linear-gradient(135deg, #43a047 0%, #1b5e20 100%);
  color: white;
  padding: 1.5rem;
  text-align: center;
}

.card-header h2 {
  margin: 0;
  font-size: 2rem;
  font-weight: 600;
}

.subtitle {
  margin-top: 0.5rem;
  font-size: 1.1rem;
  opacity: 0.9;
}

.upload-section {
  padding: 2rem;
}

.file-drop-area {
  border: 2px dashed #cfd8dc;
  border-radius: 12px;
  padding: 3rem 2rem;
  text-align: center;
  cursor: pointer;
  transition: all 0.3s ease;
  background-color: #f8f9fa;
  position: relative;
  min-height: 250px;

  display: flex;
  align-items: center;
  justify-content: center;
}

.active-dropzone {
  background-color: #e8f5e9;
  border-color: #43a047;
}

.file-input {
  opacity: 0;
  position: absolute;
  width: 100%;
  height: 100%;
  top: 0;
  left: 0;
  cursor: pointer;
  z-index: 10;
}

.upload-prompt {
  pointer-events: none;
  width: 100%;
}

.upload-icon {
  font-size: 3.5rem;

  color: #43a047;

  margin-bottom: 1.5rem;
}

.file-label {
  color: #43a047;
  font-weight: 600;
  cursor: pointer;
  text-decoration: underline;
}

.upload-hint {
  margin-top: 1.5rem;
  font-size: 0.9rem;
  color: #90a4ae;
}

.image-preview-container {
  position: relative;
  width: 100%;
  text-align: center;
}

.image-preview {
  max-width: 100%;
  max-height: 400px;

  border-radius: 8px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

.change-image-btn {
  position: absolute;
  top: 10px;
  right: 10px;
  background-color: rgba(255, 255, 255, 0.9);
  border: none;
  border-radius: 20px;
  padding: 8px 12px;
  font-size: 0.9rem;
  color: #333;
  cursor: pointer;
  transition: all 0.2s ease;
}

.change-image-btn:hover {
  background-color: #fff;
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.2);
}

.predict-btn {
  width: 100%;
  padding: 1rem;
  margin-top: 1.5rem;
  background-color: #43a047;
  color: white;
  border: none;
  border-radius: 8px;
  font-size: 1.1rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
}

.predict-btn:hover:not(:disabled) {
  background-color: #2e7d32;
  transform: translateY(-2px);
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.15);
}

.predict-btn:disabled {
  background-color: #bdbdbd;
  cursor: not-allowed;
}

.error-message {
  margin: 1rem 2rem;
  padding: 1rem;
  background-color: #ffebee;
  color: #c62828;
  border-radius: 8px;
  font-size: 0.9rem;
  text-align: center;
}

.result-section {
  padding: 2rem;
  border-top: 1px solid #e0e0e0;
}

.result-header {
  display: flex;
  flex-direction: column;
  align-items: center;
  margin-bottom: 1.5rem;
}

.result-badge {
  display: inline-block;
  padding: 0.6rem 2rem;
  border-radius: 30px;
  font-weight: 600;
  font-size: 1.4rem;
  margin-bottom: 1.5rem;
  color: white;
}

/* Badge classes for the waste types */
.badge-glass {
  background-color: #00bcd4;
  /* Cyan */
}

.badge-paper {
  background-color: #ffb74d;
  /* Orange */
}

.badge-cardboard {
  background-color: #8d6e63;
  /* Brown */
}

.badge-plastic {
  background-color: #2196f3;
  /* Blue */
}

.badge-metal {
  background-color: #9e9e9e;
  /* Grey */
}

.badge-trash {
  background-color: #607d8b;
  /* Blue Grey */
}

.badge-default {
  background-color: #757575;
}

.confidence-meter {
  width: 100%;
  max-width: 500px;

}

.confidence-label {
  margin-bottom: 0.6rem;
  font-size: 1rem;
  color: #757575;
}

.progress {
  height: 1rem;

  border-radius: 10px;
  background-color: #e0e0e0;
  overflow: hidden;
}

.progress-bar {
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  font-size: 0.8rem;
  font-weight: bold;
  transition: width 1s ease-in-out;
  background-color: #4caf50;

}

.waste-instructions {
  background-color: #f5f7fa;
  border-radius: 12px;
  padding: 2rem;
  margin: 1.5rem 0;
}

.waste-instructions h3 {
  margin-top: 0;
  margin-bottom: 1.2rem;
  font-size: 1.3rem;
  color: #37474f;
  text-align: center;
}

.instruction-content {
  color: #546e7a;
  font-size: 1rem;
}

.instruction-content ul {
  padding-left: 1.5rem;
  margin-bottom: 0;
}

.instruction-content li {
  margin-bottom: 0.7rem;
  line-height: 1.5;
}

.classify-another-btn {
  width: 100%;
  padding: 1rem;
  background-color: #546e7a;
  color: white;
  border: none;
  border-radius: 8px;
  font-size: 1.1rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
}

.classify-another-btn:hover {
  background-color: #455a64;
  transform: translateY(-2px);
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.15);
}

@media (max-width: 950px) {
  .classifier-card {
    min-width: auto;
    max-width: 95%;
  }
}

@media (max-width: 768px) {
  .classifier-card {
    border-radius: 12px;
    box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
  }

  .file-drop-area {
    padding: 2rem 1rem;
    min-height: 200px;
  }

  .upload-icon {
    font-size: 2.5rem;
  }
}
</style>