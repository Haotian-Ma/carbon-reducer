<script setup>
import { ref } from 'vue';
import { RouterView } from 'vue-router';
import BHeader from './components/BHeader.vue';
import './assets/style.css';

// Password protection
const isAuthenticated = ref(localStorage.getItem('siteAuthenticated') === 'true');
const password = ref('');
const errorMessage = ref('');

const checkPassword = () => {
  if (password.value === import.meta.env.VITE_APP_SITE_PASSWORD) { // Use environment variable for password
    isAuthenticated.value = true;
    localStorage.setItem('siteAuthenticated', 'true');
  } else {
    errorMessage.value = 'Incorrect password. Please try again.';
  }
};
</script>

<template>
  <div v-if="!isAuthenticated" class="password-overlay">
    <div class="password-box">
      <h2>Password Required</h2>
      <p>Please enter the password to access this website.</p>
      <input type="password" v-model="password" @keyup.enter="checkPassword" placeholder="Enter password" />
      <button @click="checkPassword">Submit</button>
      <p v-if="errorMessage" class="error-message">{{ errorMessage }}</p>
    </div>
  </div>

  <div v-else class="main-container">
    <header>
      <BHeader />
    </header>

    <main class="main-box">
      <router-view></router-view>
    </main>
  </div>
</template>

<style>
/* Password protection styles */
.password-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: rgba(0, 0, 0, 0.8);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 9999;
}

.password-box {
  background-color: white;
  padding: 40px;
  border-radius: 10px;
  text-align: center;
  width: 90%;
  max-width: 400px;
  box-shadow: 0 5px 15px rgba(0, 0, 0, 0.3);
}

.password-box h2 {
  margin-bottom: 10px;
  color: #333;
  font-size: 24px;
}

.password-box p {
  margin-bottom: 20px;
  color: #666;
}

.password-box input {
  width: 100%;
  padding: 12px;
  margin-bottom: 20px;
  border: 1px solid #ddd;
  border-radius: 5px;
  font-size: 16px;
  box-sizing: border-box;
}

.password-box button {
  background-color: #1e6a5c;
  color: white;
  border: none;
  padding: 12px 24px;
  border-radius: 5px;
  cursor: pointer;
  font-size: 16px;
  transition: background-color 0.3s;
}

.password-box button:hover {
  background-color: #14574b;
}

.error-message {
  color: #e53935;
  margin-top: 15px;
  font-size: 14px;
}
</style>

<style scoped>
header {
  line-height: 1.5;
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  z-index: 1000;
}

.logo {
  display: block;
  margin: 0 auto 2rem;
}

.container {
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
  max-width: 80vw;
  margin: 0 auto;
  padding: 20px;
  /* background-color: #e0bfbf; */
  border-radius: 10px;
}

/* Class selectors */
.form {
  text-align: center;
  margin-top: 50px;
}
</style>