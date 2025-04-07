<!-- EcoAction.vue -->
<template>
    <div class="eco-action">
        <div class="hero-section" :style="{ backgroundImage: `url(${currentBackground})` }">
            <header class="header">
                <h1>Eco Action</h1>
                <p class="white-text">Personal Carbon Assessment & Environmental Action Suggestions</p>
            </header>
            <div class="step-indicator">
                <div v-for="(step, index) in steps" :key="step.id" :class="{
                    'active': currentStep === step.id,
                    'completed': step.completed,
                    'first': index === 0,
                    'last': index === steps.length - 1
                }" @click="goToStep(step.id)">
                    <div class="step-number">{{ step.id }}</div>
                    <div class="step-title">{{ step.title }}</div>
                </div>
            </div>
        </div>
        <section class="assessment-section">
            <h2>Carbon Footprint Assessment - Step {{ currentStep }} of {{ steps.length }}</h2>
            <div v-if="currentStep === 1" class="assessment-group">
                <h3>1. Transportation Habits</h3>
                <div class="assessment-subgroup">
                    <label>Daily Commuting:<span class="required-field">*</span></label>
                    <div class="checkbox-group">
                        <label class="checkbox-label">
                            <input type="checkbox" v-model="transportation.commuting.walking"> Walking/Bicycle
                        </label>
                        <label class="checkbox-label">
                            <input type="checkbox" v-model="transportation.commuting.publicTransport"> Public
                            Transportation
                        </label>
                        <label class="checkbox-label">
                            <input type="checkbox" v-model="transportation.commuting.fuelCar"> Fuel Car
                        </label>
                        <label class="checkbox-label">
                            <input type="checkbox" v-model="transportation.commuting.electricCar"> Electric Car
                        </label>
                    </div>
                </div>

                <div class="assessment-subgroup">
                    <label>Long-Distance Travel:</label>
                    <div class="checkbox-group">
                        <label class="checkbox-label">
                            <input type="checkbox" v-model="transportation.longDistance.airplane"> Airplane
                        </label>
                        <div class="nested-option" v-if="transportation.longDistance.airplane">
                            <select v-model="transportation.longDistance.airplaneFrequency" class="sub-select">
                                <option value="low">Less than 2 times/year</option>
                                <option value="medium">3-5 times/year</option>
                                <option value="high">More than 5 times/year</option>
                            </select>
                        </div>
                        <label class="checkbox-label">
                            <input type="checkbox" v-model="transportation.longDistance.train"> Train
                        </label>
                        <label class="checkbox-label">
                            <input type="checkbox" v-model="transportation.longDistance.selfDriving"> Self-Driving
                        </label>
                    </div>
                </div>

                <div class="assessment-subgroup">
                    <label>Additional Options:</label>
                    <div class="checkbox-group">
                        <label class="checkbox-label">
                            <input type="checkbox" v-model="transportation.additional.carpool"> I often
                            carpool</label>
                        <label class="checkbox-label">
                            <input type="checkbox" v-model="transportation.additional.remoteWork"> I often work
                            remotely
                        </label>
                    </div>
                </div>
            </div>

            <!-- step2 -->
            <div v-else-if="currentStep === 2" class="assessment-group">
                <h3>2. Household Energy</h3>
                <div class="assessment-subgroup">
                    <label>Number of Family Members:<span class="required-field">*</span></label>
                    <input type="number" v-model="household.familyMembers" min="1" class="number-input" required>
                </div>

                <div class="assessment-subgroup">
                    <label>Monthly Electricity Consumption (kWh): <span class="required-field">*</span></label>
                    <input type="number" v-model="household.electricityConsumption" min="0" class="number-input"
                        required>

                    <div v-if="household.familyMembers" class="reference-value">
                        <p>
                            Reference: {{ getReferenceElectricityUsage() }} kWh/month
                            <span v-if="household.city">(Average for {{ getCityName() }} {{ displayFamilySize() }}
                                household)</span>
                            <span v-else>(Average for Australian {{ displayFamilySize() }} household)</span>
                        </p>
                    </div>
                </div>

                <div class="assessment-subgroup">
                    <label>City (Optional):</label>
                    <select v-model="household.city" class="preference-select">
                        <option value="">-- Select City --</option>
                        <option value="sydney">Sydney</option>
                        <option value="brisbane">Brisbane</option>
                        <option value="adelaide">Adelaide</option>
                        <option value="melbourne">Melbourne</option>
                        <option value="canberra">Canberra</option>
                        <option value="hobart">Hobart</option>
                    </select>
                </div>

                <div class="assessment-subgroup">
                    <label>Energy-Saving Habits:</label>
                    <div class="checkbox-group">
                        <label class="checkbox-label">
                            <input type="checkbox" v-model="household.habits.turnOff"> Often turn off
                            lights/electrical
                            appliances
                        </label>
                        <label class="checkbox-label">
                            <input type="checkbox" v-model="household.habits.energySaving"> Use energy-saving
                            equipment
                        </label>
                        <label class="checkbox-label">
                            <input type="checkbox" v-model="household.habits.noSpecial"> No special habits
                        </label>
                    </div>
                </div>
            </div>

            <!-- step 3 -->
            <div v-else-if="currentStep === 3" class="assessment-group">
                <h3>3. Environmental Preferences</h3>
                <p>Topics you care about (select one or more):</p>

                <div class="checkbox-group">
                    <label class="checkbox-label">
                        <input type="checkbox" v-model="preferences.waterResources"> Water Resources
                    </label>
                    <label class="checkbox-label">
                        <input type="checkbox" v-model="preferences.energyUsage"> Energy Usage
                    </label>
                    <label class="checkbox-label">
                        <input type="checkbox" v-model="preferences.wasteManagement"> Waste Management
                    </label>
                    <label class="checkbox-label">
                        <input type="checkbox" v-model="preferences.biodiversity"> Biodiversity
                    </label>
                    <label class="checkbox-label">
                        <input type="checkbox" v-model="preferences.airQuality"> Air Quality
                    </label>
                </div>
            </div>

            <!-- step 4 -->
            <div v-else-if="currentStep === 4" class="assessment-group">
                <h3>4. Housing Type</h3>
                <select v-model="housingType" class="preference-select">
                    <option value="">-- Select Housing Type --</option>
                    <option value="apartment">Apartment</option>
                    <option value="house">House</option>
                    <option value="townhouse">Townhouse</option>
                </select>
            </div>

            <div class="step-navigation">
                <button v-if="currentStep > 1" @click="goToPrevStep" class="nav-button prev-button">
                    Previous
                </button>
                <button @click="goToNextStep" class="nav-button next-button">
                    {{ currentStep < steps.length ? 'Next' : 'Calculate My Carbon Footprint' }} </button>
            </div>
        </section>

        <!-- Loading Indicator -->
        <div class="loading-indicator" v-if="loading">
            <div class="spinner"></div>
            <p>{{ loadingMessage }}</p>
        </div>

        <!-- Carbon Footprint Results -->
        <section class="results-section" v-if="carbonLevel">
            <h2>Your Carbon Footprint Assessment</h2>

            <div class="carbon-rating">
                <div class="rating-label">Your Carbon Footprint Level:</div>
                <div class="rating-value" :class="'carbon-level-' + carbonLevel.toLowerCase()">
                    {{ carbonLevel }}
                </div>
                <div class="rating-description">{{ getCarbonLevelDescription() }}</div>
            </div>

            <div class="action-button-container">
                <button @click="getEcoSuggestions" class="primary-button" :disabled="loading">
                    Get Personalized Eco Suggestions
                </button>
            </div>
        </section>

        <!-- Eco Suggestions Section -->
        <section class="results-section" v-if="suggestions && suggestions.length > 0">
            <h2>Your Personalized Eco Suggestions</h2>
            <div class="suggestions-container">
                <div v-for="(suggestion, index) in suggestions" :key="index" class="suggestion-card">
                    <h3>{{ suggestion.title }} <span class="emoji">{{ suggestion.emoji }}</span></h3>
                    <p>{{ suggestion.content }}</p>
                    <div v-if="suggestion.reason" class="suggestion-reason">
                        {{ suggestion.reason }}
                    </div>
                    <div class="difficulty-level" :class="'level-' + suggestion.difficulty">
                        Difficulty: {{ getDifficultyText(suggestion.difficulty) }}
                    </div>
                    <div class="impact-level" :class="'impact-' + suggestion.impact">
                        Impact: {{ getImpactText(suggestion.impact) }}
                    </div>
                    <button class="complete-button" :class="{ 'completed': suggestion.completed }"
                        @click="markTaskComplete(suggestion)">
                        <span v-if="suggestion.completed">✓ Done</span>
                        <span v-else>Complete</span>
                    </button>
                </div>
            </div>
        </section>

        <!-- Feedback Section -->
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
            <p>Eco Action uses AI to provide personalized environmental suggestions based on your carbon footprint.
                Our
                recommendations are general information only. Please refer to local regulations for specific
                actions.
            </p>
        </footer>
        <div v-if="showCompletionModal" class="modal">
            <div class="modal-content completion-modal">
                <span @click="showCompletionModal = false" class="close-button">&times;</span>
                <div class="celebration-animation">
                    <span class="celebration-icon">🎉</span>
                </div>
                <h3>Great job!</h3>
                <p>You just earned <span class="energy-value">{{ earnedEnergy }}</span> energy points!</p>
                <p class="task-completed">Task: {{ completedTaskTitle }}</p>
                <button @click="showCompletionModal = false" class="primary-button">Continue</button>
            </div>
        </div>
    </div>
