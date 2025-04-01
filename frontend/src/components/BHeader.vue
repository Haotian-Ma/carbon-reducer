<template>
    <div>
        <div class="header-placeholder" v-if="isSticky"></div>
        <header class="header" :class="{ 'sticky': isSticky }">
            <div class="container header-container">
                <div class="logo-title-container">
                    <router-link to="/" class="logo-link">
                        <img src="../assets/images/logo.jpg" alt="Logo" class="logo-image" />
                    </router-link>
                    <h1 class="title">EcoSphere - Carbon Reduction</h1>
                </div>
                <ul class="nav">
                    <li class="nav-item">
                        <router-link to="/" class="nav-link" active-class="active"
                            aria-current="page">Home</router-link>
                    </li>
                    <li class="nav-item">
                        <router-link to="/about" class="nav-link" active-class="active">About</router-link>
                    </li>
                    <!-- <li class="nav-item">
                        <router-link to="/emission-calculator" class="nav-link" active-class="active">Carbon Calculator</router-link>
                    </li> -->
                </ul>
            </div>
        </header>
    </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue';

const isSticky = ref(false);
const headerHeight = ref(0);

const handleScroll = () => {
    const scrollPosition = window.scrollY;
    isSticky.value = scrollPosition > 10;
};

onMounted(() => {
    const headerElement = document.querySelector('.header');
    if (headerElement) {
        headerHeight.value = headerElement.offsetHeight;
    }

    window.addEventListener('scroll', handleScroll);
    handleScroll();
});

onUnmounted(() => {
    window.removeEventListener('scroll', handleScroll);
});
</script>

<style scoped>
.logo-title-container {
    display: flex;
    align-items: center;
    gap: 15px;
}

.logo-link {
    display: flex;
    align-items: center;
}

.title {
    margin: 0;
    font-size: 24px;
    color: white;
    font-weight: bold;
}

.header {
    width: 100%;
    background: linear-gradient(135deg, var(--primary-gradient-start), var(--primary-gradient-end));
    box-shadow: var(--shadow);
    border-radius: var(--border-radius);
    transition: var(--transition);
    z-index: 1000;
}

.header.sticky {
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    border-radius: 0 0 var(--border-radius) var(--border-radius);
    box-shadow: var(--shadow-hover);
    animation: slideDown 0.3s ease-out;
}

.header-placeholder {
    height: 70px;
}



.header-container {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 10px 20px;
}

.logo-image {
    height: 50px;
    width: 50px;
    border-radius: 50%;
    transition: transform 0.3s ease;
}

.logo-link:hover .logo-image {
    transform: scale(1.1);
}


@media (max-width: 768px) {
    .header-container {
        flex-direction: column;
        align-items: flex-start;
        padding: 10px;
    }

    .logo-title-container {
        margin-bottom: 10px;
        width: 100%;
    }

    .nav {
        flex-direction: column;
        gap: 10px;
        width: 100%;
    }

    .nav-item .nav-link {
        width: 100%;
        text-align: center;
    }

    .header-placeholder {
        height: 150px;
    }
}
</style>