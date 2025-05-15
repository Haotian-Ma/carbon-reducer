<template>
    <div class="container mt-5">
        <div class="row">
            <div class="col-md-12 offset-md-0">
                <section class="about-us">
                    <h2 class="text-center mb-4">Virtual Tree</h2>
                    <div class="animation-container">
                        <div ref="animationContainer" class="lottie-animation"></div>
                    </div>
                    <!-- Care actions -->
                    <div class="care-actions mt-4" v-if="currentStageIndex < growthStages.length - 1">
                        <div class="d-flex justify-content-center gap-3">
                            <button @click="careTree('water')" class="btn btn-water care-button"
                                :disabled="userPoints < carePointsCost">
                                <i class="fas fa-tint me-2"></i>Water
                                <span class="badge bg-light text-dark ms-2">-{{ carePointsCost }} points</span>
                            </button>

                            <button @click="careTree('fertilizer')" class="btn btn-fertilizer care-button"
                                :disabled="userPoints < carePointsCost">
                                <i class="fas fa-seedling me-2"></i>Fertilize
                                <span class="badge bg-light text-dark ms-2">-{{ carePointsCost }} points</span>
                            </button>

                            <button @click="careTree('sunlight')" class="btn btn-sunlight care-button"
                                :disabled="userPoints < carePointsCost">
                                <i class="fas fa-sun me-2"></i>Sunlight
                                <span class="badge bg-light text-dark ms-2">-{{ carePointsCost }} points</span>
                            </button>
                            <button @click="getPoints" class="btn btn-success get-points-button">
                                <i class="fas fa-coins me-2"></i>Get Points
                                <span class="badge bg-light text-success ms-2">+100 points</span>
                            </button>
                        </div>
                    </div>
                    <!-- Get points button -->






                    <div v-else class="mature-tree-message text-center mt-4">
                        <p class="text-success fw-bold fs-5">
                            <i class="fas fa-check-circle me-2"></i>Your tree is fully mature and no longer needs care!
                        </p>
                        <button @click="plantNewTree" class="btn btn-primary btn-lg mt-3">
                            <i class="fas fa-seedling me-2"></i>Plant a New Tree
                        </button>
                    </div>

                    <!-- Growth stage display -->
                    <div class="stage-display text-center mt-3">
                        <h4>{{ currentStage.label }}</h4>
                        <p v-if="currentStageIndex < growthStages.length - 1">
                            Next stage: {{ nextStage.label }}
                            <span class="badge bg-warning text-dark">
                                Requires {{ nextStage.requiredPoints - totalPoints }} more points
                            </span>
                        </p>
                        <p v-else class="text-success fw-bold">
                            <i class="fas fa-check-circle me-2"></i>Your tree is fully mature! 🌳
                        </p>
                    </div>

                    <!-- Points and progress -->
                    <div class="progress-container mt-4 mb-4">
                        <div class="points-display mb-3">
                            <span class="badge bg-primary me-3">
                                <i class="fas fa-coins me-1"></i>Your Points: {{ userPoints }}
                            </span>
                            <span class="badge bg-success">
                                <i class="fas fa-chart-line me-1"></i>Total Growth Points: {{ totalPoints }}
                            </span>
                        </div>
                        <div class="progress" style="height: 30px;">
                            <div class="progress-bar progress-bar-striped progress-bar-animated" role="progressbar"
                                :style="{ width: stageProgress + '%' }">
                                {{ stageProgress }}%
                            </div>
                        </div>
                    </div>
                    <div class="tree-stats text-center mt-3">
                        <span class="badge bg-success me-2">
                            <i class="fas fa-tree me-1"></i>Trees Planted: {{ totalTreesPlanted }}
                        </span>
                    </div>


                    <!-- Completion modal for final stage -->
                    <div v-if="currentStageIndex === growthStages.length - 1 && !hasShownCompletion"
                        class="completion-modal">
                        <div class="modal-backdrop show"></div>
                        <div class="modal d-block">
                            <div class="modal-dialog modal-dialog-centered">
                                <div class="modal-content">
                                    <div class="modal-header bg-success text-white">
                                        <h5 class="modal-title">
                                            <i class="fas fa-trophy me-2"></i>Congratulations!
                                        </h5>
                                    </div>
                                    <div class="modal-body text-center">
                                        <p class="fs-5">Your tree has reached full maturity! 🌳</p>
                                        <p>You've used {{ totalPoints }} points to grow this beautiful tree.</p>
                                        <p class="fw-bold">Would you like to plant a new tree?</p>
                                    </div>
                                    <div class="modal-footer justify-content-center">
                                        <button @click="resetTree" class="btn btn-success">
                                            <i class="fas fa-redo me-2"></i>Plant New Tree
                                        </button>
                                        <button @click="continueAdmiring" class="btn btn-outline-secondary">
                                            <i class="fas fa-eye me-2"></i>Continue Admiring
                                        </button>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>

                    <!-- Growth history -->
                    <div class="history mt-4" v-if="growthHistory.length > 0">
                        <h5 class="text-center mb-3">
                            <i class="fas fa-history me-2"></i>Growth History
                        </h5>
                        <ul class="list-group">
                            <li class="list-group-item" v-for="(record, index) in growthHistory" :key="index">
                                <small class="text-muted">{{ record }}</small>
                            </li>
                        </ul>
                    </div>
                </section>
            </div>
        </div>
    </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted, computed } from 'vue';
