<template>
    <div class="dashboard-container my-4">
        <div class="dashboard-content">
            <h2 class="text-center mb-5 dashboard-title">My Points Dashboard</h2>

            <!-- Total Points Card -->
            <div class="row mb-5">
                <div class="col-12">
                    <div class="card total-points-card">
                        <div class="card-body text-center py-5">
                            <h3 class="mb-4 display-6">Total Points Balance</h3>
                            <div class="points-display">
                                <i class="fas fa-coins points-icon"></i>
                                <span class="points-number">{{ userPoints }}</span>
                            </div>
                            <p class="lead mt-3">Use your points for eco activities!</p>
                        </div>
                    </div>
                </div>
            </div>

            <!-- Points Sources -->
            <div class="row mb-5">
                <div class="col-md-6 mb-4">
                    <div class="card source-card h-100">
                        <div class="card-header bg-success text-white py-3">
                            <h4 class="mb-0">
                                <i class="fas fa-tree me-2"></i>Virtual Tree
                            </h4>
                        </div>
                        <div class="card-body p-4">
                            <div class="points-breakdown">
                                <div class="breakdown-item">
                                    <span class="label">Points Spent on Tree Care:</span>
                                    <span class="value">{{ treePointsSpent }}</span>
                                </div>
                                <div class="breakdown-item">
                                    <span class="label">Current Tree Stage:</span>
                                    <span class="value">{{ currentTreeStage }}</span>
                                </div>
                                <div class="breakdown-item">
                                    <span class="label">Trees Planted:</span>
                                    <span class="value">{{ totalTreesPlanted }}</span>
                                </div>
                                <router-link to="/virtual-tree/tree-planting" class="btn btn-success btn-lg mt-4 w-100">
                                    Go to Virtual Tree
                                </router-link>
                            </div>
                        </div>
                    </div>
                </div>

                <div class="col-md-6 mb-4">
                    <div class="card source-card h-100">
                        <div class="card-header bg-info text-white py-3">
                            <h4 class="mb-0">
                                <i class="fas fa-recycle me-2"></i>Eco Action
                            </h4>
                        </div>
                        <div class="card-body p-4">
                            <div class="points-breakdown">
                                <div class="breakdown-item">
                                    <span class="label">Points Earned from Actions:</span>
                                    <span class="value">{{ ecoPointsEarned }}</span>
                                </div>
                                <div class="breakdown-item">
                                    <span class="label">Total Actions Completed:</span>
                                    <span class="value">{{ totalEcoActions }}</span>
                                </div>
                                <router-link to="/eco-action" class="btn btn-info btn-lg mt-4 w-100">
                                    Go to Eco Action
                                </router-link>
                            </div>
                        </div>
                    </div>
                </div>
            </div>

            <!-- Transaction History and Quick Actions -->
            <div class="row mb-5">
                <div class="col-lg-8 mb-4">
                    <div class="card h-100">
                        <div class="card-header py-3">
                            <h4 class="mb-0">
                                <i class="fas fa-history me-2"></i>Recent Transactions
                            </h4>
                        </div>
                        <div class="card-body p-4">
                            <div v-if="transactions.length === 0" class="text-center text-muted py-5">
                                <i class="fas fa-inbox fa-3x mb-3"></i>
                                <p>No transactions yet</p>
                            </div>
                            <div v-else class="transaction-list">
                                <div v-for="(transaction, index) in sortedTransactions" :key="index"
                                    class="transaction-item">
                                    <div class="transaction-info">
                                        <div class="transaction-icon"
                                            :class="transaction.type === 'earn' ? 'earn' : 'spend'">
                                            <i :class="transaction.icon"></i>
                                        </div>
                                        <div class="transaction-details">
                                            <strong>{{ transaction.description }}</strong>
                                            <small class="text-muted">{{ formatDate(transaction.date) }}</small>
                                        </div>
                                    </div>
                                    <div class="transaction-amount"
                                        :class="transaction.type === 'earn' ? 'text-success' : 'text-danger'">
                                        {{ transaction.type === 'earn' ? '+' : '-' }}{{ transaction.amount }} pts
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>

                <div class="col-lg-4 mb-4">
                    <div class="card h-100">
                        <div class="card-header py-3">
                            <h4 class="mb-0">
                                <i class="fas fa-bolt me-2"></i>Quick Actions
                            </h4>
                        </div>
                        <div class="card-body p-4">
                            <div class="d-grid gap-3">
                                <button @click="addBonusPoints" class="btn btn-primary btn-lg">
                                    <i class="fas fa-gift me-2"></i>Claim Daily Bonus
                                    <span class="badge bg-light text-primary ms-2">+50 pts</span>
                                </button>
                                <router-link to="/virtual-tree/tree-planting" class="btn btn-success btn-lg">
                                    <i class="fas fa-tree me-2"></i>Care for Tree
                                </router-link>
                                <router-link to="/eco-action" class="btn btn-info btn-lg">
                                    <i class="fas fa-leaf me-2"></i>Complete Eco Action
                                </router-link>
                            </div>
                        </div>
                    </div>
                </div>
            </div>


        </div>
    </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue';

