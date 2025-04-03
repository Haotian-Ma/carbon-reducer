<!-- EcoAction.vue -->
<template>
    <div class="eco-action">
        <header class="header">
            <h1>Eco Action</h1>
            <p>Personalized Environmental Action Suggestions</p>
        </header>

        <!-- Location Selection Section -->
        <section class="location-section">
            <h2>Select Location</h2>
            <div class="location-controls">
                <select v-model="selectedCity" class="city-select">
                    <option value="">-- Select a City --</option>
                    <option v-for="city in australianCities" :key="city.value" :value="city.value">
                        {{ city.label }}
                    </option>
                </select>
                <button @click="getUserLocation" class="secondary-button" :disabled="loading">
                    <span v-if="!loading">Use My Location</span>
                    <span v-else>Loading...</span>
                </button>
            </div>
            <div v-if="locationError" class="error-message">
                {{ locationError }}
            </div>
        </section>

        <!-- Preferences Section (Displays only when city is selected) -->
        <section class="preferences-section" v-if="selectedCity">
            <h2>Environmental Preferences (Optional)</h2>
            <div class="preferences-controls">
                <div class="preference-item">
                    <label>Main Concern:</label>
                    <select v-model="environmentalConcern" class="preference-select">
                        <option value="">-- Select Concern --</option>
                        <option value="water">Water Resources</option>
                        <option value="energy">Energy Usage</option>
                        <option value="waste">Waste Management</option>
                        <option value="biodiversity">Biodiversity</option>
                        <option value="air">Air Quality</option>
                    </select>
                </div>
                <div class="preference-item">
                    <label>Housing Type:</label>
                    <select v-model="housingType" class="preference-select">
                        <option value="">-- Select Housing Type --</option>
                        <option value="apartment">Apartment</option>
                        <option value="house">House</option>
                        <option value="townhouse">Townhouse</option>
                    </select>
                </div>
            </div>

            <!-- Get Suggestions button moved here, only appears when city is selected -->
            <div class="action-button-container">
                <button @click="getEcoSuggestions" class="primary-button" :disabled="!selectedCity || loading">
                    Get Suggestions
                </button>
            </div>
        </section>

        <div class="loading-indicator" v-if="loading">
            <div class="spinner"></div>
            <p>Generating your personalized eco suggestions...</p>
        </div>

        <section class="results-section" v-if="suggestions && suggestions.length > 0">
            <h2>Your Personalized Eco Suggestions</h2>
            <div class="location-info">
                <h3>{{ cityInfo.name }}, {{ cityInfo.state }}</h3>
                <p>{{ cityInfo.description }}</p>
            </div>

            <div class="suggestions-container">
                <div v-for="(suggestion, index) in suggestions" :key="index" class="suggestion-card">
                    <h3>{{ suggestion.title }}</h3>
                    <p>{{ suggestion.content }}</p>
                    <div class="difficulty-level" :class="'level-' + suggestion.difficulty">
                        Difficulty: {{ getDifficultyText(suggestion.difficulty) }}
                    </div>
                </div>
            </div>
        </section>

        <section class="feedback-section" v-if="suggestions && suggestions.length > 0">
            <h3>Were these suggestions helpful?</h3>
            <div class="feedback-buttons">
                <button @click="submitFeedback(true)" class="feedback-button positive">Helpful</button>
                <button @click="submitFeedback(false)" class="feedback-button negative">Needs Improvement</button>
            </div>
            <div v-if="feedbackSubmitted" class="feedback-thanks">
                Thank you for your feedback!
            </div>
        </section>

        <footer class="footer">
            <p>Eco Action uses AI to provide personalized environmental suggestions. Our recommendations are based on
                general information. Please refer to local regulations for specific actions.</p>
        </footer>
    </div>
</template>

<script setup>
import { ref, reactive } from 'vue';

// User selections
const selectedCity = ref('');
const environmentalConcern = ref('');
const housingType = ref('');

