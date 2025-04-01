<script setup>
import { ref, onMounted, onBeforeUnmount } from 'vue';
import { useRouter } from 'vue-router';
// import ArticlesList from '../components/ArticleList.vue';
import axios from 'axios'
// Data for carousel images
const carouselImages = [
    "https://media.istockphoto.com/id/1366228771/photo/volunteer-planting-trees-in-forest-carbon-emission-reforestation-restoration-gardener-with.jpg?s=1024x1024&w=is&k=20&c=C3FXOVv2nTUvNDhQYCeZ7_Z0-lX1VF0vf0FPGdE1FPQ=",
    "https://media.istockphoto.com/id/1368724296/photo/recycling-conservation-in-the-park-group-of-happy-volunteer-with-garbage-bags-cleaning-area.jpg?s=612x612&w=0&k=20&c=z0QvnhTUfRFIKlARzNkk_uowU9yTNwgFBaX11-mzlsA=",
    "https://media.istockphoto.com/id/1284382234/photo/young-couple-planting-tree-in-garden-together-as-save-world-concept.jpg?s=612x612&w=0&k=20&c=KBGW0mGxYV9v1_EAVF_wh7S9AFOGmGrQUZ_Z-4MTKFc=",
];

import { computed } from 'vue';

const currentImage = computed(() => {
    return carouselImages[currentSlide.value];
});

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

// Carousel logic with auto-rotation
const currentSlide = ref(0);
const isCarouselPaused = ref(false);
let carouselInterval = null;

const nextSlide = () => {
    currentSlide.value = (currentSlide.value + 1) % carouselImages.length;
};

const prevSlide = () => {
    currentSlide.value = (currentSlide.value - 1 + carouselImages.length) % carouselImages.length;
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

// Animation on scroll
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
            console.error('Failed：', error);
        });
});

onBeforeUnmount(() => {
    clearInterval(carouselInterval);
});
</script>

<template>
    <div class="home-page">
        <!-- Hero Section - Enhanced Carousel -->
        <!-- <section class="hero">
            <div class="carousel" @mouseenter="pauseCarousel" @mouseleave="resumeCarousel">
                <div class="carousel-container">
                    <transition name="fade">
                        <img v-if="currentImage" :src="currentImage" alt="Carousel Image" class="carousel-image" />
                    </transition>
                    <div class="carousel-content">
                        <h1 class="carousel-title">Plant Trees, Reduce Carbon, Save Earth</h1>
                        <p class="carousel-subtitle">Join our mission to combat climate change through tree planting and
                            carbon reduction</p>
                    </div>
                </div>
                <button class="carousel-button prev" @click="prevSlide">&#10094;</button>
                <button class="carousel-button next" @click="nextSlide">&#10095;</button>
                <div class="carousel-indicators">
                    <span v-for="(image, index) in carouselImages" :key="index"
                        :class="{ active: currentSlide === index }" @click="currentSlide = index">
                    </span>
                </div>
            </div>
        </section> -->

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
<style scoped></style>