</template>

<script setup>
import { ref, reactive, computed } from 'vue';
import electricityData from '../assets/jsons/electricity-data.json'

//background image
const backgroundImages = {
    1: new URL('../assets/images/eco-action-step1.jpg', import.meta.url).href,
    2: new URL('../assets/images/eco-action-step2.jpg', import.meta.url).href,
    3: new URL('../assets/images/eco-action-step3.jpg', import.meta.url).href,
    4: new URL('../assets/images/eco-action-step4.jpg', import.meta.url).href
};
const currentBackground = computed(() => backgroundImages[currentStep.value]);


// User selections 
const housingType = ref('');

// API status
const loading = ref(false);
const suggestions = ref([]);
const feedbackSubmitted = ref(false);
const loadingMessage = ref('Processing your information...');
// Show completion modal
const showCompletionModal = ref(false);
const earnedEnergy = ref(0);
const completedTaskTitle = ref('');
// Dify API configuration
const difyConfig = {
    apiKey: 'app-qdqefgJOJ5PCIOyziUDhQgYY',
    endpoint: 'https://api.dify.ai/v1/chat-messages'
};
const currentStep = ref(1); // Current step in the assessment process
const steps = [
    { id: 1, title: "Transportation Habits", completed: false },
    { id: 2, title: "Household Energy", completed: false },
    { id: 3, title: "Environmental Preferences", completed: false },
    { id: 4, title: "Housing Type", completed: false }
];
const goToNextStep = () => {

    if (!validateCurrentStep()) {
        return;
    }


    steps[currentStep.value - 1].completed = true;

    if (currentStep.value < steps.length) {
        currentStep.value++;
    } else {

        calculateCarbonFootprint();
    }
};

