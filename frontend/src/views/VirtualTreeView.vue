<template>
    <div class="container mt-5">
        <div class="row">
            <div class="col-md-10 offset-md-1">
                <section class="about-us">
                    <h2 class="text-center mb-4 display-5 fw-bold tree-title">
                        <i class="fas fa-tree text-success me-2"></i>Virtual Tree
                    </h2>

                    <!-- Feedback message toast -->
                    <div class="position-fixed top-0 end-0 p-3" style="z-index: 11">
                        <div :class="['toast show feedback-toast', toastType]" v-if="showToast" role="alert"
                            aria-live="assertive" aria-atomic="true">
                            <div class="toast-header">
                                <i :class="toastIcon"></i>
                                <strong class="me-auto ms-2">{{ toastTitle }}</strong>
                                <button type="button" class="btn-close" @click="showToast = false"></button>
                            </div>
                            <div class="toast-body">
                                {{ toastMessage }}
                            </div>
                        </div>
                    </div>

                    <!-- Weather effects container -->
                    <div class="weather-container" ref="weatherContainer">
                        <div v-if="showRain" class="rain"></div>
                        <div v-if="showSunshine" class="sunshine"></div>
                    </div>

                    <!-- Animation Container with improved size constraints -->
                    <div class="animation-container">
                        <div ref="animationContainer" class="lottie-animation"></div>

                        <!-- Floating icons for care actions -->
                        <div v-if="showWaterDrop" class="floating-icon water-drop">
                            <i class="fas fa-tint"></i>
                        </div>
                        <div v-if="showFertilizer" class="floating-icon fertilizer">
                            <i class="fas fa-leaf"></i>
                        </div>
                        <div v-if="showSun" class="floating-icon sun-icon">
                            <i class="fas fa-sun"></i>
                        </div>

                        <!-- Stage up animation -->
                        <div v-if="showLevelUp" class="level-up-animation">
                            <div class="level-up-text">Level Up!</div>
                        </div>
                    </div>

                    <!-- Tree chat bubble -->
                    <div class="speech-bubble" v-if="showTreeMessage">
                        <p>{{ treeMessage }}</p>
                    </div>
                    <!-- Care actions with improved button styling and hover effects -->
                    <div class="care-actions my-4" v-if="currentStageIndex < growthStages.length - 1">
                        <div class="d-flex flex-wrap justify-content-center gap-3">
                            <button @click="careTree('water')" class="btn btn-water care-button"
                                :disabled="userPoints < waterPointsCost" :class="{ 'shake-animation': waterBtnShake }">
                                <i class="fas fa-tint me-2"></i>Water
                                <span class="badge bg-white text-primary ms-1">-{{ waterPointsCost }}</span>
                                <div class="btn-hover-effect water-effect"></div>
                            </button>

                            <button @click="careTree('fertilizer')" class="btn btn-fertilizer care-button"
                                :disabled="userPoints < fertilizerPointsCost"
                                :class="{ 'shake-animation': fertilizerBtnShake }">
                                <i class="fas fa-seedling me-2"></i>Fertilize
                                <span class="badge bg-white text-primay ms-1">-{{ fertilizerPointsCost }}</span>
                                <div class="btn-hover-effect fertilizer-effect"></div>
                            </button>

                            <button @click="careTree('sunlight')" class="btn btn-sunlight care-button"
                                :disabled="userPoints < fertilizerPointsCost"
                                :class="{ 'shake-animation': sunlightBtnShake }">
                                <i class="fas fa-sun me-2"></i>Sunlight
                                <span class="badge bg-white text-warning ms-1">-{{ sunlightPointsCost }}</span>
                                <div class="btn-hover-effect sunlight-effect"></div>
                            </button>

                            <button @click="getPoints" class="btn btn-success get-points-button"
                                :class="{ 'pulse-animation': getPointsBtnPulse }">
                                <i class="fas fa-coins me-2"></i>Get Points
                                <span class="badge bg-white text-success ms-1">+100</span>
                                <div class="btn-hover-effect coins-effect"></div>
                            </button>
                        </div>
                    </div>
                    <!-- Mature tree message with improved styling and confetti animation -->
                    <div v-else class="mature-tree-message text-center my-4 p-4">
                        <div class="achievement-icon mb-3">
                            <i class="fas fa-award text-warning" style="font-size: 3rem;"></i>
                        </div>
                        <div class="confetti-container" v-if="showConfetti">
                            <div v-for="n in 30" :key="n" :class="'confetti-' + n"></div>
                        </div>
                        <p class="text-success fw-bold fs-5 mb-3">
                            <i class="fas fa-check-circle me-2"></i>Your tree is fully mature and thriving!
                        </p>
                        <button @click="plantNewTree" class="btn btn-primary btn-lg mt-2 plant-new-btn">
                            <i class="fas fa-seedling me-2"></i>Plant a New Tree
                            <div class="btn-hover-effect plant-effect"></div>
                        </button>
                    </div>

                    <!-- Growth stage display - With animation and improved styling -->
                    <div class="stage-display text-center my-4 p-4 nature-theme mb-5"
                        :class="{ 'pulse-animation': stageChanged }">
                        <div class="stage-icon">
                            <i class="fas fa-tree text-success"></i>
                        </div>
                        <h4 class="fw-bold mt-2">{{ currentStage.label }}</h4>
                        <div v-if="currentStageIndex < growthStages.length - 1" class="next-stage-info mb-0 mt-3">
                            <span class="text-muted fs-6">Next stage: {{ nextStage.label }}</span>
                            <span class="badge bg-warning text-dark ms-2 progress-badge">
                                <i class="fas fa-star me-1"></i>Needs {{ nextStage.requiredPoints - totalPoints }}
                                points
                            </span>
                        </div>
                        <p v-else class="text-success fw-bold mb-0 mt-3">
                            <i class="fas fa-check-circle me-2"></i>Your tree is fully mature! 🌳
                        </p>
                    </div>

                    <!-- Points and progress section - UNCHANGED -->
                    <div class="progress-container mt-5 mb-4">
                        <div class="points-display d-flex justify-content-between mb-3">
                            <span class="badge bg-primary fs-6 d-flex align-items-center"
                                :class="{ 'bounce-animation': pointsChanged }">
                                <i class="fas fa-coins me-2"></i>Your Points: {{ userPoints }}
                            </span>
                            <span class="badge bg-success fs-6 d-flex align-items-center"
                                :class="{ 'bounce-animation': growthPointsChanged }">
                                <i class="fas fa-chart-line me-2"></i>Growth Points: {{ totalPoints }}
                            </span>
                        </div>
                        <div class="progress" style="height: 25px; border-radius: 12px;">
                            <div class="progress-bar progress-bar-striped progress-bar-animated" role="progressbar"
                                :style="{ width: stageProgress + '%' }" :class="progressBarColor">
                                {{ stageProgress }}%
                            </div>
                        </div>
                        <div class="tree-stats text-center mt-3">
                            <span class="badge bg-success me-2 fs-6">
                                <i class="fas fa-tree me-2"></i>Trees Planted: {{ totalTreesPlanted }}
                            </span>
                        </div>
                    </div>
                    <!-- Growth history with card styling and animations -->
                    <div class="history mt-4 card shadow-sm" v-if="growthHistory.length > 0">
                        <div class="card-header bg-light">
                            <h5 class="mb-0 text-center">
                                <i class="fas fa-history me-2"></i>Growth Journey
                            </h5>
                        </div>
                        <ul class="list-group list-group-flush">
                            <li class="list-group-item py-2" v-for="(record, index) in growthHistory" :key="index"
                                :class="{ 'fade-in-animation': index === 0 && newHistoryItem }">
                                <small class="text-muted">{{ record }}</small>
                            </li>
                        </ul>
                    </div>
                    <!-- Tree Guide -->
                    <div class="tree-guide mt-5 card shadow-sm">
                        <div class="card-header bg-light py-3">
                            <h5 class="mb-0 text-center fw-bold">
                                <i class="fas fa-book me-2"></i>Tree Growth Guide
                            </h5>
                        </div>
                        <div class="card-body p-0">
                            <!-- Content container -->
                            <div class="guide-content">
                                <!-- Carousel container -->
                                <div class="carousel-container position-relative">
                                    <div class="stage-carousel"
                                        :style="{ transform: `translateX(-${currentGuideIndex * 100}%)` }">
                                        <div v-for="(stage, index) in growthStages" :key="index" class="stage-slide">
                                            <div class="stage-content"
                                                :class="{ 'current-stage': index === currentStageIndex }">
                                                <div class="guide-image-container" :ref="el => setStageRef(el, index)">
                                                </div>
                                                <div class="stage-info p-4">
                                                    <h4
                                                        class="stage-title mb-2 d-flex align-items-center justify-content-between">
                                                        {{ stage.label }}
                                                        <span v-if="index === currentStageIndex"
                                                            class="current-badge">Current</span>
                                                    </h4>
                                                    <p class="stage-points my-3">
                                                        <i class="fas fa-star me-2 text-warning"></i>
                                                        <strong>Required Points:</strong> {{ stage.requiredPoints }}
                                                    </p>
                                                    <p class="stage-description">
                                                        Learn about the characteristics of this growth stage and how to
                                                        care for your tree.
                                                    </p>
                                                </div>
                                            </div>
                                        </div>
                                    </div>

                                    <!-- Left and right navigation buttons -->
                                    <button class="carousel-control carousel-control-prev" @click="goToPrevGuideStage"
                                        :disabled="currentGuideIndex === 0">
                                        <i class="fas fa-chevron-left"></i>
                                    </button>
                                    <button class="carousel-control carousel-control-next" @click="goToNextGuideStage"
                                        :disabled="currentGuideIndex === growthStages.length - 1">
                                        <i class="fas fa-chevron-right"></i>
                                    </button>
                                </div>

                                <!-- Stage indicators - modified for horizontal layout -->
                                <div class="stage-indicators py-3 d-flex justify-content-center">
                                    <div v-for="(stage, idx) in growthStages" :key="'ind-' + idx"
                                        class="stage-indicator mx-2" :class="{ 'active': currentGuideIndex === idx }"
                                        @click="currentGuideIndex = idx">
                                        <span class="stage-dot"></span>
                                        <small class="stage-name">{{ stage.label }}</small>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                </section>
            </div>
        </div>
    </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted, computed, watch } from 'vue';
