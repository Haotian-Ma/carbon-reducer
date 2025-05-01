<template>
  <div class="climate-insight">
    <header class="insight-header">
      <h1>Climate Insight</h1>
      <p class="subtitle">Data-driven analysis of climate trends and carbon emissions</p>
    </header>

    <!-- Section 1: Global Temperature and Emissions -->
    <section class="section-group">
      <h2 class="section-group-title">Global Temperature and Emissions Trends</h2>
      <p class="section-description">
        Scientists worldwide have tracked Earth's temperature for decades. The data clearly shows our planet's average
        temperature rising at an unprecedented rate, particularly since the mid-20th century, strongly correlated with
        increasing greenhouse gas emissions.
      </p>

      <div class="chart-section temperature-analysis">
        <div class="container">
          <h3>Temperature Analysis</h3>
          <div class="tab-controls">
            <button :class="['tab-button', { active: activeTempTab === 'confidence' }]"
              @click="activeTempTab = 'confidence'">
              Temperature with Confidence Interval
            </button>
            <button :class="['tab-button', { active: activeTempTab === 'emissions' }]"
              @click="activeTempTab = 'emissions'">
              Temperature and Emissions Over Time
            </button>
          </div>

          <div class="chart-tab-content">
            <div v-show="activeTempTab === 'confidence'" class="chart-container" ref="chartContainer1">
              <!-- Confidence Interval chart will be rendered here -->
            </div>
            <div v-show="activeTempTab === 'emissions'" class="chart-container" ref="chartContainer2">
              <!-- Temperature and Emissions chart will be rendered here -->
            </div>
            <div v-if="loading1 || loading2" class="loading-indicator"></div>
          </div>

          <div class="chart-description-panel">
            <div v-if="activeTempTab === 'confidence'">
              <p class="chart-description">
                This chart tracks global average temperature anomaly (deviation from baseline average) from 1850 to
                present. The confidence interval narrows over time, reflecting improved accuracy in measurements as
                technology advances.
              </p>
              <p class="simple-explanation">
                <strong>Simply put:</strong> This shows how Earth is getting warmer compared to normal temperatures. The
                gray area gets narrower in recent years because our measuring tools got better.
              </p>
            </div>
            <div v-if="activeTempTab === 'emissions'">
              <p class="chart-description">
                This visualization shows the relationship between rising greenhouse gas emissions and global
                temperature. CO₂ from burning fossil fuels is the main contributor, but Methane (CH₄) and other gases
                also trap heat
                in our atmosphere.
              </p>
              <p class="simple-explanation">
                <strong>Simply put:</strong> As we burn more fossil fuels, we release more greenhouse gases, and the
                planet gets warmer - this graph shows this direct connection.
              </p>
            </div>
          </div>
        </div>
      </div>
    </section>
    <!-- Section 2: Emissions Breakdown and Impact -->
    <section class="section-group">
      <h2 class="section-group-title">Carbon Emissions and Environmental Impact</h2>
      <p class="section-description">
        Human activities contribute to climate change through various sectors. Understanding these emissions sources and
        their environmental impacts is crucial for developing effective climate policies.
      </p>

      <div class="chart-section chart-section3">
        <div class="container">
          <h3>CO₂ Emissions by Sector in Australia (2021)</h3>

          <div class="chart-container" ref="chartContainer3">
            <!-- Plotly chart will be rendered here -->
          </div>
          <div v-if="loading3" class="loading-indicator"></div>
          <div class="simple-explanation">
            <strong>Simply put:</strong> This pie chart shows which activities in Australia create the most carbon
            pollution, helping us identify where changes would have the biggest impact.
          </div>
        </div>
      </div>


      <div class="chart-section forest-analysis">
        <div class="container">
          <h3>Forest Change Analysis</h3>
          <div class="tab-controls">
            <button :class="['tab-button', { active: activeForestTab === 'percentage' }]"
              @click="activeForestTab = 'percentage'">
              Percentage Change by Country
            </button>
            <button :class="['tab-button', { active: activeForestTab === 'distribution' }]"
              @click="activeForestTab = 'distribution'">
              Global Distribution
            </button>
          </div>

          <div class="chart-tab-content">
            <div v-show="activeForestTab === 'percentage'" class="chart-container" ref="chartContainer4">
              <!-- Percentage Change chart will be rendered here -->
            </div>
            <div v-show="activeForestTab === 'distribution'" class="chart-container" ref="chartContainer5">
              <!-- Distribution chart will be rendered here -->
            </div>
            <div v-if="loading4 || loading5" class="loading-indicator"></div>
          </div>

          <div class="chart-description-panel">
            <div v-if="activeForestTab === 'percentage'">
              <p class="chart-description">
                Forests act as major carbon sinks, absorbing billions of tons of CO₂ annually. This chart shows how
                forest cover has changed globally, with some regions experiencing significant deforestation.
              </p>
              <p class="simple-explanation">
                <strong>Simply put:</strong> This shows which countries are losing or gaining forests - forests help
                fight climate change by absorbing carbon dioxide from the air.
              </p>
            </div>
            <div v-if="activeForestTab === 'distribution'">
              <p class="chart-description">
                This distribution shows that most countries fall within moderate ranges of forest change, with fewer at
                the extremes. The peak suggests that moderate changes in forest cover are most common globally.
              </p>
              <p class="simple-explanation">
                <strong>Simply put:</strong> Most countries have small changes in forest cover (middle of graph), while
                fewer countries have experienced dramatic forest loss or gain (edges of graph).
              </p>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- Section 3: Urban Heat Impact -->
    <section class="section-group">
      <h2 class="section-group-title">Urban Heat Impact in Australian Cities</h2>
      <p class="section-description">
        Climate change is causing more frequent and intense heat waves in urban areas. Recent studies suggest extreme
        heat in Australia's cities may be underreported by traditional measurement methods.
      </p>

      <div class="chart-section chart-section6">
        <div class="container">
          <h3>Number of Hot Days per Year by City</h3>

          <div class="chart-container" ref="chartContainer6">
            <!-- Plotly chart will be rendered here -->
          </div>
          <div v-if="loading6" class="loading-indicator"></div>
          <div class="simple-explanation">
            <strong>Simply put:</strong> This chart counts extremely hot days in Australian cities each year - more hot
            days means more health risks, higher energy costs, and greater strain on infrastructure.
          </div>
        </div>
      </div>

      <div class="impact-box">
        <h3>Climate Change Impacts</h3>
        <div class="impact-grid">
          <div class="impact-item">
            <h4>Health Risks</h4>
            <p>Beyond heatstroke, climate change affects health through worse air quality (bushfire smoke, pollution),
              potentially changing patterns of infectious diseases, and impacts on mental health.</p>
          </div>
          <div class="impact-item">
            <h4>Nature Under Pressure</h4>
            <p>Increased bushfire risk threatens forests like the Blue Mountains. Unique ecosystems face disruptions,
              and iconic wildlife struggle with changing conditions.</p>
          </div>
          <div class="impact-item">
            <h4>Economic Costs</h4>
            <p>Climate impacts have real economic costs: rising insurance premiums, infrastructure damage from extreme
              weather, agricultural disruption affecting food prices, and effects on tourism.</p>
          </div>
        </div>
      </div>
    </section>

    <!-- Taking Action Section -->
    <section class="action-brief">
      <h2>Taking Action Together</h2>
      <p class="section-description">
        The challenge is significant, but despair is not an option. We have the knowledge and increasingly the tools to
        make a difference. As urban residents, our collective actions and choices matter.
      </p>

      <div class="action-button-container">
        <a href="/eco-action" class="action-button">Explore EcoAction Solutions</a>
      </div>
    </section>
  </div>