// Points data
const userPoints = ref(0);
const transactions = ref([]);

// Tree data
const treePointsSpent = ref(0);
const currentTreeStage = ref('Seed Stage');
const totalTreesPlanted = ref(0);

// Eco action data
const ecoPointsEarned = ref(0);
const totalEcoActions = ref(0);

// Statistics
const lifetimePoints = ref(0);
const lastBonusDate = ref(null);

// Load all data from localStorage
const loadPointsData = () => {
    // Load user points
    userPoints.value = parseInt(localStorage.getItem('userPoints')) || 200;

    // Load tree data
    const waterCount = parseInt(localStorage.getItem('waterCount')) || 0;
    const fertilizerCount = parseInt(localStorage.getItem('fertilizerCount')) || 0;
    const sunlightCount = parseInt(localStorage.getItem('sunlightCount')) || 0;
    treePointsSpent.value = (waterCount + fertilizerCount + sunlightCount) * 35;

    // Load current tree stage
    const stageIndex = parseInt(localStorage.getItem('currentStageIndex')) || 0;
    const stages = ['Seed Stage', 'Sprouting', 'Small Tree', 'Growing Tree', 'Mature Tree'];
    currentTreeStage.value = stages[stageIndex];
    totalTreesPlanted.value = parseInt(localStorage.getItem('totalTreesPlanted')) || 0;

    // Load eco action data
    ecoPointsEarned.value = parseInt(localStorage.getItem('ecoPointsEarned')) || 0;
    totalEcoActions.value = parseInt(localStorage.getItem('totalEcoActions')) || 0;

    // Load transactions
    transactions.value = JSON.parse(localStorage.getItem('pointsTransactions')) || [];

    // Load lifetime points
    lifetimePoints.value = parseInt(localStorage.getItem('lifetimePoints')) || 200;

    // Load last bonus date
    lastBonusDate.value = localStorage.getItem('lastBonusDate');
};

// Add transaction to history
const addTransaction = (description, amount, type, icon) => {
    const transaction = {
        description,
        amount,
        type, // 'earn' or 'spend'
        icon,
        date: new Date().toISOString()
    };

    transactions.value.unshift(transaction);

    // Keep only last 50 transactions
    if (transactions.value.length > 50) {
        transactions.value = transactions.value.slice(0, 50);
    }

    // Save to localStorage
    localStorage.setItem('pointsTransactions', JSON.stringify(transactions.value));

    // Update lifetime points if earning
    if (type === 'earn') {
        lifetimePoints.value += amount;
        localStorage.setItem('lifetimePoints', lifetimePoints.value);
    }
};

// Claim daily bonus
const addBonusPoints = () => {
    const today = new Date().toDateString();

    if (lastBonusDate.value === today) {
        alert('You have already claimed your daily bonus today!');
        return;
    }

    const bonusAmount = 50;
    userPoints.value += bonusAmount;
    lastBonusDate.value = today;

    // Save to localStorage
    localStorage.setItem('userPoints', userPoints.value);
    localStorage.setItem('lastBonusDate', today);

    // Add transaction
    addTransaction('Daily Bonus', bonusAmount, 'earn', 'fas fa-gift');

    alert('Daily bonus claimed! +50 points');
};

// Computed properties
const sortedTransactions = computed(() => {
    return transactions.value.sort((a, b) => new Date(b.date) - new Date(a.date));
});