import lottie from 'lottie-web';

const animationContainer = ref(null);
const weatherContainer = ref(null);
let animation = null;
let frameByFrameInterval = null;
const treesPlanted = ref(parseInt(localStorage.getItem('treesPlanted')) || 0);
const stageAnimations = ref([]);
const stageRefs = ref([]);
const currentGuideIndex = ref(0);

const setStageRef = (el, index) => {
    if (el) {
        stageRefs.value[index] = el;
    }
};
const goToNextGuideStage = () => {
    if (currentGuideIndex.value < growthStages.length - 1) {
        currentGuideIndex.value++;
    }
};

const goToPrevGuideStage = () => {
    if (currentGuideIndex.value > 0) {
        currentGuideIndex.value--;
    }
};



// User points from local storage - starting with more points for better gameplay
const userPoints = ref(parseInt(localStorage.getItem('userPoints')) || 200);

// Care cost
const waterPointsCost = 30;
const fertilizerPointsCost = 40;
const sunlightPointsCost = 35;
// Care counters
const careCount = ref({
    water: parseInt(localStorage.getItem('waterCount')) || 0,
    fertilizer: parseInt(localStorage.getItem('fertilizerCount')) || 0,
    sunlight: parseInt(localStorage.getItem('sunlightCount')) || 0
});

