<script setup>
import { ref, onMounted, onBeforeUnmount } from 'vue';
import { useRouter } from 'vue-router';
import carouselData from '../assets/jsons/carousel.json';
import axios from 'axios'


import { computed } from 'vue';

const slides = ref(carouselData.slides);

const currentImage = computed(() => {
    return carouselImages[currentSlide.value];
});
// Carousel logic with auto-rotation
const currentSlide = ref(0);
const isCarouselPaused = ref(false);
let carouselInterval = null;

const nextSlide = () => {
    currentSlide.value = (currentSlide.value + 1) % slides.value.length;
};

const prevSlide = () => {
    currentSlide.value = (currentSlide.value - 1 + slides.value.length) % slides.value.length;
};

const pauseCarousel = () => {
    isCarouselPaused.value = true;
    clearInterval(carouselInterval);
};

const resumeCarousel = () => {
    isCarouselPaused.value = false;
    startCarouselInterval();
};

const startCarouselInterval = () => {
    carouselInterval = setInterval(() => {
        if (!isCarouselPaused.value) {
            nextSlide();
        }
    }, 5000);
};
const setupIntersectionObserver = () => {
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('visible');
            }
        });
    }, { threshold: 0.2 });

    document.querySelectorAll('.animate-on-scroll').forEach(el => {
        observer.observe(el);
    });
};




// Router for navigation
const router = useRouter();


const goToAbout = () => {
    router.push('/about');
};

const apiUrl = import.meta.env.VITE_APP_API_URL;
// Lifecycle hooks
onMounted(() => {
    startCarouselInterval();
    setupIntersectionObserver();

});

onBeforeUnmount(() => {
    clearInterval(carouselInterval);
});
</script>

<template>
    <div class="home-page">
        <!-- Hero Section - Enhanced Carousel -->
        <section class="hero">
            <div class="carousel" @mouseenter="pauseCarousel" @mouseleave="resumeCarousel">
                <div class="carousel-container">
                    <transition name="fade" mode="out-in">
                        <div class="carousel-item" :key="currentSlide"
                            :style="{ 'background-image': `url(${slides[currentSlide].image})` }">
                            <div class="carousel-overlay">
                                <div class="carousel-content">
                                    <h1 class="carousel-title">{{ slides[currentSlide].title }}</h1>
                                    <p class="carousel-subtitle">{{ slides[currentSlide].description }}</p>

                                    <div class="carousel-actions">
                                        <router-link :to="slides[currentSlide].buttonLink"
                                            class="carousel-action-button">
                                            {{ slides[currentSlide].buttonText }}
                                        </router-link>
                                    </div>
                                </div>

                            </div>

                            <div class="location-tag">{{ slides[currentSlide].location }}</div>
                        </div>
                    </transition>
                </div>
                <button class="carousel-button prev" @click="prevSlide">&#10094;</button>
                <button class="carousel-button next" @click="nextSlide">&#10095;</button>
                <div class="carousel-indicators">
                    <span v-for="(slide, index) in slides" :key="index" :class="{ active: currentSlide === index }"
                        @click="currentSlide = index">
                    </span>
                </div>
            </div>
        </section>

        <!-- Features Section -->
        <section class="features-section">
            <div class="features-container">
                <h2 class="features-title">Discover Our Offers</h2>
                <p class="features-subtitle">See how you can contribute to environmental conservation and make a
                    difference.</p>

                <div class="features-grid">
                    <div class="feature-card">
                        <div class="feature-image">
                            <img src="../assets/images/feature1.jpg" alt="Buy Trees">
                        </div>
                        <div class="feature-content">
                            <h3>Eco Action</h3>
                            <p>Assess your personal carbon footprint and show some suggestions.</p>
                            <router-link to="/eco-action" class="feature-button">
                                Start Now
                            </router-link>
                        </div>
                    </div>

                    <div class="feature-card">
                        <div class="feature-image">
                            <img src="../assets/images/feature2.jpg" alt="Give a Gift">
                        </div>
                        <div class="feature-content">
                            <h3>Virtual Tree Planting</h3>
                            <p>Contribute to global reforestation and offset your carbon emissions online.</p>
                            <router-link to="/virtual-tree/tree-planting" class="feature-button">
                                Plant Trees
                            </router-link>
                        </div>
                    </div>

                    <div class="feature-card">
                        <div class="feature-image">
                            <img src="../assets/images/feature3.jpg" alt="Forest Subscription">
                        </div>
                        <div class="feature-content">
                            <h3>Climate Insight</h3>
                            <p>Quickly understand environmental conditions and carbon emissions</p>
                            <router-link to="/resources/climate-insight" class="feature-button">
                                View Insights
                            </router-link>
                        </div>
                    </div>

                    <div class="feature-card">
                        <div class="feature-image">
                            <img src="../assets/images/feature4.jpg" alt="Biodiversity">
                        </div>
                        <div class="feature-content">
                            <h3>Kids Learning</h3>
                            <p>Help children learn about climate change, sustainability, and environmental conservation.
                            </p>
                            <router-link to="resources/kids-learning" class="feature-button">
                                Explore Resources
                            </router-link>
                        </div>
                    </div>
                </div>
            </div>
        </section>

        <!-- Events Section -->
        <!-- <section class="events animate-on-scroll">
            <h2>Upcoming Events</h2>
            <div class="event-list">
                <div v-for="event in events" :key="event.id" class="event-card">
                    <div class="event-header">
                        <span class="event-date">{{ event.date }}</span>
                    </div>
                    <h3>{{ event.title }}</h3>
                    <p><strong>Location:</strong> {{ event.location }}</p>
                    <p>{{ event.description }}</p>
                    <div class="event-footer">
                        <button class="btn-primary" @click="$event.target.classList.add('clicked')">Register
                            Now</button>
                    </div>
                </div>
            </div>
        </section> -->

        <!-- Hope Stories Section -->
        <section class="about animate-on-scroll">
            <div class="about-content">
                <h2>About us</h2>
                <p>
                    Ecospere is a non-profit website dedicated to reducing Carbon Emissions through
                    tree planting and environmental education. Through community engagement, outreach programs, and
                    advocacy,
                    we aim to protect our planet and create a sustainable future for all.
                </p>
                <div class="about-cta">
                    <button class="btn-primary" @click="goToAbout">Learn More About Our Mission</button>
                </div>
            </div>
        </section>

        <!-- Footer Section -->
        <footer class="footer">
            <div class="footer-content">
                <div class="footer-section">
                    <h3>EcoSphere Initiative</h3>
                    <p>Planting trees, reducing carbon, saving our planet.</p>
                </div>

                <div class="footer-section">
                    <h3>Quick Links</h3>
                    <ul>
                        <li>
                            <router-link to="/">Home</router-link>
                        </li>
                        <li>
                            <router-link to="/about">About Us</router-link>
                        </li>
                        <li>
                            <router-link to="/eco-action">Eco action</router-link>
                        </li>
                        <li>
                            <a href="#">Contact</a>
                        </li>
                    </ul>
                </div>

                <div class="footer-section">
                    <h3>Connect With Us</h3>
                    <div class="social-links">
                        <a href="#">Facebook</a>
                        <a href="#">Instagram</a>
                        <a href="#">Twitter</a>
                    </div>
                </div>
            </div>

            <div class="footer-bottom">
                <p>© 2025 EcoSphere Initiative. All rights reserved.</p>
            </div>
        </footer>
    </div>