// Format date
const formatDate = (dateString) => {
    const date = new Date(dateString);
    const now = new Date();
    const diffTime = Math.abs(now - date);
    const diffDays = Math.floor(diffTime / (1000 * 60 * 60 * 24));

    if (diffDays === 0) {
        const diffHours = Math.floor(diffTime / (1000 * 60 * 60));
        if (diffHours === 0) {
            const diffMinutes = Math.floor(diffTime / (1000 * 60));
            return `${diffMinutes} minutes ago`;
        }
        return `${diffHours} hours ago`;
    } else if (diffDays === 1) {
        return 'Yesterday';
    } else if (diffDays < 7) {
        return `${diffDays} days ago`;
    } else {
        return date.toLocaleDateString();
    }
};

// Update from other sources
const updateFromExternalSources = () => {
    // Check for points changes
    const currentPoints = parseInt(localStorage.getItem('userPoints')) || 200;

    // Check for Virtual Tree care activities
    const currentWaterCount = parseInt(localStorage.getItem('waterCount')) || 0;
    const currentFertilizerCount = parseInt(localStorage.getItem('fertilizerCount')) || 0;
    const currentSunlightCount = parseInt(localStorage.getItem('sunlightCount')) || 0;

    // Get previous counts
    const prevWaterCount = parseInt(localStorage.getItem('prevWaterCount')) || 0;
    const prevFertilizerCount = parseInt(localStorage.getItem('prevFertilizerCount')) || 0;
    const prevSunlightCount = parseInt(localStorage.getItem('prevSunlightCount')) || 0;

    // Check for changes and add transactions
    if (currentWaterCount > prevWaterCount) {
        addTransaction('Virtual Tree: Water applied', 35, 'spend', 'fas fa-tint');
        localStorage.setItem('prevWaterCount', currentWaterCount);
    }

    if (currentFertilizerCount > prevFertilizerCount) {
        addTransaction('Virtual Tree: Fertilizer applied', 35, 'spend', 'fas fa-seedling');
        localStorage.setItem('prevFertilizerCount', currentFertilizerCount);
    }

    if (currentSunlightCount > prevSunlightCount) {
        addTransaction('Virtual Tree: Sunlight applied', 35, 'spend', 'fas fa-sun');
        localStorage.setItem('prevSunlightCount', currentSunlightCount);
    }

    // Check for points changes (for Get Points and other actions)
    if (currentPoints !== userPoints.value) {
        const diff = currentPoints - userPoints.value;
        userPoints.value = currentPoints;

        if (diff === 100) {
            // This is likely from Virtual Tree Get Points
            addTransaction('Virtual Tree: Points received', 100, 'earn', 'fas fa-tree');
        } else if (diff > 0) {
            // Points earned
            addTransaction('Points earned', diff, 'earn', 'fas fa-coins');
        } else if (diff < 0) {
            // Points spent (already handled above for tree care)
            // This could be from other sources
        }
    }
};

// Initialize
onMounted(() => {
    loadPointsData();
    const waterCount = parseInt(localStorage.getItem('waterCount')) || 0;
    const fertilizerCount = parseInt(localStorage.getItem('fertilizerCount')) || 0;
    const sunlightCount = parseInt(localStorage.getItem('sunlightCount')) || 0;

    localStorage.setItem('prevWaterCount', waterCount);
    localStorage.setItem('prevFertilizerCount', fertilizerCount);
    localStorage.setItem('prevSunlightCount', sunlightCount);

    // Set up interval to check for external changes
    const interval = setInterval(() => {
        updateFromExternalSources();
        loadPointsData();
    }, 1000); // Check every second

    // Clean up on unmount
    return () => clearInterval(interval);
});
</script>

<style scoped>
/* Container */
.dashboard-container {
    width: 100%;
    max-width: 1400px;
    margin: 0 auto;
    padding: 0 20px;
}

.dashboard-content {
    width: 100%;
}

.dashboard-title {
    font-size: 2.5rem;
    font-weight: bold;
    color: #333;
}

/* Main cards */
.total-points-card {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
    border: none;
    box-shadow: 0 6px 20px rgba(0, 0, 0, 0.15);
    border-radius: 15px;
}

.points-display {
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 30px;
}

.points-icon {
    font-size: 4rem;
    color: #ffd700;
    animation: bounce 2s infinite;
}

.points-number {
    font-size: 5rem;
    font-weight: bold;
    letter-spacing: -2px;
}

@keyframes bounce {

    0%,
    100% {
        transform: translateY(0);
    }

    50% {
        transform: translateY(-10px);
    }
}