const growthHistory = ref(JSON.parse(localStorage.getItem('growthHistory')) || []);
const currentStageIndex = ref(parseInt(localStorage.getItem('currentStageIndex')) || 0);
const hasShownCompletion = ref(false);

// Animation state variables
const showWaterDrop = ref(false);
const showFertilizer = ref(false);
const showSun = ref(false);
const showLevelUp = ref(false);
const showRain = ref(false);
const showSunshine = ref(false);
const showConfetti = ref(false);
const pointsChanged = ref(false);
const growthPointsChanged = ref(false);
const stageChanged = ref(false);
const waterBtnShake = ref(false);
const fertilizerBtnShake = ref(false);
const sunlightBtnShake = ref(false);
const getPointsBtnPulse = ref(false);
const newHistoryItem = ref(false);

// Toast notification system
const showToast = ref(false);
const toastMessage = ref('');
const toastTitle = ref('');
const toastType = ref('');
const toastIcon = ref('');


// Tree message bubble
const showTreeMessage = ref(false);
const treeMessage = ref('');

// Define growth stages with exponential point requirements
const growthStages = [
    { label: 'Seed Stage', startFrame: 20, endFrame: 60, requiredPoints: 0 },
    { label: 'Sprouting', startFrame: 240, endFrame: 280, requiredPoints: 100 },
    { label: 'Small Tree', startFrame: 450, endFrame: 500, requiredPoints: 300 },  // 100 + 200
    { label: 'Growing Tree', startFrame: 650, endFrame: 720, requiredPoints: 700 }, // 300 + 400
    { label: 'Mature Tree', startFrame: 900, endFrame: 960, requiredPoints: 1500 }  // 700 + 800
];

// Tree messages for different stages and actions
const treeMessages = {
    water: [
        "Ahh, that's refreshing! Thank you for the water!",
        "I was so thirsty! Thank you!",
        "Water helps my roots grow strong!",
        "Slurp! Delicious water!",
        "I feel refreshed now!"
    ],
    fertilizer: [
        "Mmm, nutrients! Just what I needed!",
        "This will help me grow big and strong!",
        "Thank you for the food!",
        "Yummy fertilizer! My favorite!",
        "I can feel myself getting stronger!"
    ],
    sunlight: [
        "Ahhh, warm sunshine! Perfect for photosynthesis!",
        "I love basking in the sun!",
        "Sunlight gives me energy to grow!",
        "The sun feels so good on my leaves!",
        "Sunshine makes me happy!"
    ],
    stageChange: [
        "I'm growing! I can feel it!",
        "Look at me now! I'm getting bigger!",
        "Wow! I reached a new stage!",
        "Thank you for helping me grow!",
        "I'm one step closer to becoming a magnificent tree!"
    ],
    mature: [
        "I've reached my full potential! Thank you for nurturing me!",
        "I'm a fully grown tree now! I couldn't have done it without you!",
        "Look at me! From a tiny seed to a majestic tree!",
        "I'll provide shade and oxygen for years to come. Thank you!",
        "We did it! I'm all grown up now!"
    ]
};

const playCurrentStageAnimation = () => {
    if (!animation) return;

    const stage = growthStages[currentStageIndex.value];
    playFrameByFrame(stage.startFrame, stage.endFrame, 24);
};

// Computed properties
const totalPoints = computed(() => {
    return (careCount.value.water * waterPointsCost +
        careCount.value.fertilizer * fertilizerPointsCost +
        careCount.value.sunlight * sunlightPointsCost);
});

const currentStage = computed(() => {
    return growthStages[currentStageIndex.value];
});

const nextStage = computed(() => {
    return currentStageIndex.value < growthStages.length - 1
        ? growthStages[currentStageIndex.value + 1]
        : { label: 'Max Stage', requiredPoints: 0 };
});

const stagePoints = computed(() => {
    return totalPoints.value - currentStage.value.requiredPoints;
});

const stageProgress = computed(() => {
    if (currentStageIndex.value >= growthStages.length - 1) return 100;
    const currentRequired = currentStage.value.requiredPoints;
    const nextRequired = nextStage.value.requiredPoints;
    const progress = ((totalPoints.value - currentRequired) / (nextRequired - currentRequired)) * 100;
    return Math.min(100, Math.max(0, Math.floor(progress)));
});

// New computed property for progress bar color
const progressBarColor = computed(() => {
    const progress = stageProgress.value;
    if (progress < 25) return 'bg-danger';
    if (progress < 50) return 'bg-warning';
    if (progress < 75) return 'bg-info';
    return 'bg-success';
});

// Helper function to display toast
const showToastMessage = (title, message, type) => {
    toastTitle.value = title;
    toastMessage.value = message;
    toastType.value = type;

    // Set icon based on type
    if (type === 'toast-success') {
        toastIcon.value = 'fas fa-check-circle text-success me-2';
    } else if (type === 'toast-water') {
        toastIcon.value = 'fas fa-tint text-primary me-2';
    } else if (type === 'toast-fertilizer') {
        toastIcon.value = 'fas fa-seedling text-brown me-2';
    } else if (type === 'toast-sunlight') {
        toastIcon.value = 'fas fa-sun text-warning me-2';
    } else {
        toastIcon.value = 'fas fa-info-circle text-info me-2';
    }

    showToast.value = true;

    // Hide toast after 3 seconds
    setTimeout(() => {
        showToast.value = false;
    }, 3000);
};

// Show tree message

const displayTreeMessage = (type) => {
    let messages;
    if (type === 'stageChange') {
        messages = treeMessages.stageChange;
    } else if (type === 'mature') {
        messages = treeMessages.mature;
    } else {
        messages = treeMessages[type];
    }

    // Get random message from array
    const randomIndex = Math.floor(Math.random() * messages.length);
    treeMessage.value = messages[randomIndex];

    // Show message
    showTreeMessage.value = true;

    // Hide message after 4 seconds
    setTimeout(() => {
        showTreeMessage.value = false;
    }, 4000);
};

