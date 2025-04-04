<template>
    <div class="climate-insight">
        <header class="insight-header">
            <h1>Climate Insight</h1>
            <p class="subtitle">Data-driven analysis of climate trends and carbon emissions</p>
        </header>

        <section class="filter-section">
            <div class="container">
                <div class="filter-controls">
                    <div class="filter-group">
                        <label for="region-select">Region</label>
                        <select id="region-select" v-model="selectedRegion" class="filter-select">
                            <option value="global">Global</option>
                            <option value="asia">Asia</option>
                            <option value="europe">Europe</option>
                            <option value="northAmerica">North America</option>
                            <option value="southAmerica">South America</option>
                            <option value="africa">Africa</option>
                            <option value="oceania">Oceania</option>
                        </select>
                    </div>

                    <div class="filter-group">
                        <label for="dataType-select">Data Type</label>
                        <select id="dataType-select" v-model="selectedDataType" class="filter-select">
                            <option value="emissions">Carbon Emissions</option>
                            <option value="temperature">Temperature Change</option>
                            <option value="sealevel">Sea Level Rise</option>
                            <option value="icemelt">Ice Sheet Melting</option>
                        </select>
                    </div>

                    <div class="filter-group">
                        <label for="timeframe-select">Timeframe</label>
                        <select id="timeframe-select" v-model="selectedTimeframe" class="filter-select">
                            <option value="lastYear">Last Year</option>
                            <option value="last5Years">Last 5 Years</option>
                            <option value="last10Years">Last 10 Years</option>
                            <option value="last50Years">Last 50 Years</option>
                            <option value="historical">Historical Record</option>
                        </select>
                    </div>

                    <button @click="updateData" class="update-button" :disabled="loading">
                        <span v-if="!loading">Update View</span>
                        <span v-else>Loading...</span>
                    </button>
                </div>
            </div>
        </section>

        <section class="visualization-section">
            <div class="container">
                <div class="visualization-wrapper">
                    <div v-if="loading" class="loading-overlay">
                        <div class="spinner"></div>
                        <p>Loading climate data...</p>
                    </div>

                    <!-- Chart Area -->
                    <div class="chart-container" ref="chartContainer">
                        <!-- This will be populated by a visualization library -->
                    </div>

                    <!-- Key Metrics Cards -->
                    <div class="metrics-container">
                        <!-- Key metric cards will be displayed here -->
                    </div>
                </div>
            </div>
        </section>

        <section class="data-table-section">
            <div class="container">
                <h2>Detailed Climate Data</h2>
                <p class="section-description">
                    Explore the raw data behind the visualizations with our comprehensive data tables.
                </p>

                <div class="data-table-wrapper">
                    <div v-if="loading" class="loading-overlay">
                        <div class="spinner"></div>
                        <p>Loading table data...</p>
                    </div>

                    <div class="table-controls">
                        <div class="search-control">
                            <input type="text" v-model="searchQuery" placeholder="Search data..."
                                class="search-input" />
                        </div>
                        <div class="table-pagination">
                            <!-- Pagination controls will be placed here -->
                        </div>
                    </div>

                    <!-- Data table will be rendered here -->
                    <div class="table-container">
                        <!-- Data table will be populated by external component or API data -->
                    </div>

                    <div class="table-footer">
                        <div class="download-options">
                            <button @click="downloadData('csv')" class="download-button">
                                Download CSV
                            </button>
                            <button @click="downloadData('excel')" class="download-button">
                                Download Excel
                            </button>
                        </div>
                    </div>
                </div>
            </div>
        </section>

        <section class="methodology-section">
            <div class="container">
                <h2>Data Methodology</h2>
                <p>
                    The climate data presented on this page is sourced from reputable scientific organizations
                    including NASA, NOAA, and the IPCC. Our visualizations are updated regularly to ensure
                    accuracy and relevance.
                </p>
            </div>
        </section>
    </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';

// Filter state
const selectedRegion = ref('global');
const selectedDataType = ref('emissions');
const selectedTimeframe = ref('last10Years');
const loading = ref(false);
const searchQuery = ref('');

// Chart reference
const chartContainer = ref(null);

// Method to update data
const updateData = () => {
    loading.value = true;
    // Actual data fetching logic should be added here
    setTimeout(() => {
        loading.value = false;
    }, 1000);
};