</template>

<script setup>
import { ref, onMounted, watch } from 'vue';
import Plotly from 'plotly.js-dist-min';
const API_BASE_URL = import.meta.env.VITE_API_BASE_URL;

// Filter state
const selectedRegion = ref('global');
const selectedDataType = ref('emissions');
const selectedTimeframe = ref('last10Years');
const loading = ref(false);
const searchQuery = ref('');

// Chart reference
const chartContainer1 = ref(null)
const chartContainer2 = ref(null)
const chartContainer3 = ref(null)
const chartContainer4 = ref(null)
const chartContainer5 = ref(null)
const chartContainer6 = ref(null)
const loading1 = ref(false)
const loading2 = ref(false)
const loading3 = ref(false)
const loading4 = ref(false)
const loading5 = ref(false)
const loading6 = ref(false)
const activeForestTab = ref('percentage');
const activeTempTab = ref('confidence');

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

const fetchChartData1 = async () => {
  try {
    loading1.value = true;
    const response = await fetch(`${API_BASE_URL}/api/chartdata1`);
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }
    const chartData = await response.json();
    Plotly.newPlot(chartContainer1.value, chartData.data, chartData.layout);
  } catch (error) {
    console.error("Error fetching chart data:", error);
  } finally {
    loading1.value = false;
  }
};