// Care function
const careTree = (type) => {
    let pointsCost = 0;
    if (type === 'water') {
        pointsCost = waterPointsCost;
    } else if (type === 'fertilizer') {
        pointsCost = fertilizerPointsCost;
    } else if (type === 'sunlight') {
        pointsCost = sunlightPointsCost;
    }
    if (userPoints.value < pointsCost) return;

    // Deduct points
    userPoints.value -= pointsCost;
    localStorage.setItem('userPoints', userPoints.value);

    // Animate points change
    pointsChanged.value = true;
    setTimeout(() => {
        pointsChanged.value = false;
    }, 1000);

    // Add to care count
    careCount.value[type]++;

    // Save care counts to localStorage
    localStorage.setItem('waterCount', careCount.value.water);
    localStorage.setItem('fertilizerCount', careCount.value.fertilizer);
    localStorage.setItem('sunlightCount', careCount.value.sunlight);

    // Animate growth points change
    growthPointsChanged.value = true;
    setTimeout(() => {
        growthPointsChanged.value = false;
    }, 1000);

    // Add action to history
    const actionText = `${type.charAt(0).toUpperCase() + type.slice(1)} applied (${pointsCost} points used)`;
    growthHistory.value.unshift(actionText);

    // Animate new history item
    newHistoryItem.value = true;
    setTimeout(() => {
        newHistoryItem.value = false;
    }, 1000);

    // Keep only last 5 records
    if (growthHistory.value.length > 5) {
        growthHistory.value.pop();
    }

    // Save history
    localStorage.setItem('growthHistory', JSON.stringify(growthHistory.value));

    // Show toast notification
    showToastMessage(
        `${type.charAt(0).toUpperCase() + type.slice(1)} Applied`,
        `You applied ${type} to your tree. It's growing healthier!`,
        `toast-${type}`
    );

    // Show tree message
    displayTreeMessage(type);

    // Play visual effects
    if (type === 'water') {
        // Show water drops animation
        showWaterDrop.value = true;
        setTimeout(() => {
            showWaterDrop.value = false;
        }, 2000);

        // Show rain effect
        showRain.value = true;
        setTimeout(() => {
            showRain.value = false;
        }, 3000);

        // Shake water button
        waterBtnShake.value = true;
        setTimeout(() => {
            waterBtnShake.value = false;
        }, 1000);
    } else if (type === 'fertilizer') {
        // Show fertilizer animation
        showFertilizer.value = true;
        setTimeout(() => {
            showFertilizer.value = false;
        }, 2000);

        // Shake fertilizer button
        fertilizerBtnShake.value = true;
        setTimeout(() => {
            fertilizerBtnShake.value = false;
        }, 1000);
    } else if (type === 'sunlight') {
        // Show sun animation
        showSun.value = true;
        setTimeout(() => {
            showSun.value = false;
        }, 2000);

        // Show sunshine effect
        showSunshine.value = true;
        setTimeout(() => {
            showSunshine.value = false;
        }, 3000);

        // Shake sunlight button
        sunlightBtnShake.value = true;
        setTimeout(() => {
            sunlightBtnShake.value = false;
        }, 1000);
    }

    // Check if we've reached the next stage
    checkGrowth();
};

const checkGrowth = () => {
    // Find the highest stage the tree has reached based on points
    let newStageIndex = 0;
    for (let i = growthStages.length - 1; i >= 0; i--) {
        if (totalPoints.value >= growthStages[i].requiredPoints) {
            newStageIndex = i;
            break;
        }
    }

    // If stage changed, update animation and add to history
    if (newStageIndex !== currentStageIndex.value) {
        const oldStage = currentStage.value.label;
        currentStageIndex.value = newStageIndex;
        const newStage = growthStages[newStageIndex];

        // Update animation
        if (animation) {
            animation.goToAndStop(newStage.endFrame, true);
        }

        // Stop current animation
        stopFrameByFrameAnimation();

        // Play new stage animation
        playCurrentStageAnimation();

        // Show level up animation
        showLevelUp.value = true;
        setTimeout(() => {
            showLevelUp.value = false;
        }, 2000);

        // Animate stage display
        stageChanged.value = true;
        setTimeout(() => {
            stageChanged.value = false;
        }, 1500);

        // Show tree message for stage change
        if (newStageIndex === growthStages.length - 1) {
            displayTreeMessage('mature');
        } else {
            displayTreeMessage('stageChange');
        }

        // Show toast notification for level up
        showToastMessage(
            'Level Up!',
            `Your tree has grown to ${newStage.label}!`,
            'toast-success'
        );

        // Add to growth history
        growthHistory.value.unshift(`🌱 Advanced to ${newStage.label} (Total points: ${totalPoints.value})`);

        // Animate new history item
        newHistoryItem.value = true;
        setTimeout(() => {
            newHistoryItem.value = false;
        }, 1000);

        // Keep only last 5 records
        if (growthHistory.value.length > 5) {
            growthHistory.value.pop();
        }

        // Save to localStorage
        localStorage.setItem('currentStageIndex', currentStageIndex.value);
        localStorage.setItem('growthHistory', JSON.stringify(growthHistory.value));

        // Check if reached final stage
        if (currentStageIndex.value === growthStages.length - 1 && !hasShownCompletion.value) {
            handleTreeMatured();
            hasShownCompletion.value = false;
        }
    }
};