const goToPrevStep = () => {
    if (currentStep.value > 1) {
        currentStep.value--;
    }
};
const validateCurrentStep = () => {
    switch (currentStep.value) {
        case 1:
            if (!transportation.commuting.walking &&
                !transportation.commuting.publicTransport &&
                !transportation.commuting.fuelCar &&
                !transportation.commuting.electricCar) {
                alert("Please select at least one transportation method");
                return false;
            }
            break;
        case 2:
            if (!household.electricityConsumption) {
                alert("Please enter your monthly electricity consumption");
                return false;
            }
            break;

    }
    return true;
};

// Carbon assessment results
const carbonLevel = ref(''); // Will be one of: 'Low', 'Medium', 'High'

// New data structures for carbon assessment
const transportation = reactive({
    commuting: {
        walking: false,
        publicTransport: false,
        fuelCar: false,
        electricCar: false
    },
    longDistance: {
        airplane: false,
        airplaneFrequency: 'low',
        train: false,
        selfDriving: false
    },
    additional: {
        carpool: false,
        remoteWork: false
    }
});

const household = reactive({
    familyMembers: 1,
    electricityConsumption: 0,
    city: '',
    habits: {
        turnOff: false,
        energySaving: false,
        noSpecial: false
    }
});

const preferences = reactive({
    waterResources: false,
    energyUsage: false,
    wasteManagement: false,
    biodiversity: false,
    airQuality: false
});
// get reference electricity usage
const getReferenceElectricityUsage = () => {
    const familySize = household.familyMembers >= 5 ? "5+" : household.familyMembers.toString();

    if (household.city && electricityData.monthlyElectricityUsage[household.city]) {
        return electricityData.monthlyElectricityUsage[household.city][familySize];
    } else {
        return electricityData.monthlyElectricityUsage.average[familySize];
    }
};

// show city name
const getCityName = () => {
    const cityNames = {
        sydney: "Sydney",
        brisbane: "Brisbane",
        adelaide: "Adelaide",
        melbourne: "Melbourne",
        canberra: "Canberra",
        hobart: "Hobart"
    };

    return cityNames[household.city] || "";
};

