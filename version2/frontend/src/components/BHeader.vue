<template>
    <div>
        <div class="header-placeholder" v-if="isSticky"></div>
        <header class="header" :class="{ 'sticky': isSticky }">
            <div class="container header-container">
                <div class="logo-title-container">
                    <router-link to="/" class="logo-link">
                        <img src="../assets/images/logo.jpg" alt="Logo" class="logo-image" />
                    </router-link>
                    <h1 class="title">EcoSphere</h1>
                </div>
                <ul class="nav">
                    <li class="nav-item">
                        <router-link to="/" class="nav-link" active-class="active"
                            aria-current="page">Home</router-link>
                    </li>
                    <li class="nav-item">
                        <router-link to="/eco-action" class="nav-link" active-class="active">Eco Action</router-link>
                    </li>
                    <li class="nav-item">
                        <router-link to="/virtual-tree" class="nav-link" active-class="active">Virtual
                            Tree</router-link>
                    </li>
                    <!-- Resources Dropdown -->
                    <li class="nav-item dropdown">
                        <a href="#" class="nav-link dropdown-toggle" @click.prevent="toggleResourcesDropdown">
                            Resources
                            <span class="dropdown-icon" :class="{ 'open': isResourcesOpen }">▼</span>
                        </a>
                        <ul class="dropdown-menu" v-show="isResourcesOpen">
                            <li class="dropdown-item">
                                <router-link to="/resources/climate-insight" class="dropdown-link">
                                    Climate Insight
                                </router-link>
                            </li>
                            <li class="dropdown-item">
                                <router-link to="/resources/kids-learning" class="dropdown-link">
                                    Kids Learning
                                </router-link>
                            </li>
                            <li class="dropdown-item">
                                <router-link to="/resources/Map" class="dropdown-link">
                                    VegetationMap
                                </router-link>
                            </li>
                        </ul>
                    </li>
                    <li class="nav-item">
                        <router-link to="/about" class="nav-link" active-class="active">About</router-link>
                    </li>
                </ul>
            </div>
        </header>
    </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue';

const isSticky = ref(false);
const headerHeight = ref(0);
const isResourcesOpen = ref(false);

const handleScroll = () => {
    const scrollPosition = window.scrollY;
    isSticky.value = scrollPosition > 10;
};

const toggleResourcesDropdown = () => {
    isResourcesOpen.value = !isResourcesOpen.value;
};

// Close dropdown when clicking outside
const handleClickOutside = (event) => {
    const dropdown = document.querySelector('.dropdown');
    if (dropdown && !dropdown.contains(event.target) && isResourcesOpen.value) {
        isResourcesOpen.value = false;
    }
};

onMounted(() => {
    const headerElement = document.querySelector('.header');
    if (headerElement) {
        headerHeight.value = headerElement.offsetHeight;
    }

    window.addEventListener('scroll', handleScroll);
    document.addEventListener('click', handleClickOutside);
    handleScroll();
});

onUnmounted(() => {
    window.removeEventListener('scroll', handleScroll);
    document.removeEventListener('click', handleClickOutside);
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
    width: 100vw;
    max-width: 100vw;
    margin-left: calc(-50vw + 50%);
    margin-right: calc(-50vw + 50%);
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

/* Navigation Items */
.nav {
    display: flex;
    list-style: none;
    margin: 0;
    padding: 0;
    gap: 20px;
}

.nav-item {
    position: relative;
}

.nav-link {
    color: white;
    text-decoration: none;
    font-weight: 500;
    padding: 8px 12px;
    border-radius: 4px;
    transition: background-color 0.2s;
    display: block;
}

.nav-link:hover,
.nav-link.active {
    background-color: rgba(255, 255, 255, 0.2);
}

/* Dropdown Styling */
.dropdown {
    position: relative;
}

.dropdown-toggle {
    display: flex;
    align-items: center;
    gap: 5px;
}

.dropdown-icon {
    font-size: 10px;
    transition: transform 0.2s ease;
}

.dropdown-icon.open {
    transform: rotate(180deg);
}

.dropdown-menu {
    position: absolute;
    top: 100%;
    left: 0;
    background-color: white;
    min-width: 180px;
    border-radius: 4px;
    box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
    padding: 8px 0;
    margin-top: 5px;
    list-style: none;
    z-index: 1001;
}

.dropdown-item {
    margin: 0;
    padding: 0;
}

.dropdown-link {
    color: var(--text-color);
    text-decoration: none;
    padding: 8px 16px;
    display: block;
    transition: background-color 0.2s;
}

.dropdown-link:hover {
    background-color: #f5f5f5;
    color: var(--primary-gradient-end);
}

@keyframes slideDown {
    from {
        transform: translateY(-100%);
    }

    to {
        transform: translateY(0);
    }
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

    .dropdown-toggle {
        text-align: center;
        justify-content: center;
    }

    .dropdown-menu {
        position: static;
        width: 100%;
        box-shadow: none;
        margin-top: 5px;
        border: 1px solid #eee;
    }

    .header-placeholder {
        height: 150px;
    }
}
</style>