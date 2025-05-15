<template>
  <div class="kids-climate-container">
    <!-- Hero Section -->
    <div class="hero-section">
      <div class="container">
        <h1 class="text-center">Climate Kids Corner</h1>
        <p class="text-center hero-subtitle">Join us on an adventure to learn about our planet and how we can protect
          it!</p>
      </div>
    </div>

    <!-- Main Content -->
    <div class="container mt-4">
      <!-- Introduction -->
      <div class="row mb-5">
        <div class="col-lg-8 offset-lg-2">
          <div class="intro-card">
            <h2>Hey Climate Explorers! 🌍</h2>
            <p>Our planet Earth is amazing! It's home to millions of plants, animals, and of course, us! But our planet
              is changing because of something called <strong>climate change</strong>.</p>
            <p>Climate change means that Earth is getting warmer, and that can cause problems for all living things. But
              don't worry! By learning about climate change, you can become a Planet Protector and help make a
              difference!</p>
          </div>
        </div>
      </div>

      <!-- YouTube Video Section -->
      <div class="video-section mt-5 mb-5">
        <h2 class="section-title text-center mb-4">Learn with Videos</h2>

        <div class="row mb-4">
          <div class="col-12">
            <div class="topic-buttons">
              <button v-for="topic in videoTopics" :key="topic.id" @click="selectTopic(topic)"
                :class="{ active: selectedTopic.id === topic.id }" class="topic-button">
                {{ topic.name }}
              </button>
            </div>

            <!-- searching bar -->
            <div class="custom-search mt-3">
              <input type="text" v-model="customSearchQuery" placeholder="Search for environmental videos..."
                class="search-input" @keyup.enter="searchCustomTopic">
              <button @click="searchCustomTopic" class="search-button">
                Search
              </button>
              <p class="search-note">Note: All searches are limited to environmental topics</p>
            </div>
          </div>
        </div>

        <div class="row justify-content-center">
          <div class="col-12">
            <div v-if="showRateLimitWarning" class="alert alert-warning">
              <i class="fas fa-exclamation-triangle"></i> Too many requests. Please wait a moment before searching
              again.
            </div>
            <!-- loading status -->
            <div v-if="isLoading" class="loading-spinner">
              <div class="spinner"></div>
              <p>Loading videos...</p>
            </div>

            <!-- video lists -->
            <div v-if="selectedVideos.length > 0" class="video-list">
              <div v-for="(video, index) in selectedVideos" :key="index" class="video-item">
                <div class="video-container">
                  <iframe width="100%" height="315" :src="'https://www.youtube.com/embed/' + video.id.videoId"
                    frameborder="0"
                    allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
                    allowfullscreen>
                  </iframe>
                  <h3 class="video-title">{{ video.snippet.title }}</h3>
                  <p class="video-description">{{ truncateDescription(video.snippet.description) }}</p>
                </div>
              </div>
            </div>

            <!-- no video tips -->
            <div v-else class="video-placeholder">
              <p>Select a topic above or search for environmental videos!</p>
            </div>
          </div>
        </div>
        <!-- Interactive Resources -->
        <h2 class="section-title text-center mb-4">Fun Learning Activities</h2>

        <div class="row resource-cards">
          <!-- Card 1 -->
          <div class="col-md-6 col-lg-3 mb-4">
            <div class="resource-card">
              <div class="card-image-container">
                <img src="https://placehold.co/600x400/9DDCFF/333333?text=RecycleCity" alt="RecycleCity Game"
                  class="card-img">
              </div>
              <div class="card-content">
                <h3>RecycleCity Game (Age: 6-15)</h3>
                <p>Explore RecycleCity and learn how recycling works! Visit different locations and discover how to
                  reduce
                  waste in your community.</p>
                <!-- <div class="button-container">
                <a href="/games/recyclecity/index.htm" target="_blank" class="resource-button">Play Now</a>
              </div> -->
                <div class="button-container">
                  <router-link to="/recyclecity" class="resource-button">Play Now</router-link>
                </div>
              </div>
            </div>
          </div>

        </div>


        <!-- Fun Facts Section -->
        <div class="fun-facts-section mt-5">
          <h2 class="section-title text-center mb-4">Cool Climate Facts</h2>

          <div class="row">
            <div class="col-md-4 mb-4">
              <div class="fact-bubble fact-bubble-1">
                <p>Did you know that trees are like nature's air filters? They absorb carbon dioxide (a greenhouse gas)
                  and release oxygen that we breathe!</p>
              </div>
            </div>

            <div class="col-md-4 mb-4">
              <div class="fact-bubble fact-bubble-2">
                <p>Polar bears are amazing swimmers, but they need ice to rest and hunt. As the Arctic ice melts due to
                  climate change, polar bears have to swim longer distances!</p>
              </div>
            </div>

            <div class="col-md-4 mb-4">
              <div class="fact-bubble fact-bubble-3">
                <p>The energy from the sun that reaches Earth in just one hour could power the entire world for a whole
                  year! That's why solar power is so important.</p>
              </div>
            </div>
          </div>
        </div>

        <!-- What You Can Do Section -->
        <div class="action-section mt-5 mb-5">
          <h2 class="section-title text-center mb-4">Be a Planet Protector!</h2>

          <div class="row">
            <div class="col-lg-8 offset-lg-2">
              <div class="action-card">
                <h3 class="text-center">Here are 5 super easy ways YOU can help:</h3>

                <ol class="action-list">
                  <li>Turn off lights when you leave a room to save energy</li>
                  <li>Use reusable water bottles instead of plastic ones</li>
                  <li>Walk, bike, or take the bus when possible</li>
                  <li>Plant flowers or trees that help butterflies and bees</li>
                  <li>Tell your friends and family what you've learned about climate change</li>
                </ol>

                <div class="text-center mt-4">
                  <a href="/eco-action" class="pledge-button">I Pledge to Help Our Planet!</a>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