// show family size
const displayFamilySize = () => {
    return household.familyMembers >= 5 ? "5+ person" : household.familyMembers + " person";
};

// Calculate carbon footprint score
const calculateCarbonFootprint = () => {
    const errors = [];

    const hasTransportationMethod = transportation.commuting.walking ||
        transportation.commuting.publicTransport ||
        transportation.commuting.fuelCar ||
        transportation.commuting.electricCar;

    if (!hasTransportationMethod) {
        errors.push("Please select at least one transportation method");
    }

    if (!household.electricityConsumption) {
        errors.push("Please enter your monthly electricity consumption");
    }

    if (errors.length > 0) {
        alert(errors.join("\n"));
        return;
    }
    loading.value = true;
    loadingMessage.value = "Calculating your carbon footprint...";

    let score = 0;

    // Transportation score (0-100, higher is worse for environment)
    let transportScore = 0;

    // Commuting impact
    if (transportation.commuting.walking) transportScore -= 20;
    if (transportation.commuting.publicTransport) transportScore += 10;
    if (transportation.commuting.fuelCar) transportScore += 40;
    if (transportation.commuting.electricCar) transportScore += 15;

    // Long distance travel impact
    if (transportation.longDistance.airplane) {
        if (transportation.longDistance.airplaneFrequency === 'low') transportScore += 20;
        else if (transportation.longDistance.airplaneFrequency === 'medium') transportScore += 35;
        else if (transportation.longDistance.airplaneFrequency === 'high') transportScore += 50;
    }

    if (transportation.longDistance.train) transportScore += 10;
    if (transportation.longDistance.selfDriving) transportScore += 30;

    // Mitigating factors
    if (transportation.additional.carpool) transportScore -= 15;
    if (transportation.additional.remoteWork) transportScore -= 20;

    // Normalize transportation score (0-100)
    transportScore = Math.max(0, Math.min(100, transportScore));

    // Household energy score (0-100)
    let householdScore = 0;
    // Get reference electricity usage
    let referenceUsage = getReferenceElectricityUsage();
    const actualUsage = household.electricityConsumption;

    if (referenceUsage > 0) {
        // calculate usage ratio
        const usageRatio = actualUsage / referenceUsage;

        // rating based on usage ratio
        if (usageRatio < 0.7) {
            householdScore = 20; // low usage
        } else if (usageRatio < 0.9) {
            householdScore = 35; // below average usage
        } else if (usageRatio < 1.1) {
            householdScore = 50; // average usage
        } else if (usageRatio < 1.3) {
            householdScore = 65; // above average usage
        } else if (usageRatio < 1.5) {
            householdScore = 80; // high usage
        } else {
            householdScore = 100; // very high usage
        }
    } else {
        // if no reference data, use actual usage
        const perPerson = actualUsage / Math.max(1, household.familyMembers);

        // rating based on per person usage
        if (perPerson < 100) householdScore = 20;
        else if (perPerson < 167) householdScore = 40;
        else if (perPerson < 233) householdScore = 60;
        else if (perPerson < 300) householdScore = 80;
        else householdScore = 100;
    }

    // Household habits impact
    if (household.habits.turnOff) householdScore -= 10;
    if (household.habits.energySaving) householdScore -= 15;
    if (household.habits.noSpecial) householdScore += 10;

    // Housing type impact
    if (housingType.value === 'apartment') householdScore -= 10;
    else if (housingType.value === 'house') householdScore += 10;
    else if (housingType.value === 'townhouse') householdScore += 5;

    // Normalize household score (0-100)
    householdScore = Math.max(0, Math.min(100, householdScore));

    // Calculate final score (weighted average)
    score = (transportScore * 0.6) + (householdScore * 0.4);

    // Determine carbon level
    if (score < 40) carbonLevel.value = 'Low';
    else if (score < 70) carbonLevel.value = 'Medium';
    else carbonLevel.value = 'High';

    // For debugging
    console.log('Carbon assessment:', {
        transportScore,
        householdScore,
        finalScore: score,
        level: carbonLevel.value
    });

    loading.value = false;
};

// Get carbon level description
const getCarbonLevelDescription = () => {
    switch (carbonLevel.value) {
        case 'Low':
            return "Your carbon footprint is below average. Great job! We'll suggest ways to maintain and improve your eco-friendly lifestyle.";
        case 'Medium':
            return "Your carbon footprint is average. There are several areas where you could make changes to reduce your environmental impact.";
        case 'High':
            return "Your carbon footprint is above average. We'll suggest key areas where you can make changes to significantly reduce your environmental impact.";
        default:
            return "";
    }
};