// Add new function to handle tree maturation
const handleTreeMatured = () => {
    // Show confetti animation
    showConfetti.value = true;
    setTimeout(() => {
        showConfetti.value = false;
    }, 5000);

    // Increment trees planted count
    treesPlanted.value++;
    localStorage.setItem('treesPlanted', treesPlanted.value);

    // Add achievement transaction
    const transactions = JSON.parse(localStorage.getItem('pointsTransactions')) || [];
    const transaction = {
        description: `Mature Tree Achievement - Tree #${treesPlanted.value}`,
        amount: 0, // No points for this, just a record
        type: 'achievement',
        icon: 'fas fa-tree',
        date: new Date().toISOString()
    };
    transactions.unshift(transaction);

    // Keep only last 50 transactions
    if (transactions.length > 50) {
        transactions.splice(50);
    }
    localStorage.setItem('pointsTransactions', JSON.stringify(transactions));

    // Update tree statistics
    localStorage.setItem('totalTreesPlanted', treesPlanted.value);

    // Show toast notification for completion
    showToastMessage(
        'Achievement Unlocked!',
        `Congratulations! You've grown a mature tree!`,
        'toast-success'
    );
};

// Add new function for planting new tree
const plantNewTree = () => {
    resetTree();

    // Show toast notification
    showToastMessage(
        'New Tree Planted',
        `You've started growing a new tree! Let's see how fast it grows.`,
        'toast-success'
    );

    // Show tree message
    treeMessage.value = "Hello! I'm just a little seed now. Can you help me grow?";
    showTreeMessage.value = true;
    setTimeout(() => {
        showTreeMessage.value = false;
    }, 4000);
};

// Modify the resetTree function
const resetTree = () => {
    // Clear all game data
    careCount.value = { water: 0, fertilizer: 0, sunlight: 0 };
    currentStageIndex.value = 0;
    growthHistory.value = [`New tree #${treesPlanted.value + 1} planted!`];
    hasShownCompletion.value = true;

    // Reset animation
    if (animation) {
        stopFrameByFrameAnimation();
        playCurrentStageAnimation();
        animation.goToAndStop(growthStages[0].endFrame, true);
    }

    // Clear localStorage
    localStorage.removeItem('waterCount');
    localStorage.removeItem('fertilizerCount');
    localStorage.removeItem('sunlightCount');
    localStorage.removeItem('currentStageIndex');
    localStorage.setItem('growthHistory', JSON.stringify(growthHistory.value));

    // Animate new history item
    newHistoryItem.value = true;
    setTimeout(() => {
        newHistoryItem.value = false;
    }, 1000);
};

// Add tree count display to computed properties
const totalTreesPlanted = computed(() => {
    return treesPlanted.value;
});

// Animation control functions
const playFrameByFrame = (startFrame, endFrame, frameRate = 24) => {
    if (!animation) return;
    stopFrameByFrameAnimation();
    animation.goToAndStop(startFrame, true);
    const frameInterval = 1000 / frameRate;
    let currentFrame = startFrame;
    frameByFrameInterval = setInterval(() => {
        currentFrame++;
        animation.goToAndStop(currentFrame, true);
        if (currentFrame >= endFrame) {
            stopFrameByFrameAnimation();
            animation.goToAndStop(endFrame, true);
        }
    }, frameInterval);
};

const stopFrameByFrameAnimation = () => {
    if (frameByFrameInterval) {
        clearInterval(frameByFrameInterval);
        frameByFrameInterval = null;
    }
};

// Add points function
const getPoints = () => {
    userPoints.value += 100;
    localStorage.setItem('userPoints', userPoints.value);

    // Animate button and points
    getPointsBtnPulse.value = true;
    setTimeout(() => {
        getPointsBtnPulse.value = false;
    }, 1000);

    pointsChanged.value = true;
    setTimeout(() => {
        pointsChanged.value = false;
    }, 1000);

    // Add to history
    growthHistory.value.unshift('💰 Received 100 points!');

    // Animate new history item
    newHistoryItem.value = true;
    setTimeout(() => {
        newHistoryItem.value = false;
    }, 1000);

    // Keep only last 5 records
    if (growthHistory.value.length > 5) {
        growthHistory.value.pop();
    }

    // Save history
    localStorage.setItem('growthHistory', JSON.stringify(growthHistory.value));

    // Show toast notification
    showToastMessage(
        'Points Added',
        'You received 100 points! Use them to help your tree grow.',
        'toast-success'
    );
};

onMounted(async () => {
    try {
        // Load animation data
        const animationData = await import('../assets/animations/virtual-tree-animation.json');

        if (animationContainer.value) {
            // Initialize Lottie animation
            animation = lottie.loadAnimation({
                container: animationContainer.value,
                renderer: 'svg',
                loop: false,
                autoplay: false,
                animationData: animationData.default || animationData
            });

            // Set initial state when animation is loaded
            animation.addEventListener('DOMLoaded', () => {
                playCurrentStageAnimation();
                const currentFrame = growthStages[currentStageIndex.value].endFrame;
                animation.goToAndStop(currentFrame, true);

                // If it's a new session and tree isn't mature, show welcome message
                if (currentStageIndex.value < growthStages.length - 1) {
                    setTimeout(() => {
                        treeMessage.value = "Hello again! I'm happy to see you. Help me grow more!";
                        showTreeMessage.value = true;
                        setTimeout(() => {
                            showTreeMessage.value = false;
                        }, 4000);
                    }, 1000);
                }


                setTimeout(() => {

                    growthStages.forEach((stage, index) => {
                        if (stageRefs.value[index]) {
                            const stageAnim = lottie.loadAnimation({
                                container: stageRefs.value[index],
                                renderer: 'svg',
                                loop: false,
                                autoplay: false,
                                animationData: animationData.default || animationData
                            });


                            stageAnim.goToAndStop(stage.endFrame, true);


                            stageAnimations.value[index] = stageAnim;
                        }
                    });
                }, 500);
            });
        }
    } catch (error) {
        console.error('Error loading animation:', error);
    }
});

onUnmounted(() => {
    stopFrameByFrameAnimation();
    if (animation) {
        animation.destroy();
        animation = null;
    }
    stageAnimations.value.forEach(anim => {
        if (anim) {
            anim.destroy();
        }
    });
});
watch(currentStageIndex, (newIndex) => {
    currentGuideIndex.value = newIndex;
});

</script>