// API status
const loading = ref(false);
const locationError = ref('');
const suggestions = ref([]);
const feedbackSubmitted = ref(false);

// City info (for display)
const cityInfo = reactive({
    name: '',
    state: '',
    description: ''
});

// Australian cities data
const australianCities = ref([
    { value: 'sydney', label: 'Sydney', state: 'New South Wales' },
    { value: 'melbourne', label: 'Melbourne', state: 'Victoria' },
    { value: 'brisbane', label: 'Brisbane', state: 'Queensland' },
    { value: 'perth', label: 'Perth', state: 'Western Australia' },
    { value: 'adelaide', label: 'Adelaide', state: 'South Australia' },
    { value: 'hobart', label: 'Hobart', state: 'Tasmania' },
    { value: 'darwin', label: 'Darwin', state: 'Northern Territory' },
    { value: 'canberra', label: 'Canberra', state: 'Australian Capital Territory' },
    { value: 'goldcoast', label: 'Gold Coast', state: 'Queensland' },
    { value: 'cairns', label: 'Cairns', state: 'Queensland' }
]);


// City geographic coordinates (for location matching)
const cityCoordinates = {
    sydney: { lat: -33.8688, lon: 151.2093 },
    melbourne: { lat: -37.8136, lon: 144.9631 },
    brisbane: { lat: -27.4698, lon: 153.0251 },
    perth: { lat: -31.9505, lon: 115.8605 },
    adelaide: { lat: -34.9285, lon: 138.6007 },
    hobart: { lat: -42.8821, lon: 147.3272 },
    darwin: { lat: -12.4634, lon: 130.8456 },
    canberra: { lat: -35.2809, lon: 149.1300 },
    goldcoast: { lat: -28.0167, lon: 153.4000 },
    cairns: { lat: -16.9186, lon: 145.7781 }
};

// Dify API configuration
const difyConfig = {
    apiKey: 'app-qdqefgJOJ5PCIOyziUDhQgYY',
    endpoint: 'https://api.dify.ai/v1/chat-messages'
};

// Get user geolocation
const getUserLocation = () => {
    loading.value = true;
    locationError.value = '';

    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(
            handleLocationSuccess,
            handleLocationError,
            {
                enableHighAccuracy: true,
                timeout: 10000,
                maximumAge: 0
            }
        );
    } else {
        locationError.value = "Your browser doesn't support geolocation";
        loading.value = false;
    }
};

// Handle successful location retrieval
const handleLocationSuccess = (position) => {
    const lat = position.coords.latitude;
    const lon = position.coords.longitude;

    // Find nearest Australian city
    const nearestCity = findNearestAustralianCity(lat, lon);

    if (nearestCity) {
        selectedCity.value = nearestCity;
        loading.value = false; // Stop loading state without triggering suggestions
    } else {
        locationError.value = "Could not find a matching Australian city, please select manually";
        loading.value = false;
    }
};

// Handle location retrieval error
const handleLocationError = (error) => {
    loading.value = false;
    switch (error.code) {
        case error.PERMISSION_DENIED:
            locationError.value = "Location request was denied";
            break;
        case error.POSITION_UNAVAILABLE:
            locationError.value = "Location information is unavailable";
            break;
        case error.TIMEOUT:
            locationError.value = "Location request timed out";
            break;
        default:
            locationError.value = "Unknown error occurred when getting location";
    }
};

// Find nearest Australian city
const findNearestAustralianCity = (lat, lon) => {
    // Check if coordinates are roughly in Australia
    if (lat < -10 && lat > -45 && lon > 110 && lon < 155) {
        let nearestCity = null;
        let shortestDistance = Infinity;

        // Calculate distances to each city
        for (const [city, coords] of Object.entries(cityCoordinates)) {
            const distance = calculateDistance(lat, lon, coords.lat, coords.lon);
            if (distance < shortestDistance) {
                shortestDistance = distance;
                nearestCity = city;
            }
        }

        return nearestCity;
    }

    return null;
};