// Method to download data
const downloadData = (format) => {
    console.log(`Downloading data in ${format} format`);
    // Implement download functionality
};

onMounted(() => {
    // Initialization logic when the page loads
});
</script>

<style scoped>
.climate-insight {
    max-width: 1200px;
    margin: 0 auto;
    padding: 20px;
}

.insight-header {
    text-align: center;
    margin-bottom: 30px;
}

.insight-header h1 {
    color: var(--primary-color, #2c3e50);
    margin-bottom: 5px;
}

.subtitle {
    color: var(--text-light, #666);
    font-size: 18px;
}

.container {
    margin-bottom: 30px;
}

/* Filter section styles */
.filter-section {
    background-color: #f9f9f9;
    padding: 20px;
    border-radius: 8px;
    margin-bottom: 30px;
}

.filter-controls {
    display: flex;
    flex-wrap: wrap;
    gap: 15px;
    align-items: flex-end;
}

.filter-group {
    display: flex;
    flex-direction: column;
    min-width: 200px;
}

.filter-group label {
    margin-bottom: 5px;
    font-weight: 500;
}

.filter-select {
    padding: 10px;
    border: 1px solid #ddd;
    border-radius: 4px;
    font-size: 16px;
}

.update-button {
    background-color: var(--primary-color, #2c3e50);
    color: white;
    border: none;
    padding: 10px 20px;
    border-radius: 4px;
    cursor: pointer;
    font-size: 16px;
    height: 42px;
}

.update-button:hover {
    background-color: var(--primary-hover, #1e2b3c);
}

.update-button:disabled {
    background-color: #cccccc;
    cursor: not-allowed;
}

/* Visualization section styles */
.visualization-section {
    margin-bottom: 40px;
}

.visualization-wrapper {
    position: relative;
    min-height: 400px;
}

.chart-container {
    height: 400px;
    background-color: #f9f9f9;
    border-radius: 8px;
    border: 1px dashed #ddd;
    display: flex;
    align-items: center;
    justify-content: center;
}

.metrics-container {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
    gap: 20px;
    margin-top: 20px;
}

/* Data table section styles */
.data-table-section h2 {
    margin-bottom: 10px;
}

.section-description {
    color: var(--text-light, #666);
    margin-bottom: 20px;
}

.data-table-wrapper {
    position: relative;
    background-color: white;
    border-radius: 8px;
    box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
    padding: 20px;
}

.table-controls {
    display: flex;
    justify-content: space-between;
    margin-bottom: 15px;
}

.search-input {
    padding: 10px;
    border: 1px solid #ddd;
    border-radius: 4px;
    font-size: 16px;
    width: 250px;
}

.table-container {
    min-height: 300px;
    background-color: #f9f9f9;
    border-radius: 8px;
    border: 1px dashed #ddd;
    margin-bottom: 20px;
    display: flex;
    align-items: center;
    justify-content: center;
}

.table-footer {
    display: flex;
    justify-content: flex-end;
}

.download-button {
    background-color: #f0f0f0;
    border: 1px solid #ddd;
    padding: 8px 15px;
    border-radius: 4px;
    margin-left: 10px;
    cursor: pointer;
}

.download-button:hover {
    background-color: #e0e0e0;
}

/* Loader styles */
.loading-overlay {
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background-color: rgba(255, 255, 255, 0.8);
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    z-index: 10;
    border-radius: 8px;
}

.spinner {
    border: 4px solid #f3f3f3;
    border-top: 4px solid var(--primary-color, #2c3e50);
    border-radius: 50%;
    width: 40px;
    height: 40px;
    animation: spin 1s linear infinite;
    margin-bottom: 10px;
}

@keyframes spin {
    0% {
        transform: rotate(0deg);
    }

    100% {
        transform: rotate(360deg);
    }
}

/* Responsive design */
@media (max-width: 768px) {
    .filter-controls {
        flex-direction: column;
    }

    .filter-group {
        width: 100%;
    }

    .update-button {
        width: 100%;
        margin-top: 10px;
    }

    .table-controls {
        flex-direction: column;
        gap: 10px;
    }

    .search-input {
        width: 100%;
    }
}
</style>