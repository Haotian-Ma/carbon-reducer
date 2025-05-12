<template>
    <div class="classifier-container">
      <h2>Garbage Image Classifier</h2>
  
      <input
        type="file"
        @change="onFileChange"
        accept="image/*"
      />
  
      <button
        :disabled="!file || loading"
        @click="upload"
      >
        {{ loading ? 'Processing...' : 'Classify Image' }}
      </button>
  
      <div v-if="previewUrl" class="preview">
        <h3>Preview</h3>
        <img :src="previewUrl" alt="Image Preview" />
      </div>
  
      <div v-if="loading" class="spinner"></div>
  
      <div v-if="result" class="result">
        <h3>Result</h3>
        <p><strong>Class:</strong> {{ result.class }}</p>
        <p><strong>Confidence:</strong> {{ (result.confidence * 100).toFixed(1) }}%</p>
      </div>
  
      <div v-if="error" class="error">
        {{ error }}
      </div>
    </div>
  </template>
  
  <script setup>
  import { ref } from 'vue'
  import axios from 'axios'
  
  const file       = ref(null)
  const previewUrl = ref('')
  const result     = ref(null)
  const error      = ref('')
  const loading    = ref(false)
  
  function onFileChange(event) {
    file.value     = event.target.files[0] || null
    previewUrl.value = file.value ? URL.createObjectURL(file.value) : ''
    result.value   = null
    error.value    = ''
  }
  
  async function upload() {
    if (!file.value) return
    loading.value = true
    result.value  = null
    error.value   = ''
  
    const formData = new FormData()
    formData.append('file', file.value)
  
    try {
      const response = await axios.post(
        'http://localhost:5000/predict',
        formData,
        { headers: { 'Content-Type': 'multipart/form-data' } }
      )
      result.value = response.data
    } catch (e) {
      error.value = e.response?.data?.error || 'An error occurred. Please try again.'
    } finally {
      loading.value = false
    }
  }
  </script>
  
  <style scoped>
  .classifier-container {
    max-width: 400px;
    margin: 2rem auto;
    padding: 1.5rem;
    background: #fff;
    border-radius: 8px;
    box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    text-align: center;
  }
  .classifier-container h2 {
    margin-bottom: 1rem;
    color: #333;
  }
  .classifier-container input[type="file"] {
    margin: 1rem 0;
  }
  .classifier-container button {
    padding: 0.6rem 1.2rem;
    border: none;
    border-radius: 4px;
    background-color: #3498db;
    color: #fff;
    font-size: 1rem;
    cursor: pointer;
    transition: background 0.2s;
  }
  .classifier-container button:hover:not([disabled]) {
    background-color: #2980b9;
  }
  .classifier-container button[disabled] {
    background-color: #ccc;
    cursor: not-allowed;
  }
  .preview {
    margin-top: 1rem;
  }
  .preview img {
    max-width: 100%;
    border: 1px solid #ccc;
    border-radius: 4px;
  }
  .spinner {
    margin: 1.5rem auto;
    width: 40px;
    height: 40px;
    border: 4px solid rgba(0,0,0,0.1);
    border-top-color: #3498db;
    border-radius: 50%;
    animation: spin 1s linear infinite;
  }
  @keyframes spin {
    to { transform: rotate(360deg); }
  }
  .result {
    margin-top: 1rem;
    text-align: left;
  }
  .result h3 {
    margin-bottom: 0.5rem;
  }
  .result p {
    margin: 0.3rem 0;
  }
  .error {
    margin-top: 1rem;
    color: #e74c3c;
    font-weight: bold;
  }
  </style>
  