// Calculate distance between two points using Haversine formula
const calculateDistance = (lat1, lon1, lat2, lon2) => {
    const R = 6371; // Earth's radius in km
    const dLat = (lat2 - lat1) * Math.PI / 180;
    const dLon = (lon2 - lon1) * Math.PI / 180;
    const a =
        Math.sin(dLat / 2) * Math.sin(dLat / 2) +
        Math.cos(lat1 * Math.PI / 180) * Math.cos(lat2 * Math.PI / 180) *
        Math.sin(dLon / 2) * Math.sin(dLon / 2);
    const c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1 - a));
    return R * c; // Distance in km
};

// Get eco suggestions
const getEcoSuggestions = async () => {
    // Validate input
    if (!selectedCity.value) {
        locationError.value = "Please select a city";
        return;
    }

    loading.value = true;
    suggestions.value = [];
    locationError.value = '';

    try {
        // Set city info
        const cityData = australianCities.value?.find(city =>
            city.value === selectedCity.value
        );
        if (!cityData) throw new Error("Invalid city selection");

        cityInfo.value = {
            name: cityData.label,
            state: cityData.state,
            description: getCityDescription(selectedCity.value)
        };

        // Prepare API payload with strict English requirements
        const payload = {
            inputs: {
                location: selectedCity.value,
                region_characteristics: getRegionCharacteristics(selectedCity.value),
                environmental_concern: environmentalConcern.value || "general",
                housing_type: housingType.value || "not specified",
                language: "en" // Force English output
            },
            query: `Provide exactly 5 eco-tips for ${cityData.label} following these rules:
                    - Use English only
                    - Each tip: max 25 words
                    - Include difficulty (1-3)
                    - Format as JSON`,
            response_mode: "blocking",
            user: "test_user",

        };

        // Actual API call (remove mock in production)
        const response = await callDifyAPI(payload);
        suggestions.value = parseStreamingResponse(response);

    } catch (error) {
        console.error("API Error:", error);
        locationError.value = "Failed to load suggestions. Showing sample data...";
        suggestions.value = getMockSuggestions(selectedCity.value);
    } finally {
        loading.value = false;
    }
};
// Strict response parser for English content
const parseStreamingResponse = (response) => {
    console.log('Raw API response:', JSON.stringify(response, null, 2));

    try {
        if (Array.isArray(response.suggestions)) {
            return response.suggestions;
        }

        if (typeof response.answer === 'string') {
            // 直接移除 Markdown 代码块
            const jsonStr = response.answer.replace(/```json|```/g, '').trim();
            const parsed = JSON.parse(jsonStr);

            if (Array.isArray(parsed.suggestions)) {
                return parsed.suggestions;
            }
        }

        throw new Error('Unrecognized response format');
    } catch (error) {
        console.error('Parsing failed:', error);
        return getMockSuggestions();
    }
};