import lottie from 'lottie-web';

const animationContainer = ref(null);
let animation = null;
let frameByFrameInterval = null;
const treesPlanted = ref(parseInt(localStorage.getItem('treesPlanted')) || 0);

// User points from local storage - starting with more points for better gameplay
const userPoints = ref(parseInt(localStorage.getItem('userPoints')) || 200);

// Care cost
const carePointsCost = 35; // Cost for each care action (water, fertilize, sunlight)

// Care counters
const careCount = ref({
    water: parseInt(localStorage.getItem('waterCount')) || 0,
    fertilizer: parseInt(localStorage.getItem('fertilizerCount')) || 0,
    sunlight: parseInt(localStorage.getItem('sunlightCount')) || 0
});

const growthHistory = ref(JSON.parse(localStorage.getItem('growthHistory')) || []);
const currentStageIndex = ref(parseInt(localStorage.getItem('currentStageIndex')) || 0);
const hasShownCompletion = ref(false);

// Define growth stages with exponential point requirements
const growthStages = [
    { label: 'Seed Stage', startFrame: 20, endFrame: 60, requiredPoints: 0 },
    { label: 'Sprouting', startFrame: 240, endFrame: 280, requiredPoints: 100 },
    { label: 'Small Tree', startFrame: 450, endFrame: 500, requiredPoints: 300 },  // 100 + 200
    { label: 'Growing Tree', startFrame: 650, endFrame: 720, requiredPoints: 700 }, // 300 + 400
    { label: 'Mature Tree', startFrame: 900, endFrame: 960, requiredPoints: 1500 }  // 700 + 800
];
const playCurrentStageAnimation = () => {
    if (!animation) return;

    const stage = growthStages[currentStageIndex.value];
    playFrameByFrame(stage.startFrame, stage.endFrame, 24);
};