const fetchChartData2 = async () => {
  try {
    loading2.value = true;
    const response = await fetch(`${API_BASE_URL}/api/chartdata2`);
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }
    const chartData = await response.json();
    Plotly.newPlot(chartContainer2.value, chartData.data, chartData.layout);
  } catch (error) {
    console.error("Error fetching chart data:", error);
  } finally {
    loading2.value = false;
  }
};

const fetchChartData3 = async () => {
  try {
    loading3.value = true;
    const response = await fetch(`${API_BASE_URL}/api/chartdata3`);
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }
    const chartData = await response.json();
    Plotly.newPlot(chartContainer3.value, chartData.data, chartData.layout);
  } catch (error) {
    console.error("Error fetching chart data:", error);
  } finally {
    loading3.value = false;
  }
};

const fetchChartData4 = async () => {
  try {
    loading4.value = true;
    const response = await fetch(`${API_BASE_URL}/api/chartdata4`);
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }
    const chartData = await response.json();
    Plotly.newPlot(chartContainer4.value, chartData.data, chartData.layout);
  } catch (error) {
    console.error("Error fetching chart data:", error);
  } finally {
    loading4.value = false;
  }
};

const fetchChartData5 = async () => {
  try {
    loading5.value = true;
    const response = await fetch(`${API_BASE_URL}/api/chartdata5`);
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }
    const chartData = await response.json();
    Plotly.newPlot(chartContainer5.value, chartData.data, chartData.layout);
  } catch (error) {
    console.error("Error fetching chart data:", error);
  } finally {
    loading5.value = false;
  }
};

const fetchChartData6 = async () => {
  try {
    loading6.value = true;
    const response = await fetch(`${API_BASE_URL}/api/chartdata6`);
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }
    const chartData = await response.json();
    Plotly.newPlot(chartContainer6.value, chartData.data, chartData.layout);
  } catch (error) {
    console.error("Error fetching chart data:", error);
  } finally {
    loading6.value = false;
  }
};
onMounted(() => {
  fetchChartData1();
  fetchChartData2();
  fetchChartData3();
  fetchChartData4();
  fetchChartData5();
  fetchChartData6();
});

watch(activeTempTab, (newVal) => {
  if (newVal === 'emissions' && chartContainer2.value) {
    setTimeout(() => Plotly.relayout(chartContainer2.value, { autosize: true }), 150);
  }
});

watch(activeForestTab, (newVal) => {
  if (newVal === 'distribution' && chartContainer5.value) {
    setTimeout(() => Plotly.relayout(chartContainer5.value, { autosize: true }), 150);
  }
});
</script>

<style scoped>
.climate-insight {
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
  background-color: var(--background);
  color: var(--text-dark);
}

.insight-header {
  text-align: center;
  margin-bottom: 40px;
  padding: 60px 20px;
  background-color: var(--primary-light);
  background-image: url('../assets/images/climate-insight-back.jpg');
  background-size: cover;
  background-position: center;
  background-repeat: no-repeat;
  border-radius: var(--border-radius);
  box-shadow: var(--box-shadow);
  position: relative;
}

.insight-header::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: rgba(0, 0, 0, 0.4);
  border-radius: var(--border-radius);
}

.insight-header h1,
.insight-header .subtitle {
  position: relative;
  z-index: 1;
  color: white;
}

.insight-header h1 {
  margin-bottom: 15px;
  font-size: 42px;
  font-weight: 700;
}

.insight-header .subtitle {
  font-size: 18px;
  max-width: 700px;
  margin: 0 auto;
  opacity: 0.9;
}

.subtitle {
  color: var(--text-light);
  font-size: 18px;
  max-width: 700px;
  margin: 0 auto;
}

.section-group {
  margin-bottom: 60px;
  background-color: var(--section-bg);
  border-radius: var(--border-radius);
  padding: 30px;
  box-shadow: var(--box-shadow);
}

.section-group-title {
  color: var(--primary-color);
  margin-bottom: 15px;
  font-size: 24px;
  border-bottom: 2px solid var(--primary-light);
  padding-bottom: 15px;
}

.chart-section {
  margin-bottom: 40px;
}

.chart-row {
  display: flex;
  flex-wrap: wrap;
  gap: 30px;
  margin-top: 30px;
}