const videoCache = ref({});
const CACHE_DURATION = 24 * 60 * 60 * 1000;
const RATE_LIMIT_DURATION = 5000;
const presetVideos = {
  'climate change for kids': [
    {
      id: { videoId: 'Sv7OHfpIRfU' },
      snippet: {
        title: "Climate Change for Kids - Learn about Global Warming",
        description: "Learn about climate change and global warming in a fun and simple way. This educational video explains what climate change is, why it happens, and what we can do to help our planet."
      }
    },
    {
      id: { videoId: 'DkZ7BJQupVA' },
      snippet: {
        title: "What is Climate Change? | Educational Video for Kids",
        description: "Climate change explained for children. Understand the greenhouse effect, global warming, and how we can protect our Earth together."
      }
    },
    {
      id: { videoId: 'NCatQ0ndc0Q' },
      snippet: {
        title: "Climate Change: How Can We Help? | Kids Science",
        description: "Discover simple ways kids can help fight climate change. From recycling to saving energy, learn how small actions make a big difference."
      }
    }
  ],
  'renewable energy for children': [
    {
      id: { videoId: 'wMOpMka6PJI' },
      snippet: {
        title: "Renewable Energy for Kids | Solar, Wind & Water Power",
        description: "Learn about renewable energy sources like solar panels, wind turbines, and hydroelectric power. See how clean energy helps our planet."
      }
    },
    {
      id: { videoId: '1kUE0BZtTRc' },
      snippet: {
        title: "Clean Energy Explained for Kids",
        description: "What is renewable energy? This fun educational video explains solar, wind, and other clean energy sources that don't pollute our Earth."
      }
    }
  ],
  'recycling for kids': [
    {
      id: { videoId: 'OasbYWF4_S8' },
      snippet: {
        title: "Recycling for Kids | How to Reduce, Reuse, Recycle",
        description: "Learn how recycling works and why it's important for our planet. Discover the three Rs: Reduce, Reuse, and Recycle!"
      }
    },
    {
      id: { videoId: '_6xlNyWPpB8' },
      snippet: {
        title: "Where Does Our Recycling Go? | Kids Learn About Recycling",
        description: "Follow the journey of recycled materials and see how they become new products. Learn what can and can't be recycled."
      }
    }]
};
const showRateLimitWarning = ref(false);
let lastRequestTime = 0;

// YouTube API key 
const YOUTUBE_API_KEY = import.meta.env.VITE_YOUTUBE_API_KEY;
const MAX_RESULTS = 3; // Number of videos to show per topic

// Video topics
const videoTopics = ref([
  { id: 1, name: 'Climate Basics', query: 'climate change for kids' },
  { id: 2, name: 'Renewable Energy', query: 'renewable energy for children' },
  { id: 3, name: 'Recycling', query: 'recycling for kids' },
  { id: 4, name: 'Endangered Animals', query: 'endangered animals climate change' },
  { id: 5, name: 'Weather vs Climate', query: 'weather vs climate for kids' }
]);

