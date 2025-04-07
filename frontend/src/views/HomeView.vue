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

// Data for events
const events = [
    {
        id: 1,
        title: "Community Tree Planting Day",
        date: "October 15, 2023",
        location: "City Park",
        description: "Join us for a free community event to plant trees and reduce our carbon footprint.",
    },
    {
        id: 2,
        title: "Carbon Reduction Workshop",
        date: "November 1, 2023",
        location: "Community Center",
        description: "Learn practical ways to reduce your carbon emissions at home and in your community.",
    },
];


// Router for navigation
const router = useRouter();

const goToEmissionCalculator = () => {
    router.push('/emission-calculator');
};

const goToAbout = () => {
    router.push('/about');
};

const apiUrl = import.meta.env.VITE_APP_API_URL;
// Lifecycle hooks
onMounted(() => {
    startCarouselInterval();
    setupIntersectionObserver();
    axios.get(`${apiUrl}/api/chart-data`)
        .then(response => {
            const fig = response.data;
            fig.layout.title = {
                text: "Carbon Emission Reduction by Tree Planting Initiatives",
                x: 0.5,
                font: { size: 24 }
            };
            Plotly.newPlot('chart', fig.data, fig.layout);
        })
        .catch(error => {
            console.error('Failed:', error);
        });
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
        <!-- Check Carbon Footprint Section -->
        <section class="check-carbon">
            <h2>Calculate Your Carbon Footprint</h2>
            <p>Stay informed about your personal impact on the environment and find ways to reduce it.</p>
            <button class="btn-primary" @click="goToEmissionCalculator">Calculate Now</button>

            <div class="carbon-scale-container">
                <span class="carbon-label low">Low Impact</span>
                <div class="carbon-meter-scale">
                    <div class="scale-segment low"></div>
                    <div class="scale-segment moderate"></div>
                    <div class="scale-segment high"></div>
                    <div class="scale-segment very-high"></div>
                    <div class="scale-segment extreme"></div>
                </div>
                <span class="carbon-label high">High Impact</span>
            </div>
        </section>

        <!-- Data Section -->
        <section class="data-section animate-on-scroll">
            <h2>Impact Analytics</h2>
            <div id="chart" style="width: 100%; height: 500px;"></div>
        </section>

        <!-- Events Section -->
        <section class="events animate-on-scroll">
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
        </section>

        <!-- About Section -->
        <section class="about animate-on-scroll">
            <div class="about-content">
                <h2>About Us</h2>
                <p>
                    GreenEarth Initiative is a non-profit organization dedicated to reducing carbon emissions through
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
                            <router-link to="/emission-calculator">Carbon Calculator</router-link>
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
</style>