<style scoped>
.animation-container {
    height: 450px;
    margin: 20px auto;
    display: flex;
    justify-content: center;
    align-items: center;
    background-color: rgba(240, 255, 240, 0.3);
    border-radius: 16px;
    overflow: hidden;
    position: relative;
}

.lottie-animation {
    width: 100%;
    height: 100%;
    max-width: 700px;
    z-index: 2;
}

.stage-display {
    background-color: #f8f9fa;
    border-radius: 16px;
    box-shadow: 0 3px 10px rgba(0, 0, 0, 0.08);
    transition: all 0.3s ease;
}

.care-actions {
    max-width: 700px;
    margin: 0 auto;
}

.care-button {
    font-size: 1.05rem;
    padding: 10px 16px;
    border-radius: 10px;
    box-shadow: 0 3px 6px rgba(0, 0, 0, 0.12);
    transition: all 0.3s ease;
    font-weight: 600;
    position: relative;
    overflow: hidden;
}

.care-button:hover:not(:disabled) {
    transform: translateY(-3px);
    box-shadow: 0 5px 12px rgba(0, 0, 0, 0.18);
}

.care-button:active:not(:disabled) {
    transform: translateY(1px);
}

/* Button hover effects */
.btn-hover-effect {
    position: absolute;
    width: 100%;
    height: 100%;
    top: 0;
    left: 0;
    opacity: 0;
    pointer-events: none;
    transition: opacity 0.3s ease;
    z-index: 1;
}

.care-button:hover .btn-hover-effect {
    opacity: 0.5;
}

.water-effect {
    background: radial-gradient(circle, rgba(0, 123, 255, 0) 30%, rgba(0, 123, 255, 0.8) 100%);
}

.fertilizer-effect {
    background: radial-gradient(circle, rgba(121, 85, 72, 0) 30%, rgba(121, 85, 72, 0.8) 100%);
}

.sunlight-effect {
    background: radial-gradient(circle, rgba(255, 152, 0, 0) 30%, rgba(255, 152, 0, 0.8) 100%);
}

.coins-effect {
    background: radial-gradient(circle, rgba(40, 167, 69, 0) 30%, rgba(40, 167, 69, 0.8) 100%);
}

.plant-effect {
    background: radial-gradient(circle, rgba(13, 110, 253, 0) 30%, rgba(13, 110, 253, 0.8) 100%);
}

.progress-container {
    max-width: 700px;
    margin: 0 auto;
    padding: 20px;
    background-color: #f8f9fa;
    border-radius: 16px;
    box-shadow: 0 3px 10px rgba(0, 0, 0, 0.08);
}

.points-display {
    margin-bottom: 12px;
}


.stage-display {
    max-width: 740px;
    margin-left: auto;
    margin-right: auto;
    border-radius: 16px;
    box-shadow: 0 3px 10px rgba(0, 0, 0, 0.08);
}

.nature-theme {
    background-color: #f1f8e9;
    border-left: 5px solid #7cb342;
}

.stage-icon {
    font-size: 2.2rem;
    color: #4caf50;
    margin-bottom: 5px;
}

.progress-badge {
    font-weight: 600;
    padding: 7px 10px;
    border-radius: 8px;
}

/* Ensure alignment with the progress container */
.progress-container {
    max-width: 700px;
    margin-left: auto;
    margin-right: auto;
}

.mature-message {
    font-size: 1.2rem;
    position: relative;
    z-index: 1;
}