/* Source cards */
.source-card {
    height: 100%;
    transition: all 0.3s ease;
    border-radius: 12px;
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

.source-card:hover {
    transform: translateY(-8px);
    box-shadow: 0 8px 15px rgba(0, 0, 0, 0.2);
}

.source-card .card-header {
    font-size: 1.25rem;
}

.points-breakdown {
    display: flex;
    flex-direction: column;
    gap: 20px;
}

.breakdown-item {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 15px 0;
    border-bottom: 2px solid #f0f0f0;
    font-size: 1.1rem;
}

.breakdown-item:last-child {
    border-bottom: none;
}

.breakdown-item .label {
    font-weight: 500;
    color: #555;
}

.breakdown-item .value {
    font-weight: bold;
    color: #333;
    font-size: 1.25rem;
}

/* Transaction list */
.transaction-list {
    max-height: 500px;
    overflow-y: auto;
    scrollbar-width: thin;
    scrollbar-color: #ddd #f5f5f5;
}

.transaction-list::-webkit-scrollbar {
    width: 8px;
}

.transaction-list::-webkit-scrollbar-track {
    background: #f5f5f5;
}

.transaction-list::-webkit-scrollbar-thumb {
    background: #ddd;
    border-radius: 4px;
}

.transaction-item {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 16px 20px;
    border-bottom: 1px solid #f0f0f0;
    transition: all 0.2s;
}

.transaction-item:hover {
    background-color: #f8f9fa;
    padding-left: 25px;
}

.transaction-item:last-child {
    border-bottom: none;
}

.transaction-info {
    display: flex;
    align-items: center;
    gap: 20px;
}

.transaction-icon {
    width: 48px;
    height: 48px;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 1.3rem;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.transaction-icon.earn {
    background-color: #d4edda;
    color: #155724;
}

.transaction-icon.spend {
    background-color: #f8d7da;
    color: #721c24;
}

.transaction-details {
    display: flex;
    flex-direction: column;
    gap: 4px;
}

.transaction-details strong {
    font-size: 1.1rem;
}

.transaction-amount {
    font-weight: bold;
    font-size: 1.3rem;
    min-width: 100px;
    text-align: right;
}

/* Statistics */
.stat-item {
    padding: 30px;
    border-radius: 12px;
    background-color: #f8f9fa;
    transition: all 0.3s ease;
    box-shadow: 0 2px 5px rgba(0, 0, 0, 0.08);
}

.stat-item:hover {
    transform: translateY(-5px);
    box-shadow: 0 5px 15px rgba(0, 0, 0, 0.15);
}

.stat-item h2 {
    font-weight: 700;
    margin-bottom: 15px;
}

/* Quick Actions */
.btn-lg {
    padding: 15px 20px;
    font-size: 1.1rem;
    font-weight: 500;
    border-radius: 10px;
    transition: all 0.3s ease;
}

.btn-lg:hover {
    transform: translateY(-2px);
    box-shadow: 0 5px 15px rgba(0, 0, 0, 0.2);
}

/* Cards General */
.card {
    border: none;
    border-radius: 12px;
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    animation: fadeIn 0.5s ease-out;
    margin-bottom: 0;
}

.card-header {
    background-color: transparent;
    border-bottom: 2px solid #f0f0f0;
    font-weight: 600;
}

.card-body {
    padding: 1.5rem;
}

/* Responsive */
@media (max-width: 1200px) {
    .dashboard-container {
        max-width: 100%;
    }
}

@media (max-width: 768px) {
    .points-number {
        font-size: 3rem;
    }

    .points-icon {
        font-size: 2.5rem;
    }

    .dashboard-title {
        font-size: 2rem;
    }

    .stat-item h2 {
        font-size: 1.8rem;
    }

    .btn-lg {
        padding: 10px 15px;
        font-size: 1rem;
    }
}

/* Animations */
@keyframes fadeIn {
    from {
        opacity: 0;
        transform: translateY(20px);
    }

    to {
        opacity: 1;
        transform: translateY(0);
    }
}

/* Additional Styling */
.display-5 {
    font-size: 2.5rem;
}

.display-6 {
    font-size: 2rem;
}

.lead {
    font-size: 1.25rem;
}

.fs-5 {
    font-size: 1.1rem;
}

/* Scrollbar for entire page */
::-webkit-scrollbar {
    width: 12px;
}

::-webkit-scrollbar-track {
    background: #f1f1f1;
}

::-webkit-scrollbar-thumb {
    background: #888;
    border-radius: 6px;
}

::-webkit-scrollbar-thumb:hover {
    background: #555;
}
</style>