</template>
<style scoped>
/* Hero Section - Carousel */
.hero {
    width: 100vw;
    margin-left: calc(-50vw + 50%);
    margin-right: calc(-50vw + 50%);
}

.carousel {
    position: relative;
    width: 100%;
    height: 600px;
    overflow: hidden;
    border-radius: var(--border-radius, 10px);
    box-shadow: var(--shadow, 0 4px 6px rgba(0, 0, 0, 0.1));
}

.carousel-container {
    position: relative;
    width: 100%;
    height: 100%;
}

.carousel-item {
    position: relative;
    width: 100%;
    height: 600px;
    background-size: cover;
    background-position: center;
    display: flex;
    align-items: center;
}

.carousel-item::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background: linear-gradient(to right, rgba(0, 0, 0, 0.6) 0%, rgba(0, 0, 0, 0.3) 60%, rgba(0, 0, 0, 0.1) 100%);
}

.carousel-overlay {
    position: relative;
    z-index: 2;
    width: 100%;
    height: 100%;
    display: flex;
    align-items: center;
    padding: 0 10%;
}

.carousel-content {
    display: flex;
    flex-direction: column;
    color: white;
    max-width: 600px;
    text-align: left;
    gap: 1rem;
}

.carousel-title {
    font-size: 3rem;
    margin-bottom: 0.5rem;
    line-height: 1.2;
}

.carousel-subtitle {
    font-size: 1.2rem;
    margin-bottom: 1rem;
    max-width: 500px;
    line-height: 1.5;
}

.carousel-actions {
    display: flex;

    margin-top: 1rem;
}

.carousel-button {
    white-space: nowrap;
    display: inline-flex;
    background-color: white;
    color: #333;
    padding: 12px 24px;
    border-radius: 30px;
    text-decoration: none;
    font-weight: 600;
    transition: all 0.3s ease;
}