/* Badge gradients for progress container */
.primary-gradient {
    background: linear-gradient(135deg, #2196f3 0%, #0d47a1 100%);
    border: none;
    padding: 10px 15px;
    box-shadow: 0 3px 5px rgba(33, 150, 243, 0.3);
}

.success-gradient {
    background: linear-gradient(135deg, #4caf50 0%, #1b5e20 100%);
    border: none;
    padding: 10px 15px;
    box-shadow: 0 3px 5px rgba(76, 175, 80, 0.3);
}

.forest-gradient {
    background: linear-gradient(135deg, #388e3c 0%, #1b5e20 100%);
    border: none;
    padding: 10px 15px;
    box-shadow: 0 3px 5px rgba(56, 142, 60, 0.3);
}

/* Progress bar improvements */
.progress-bar-striped {
    background-size: 1rem 1rem;
}



.progress {
    box-shadow: inset 0 1px 3px rgba(0, 0, 0, 0.1);
    border-radius: 12px;
    overflow: hidden;
}

.progress-bar {
    font-weight: bold;
    font-size: 0.95rem;
}

.history {
    max-width: 700px;
    margin: 30px auto;
    border-radius: 16px;
    overflow: hidden;
}

.badge {
    font-size: 0.9em;
    padding: 0.5em 0.8em;
    border-radius: 8px;
}

.list-group-item {
    padding: 0.8rem 1.2rem;
    font-size: 0.95rem;
    transition: background-color 0.2s ease;
}

.list-group-item:hover {
    background-color: #f0f0f0;
}

button:disabled {
    opacity: 0.6;
    cursor: not-allowed;
    transform: none !important;
    box-shadow: none !important;
}

.get-points-button {
    font-size: 1.05rem;
    padding: 10px 16px;
    border-radius: 10px;
    box-shadow: 0 3px 6px rgba(0, 0, 0, 0.12);
    transition: all 0.3s ease;
    font-weight: 600;
    position: relative;
    overflow: hidden;
}

.get-points-button:hover {
    transform: translateY(-3px);
    box-shadow: 0 5px 12px rgba(0, 0, 0, 0.18);
}

/* Custom button colors */
.btn-water {
    background-color: #0d6efd;
    color: white;
    border: none;
}

.btn-water:hover:not(:disabled) {
    background-color: #0b5ed7;
    color: white;
}

.btn-fertilizer {
    background-color: #6d4c41;
    color: white;
    border: none;
}

.btn-fertilizer:hover:not(:disabled) {
    background-color: #5d4037;
    color: white;
}

.btn-sunlight {
    background-color: #ff9800;
    color: white;
    border: none;
}

.btn-sunlight:hover:not(:disabled) {
    background-color: #ed8c00;
    color: white;
}

.mature-tree-message {
    padding: 30px;
    background-color: #f8f9fa;
    border-radius: 16px;
    box-shadow: 0 3px 15px rgba(0, 0, 0, 0.1);
    position: relative;
    overflow: hidden;
}

.tree-stats {
    margin: 15px 0;
}

.tree-stats .badge {
    font-size: 1rem;
    padding: 0.6rem 1rem;
}

.card-header {
    background-color: rgba(0, 0, 0, 0.03);
    padding: 12px;
}

.text-brown {
    color: #6d4c41;
}

/* Toast notifications */
.feedback-toast {
    max-width: 350px;
    border-radius: 10px;
    box-shadow: 0 5px 15px rgba(0, 0, 0, 0.2);
    backdrop-filter: blur(5px);
}

.toast-success {
    background-color: rgba(40, 167, 69, 0.9);
    color: white;
}

.toast-water {
    background-color: rgba(13, 110, 253, 0.9);
    color: white;
}

.toast-fertilizer {
    background-color: rgba(109, 76, 65, 0.9);
    color: white;
}

.toast-sunlight {
    background-color: rgba(255, 152, 0, 0.9);
    color: white;
}

.toast-header {
    background-color: rgba(255, 255, 255, 0.2);
    color: inherit;
    border-bottom: none;
}

.toast-header .btn-close {
    filter: invert(1);
}

/* Tree speech bubble */
.speech-bubble {
    position: absolute;
    max-width: 250px;
    background-color: white;
    border-radius: 15px;
    padding: 12px;
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.15);
    top: 30%;
    left: 60%;
    z-index: 10;
    animation: fadeInUp 0.5s ease-out;
}

.speech-bubble:after {
    content: '';
    position: absolute;
    bottom: -10px;
    left: 20px;
    border-width: 10px 10px 0;
    border-style: solid;
    border-color: white transparent;
}

.speech-bubble p {
    margin: 0;
    font-size: 0.95rem;
}

/* Weather effects */
.weather-container {
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    pointer-events: none;
    z-index: 3;
}

.rain {
    position: absolute;
    width: 100%;
    height: 100%;
    background-image: url('data:image/svg+xml;utf8,<svg xmlns="http://www.w3.org/2000/svg" width="10" height="20" viewBox="0 0 10 20"><path d="M5,0 L5,20" stroke="%230d6efd" stroke-width="2" stroke-linecap="round"/></svg>');
    background-size: 10px 20px;
    animation: rain 1s linear infinite;
    opacity: 0.7;
}

.sunshine {
    position: absolute;
    width: 100%;
    height: 100%;
    background: radial-gradient(circle at top right, rgba(255, 236, 0, 0.8) 0%, rgba(255, 236, 0, 0) 70%);
    animation: sunshine 3s ease infinite;
    opacity: 0.7;
}

/* Floating icons */
.floating-icon {
    position: absolute;
    font-size: 1.5rem;
    z-index: 5;
    pointer-events: none;
}

.water-drop {
    color: #0d6efd;
    animation: waterDrop 2s ease-in infinite;
    top: 30%;
    left: 45%;
}

.fertilizer {
    color: #6d4c41;
    animation: fertilizer 2s ease-out infinite;
    top: 60%;
    left: 48%;
}

.sun-icon {
    color: #ff9800;
    animation: sunIcon 3s ease-in-out infinite;
    top: 20%;
    right: 25%;
}

/* Level up animation */
.level-up-animation {
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    display: flex;
    justify-content: center;
    align-items: center;
    z-index: 6;
    pointer-events: none;
}

.level-up-text {
    font-size: 2.5rem;
    font-weight: bold;
    color: #28a745;
    text-shadow: 0 0 10px rgba(40, 167, 69, 0.5);
    animation: levelUp 2s ease-out;
    background: rgba(255, 255, 255, 0.7);
    padding: 10px 20px;
    border-radius: 10px;
}

/* Confetti animation */
.confetti-container {
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    pointer-events: none;
    z-index: 4;
}

[class^="confetti-"] {
    position: absolute;
    width: 10px;
    height: 10px;
    opacity: 0;
    transform: translateY(0) rotate(0);
    animation: confetti 5s ease-in-out forwards;
}



/* Tree title animation */
.tree-title {
    position: relative;
    animation: treeTitle 1s ease-out;
}

.tree-title::after {
    content: '';
    position: absolute;
    bottom: -5px;
    left: 50%;
    transform: translateX(-50%);
    width: 100px;
    height: 3px;
    background-color: #28a745;
    border-radius: 3px;
}


/* Fixed version of styles */
.tree-guide {
    max-width: 800px;
    margin: 40px auto;
    border-radius: 16px;
    overflow: hidden;
}

.guide-content {
    background-color: #f8f9fa;
}

/* Carousel container */
.carousel-container {
    overflow: hidden;
    position: relative;
    margin: 0 auto;
}

.stage-carousel {
    display: flex;
    transition: transform 0.4s ease;
    width: 100%;
}

.stage-slide {
    min-width: 100%;
    flex: 0 0 100%;
}

/* Stage content */
.stage-content {
    background-color: #f8f9fa;
    overflow: hidden;
}

.current-stage {
    background-color: rgba(40, 167, 69, 0.05);
}

.guide-image-container {
    height: 300px;
    display: flex;
    align-items: center;
    justify-content: center;
    overflow: hidden;
    background-color: rgba(240, 255, 240, 0.3);
    margin: 0 auto;
    /* Center the container */
    width: 90%;
    /* Control the width */
    max-width: 500px;
    /* Limit maximum width */
}

/* Stage information */
.stage-title {
    font-weight: bold;
    color: #2c3e50;
}

.current-badge {
    background-color: #28a745;
    color: white;
    font-size: 0.7rem;
    padding: 3px 10px;
    border-radius: 10px;
}

.stage-points {
    font-size: 1.1rem;
    color: #495057;
}

.stage-description {
    color: #6c757d;
    line-height: 1.5;
}

/* Navigation control buttons */
.carousel-control {
    position: absolute;
    top: 150px;
    /* Position at the middle of the image area */
    transform: translateY(-50%);
    background-color: rgba(255, 255, 255, 0.8);
    border: none;
    width: 40px;
    height: 40px;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 1.2rem;
    color: #495057;
    cursor: pointer;
    box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
    z-index: 5;
    transition: all 0.2s ease;
}

.carousel-control:hover:not(:disabled) {
    background-color: white;
    box-shadow: 0 3px 8px rgba(0, 0, 0, 0.15);
}

.carousel-control:disabled {
    opacity: 0.4;
    cursor: not-allowed;
}

.carousel-control-prev {
    left: 10px;
}

.carousel-control-next {
    right: 10px;
}

/* Indicator styles - modified for horizontal layout */
.stage-indicators {
    margin: 0;
    background-color: #e9ecef;
    width: 100%;
    display: flex;
    justify-content: center;
    flex-direction: row !important;
    /* Force horizontal layout */
}

.stage-indicator {
    display: flex;
    flex-direction: column;
    align-items: center;
    margin: 0 10px;
    cursor: pointer;
    transition: all 0.3s ease;
}

.stage-dot {
    width: 12px;
    height: 12px;
    border-radius: 50%;
    background-color: #dee2e6;
    margin-bottom: 6px;
    transition: all 0.3s ease;
}

.stage-indicator.active .stage-dot {
    background-color: #28a745;
    transform: scale(1.2);
}

.stage-name {
    font-size: 0.75rem;
    color: #495057;
    text-align: center;
}

.stage-indicator.active .stage-name {
    color: #28a745;
    font-weight: bold;
}

/* Responsive adjustments */
@media (max-width: 768px) {
    .guide-image-container {
        height: 220px;
    }

    .carousel-control {
        top: 110px;
        width: 32px;
        height: 32px;
        font-size: 1rem;
    }

    .stage-info {
        padding: 15px !important;
    }
}


/* Animation keyframes */
@keyframes fadeInUp {
    from {
        opacity: 0;
        transform: translateY(20px);
    }

    to {
        opacity: 1;
        transform: translateY(0);
    }
}

@keyframes pulse-animation {
    0% {
        transform: scale(1);
    }

    50% {
        transform: scale(1.05);
    }

    100% {
        transform: scale(1);
    }
}

@keyframes bounce-animation {

    0%,
    100% {
        transform: translateY(0);
    }

    50% {
        transform: translateY(-10px);
    }
}

@keyframes shake-animation {

    0%,
    100% {
        transform: translateX(0);
    }

    25% {
        transform: translateX(-5px);
    }

    50% {
        transform: translateX(5px);
    }

    75% {
        transform: translateX(-5px);
    }
}

@keyframes waterDrop {
    0% {
        opacity: 0;
        transform: translateY(-20px) scale(0.5);
    }

    50% {
        opacity: 1;
        transform: translateY(30px) scale(1);
    }

    100% {
        opacity: 0;
        transform: translateY(80px) scale(0.5);
    }
}

@keyframes fertilizer {
    0% {
        opacity: 0;
        transform: translateY(0) scale(0.5) rotate(0deg);
    }

    50% {
        opacity: 1;
        transform: translateY(-20px) scale(1) rotate(180deg);
    }

    100% {
        opacity: 0;
        transform: translateY(-40px) scale(0.5) rotate(360deg);
    }
}

@keyframes sunIcon {
    0% {
        opacity: 0;
        transform: translateY(0) scale(0.5);
    }

    50% {
        opacity: 1;
        transform: translateY(0) scale(1.5);
    }

    100% {
        opacity: 0;
        transform: translateY(0) scale(0.5);
    }
}

@keyframes rain {
    from {
        background-position: 0 0;
    }

    to {
        background-position: 0 20px;
    }
}

@keyframes sunshine {
    0% {
        opacity: 0.3;
    }

    50% {
        opacity: 0.7;
    }

    100% {
        opacity: 0.3;
    }
}

@keyframes levelUp {
    0% {
        opacity: 0;
        transform: scale(0.5);
    }

    50% {
        opacity: 1;
        transform: scale(1.2);
    }

    100% {
        opacity: 0;
        transform: scale(0.5);
    }
}

@keyframes confetti {
    0% {
        opacity: 1;
        transform: translateY(0) rotate(0);
    }

    100% {
        opacity: 0;
        transform: translateY(100vh) rotate(720deg);
    }
}

@keyframes treeTitle {
    0% {
        opacity: 0;
        transform: translateY(-20px);
    }

    100% {
        opacity: 1;
        transform: translateY(0);
    }
}

/* Apply animations to elements */
.pulse-animation {
    animation: pulse-animation 1s ease infinite;
}

.bounce-animation {
    animation: bounce-animation 0.5s ease;
}

.shake-animation {
    animation: shake-animation 0.5s ease;
}

.fade-in-animation {
    animation: fadeInUp 0.5s ease-out;
}

@media (max-width: 768px) {
    .care-actions .d-flex {
        flex-wrap: wrap;
        gap: 10px !important;
    }

    .care-button,
    .get-points-button {
        flex: 1 1 45%;
        min-width: 120px;
        font-size: 0.9rem;
    }

    .animation-container {
        height: 350px;
    }

    .speech-bubble {
        max-width: 200px;
        left: 50%;
        transform: translateX(-50%);
    }

    .toast {
        max-width: 280px;
    }
}

@media (max-width: 576px) {

    .care-button,
    .get-points-button {
        flex: 1 1 100%;
    }

    .speech-bubble {
        max-width: 180px;
        font-size: 0.85rem;
    }
}
</style>