const selectedTopic = ref(videoTopics.value[0]);
const selectedVideos = ref([]);
const isLoading = ref(false);
const customSearchQuery = ref('');
// game modal
const showGameModal = ref(false);

function truncateDescription(desc, maxLength = 150) {
  return desc.length > maxLength ? desc.substring(0, maxLength) + '...' : desc;
}
function searchCustomTopic() {
  if (!customSearchQuery.value.trim()) return;

  const searchQuery = customSearchQuery.value + ' environment|eco|green|sustainability';
  fetchVideos({
    id: 0,
    name: 'Custom Search: ' + customSearchQuery.value,
    query: searchQuery
  });
}
function getCachedVideos(query) {
  const cacheKey = `youtube_cache_${query}`;
  try {
    const cached = localStorage.getItem(cacheKey);
    if (cached) {
      const data = JSON.parse(cached);
      if (Date.now() - data.timestamp < CACHE_DURATION) {
        return data.videos;
      }
    }
  } catch (error) {
    console.error('Cache read error:', error);
  }
  return null;
}

function setCachedVideos(query, videos) {
  const cacheKey = `youtube_cache_${query}`;
  const data = {
    videos: videos,
    timestamp: Date.now()
  };
  try {
    localStorage.setItem(cacheKey, JSON.stringify(data));
  } catch (error) {
    console.error('Cache write error:', error);
  }
}


function canMakeRequest() {
  const now = Date.now();
  if (now - lastRequestTime < RATE_LIMIT_DURATION) {
    showRateLimitWarning.value = true;
    setTimeout(() => {
      showRateLimitWarning.value = false;
    }, 3000);
    return false;
  }
  lastRequestTime = now;
  return true;
}

// Function to fetch videos from YouTube API
async function fetchVideos(topic) {

  selectedTopic.value = topic;
  selectedVideos.value = [];
  if (presetVideos[topic.query]) {
    selectedVideos.value = presetVideos[topic.query];
    return;
  }


  const cachedVideos = getCachedVideos(topic.query);
  if (cachedVideos) {
    selectedVideos.value = cachedVideos;
    return;
  }


  if (!canMakeRequest()) {
    return;
  }
  isLoading.value = true;

  try {
    // Check if the topic query already includes environment-related keywords
    const query = topic.query.includes('environment|eco')
      ? topic.query
      : topic.query + ' environment|eco|green|sustainability';

    const response = await fetch(
      `https://www.googleapis.com/youtube/v3/search?part=snippet&q=${encodeURIComponent(query)}&maxResults=${MAX_RESULTS}&type=video&key=${YOUTUBE_API_KEY}`
    );

    const data = await response.json();
    selectedVideos.value = data.items || [];
    if (selectedVideos.value.length > 0) {
      setCachedVideos(topic.query, selectedVideos.value);
    }
  } catch (error) {
    console.error('Error fetching YouTube videos:', error);
    selectedVideos.value = [];
  } finally {
    isLoading.value = false;
  }
}

// Function to select a topic
function selectTopic(topic) {
  fetchVideos(topic);
}

// Fetch initial videos when component mounts
onMounted(() => {
  if (presetVideos[selectedTopic.value.query]) {
    selectedVideos.value = presetVideos[selectedTopic.value.query];
  }
});
</script>

<style>
/* Main Styles */
.kids-climate-container {
  font-family: 'Comic Sans MS', 'Chalkboard SE', 'Marker Felt', sans-serif;
  color: #333;
}