// Get eco suggestions
const getEcoSuggestions = async () => {
    if (!carbonLevel.value) {
        return;
    }

    loading.value = true;
    loadingMessage.value = "Generating your personalized eco suggestions...";
    suggestions.value = [];

    try {
        // Get primary environmental concern (or "general" if none selected)
        let primaryConcern = "general";
        if (preferences.waterResources) primaryConcern = "water";
        else if (preferences.energyUsage) primaryConcern = "energy";
        else if (preferences.wasteManagement) primaryConcern = "waste";
        else if (preferences.biodiversity) primaryConcern = "biodiversity";
        else if (preferences.airQuality) primaryConcern = "air";

        // Prepare API payload for Dify
        const payload = {
            inputs: {
                carbon_level: carbonLevel.value.toLowerCase(),
                environmental_concern: primaryConcern,
                housing_type: housingType.value || "not specified",
                transportation_habits: JSON.stringify(getTransportationSummary()),
                household_energy: JSON.stringify(getHouseholdEnergySummary()),
                language: "en" // Force English output
            },
            query: `Provide eco-tips for a person with ${carbonLevel.value.toLowerCase()} carbon footprint`,
            response_mode: "blocking",
            user: "test_user"
        };

        // Call Dify API
        try {
            const response = await callDifyAPI(payload);

            // Parse the response
            const parsedSuggestions = parseStreamingResponse(response);
            if (parsedSuggestions && parsedSuggestions.length > 0) {
                suggestions.value = parsedSuggestions;
            } else {
                throw new Error("Failed to parse suggestions from API response");
            }
        } catch (apiError) {
            console.error("API Error:", apiError);
            // Fallback to mock suggestions
            suggestions.value = getMockSuggestions(carbonLevel.value.toLowerCase());
        }
    } catch (error) {
        console.error("Error generating suggestions:", error);
        // Fallback to mock suggestions
        suggestions.value = getMockSuggestions(carbonLevel.value.toLowerCase());
    } finally {
        loading.value = false;
    }
};

// Call Dify API (from your working code)
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

// Parse streaming response for Dify API
const parseStreamingResponse = (response) => {

    try {
        // Check if response already has parsed suggestions array
        if (response && Array.isArray(response.suggestions)) {
            return response.suggestions.map(suggestion => ({
                ...suggestion,
                // Add impact level based on difficulty if not provided
                impact: suggestion.impact || suggestion.difficulty,
                // Ensure completed flag exists
                completed: false
            }));
        }

        // Check if response contains an answer field with JSON string
        if (response && typeof response.answer === 'string') {
            // Remove any markdown code blocks
            const jsonStr = response.answer.replace(/```json|```/g, '').trim();

            // Parse the JSON
            const parsed = JSON.parse(jsonStr);

            // Check for suggestions array in parsed JSON
            if (parsed && Array.isArray(parsed.suggestions)) {
                return parsed.suggestions.map(suggestion => ({
                    title: suggestion.title,
                    content: suggestion.content,
                    difficulty: suggestion.difficulty,
                    // Convert emoji to impact level or use difficulty as fallback
                    impact: suggestion.impact || suggestion.difficulty,
                    // Add emoji if available
                    emoji: suggestion.emoji || "",
                    // Add reason if available
                    reason: suggestion.reason || "",
                    // Initialize completed status
                    completed: false
                }));
            }
        }

        throw new Error('Unrecognized response format');
    } catch (error) {
        console.error('Parsing failed:', error);
        return [];
    }
};

// Helper function to get transportation summary for API
const getTransportationSummary = () => {
    const commuting = [];
    if (transportation.commuting.walking) commuting.push("walking");
    if (transportation.commuting.publicTransport) commuting.push("public_transport");
    if (transportation.commuting.fuelCar) commuting.push("fuel_car");
    if (transportation.commuting.electricCar) commuting.push("electric_car");

    const longDistance = [];
    if (transportation.longDistance.airplane) longDistance.push(`airplane_${transportation.longDistance.airplaneFrequency}`);
    if (transportation.longDistance.train) longDistance.push("train");
    if (transportation.longDistance.selfDriving) longDistance.push("self_driving");

    const additional = [];
    if (transportation.additional.carpool) additional.push("carpool");
    if (transportation.additional.remoteWork) additional.push("remote_work");

    return {
        commuting: commuting.join(","),
        long_distance: longDistance.join(","),
        additional: additional.join(",")
    };
};