// Call Dify API (implement in actual project)
const callDifyAPI = async (payload) => {
    const response = await fetch(difyConfig.endpoint, {
        method: 'POST',
        headers: {
            'Authorization': `Bearer ${difyConfig.apiKey}`,
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(payload)
    });

    if (!response.ok) {
        throw new Error(`API request failed: ${response.status}`);
    }

    return response.json();
};
const getCityDescription = (city) => {
    const descriptions = {
        sydney: "Australia's largest city with iconic harbors and beaches.",
        melbourne: "Cultural capital known for variable weather patterns.",
        brisbane: "Subtropical river city with abundant sunshine.",
        perth: "Isolated coastal city with Mediterranean climate.",
        adelaide: "Planned city with Mediterranean climate and innovative sustainability initiatives.",
        hobart: "Temperate island capital with mountain backdrop.",
        darwin: "Tropical northern capital with distinct wet and dry seasons.",
        canberra: "Planned inland capital with four distinct seasons.",
        goldcoast: "Coastal city with beaches, waterways and rainforest hinterland.",
        cairns: "Tropical gateway to the Great Barrier Reef and rainforests."
    };
    return descriptions[city] || "Australian city";
};
// Get region characteristics (example data, could be fetched from API)
const getRegionCharacteristics = (city) => {
    const characteristics = {
        sydney: "coastal, urban, occasional drought, high population density",
        melbourne: "variable weather, moderate rainfall, urban sprawl",
        brisbane: "subtropical, flood-prone, river city, high humidity",
        perth: "mediterranean climate, water scarcity, isolated",
        adelaide: "dry, murray river dependent, mediterranean climate",
        hobart: "cool temperate, mountainous surroundings, clean air",
        darwin: "tropical monsoon, cyclone-prone, wet-dry extremes",
        canberra: "inland, four distinct seasons, planned city",
        goldcoast: "coastal, high rainfall, tourism impact, canal system",
        cairns: "tropical, reef proximity, rainforest, high rainfall"
    };
    return characteristics[city] || "";
};



// Submit feedback (implement in actual project)
const submitFeedback = (isPositive) => {
    // In a real project, this would send feedback to backend
    console.log(`User submitted ${isPositive ? 'positive' : 'negative'} feedback`);
    feedbackSubmitted.value = true;

    // Could add Dify feedback API call here
};

// Get difficulty text
const getDifficultyText = (level) => {
    switch (level) {
        case 1: return "Easy";
        case 2: return "Medium";
        case 3: return "Hard";
        default: return "Not specified";
    }
};

const getMockSuggestions = (city) => {
    // Hardcoded mock data, would be fetched from Dify API
    const allSuggestions = {
        sydney: [
            {
                title: "Water Conservation",
                content: "Sydney often faces water restrictions. Install rainwater tanks for garden use, take shorter showers (4-minute limit recommended), and use drought-resistant native plants in your garden.",
                difficulty: 1
            },
            {
                title: "Public Transport",
                content: "Utilize Sydney's extensive public transport network including trains, buses, ferries, and light rail to reduce vehicle emissions in this congested city.",
                difficulty: 1
            },
            {
                title: "Harbour Health",
                content: "Be mindful about chemicals that could enter stormwater systems, as Sydney Harbour's water quality depends on responsible urban practices. Use eco-friendly cleaning products.",
                difficulty: 2
            },
            {
                title: "Heat Wave Protection",
                content: "Plant native shade trees around your property to combat urban heat island effect and reduce cooling costs during Sydney's increasingly hot summers.",
                difficulty: 2
            },
            {
                title: "Reduce Plastic Use",
                content: "Sydney is a coastal city where plastic pollution threatens marine life. Use reusable shopping bags, water bottles, and avoid single-use plastic items.",
                difficulty: 1
            }
        ],
        melbourne: [
            {
                title: "Water Efficiency",
                content: "Melbourne has faced severe drought conditions in the past. Install water-efficient appliances, collect shower warm-up water for plants, and consider drought-tolerant landscaping.",
                difficulty: 2
            },
            {
                title: "Green Transport",
                content: "Take advantage of Melbourne's excellent tram network (the largest in the world) and extensive bicycle paths. The city is designed for car-free living in many areas.",
                difficulty: 1
            },
            {
                title: "Energy Conservation",
                content: "Due to Melbourne's variable weather, ensure your home has good insulation. Use draft stoppers to prevent heat loss during the city's cool winters.",
                difficulty: 2
            },
            {
                title: "Urban Gardening",
                content: "Support Melbourne's biodiversity by creating home gardens with indigenous plants that support local wildlife, especially important in a city that has lost significant native grasslands.",
                difficulty: 2
            },
            {
                title: "Adapt to Changing Weather",
                content: "Melbourne is known for its 'four seasons in one day' weather. Prepare emergency items and adapt to rapidly changing weather conditions to reduce the impact of weather changes on energy use.",
                difficulty: 1
            }
        ],
        // Add other cities as needed
    };
}


</script>
<style scoped>
.eco-action {
    max-width: 1000px;
    margin: 0 auto;
    padding: 20px;
}

.header {
    text-align: center;
    margin-bottom: 30px;
}

.header h1 {
    color: var(--primary-color);
    margin-bottom: 5px;
}

section {
    margin-bottom: 30px;
    padding: 20px;
    background-color: #f9f9f9;
    border-radius: var(--border-radius);
    box-shadow: var(--shadow);
}

.location-controls,
.preferences-controls {
    display: flex;
    flex-wrap: wrap;
    gap: 10px;
    align-items: center;
}

.city-select,
.preference-select {
    padding: 10px;
    border: 1px solid #ccc;
    border-radius: 4px;
    font-size: 16px;
    min-width: 200px;
}

.primary-button {
    background: linear-gradient(135deg, var(--primary-gradient-start), var(--primary-gradient-end));
    color: white;
    border: none;
    padding: 10px 20px;
    border-radius: 4px;
    cursor: pointer;
    font-size: 16px;
}

.primary-button:hover {
    background-color: var(--primary-gradient-end);
}

.primary-button:disabled {
    background-color: #cccccc;
    cursor: not-allowed;
}

.secondary-button {
    background-color: #f5f5f5;
    color: #333;
    border: 1px solid #ccc;
    padding: 10px 20px;
    border-radius: 4px;
    cursor: pointer;
    font-size: 16px;
}

.secondary-button:hover {
    background-color: #e0e0e0;
}

.error-message {
    color: #d32f2f;
    margin-top: 10px;
}

.loading-indicator {
    display: flex;
    flex-direction: column;
    align-items: center;
    margin: 20px 0;
}

.spinner {
    border: 4px solid #f3f3f3;
    border-top: 4px solid var(--primary-color);
    border-radius: 50%;
    width: 40px;
    height: 40px;
    animation: spin 1s linear infinite;
    margin-bottom: 10px;
}

.location-info {
    margin-bottom: 20px;
    padding: 15px;
    background-color: #e8f5e9;
    border-radius: 4px;
}

.suggestions-container {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
    gap: 20px;
}

.suggestion-card {
    padding: 15px;
    background-color: white;
    border-radius: 8px;
    box-shadow: var(--shadow);
    border-top: 5px solid var(--primary-color);
    transition: var(--transition);
}

.suggestion-card:hover {
    transform: translateY(-5px);
    box-shadow: var(--shadow-hover);
}

.suggestion-card h3 {
    color: var(--primary-color);
    margin-top: 0;
}

.difficulty-level {
    display: inline-block;
    padding: 3px 8px;
    border-radius: 4px;
    font-size: 14px;
    margin-top: 10px;
}

.level-1 {
    background-color: #e8f5e9;
    color: var(--primary-color);
}

.level-2 {
    background-color: #fff9c4;
    color: #f57f17;
}

.level-3 {
    background-color: #ffebee;
    color: #c62828;
}

.feedback-section {
    text-align: center;
    margin-top: 30px;
}

.feedback-buttons {
    display: flex;
    justify-content: center;
    gap: 20px;
    margin-top: 10px;
}

.feedback-button {
    padding: 8px 20px;
    border-radius: 4px;
    border: none;
    cursor: pointer;
}

.feedback-button.positive {
    background-color: #e8f5e9;
    color: var(--primary-color);
}

.feedback-button.negative {
    background-color: #ffebee;
    color: #c62828;
}

.feedback-thanks {
    margin-top: 10px;
    color: var(--primary-color);
}

.preference-item {
    display: flex;
    align-items: center;
    gap: 10px;
}

.footer {
    margin-top: 40px;
    padding-top: 20px;
    border-top: 1px solid #eee;
    color: var(--text-light);
    font-size: 14px;
    text-align: center;
}

/* Responsive Design */
@media (max-width: 768px) {

    .location-controls,
    .preferences-controls {
        flex-direction: column;
        align-items: stretch;
    }

    .suggestions-container {
        grid-template-columns: 1fr;
    }
}
</style>
