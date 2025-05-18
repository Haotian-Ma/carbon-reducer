<template>
  <div class="classifier">
    <h2>Garbage Classifier</h2>
    <input
      type="file"
      accept="image/*"
      @change="onFileChange"
    />
    <button
      :disabled="!file || loading"
      @click="upload"
    >
      {{ loading ? 'Predicting…' : 'Start Prediction' }}
    </button>

    <div v-if="error" class="error">
      ❌ {{ error }}
    </div>

    <div v-if="result" class="result">
      <p>🎯 Predicted Class：<strong>{{ result.class }}</strong></p>
      <p>🔎 Confidence：<strong>{{ (result.confidence * 100).toFixed(2) }}%</strong></p>
      <img :src="previewUrl" alt="Uploaded image" class="preview" />
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
</script>

<style scoped>
.classifier {
  max-width: 400px;
  margin: 2rem auto;
  padding: 1rem;
  border: 1px solid #ddd;
  border-radius: 8px;
  text-align: center;
}
input[type="file"] {
  margin-bottom: 1rem;
}
button {
  padding: 0.5rem 1rem;
  margin-bottom: 1rem;
}
.error {
  color: #c00;
  margin-top: 1rem;
}
.result {
  margin-top: 1rem;
}
.preview {
  margin-top: 0.5rem;
  max-width: 100%;
  border: 1px solid #ccc;
  border-radius: 4px;
}
</style>
