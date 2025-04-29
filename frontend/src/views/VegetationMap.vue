<template>
    <div ref="mapWrapper"></div>
  </template>
  
  <script setup>
  import { ref, onMounted } from 'vue'
  
  const API_BASE_URL = import.meta.env.VITE_API_BASE_URL
  const mapWrapper = ref(null)
  
  onMounted(async () => {
    try {
      // 1) 拉回文字形式的 HTML
      const html = await fetch(`${API_BASE_URL}/api/map`).then(r => r.text())
  
      // 2) 临时解析成 DOM
      const parser = new DOMParser()
      const doc = parser.parseFromString(html, 'text/html')
  
      // 3) 把地图的 <div> + <link>、<style> 插入到你的容器里
      //    先把 body 里的内容弄进来
      mapWrapper.value.innerHTML = doc.body.innerHTML
  
      // 4) 然后把 <script> 标签里的 JS 代码都跑一遍
      doc.querySelectorAll('script').forEach(oldScript => {
        const newScript = document.createElement('script')
        if (oldScript.src) {
          newScript.src = oldScript.src
        } else {
          newScript.text = oldScript.text
        }
        document.body.appendChild(newScript)
      })
    } catch (e) {
      console.error('加载 Folium 地图失败', e)
    }
  })
  </script>
  