// Helper function to get household energy summary for API
const getHouseholdEnergySummary = () => {
    const habits = [];
    if (household.habits.turnOff) habits.push("turn_off");
    if (household.habits.energySaving) habits.push("energy_saving");
    if (household.habits.noSpecial) habits.push("no_special");

    return {
        family_members: household.familyMembers,
        electricity_consumption: household.electricityConsumption,
        habits: habits.join(",")
    };
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

// Get impact text
const getImpactText = (level) => {
    switch (level) {
        case 1: return "Small";
        case 2: return "Medium";
        case 3: return "Large";
        default: return "Not specified";
    }
};

// Submit feedback
const submitFeedback = (isPositive) => {
    console.log(`User submitted ${isPositive ? 'positive' : 'negative'} feedback`);
    feedbackSubmitted.value = true;
};

// Get mock suggestions based on carbon level
const getMockSuggestions = (carbonLevel) => {
    // Common suggestions for all levels
    const commonSuggestions = {
        low: [
            {
                title: "Enhanced Water Conservation",
                content: "Install a smart water meter to track and further reduce household water usage. Many utilities offer rebates for these devices.",
                difficulty: 2,
                impact: 2,
                completed: false
            },
            {
                title: "Community Sustainability",
                content: "Start or join a neighborhood sustainability initiative to multiply your environmental impact through community action.",
                difficulty: 2,
                impact: 3,
                completed: false
            },
            {
                title: "Zero Waste Challenge",
                content: "Challenge yourself to a month of zero landfill waste by composting, recycling, and avoiding packaging waste completely.",
                difficulty: 3,
                impact: 2,
                completed: false
            },
            {
                title: "Biodiversity Garden",
                content: "Convert part of your yard to native plants that support local pollinators and wildlife. Research species suited to your region.",
                difficulty: 2,
                impact: 2,
                completed: false
            },
            {
                title: "Eco-Education",
                content: "Share your knowledge with friends and family. Host a workshop on sustainable practices you've mastered.",
                difficulty: 1,
                impact: 2,
                completed: false
            }
        ],
        medium: [
            {
                title: "Smart Home Energy",
                content: "Install a smart thermostat to optimize your home's energy use. Can reduce energy bills by 10-15% annually.",
                difficulty: 2,
                impact: 2,
                completed: false
            },
            {
                title: "Meatless Mondays",
                content: "Reduce your carbon footprint by avoiding meat one day a week. Plant-based meals typically have 1/3 the carbon impact.",
                difficulty: 1,
                impact: 2,
                completed: false
            },
            {
                title: "Transportation Alternatives",
                content: "Use public transportation, carpool, or cycle for your regular commute at least 2-3 days per week.",
                difficulty: 2,
                impact: 3,
                completed: false
            },
            {
                title: "Water Usage Reduction",
                content: "Install low-flow shower heads and faucet aerators to reduce water usage by up to 60% without sacrificing water pressure.",
                difficulty: 1,
                impact: 2,
                completed: false
            },
            {
                title: "Energy Audit",
                content: "Conduct a DIY home energy audit to identify energy waste. Focus on air leaks, insulation, and appliance efficiency.",
                difficulty: 2,
                impact: 2,
                completed: false
            }
        ],
        high: [
            {
                title: "Professional Energy Audit",
                content: "Schedule a professional home energy audit to identify major inefficiencies and prioritize improvements.",
                difficulty: 2,
                impact: 3,
                completed: false
            },
            {
                title: "Reduce Air Travel",
                content: "Cut your air travel by 50% and offset remaining flights. Consider train alternatives for shorter trips.",
                difficulty: 3,
                impact: 3,
                completed: false
            },
            {
                title: "Car-Free Commuting",
                content: "Switch to public transit, cycling, or walking for your daily commute. Start with 2-3 days per week.",
                difficulty: 2,
                impact: 3,
                completed: false
            },
            {
                title: "Energy-Efficient Appliances",
                content: "Replace your oldest, least efficient appliances with Energy Star models. Start with refrigerator and washing machine.",
                difficulty: 2,
                impact: 3,
                completed: false
            },
            {
                title: "Home Insulation Upgrade",
                content: "Improve wall and attic insulation to reduce heating/cooling costs by up to 20%. Focus on biggest air leak areas first.",
                difficulty: 3,
                impact: 3,
                completed: false
            }
        ]
    };

    return commonSuggestions[carbonLevel] || commonSuggestions.medium;
};
// Calculate energy points based on difficulty
const calculateEnergyPoints = (difficulty) => {
    switch (difficulty) {
        case 1: return 25; // simple task
        case 2: return 40; // medium task
        case 3: return 60; // hard task
        default: return 30;
    }
};

// Mark task as complete
const markTaskComplete = (suggestion) => {
    suggestion.completed = !suggestion.completed;

    // If the task is marked as completed, show the completion modal
    if (suggestion.completed) {
        completedTaskTitle.value = suggestion.title;
        earnedEnergy.value = calculateEnergyPoints(suggestion.difficulty);
        showCompletionModal.value = true;
    }
};
</script>

<style scoped>
.eco-action {
    max-width: 1000px;
    margin: 0 auto;
    padding: 20px;
}

.hero-section {
    width: 100%;
    background-size: cover;
    background-position: center;
    background-repeat: no-repeat;
    position: relative;
    padding: 40px 0;
    margin-bottom: 30px;
}

.header {
    text-align: center;
    margin-bottom: 30px;
}

.header h1 {
    color: white;
    margin-bottom: 15px;
    text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.7);
    font-size: 2.5rem;
    font-weight: bold;
    letter-spacing: 1px;
}