.chart-row .chart-section {
  flex: 1 1 45%;
  min-width: 300px;
}

/* Create a specific class for centering Plotly charts */
.chart-tab-content {
  position: relative;
}

/* Ensure Plotly is centered within its container */
.chart-tab-content .js-plotly-plot,
.chart-container .js-plotly-plot {
  width: 100% !important;
}

.chart-container>div {
  display: flex;
  justify-content: center;
  width: 100%;
  height: 100%;
}

.temperature-analysis .chart-container[ref="chartContainer2"] .js-plotly-plot,
.forest-analysis .chart-container[ref="chartContainer5"] .js-plotly-plot {
  width: 100% !important;
}

.container {
  margin-bottom: 20px;
}

.container h3 {
  color: var(--primary-color);
  margin-bottom: 10px;
  font-size: 20px;
}

.chart-description {
  color: var(--text-light);
  margin-bottom: 15px;
  font-size: 15px;
  line-height: 1.5;
}

.chart-container {
  height: 450px;
  background-color: #f9f9f9;
  border-radius: 8px;
  border: 1px solid #eee;
  overflow: hidden;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
}

.loading-indicator {
  text-align: center;
  padding: 20px;
}

.impact-box {
  background-color: var(--primary-light);
  padding: 25px;
  border-radius: var(--border-radius);
  margin-top: 30px;
}

.impact-box h3 {
  color: var(--primary-color);
  margin-bottom: 20px;
  text-align: center;
}

.impact-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 20px;
}

.impact-item {
  background-color: white;
  padding: 20px;
  border-radius: 8px;
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.05);
}

.impact-item h4 {
  color: var(--primary-color);
  margin-bottom: 10px;
}

.action-section {
  background-color: var(--primary-light);
  padding: 40px 30px;
  border-radius: var(--border-radius);
  margin-bottom: 40px;
  box-shadow: var(--box-shadow);
}

.action-section h2 {
  color: var(--primary-color);
  margin-bottom: 15px;
  text-align: center;
}

.action-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
  gap: 20px;
  margin-top: 30px;
}

.action-item {
  background-color: white;
  padding: 20px;
  border-radius: 8px;
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.05);
}

.action-item h3 {
  color: var(--primary-color);
  margin-bottom: 10px;
  font-size: 18px;
}

.tab-controls {
  display: flex;
  gap: 10px;
  margin-bottom: 15px;
}

.tab-button {
  background-color: #f5f5f5;
  border: none;
  padding: 8px 16px;
  border-radius: 20px;
  cursor: pointer;
  font-size: 14px;
  transition: all 0.3s ease;
  color: var(--text-light);
}

.tab-button:hover {
  background-color: #e0e0e0;
}

.tab-button.active {
  background-color: var(--primary-color);
  color: white;
}

.chart-tab-content {
  position: relative;
}

.chart-description-panel {
  margin-top: 15px;
  padding: 15px;
  background-color: #f9f9f9;
  border-radius: 8px;
  border-left: 3px solid var(--primary-color);
}

.simple-explanation {
  background-color: #f0f7fa;
  border-left: 3px solid #2196F3;
  padding: 10px 15px;
  margin-top: 10px;
  font-size: 15px;
  line-height: 1.4;
  border-radius: 0 4px 4px 0;
}

.simple-explanation strong {
  color: #0277bd;
}

.action-brief {
  background-color: var(--primary-light);
  padding: 40px 30px;
  border-radius: var(--border-radius);
  margin-bottom: 40px;
  box-shadow: var(--box-shadow);
  text-align: center;
}

.action-brief h2 {
  color: var(--primary-color);
  margin-bottom: 15px;
}

.action-button-container {
  margin-top: 30px;
}

.action-button {
  display: inline-block;
  background-color: var(--primary-color);
  color: white;
  padding: 12px 24px;
  border-radius: 6px;
  text-decoration: none;
  font-weight: 600;
  transition: all 0.3s ease;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

.action-button:hover {
  background-color: #14574b;
  transform: translateY(-2px);
  box-shadow: 0 6px 8px rgba(0, 0, 0, 0.15);
}

/* Responsive design */
@media (max-width: 768px) {
  .chart-row {
    flex-direction: column;
  }

  .chart-row .chart-section {
    width: 100%;
  }

  .impact-grid,
  .action-grid {
    grid-template-columns: 1fr;
  }

  .chart-container {
    height: 350px;
  }

  .section-group,
  .action-section {
    padding: 20px 15px;
  }
}
</style>