.carousel-button:hover {
    background-color: #f0f0f0;
    transform: translateY(-2px);
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
}

.carousel-action-button {
    white-space: nowrap;
    display: inline-flex;
    background-color: white;
    color: #333;
    padding: 12px 24px;
    border-radius: 30px;
    text-decoration: none;
    font-weight: 600;
    transition: all 0.3s ease;
}

.carousel-action-button:hover {
    background-color: #f0f0f0;
    transform: translateY(-2px);
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
}

.button-arrow {
    margin-left: 5px;
    font-size: 1.2em;
}

.carousel-button.prev,
.carousel-button.next {
    position: absolute;
    top: 50%;
    transform: translateY(-50%);
    background: rgba(255, 255, 255, 0.3);
    color: white;
    border: none;
    width: 40px;
    height: 40px;
    border-radius: 50%;
    font-size: 18px;
    cursor: pointer;
    z-index: 10;
    display: flex;
    align-items: center;
    justify-content: center;
    transition: background 0.3s;
}

.carousel-button.prev:hover,
.carousel-button.next:hover {
    background: rgba(255, 255, 255, 0.5);
}

.carousel-button.prev {
    left: 20px;
}

.carousel-button.next {
    right: 20px;
}

.carousel-indicators {
    position: absolute;
    bottom: 20px;
    left: 50%;
    transform: translateX(-50%);
    display: flex;
    gap: 10px;
    z-index: 10;
}

.carousel-indicators span {
    width: 12px;
    height: 12px;
    border-radius: 50%;
    background: rgba(255, 255, 255, 0.5);
    cursor: pointer;
    transition: all 0.3s;
}

.carousel-indicators span.active {
    background: white;
    transform: scale(1.2);
}

.location-tag {
    position: absolute;
    bottom: 20px;
    right: 20px;
    color: white;
    padding: 5px 10px;
    border-radius: 4px;
    font-size: 0.9rem;
    z-index: 2;
}


.fade-enter-active,
.fade-leave-active {
    transition: opacity 0.5s ease;
}

.fade-enter-from,
.fade-leave-to {
    opacity: 0;
}

.features-section {
    padding: 4rem 0;
    background-color: #f4f6f9;
}

.features-container {
    max-width: 1200px;
    margin: 0 auto;
    padding: 0 15px;
}

.features-title {
    text-align: center;
    font-size: 2.5rem;
    color: #2c3e50;
    margin-bottom: 1rem;
}

.features-subtitle {
    text-align: center;
    color: #7a8b9f;
    max-width: 800px;
    margin: 0 auto 2.5rem;
    line-height: 1.6;
}

.features-grid {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 1.5rem;
}

.feature-card {
    background-color: white;
    border-radius: 12px;
    box-shadow: 0 6px 12px rgba(0, 0, 0, 0.08);
    overflow: hidden;
    transition: transform 0.3s ease, box-shadow 0.3s ease;
    height: 100%;
    display: flex;
    flex-direction: column;
}

.feature-card:hover {
    transform: translateY(-10px);
    box-shadow: 0 12px 20px rgba(0, 0, 0, 0.12);
}

.feature-image {
    height: 250px;
    overflow: hidden;
}

.feature-image img {
    width: 100%;
    height: 100%;
    object-fit: cover;
    transition: transform 0.3s ease;
}

.feature-card:hover .feature-image img {
    transform: scale(1.1);
}

.feature-content {
    padding: 1.5rem;
    text-align: center;
    flex-grow: 1;
    display: flex;
    flex-direction: column;
}

.feature-content h3 {
    color: #2c3e50;
    margin-bottom: 1rem;
    font-size: 1.3rem;
}

.feature-content p {
    color: #7a8b9f;
    margin-bottom: 1.5rem;
    line-height: 1.6;
    flex-grow: 1;
}

.feature-button {
    display: inline-block;
    background-color: #2c3e50;
    color: white;
    padding: 10px 20px;
    border-radius: 30px;
    text-decoration: none;
    font-weight: 600;
    transition: background-color 0.3s ease, transform 0.3s ease;
    margin-top: auto;
}

.feature-button:hover {
    background-color: #3a5a78;
    transform: translateY(-2px);
}

@media (max-width: 1200px) {
    .features-grid {
        grid-template-columns: repeat(2, 1fr);
    }
}

@media (max-width: 768px) {
    .features-grid {
        grid-template-columns: 1fr;
    }

    .features-title {
        font-size: 2rem;
    }

    .features-subtitle {
        font-size: 0.9rem;
    }
}
</style>