// Computed properties
const totalPoints = computed(() => {
    return (careCount.value.water + careCount.value.fertilizer + careCount.value.sunlight) * carePointsCost;
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

// Care function
const careTree = (type) => {
    if (userPoints.value < carePointsCost) return;

    // Deduct points
    userPoints.value -= carePointsCost;
    localStorage.setItem('userPoints', userPoints.value);

    // Add to care count
    careCount.value[type]++;

    // Save care counts to localStorage
    localStorage.setItem('waterCount', careCount.value.water);
    localStorage.setItem('fertilizerCount', careCount.value.fertilizer);
    localStorage.setItem('sunlightCount', careCount.value.sunlight);

    // Add action to history
    const actionText = `${type.charAt(0).toUpperCase() + type.slice(1)} applied (${carePointsCost} points used)`;
    growthHistory.value.unshift(actionText);

    // Keep only last 5 records
    if (growthHistory.value.length > 5) {
        growthHistory.value.pop();
    }

    // Save history
    localStorage.setItem('growthHistory', JSON.stringify(growthHistory.value));

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

        // Add to growth history
        growthHistory.value.unshift(`🌱 Advanced to ${newStage.label} (Total points: ${totalPoints.value})`);

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
};

// Add new function for planting new tree
const plantNewTree = () => {
    resetTree();
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

    // Add to history
    growthHistory.value.unshift('💰 Received 100 points!');

    // Keep only last 5 records
    if (growthHistory.value.length > 5) {
        growthHistory.value.pop();
    }

    // Save history
    localStorage.setItem('growthHistory', JSON.stringify(growthHistory.value));
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
});
</script>

<style scoped>
.animation-container {
    height: 500px;
    margin: 30px auto;
    display: flex;
    justify-content: center;
    align-items: center;
}

.lottie-animation {
    width: 100%;
    height: 100%;
    max-width: 800px;
}

.stage-display {
    background-color: #f8f9fa;
    padding: 20px;
    border-radius: 10px;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.care-actions {
    max-width: 800px;
    margin: 0 auto;
}

.care-button {
    font-size: 1.1rem;
    padding: 12px;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
    transition: all 0.3s ease;
}

.care-button:hover:not(:disabled) {
    transform: translateY(-2px);
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.15);
}

.progress-container {
    max-width: 800px;
    margin: 0 auto;
    padding: 20px;
    background-color: #f8f9fa;
    border-radius: 10px;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.points-display {
    display: flex;
    justify-content: center;
    align-items: center;
}

.progress {
    box-shadow: inset 0 1px 3px rgba(0, 0, 0, 0.1);
}

.progress-bar {
    background-color: #28a745;
    font-weight: bold;
}

.history {
    max-width: 800px;
    margin: 0 auto;
}

.badge {
    font-size: 1em;
    padding: 0.5em 0.8em;
}

.list-group-item {
    padding: 0.8rem 1.2rem;
    font-size: 0.95rem;
    background-color: #f8f9fa;
    border: 1px solid #dee2e6;
}

button:disabled {
    opacity: 0.6;
    cursor: not-allowed;
}

.modal {
    background-color: rgba(0, 0, 0, 0.5);
}

.modal-backdrop {
    opacity: 0.5;
}

.modal-content {
    border-radius: 10px;
    box-shadow: 0 5px 15px rgba(0, 0, 0, 0.5);
}

.modal-header {
    border-top-left-radius: 10px;
    border-top-right-radius: 10px;
}

.modal-footer {
    border-bottom-left-radius: 10px;
    border-bottom-right-radius: 10px;
}

.get-points-section {
    max-width: 800px;
    margin: 0 auto;
}

.get-points-button {
    font-size: 1.1rem;
    padding: 12px;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
    transition: all 0.3s ease;
}

.get-points-button:hover {
    transform: translateY(-2px);
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.15);
}

/* 自定义按钮颜色 */
.btn-water {
    background-color: #007bff;
    color: white;
    border: 1px solid #0056b3;
}

.btn-water:hover:not(:disabled) {
    background-color: #0056b3;
    color: white;
}

.btn-water:disabled {
    background-color: #6c757d;
    border-color: #6c757d;
}

.btn-fertilizer {
    background-color: #795548;
    color: white;
    border: 1px solid #5d4037;
}

.btn-fertilizer:hover:not(:disabled) {
    background-color: #5d4037;
    color: white;
}

.btn-fertilizer:disabled {
    background-color: #6c757d;
    border-color: #6c757d;
}

.btn-sunlight {
    background-color: #ff9800;
    color: white;
    border: 1px solid #f57c00;
}

.btn-sunlight:hover:not(:disabled) {
    background-color: #f57c00;
    color: white;
}

.btn-sunlight:disabled {
    background-color: #6c757d;
    border-color: #6c757d;
}


.care-actions .row {
    margin: 0 -5px;
}

.care-actions .col-md-3 {
    padding: 0 5px;
}


@media (max-width: 768px) {
    .care-actions .col-md-3 {
        flex: 0 0 33.333333%;
        max-width: 33.333333%;
    }
}


.care-button {
    padding: 10px 15px;
    white-space: nowrap;
    font-size: 0.95rem;
}

.care-button .badge {
    font-size: 0.8em;
}

.mature-tree-message {
    padding: 30px;
    background-color: #f8f9fa;
    border-radius: 10px;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.tree-stats {
    margin-top: 10px;
}

.tree-stats .badge {
    font-size: 1.1rem;
    padding: 0.6rem 1rem;
}
</style>