section {
    margin-bottom: 30px;
    padding: 20px;
    background-color: #f9f9f9;
    border-radius: var(--border-radius);
    box-shadow: var(--shadow);
}

.preference-select,
.sub-select {
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

.complete-button {
    padding: 6px 12px;
    border-radius: 4px;
    border: 1px solid #ccc;
    background-color: white;
    cursor: pointer;
    font-size: 14px;
    transition: all 0.2s ease;
}

.complete-button:hover {
    background-color: #f5f5f5;
}

.complete-button.completed {
    background-color: var(--primary-color);
    color: white;
    border-color: var(--primary-color);
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

.difficulty-level,
.impact-level {
    display: inline-block;
    padding: 3px 8px;
    border-radius: 4px;
    font-size: 14px;
    margin-top: 10px;
    margin-right: 10px;
}

.level-1 {
    background-color: #e8f5e9;
    color: #2e7d32;
}

.level-2 {
    background-color: #fff9c4;
    color: #f57f17;
}

.level-3 {
    background-color: #ffebee;
    color: #c62828;
}

.impact-1 {
    background-color: #e3f2fd;
    color: #1565c0;
}

.impact-2 {
    background-color: #e8eaf6;
    color: #3949ab;
}

.impact-3 {
    background-color: #ede7f6;
    color: #5e35b1;
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
    color: #2e7d32;
}

.feedback-button.negative {
    background-color: #ffebee;
    color: #c62828;
}

.feedback-thanks {
    margin-top: 10px;
    color: var(--primary-color);
}

.assessment-group {
    margin-bottom: 20px;
    padding: 15px;
    background-color: #fff;
    border-radius: 4px;
    box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
}

.assessment-group h3 {
    margin-top: 0;
    color: var(--primary-color);
    border-bottom: 1px solid #eee;
    padding-bottom: 8px;
}

.assessment-subgroup {
    margin-bottom: 15px;
}

.checkbox-group {
    display: flex;
    flex-wrap: wrap;
    gap: 10px;
    margin-top: 5px;
}

.checkbox-label {
    display: flex;
    align-items: center;
    gap: 5px;
    cursor: pointer;
}

.nested-option {
    margin-left: 25px;
    margin-top: 5px;
}

.action-button-container {
    display: flex;
    justify-content: center;
    margin-top: 20px;
}

.number-input {
    padding: 8px;
    border: 1px solid #ccc;
    border-radius: 4px;
    width: 100px;
}

.carbon-rating {
    text-align: center;
    padding: 20px;
    margin: 0 auto 20px;
    max-width: 500px;
    background-color: #f5f5f5;
    border-radius: 8px;
    box-shadow: var(--shadow);
}

.rating-label {
    font-size: 18px;
    margin-bottom: 10px;
}

.rating-value {
    font-size: 36px;
    font-weight: bold;
    margin-bottom: 15px;
    padding: 10px 20px;
    display: inline-block;
    border-radius: 4px;
}

.carbon-level-low {
    background-color: #e8f5e9;
    color: #2e7d32;
}

.carbon-level-medium {
    background-color: #fff8e1;
    color: #ff8f00;
}

.carbon-level-high {
    background-color: #ffebee;
    color: #c62828;
}

.rating-description {
    font-size: 16px;
    line-height: 1.4;
}

.footer {
    margin-top: 40px;
    padding-top: 20px;
    border-top: 1px solid #eee;
    color: var(--text-light);
    font-size: 14px;
    text-align: center;
}

.reference-value {
    margin-top: 5px;
    font-size: 0.9em;
    color: #666;
    font-style: italic;
}

.emoji {
    font-size: 1.2em;
    margin-left: 5px;
}

.suggestion-reason {
    font-style: italic;
    font-size: 0.9em;
    color: #666;
    margin-top: 5px;
    margin-bottom: 10px;
}

.modal {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background-color: rgba(0, 0, 0, 0.5);
    display: flex;
    justify-content: center;
    align-items: center;
    z-index: 1000;
}

.modal-content {
    background-color: white;
    padding: 20px;
    border-radius: 8px;
    box-shadow: 0 5px 15px rgba(0, 0, 0, 0.2);
    max-width: 500px;
    width: 90%;
    text-align: center;
}

.close-button {
    position: absolute;
    top: 10px;
    right: 10px;
    font-size: 24px;
    cursor: pointer;
    color: #999;
}

.completion-modal {
    position: relative;
    padding: 30px 20px;
}

.celebration-animation {
    margin-bottom: 20px;
}

.celebration-icon {
    font-size: 50px;
    animation: bounce 0.8s ease infinite alternate;
}

.energy-value {
    font-weight: bold;
    color: #ff9800;
    font-size: 1.2em;
}

.task-completed {
    margin-top: 10px;
    color: #666;
    font-style: italic;
}

@keyframes bounce {
    from {
        transform: translateY(0);
    }

    to {
        transform: translateY(-10px);
    }
}

.modal-enter-active,
.modal-leave-active {
    transition: opacity 0.3s;
}

.modal-enter-from,
.modal-leave-to {
    opacity: 0;
}

.step-indicator {
    display: flex;
    justify-content: space-between;
    margin-bottom: 2rem;
    position: relative;
}

.step-indicator::before {
    content: '';
    position: absolute;
    top: 15px;
    left: 0;
    right: 0;
    height: 2px;
    background-color: #e0e0e0;
    z-index: 1;
}

.step-indicator>div {
    position: relative;
    z-index: 2;
    display: flex;
    flex-direction: column;
    align-items: center;
    flex: 1;
    cursor: pointer;
}

.step-number {
    width: 30px;
    height: 30px;
    border-radius: 50%;
    background-color: #e0e0e0;
    color: #666;
    display: flex;
    align-items: center;
    justify-content: center;
    font-weight: bold;
    margin-bottom: 5px;
    transition: all 0.3s ease;
}

.step-title {
    font-size: 0.9rem;
    text-align: center;
    color: white;
    max-width: 100px;
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
    background-color: rgba(0, 0, 0, 0.5);
    text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.7);
}

.step-indicator>div.active .step-number {
    background-color: var(--primary-color);
    color: white;
}

.step-indicator>div.completed .step-number {
    background-color: #4caf50;
    color: white;
}

.step-indicator>div.active .step-title,
.step-indicator>div.completed .step-title {
    color: greenyellow;
    font-weight: 500;
}

.step-navigation {
    display: flex;
    justify-content: space-between;
    margin-top: 30px;
}

.nav-button {
    padding: 10px 20px;
    border-radius: 4px;
    cursor: pointer;
    font-size: 16px;
    transition: all 0.3s ease;
}

.prev-button {
    background-color: #f5f5f5;
    color: #333;
    border: 1px solid #ddd;
}

.prev-button:hover {
    background-color: #e0e0e0;
}

.next-button {
    background: linear-gradient(135deg, var(--primary-gradient-start), var(--primary-gradient-end));
    color: white;
    border: none;
}

.next-button:hover {
    background-color: var(--primary-gradient-end);
    box-shadow: 0 2px 5px rgba(0, 0, 0, 0.2);
}

.white-text {
    color: white;
}

@media (max-width: 768px) {
    .step-indicator {
        flex-wrap: wrap;
    }

    .step-indicator>div {
        flex: 0 0 50%;
        margin-bottom: 15px;
    }

    .step-title {
        font-size: 0.8rem;
    }

    .step-navigation {
        flex-direction: column;
        gap: 10px;
    }

    .nav-button {
        width: 100%;
    }
}

@media (max-width: 768px) {
    .checkbox-group {
        flex-direction: column;
        align-items: flex-start;
    }

    .suggestions-container {
        grid-template-columns: 1fr;
    }
}
</style>