/* Hero Section */
.hero-section {
  background: linear-gradient(135deg, #9DDCFF 0%, #AEF78E 100%);
  padding: 3rem 0;
  border-radius: 0 0 30px 30px;
  margin-bottom: 2rem;
}

.hero-section h1 {
  font-size: 3rem;
  color: #2C3E50;
  margin-bottom: 1rem;
  font-weight: bold;
  text-shadow: 2px 2px 0px rgba(255, 255, 255, 0.5);
}

.hero-subtitle {
  font-size: 1.4rem;
  color: #2C3E50;
}

/* Section Titles */
.section-title {
  color: #2C3E50;
  font-weight: bold;
  font-size: 2.2rem;
  text-shadow: 1px 1px 0px rgba(0, 0, 0, 0.1);
}

/* Intro Card */
.intro-card {
  background-color: #FFFDDE;
  border-radius: 20px;
  padding: 2rem;
  box-shadow: 0 5px 15px rgba(0, 0, 0, 0.1);
  border: 3px dashed #FFCE87;
}

.intro-card h2 {
  color: #FF8A5B;
  margin-bottom: 1rem;
  font-size: 2rem;
}

.intro-card p {
  font-size: 1.2rem;
  line-height: 1.6;
}

/* Video Section */
.video-section {
  background-color: #F5F9FF;
  border-radius: 20px;
  padding: 2rem;
  margin-bottom: 2rem;
}

.topic-buttons {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
  justify-content: center;
  margin-bottom: 20px;
}

.topic-button {
  background-color: #9DDCFF;
  border: none;
  border-radius: 30px;
  padding: 8px 20px;
  font-size: 1rem;
  cursor: pointer;
  transition: all 0.3s ease;
  font-weight: bold;
  color: #2C3E50;
}

.topic-button:hover {
  background-color: #7ACBFF;
  transform: translateY(-2px);
}

.topic-button.active {
  background-color: #FF8A5B;
  color: white;
}

.video-container {
  background-color: white;
  border-radius: 15px;
  padding: 20px;
  box-shadow: 0 5px 15px rgba(0, 0, 0, 0.1);
}

.video-title {
  margin-top: 15px;
  color: #2C3E50;
  font-size: 1.3rem;
}

.video-description {
  color: #666;
  margin-top: 10px;
  font-size: 1rem;
}

.video-placeholder {
  background-color: white;
  border-radius: 15px;
  padding: 40px 20px;
  text-align: center;
  box-shadow: 0 5px 15px rgba(0, 0, 0, 0.1);
  font-size: 1.2rem;
  color: #666;
}

/* Resource Cards */
.resource-cards {
  margin-top: 1rem;
}

.resource-card {
  background-color: white;
  border-radius: 15px;
  overflow: hidden;
  box-shadow: 0 5px 15px rgba(0, 0, 0, 0.1);
  height: 100%;
  display: flex;
  flex-direction: column;
  transition: transform 0.3s ease, box-shadow 0.3s ease;
}

.resource-card:hover {
  transform: translateY(-10px);
  box-shadow: 0 10px 25px rgba(0, 0, 0, 0.15);
}

.card-image-container {
  height: 180px;
  overflow: hidden;
}

.card-img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  transition: transform 0.3s ease;
}

.resource-card:hover .card-img {
  transform: scale(1.05);
}

.card-content {
  padding: 1.5rem;
  display: flex;
  flex-direction: column;
  flex-grow: 1;
}

.card-content h3 {
  color: #2C3E50;
  font-size: 1.3rem;
  margin-bottom: 0.8rem;
}

.card-content p {
  color: #666;
  font-size: 1rem;
  margin-bottom: 1.5rem;
  flex-grow: 1;
}

.button-container {
  margin-top: auto;
  text-align: center;
}

.resource-button {
  display: inline-block;
  background-color: #FF8A5B;
  color: white;
  padding: 8px 20px;
  border-radius: 30px;
  text-decoration: none;
  font-weight: bold;
  transition: background-color 0.3s ease, transform 0.3s ease;
}

.resource-button:hover {
  background-color: #FF6B35;
  transform: scale(1.05);
  text-decoration: none;
  color: white;
}

/* Fun Facts Section */
.fun-facts-section {
  padding: 2rem 0;
}

.fact-bubble {
  border-radius: 30px;
  padding: 1.5rem;
  height: 100%;
  box-shadow: 0 5px 15px rgba(0, 0, 0, 0.1);
}

.fact-bubble p {
  font-size: 1.1rem;
  line-height: 1.5;
  margin: 0;
}

.fact-bubble-1 {
  background-color: #DFF6FF;
  border: 3px solid #9DDCFF;
}

.fact-bubble-2 {
  background-color: #FFF3EB;
  border: 3px solid #FFCE87;
}

.fact-bubble-3 {
  background-color: #F0FFE6;
  border: 3px solid #AEF78E;
}

/* Action Section */
.action-section {
  padding: 2rem 0;
}

.action-card {
  background-color: #FFF0F0;
  border-radius: 20px;
  padding: 2rem;
  box-shadow: 0 5px 15px rgba(0, 0, 0, 0.1);
  border: 3px dashed #FFA7A7;
}

.action-card h3 {
  color: #FF6B6B;
  margin-bottom: 1.5rem;
  font-size: 1.5rem;
}

.action-list {
  padding-left: 2rem;
  margin-bottom: 1rem;
}

.action-list li {
  font-size: 1.2rem;
  padding: 0.5rem 0;
  color: #555;
}

.pledge-button {
  display: inline-block;
  background-color: #4CAF50;
  color: white;
  padding: 12px 30px;
  border-radius: 30px;
  font-size: 1.2rem;
  text-decoration: none;
  font-weight: bold;
  transition: background-color 0.3s ease, transform 0.3s ease;
  box-shadow: 0 3px 10px rgba(0, 0, 0, 0.2);
}

.pledge-button:hover {
  background-color: #3E8E41;
  transform: scale(1.05);
  text-decoration: none;
  color: white;
}

.alert {
  padding: 12px 20px;
  border-radius: 8px;
  margin-bottom: 20px;
  display: flex;
  align-items: center;
  gap: 10px;
}

.alert-warning {
  background-color: #fff3cd;
  color: #856404;
  border: 1px solid #ffeaa7;
}

.video-placeholder small {
  display: block;
  margin-top: 10px;
  font-size: 0.9rem;
}

/* Responsive Adjustments */
@media (max-width: 768px) {
  .hero-section h1 {
    font-size: 2.5rem;
  }

  .hero-subtitle {
    font-size: 1.2rem;
  }

  .section-title {
    font-size: 1.8rem;
  }

  .intro-card h2 {
    font-size: 1.7rem;
  }

  .intro-card p {
    font-size: 1.1rem;
  }

  .action-list li {
    font-size: 1.1rem;
  }

  .topic-buttons {
    flex-direction: column;
    align-items: center;
  }

  .topic-button {
    width: 100%;
    max-width: 250px;
  }

  .video-container iframe {
    height: 250px;
  }
}

.custom-search {
  margin: 20px auto;
  max-width: 600px;
  text-align: center;
}

.search-input {
  padding: 10px 15px;
  width: 70%;
  border: 2px solid #9DDCFF;
  border-radius: 30px;
  font-size: 1rem;
  outline: none;
}

.search-button {
  padding: 10px 20px;
  margin-left: 10px;
  background-color: #4CAF50;
  color: white;
  border: none;
  border-radius: 30px;
  cursor: pointer;
  font-weight: bold;
  transition: background-color 0.3s;
}

.search-button:hover {
  background-color: #3E8E41;
}

.search-note {
  font-size: 0.8rem;
  color: #666;
  margin-top: 5px;
}

.video-list {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 20px;
  margin-top: 20px;
  width: 100%;
}

.video-item {
  background: white;
  border-radius: 10px;
  overflow: hidden;
  box-shadow: 0 3px 10px rgba(0, 0, 0, 0.1);
  display: flex;
  flex-direction: column;
}

.video-container {
  flex: 1;
  display: flex;
  flex-direction: column;
  padding: 15px;
}

.video-container iframe {
  width: 100%;
  aspect-ratio: 16/9;
  border-radius: 8px;
}

.loading-spinner {
  text-align: center;
  padding: 30px;
}

.spinner {
  border: 5px solid #f3f3f3;
  border-top: 5px solid #4CAF50;
  border-radius: 50%;
  width: 50px;
  height: 50px;
  animation: spin 1s linear infinite;
  margin: 0 auto 15px;
}

.game-modal {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.7);
  z-index: 1000;
  display: flex;
  justify-content: center;
  align-items: center;
}

.game-modal-content {
  width: 90%;
  height: 90%;
  background-color: white;
  border-radius: 10px;
  position: relative;
  overflow: hidden;
}

.close-modal {
  position: absolute;
  top: 10px;
  right: 10px;
  background: #FF8A5B;
  color: white;
  border: none;
  border-radius: 50%;
  width: 30px;
  height: 30px;
  display: flex;
  justify-content: center;
  align-items: center;
  font-size: 16px;
  cursor: pointer;
  z-index: 10;
}

.game-frame {
  width: 100%;
  height: 100%;
  border: none;
}
</style>