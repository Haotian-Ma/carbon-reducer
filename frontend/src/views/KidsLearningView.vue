<template>
  <div class="kids-climate-container">
    <!-- Hero Section -->
    <div class="hero-section">
      <div class="container">
        <h1 class="text-center">Climate Kids Corner</h1>
        <p class="text-center hero-subtitle">Join us on an adventure to learn about our planet and how we can protect it!</p>
      </div>
    </div>

    <!-- Main Content -->
    <div class="container mt-4">
      <!-- Introduction -->
      <div class="row mb-5">
        <div class="col-lg-8 offset-lg-2">
          <div class="intro-card">
            <h2>Hey Climate Explorers! 🌍</h2>
            <p>Our planet Earth is amazing! It's home to millions of plants, animals, and of course, us! But our planet is changing because of something called <strong>climate change</strong>.</p>
            <p>Climate change means that Earth is getting warmer, and that can cause problems for all living things. But don't worry! By learning about climate change, you can become a Planet Protector and help make a difference!</p>
          </div>
        </div>
      </div>

      <!-- Interactive Resources -->
      <h2 class="section-title text-center mb-4">Fun Learning Activities</h2>
      
      <div class="row resource-cards">
        <!-- Card 1 -->
        <div class="col-md-6 col-lg-3 mb-4">
          <div class="resource-card">
            <div class="card-image-container">
              <img src="https://placehold.co/600x400/9DDCFF/333333?text=Card+Game" alt="Nature's Benefits Card Game" class="card-img">
            </div>
            <div class="card-content">
              <h3>Nature's Benefits Card Game(Age: 11-18)</h3>
              <p>Play a fun card game to learn how nature helps us every day! Match the cards and discover nature's superpowers.</p>
              <div class="button-container">
                <a href="https://www.epa.gov/eco-research/natures-benefits-card-game" target="_blank" class="resource-button">Play Now</a>
              </div>
            </div>
          </div>
        </div>

        <!-- Card 2 -->
        <div class="col-md-6 col-lg-3 mb-4">
          <div class="resource-card">
            <div class="card-image-container">
              <img src="https://placehold.co/600x400/FFCE87/333333?text=Virtual+Tour" alt="Indoor Air Quality House" class="card-img">
            </div>
            <div class="card-content">
              <h3>Indoor Air Quality House(Age: 6-12)</h3>
              <p>Take a virtual tour inside a house and find out how to keep the air clean and healthy for everyone!</p>
              <div class="button-container">
                <a href="https://www.epa.gov/indoor-air-quality-iaq/interactive-tour-indoor-air-quality-demo-house" target="_blank" class="resource-button">Explore</a>
              </div>
            </div>
          </div>
        </div>

        <!-- Card 3 -->
        <div class="col-md-6 col-lg-3 mb-4">
          <div class="resource-card">
            <div class="card-image-container">
              <img src="https://placehold.co/600x400/AEF78E/333333?text=Climate+Evidence" alt="Climate Change Evidence" class="card-img">
            </div>
            <div class="card-content">
              <h3>Climate Change Detectives(Age: 8-13)</h3>
              <p>Become a science detective and discover the evidence that shows our climate is changing. What clues can you find?</p>
              <div class="button-container">
                <a href="https://climatekids.nasa.gov/climate-change-evidence/" target="_blank" class="resource-button">Investigate</a>
              </div>
            </div>
          </div>
        </div>

        <!-- Card 4 -->
        <div class="col-md-6 col-lg-3 mb-4">
          <div class="resource-card">
            <div class="card-image-container">
              <img src="https://placehold.co/600x400/FFA7A7/333333?text=Clean+Buses" alt="Clean School Bus" class="card-img">
            </div>
            <div class="card-content">
              <h3>Clean School Bus Adventure(Age: 3-10)</h3>
              <p>Learn about clean school buses that help reduce pollution! Find out how your school can get involved.</p>
              <div class="button-container">
                <a href="https://www.epa.gov/cleanschoolbus/resources-engage-your-community" target="_blank" class="resource-button">Learn More</a>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Fun Facts Section -->
      <div class="fun-facts-section mt-5">
        <h2 class="section-title text-center mb-4">Cool Climate Facts</h2>
        
        <div class="row">
          <div class="col-md-4 mb-4">
            <div class="fact-bubble fact-bubble-1">
              <p>Did you know that trees are like nature's air filters? They absorb carbon dioxide (a greenhouse gas) and release oxygen that we breathe!</p>
            </div>
          </div>
          
          <div class="col-md-4 mb-4">
            <div class="fact-bubble fact-bubble-2">
              <p>Polar bears are amazing swimmers, but they need ice to rest and hunt. As the Arctic ice melts due to climate change, polar bears have to swim longer distances!</p>
            </div>
          </div>
          
          <div class="col-md-4 mb-4">
            <div class="fact-bubble fact-bubble-3">
              <p>The energy from the sun that reaches Earth in just one hour could power the entire world for a whole year! That's why solar power is so important.</p>
            </div>
          </div>
        </div>
      </div>

      <!-- What You Can Do Section -->
      <div class="action-section mt-5 mb-5">
        <h2 class="section-title text-center mb-4">Be a Planet Protector!</h2>
        
        <div class="row">
          <div class="col-lg-8 offset-lg-2">
            <div class="action-card">
              <h3 class="text-center">Here are 5 super easy ways YOU can help:</h3>
              
              <ol class="action-list">
                <li>Turn off lights when you leave a room to save energy</li>
                <li>Use reusable water bottles instead of plastic ones</li>
                <li>Walk, bike, or take the bus when possible</li>
                <li>Plant flowers or trees that help butterflies and bees</li>
                <li>Tell your friends and family what you've learned about climate change</li>
              </ol>
              
              <div class="text-center mt-4">
                <a href="/eco-action" class="pledge-button">I Pledge to Help Our Planet!</a>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
// No script needed for now
</script>

<style>
/* Main Styles */
.kids-climate-container {
  font-family: 'Comic Sans MS', 'Chalkboard SE', 'Marker Felt', sans-serif;
  color: #333;
}

/* Hero Section */
.hero-section {
  background: linear-gradient(135deg, #9DDCFF 0%, #AEF78E 100%);
  padding: 3rem 0;
  border-radius: 0 0 30px 30px;
  margin-bottom: 2rem;
}

.hero-section h1 {
  font-size: 3rem;
  color: #2C3E50;
  margin-bottom: 1rem;
  font-weight: bold;
  text-shadow: 2px 2px 0px rgba(255, 255, 255, 0.5);
}

.hero-subtitle {
  font-size: 1.4rem;
  color: #2C3E50;
}

/* Section Titles */
.section-title {
  color: #2C3E50;
  font-weight: bold;
  font-size: 2.2rem;
  text-shadow: 1px 1px 0px rgba(0, 0, 0, 0.1);
}

/* Intro Card */
.intro-card {
  background-color: #FFFDDE;
  border-radius: 20px;
  padding: 2rem;
  box-shadow: 0 5px 15px rgba(0, 0, 0, 0.1);
  border: 3px dashed #FFCE87;
}

.intro-card h2 {
  color: #FF8A5B;
  margin-bottom: 1rem;
  font-size: 2rem;
}

.intro-card p {
  font-size: 1.2rem;
  line-height: 1.6;
}

/* Resource Cards */
.resource-cards {
  margin-top: 1rem;
}

.resource-card {
  background-color: white;
  border-radius: 15px;
  overflow: hidden;
  box-shadow: 0 5px 15px rgba(0, 0, 0, 0.1);
  height: 100%;
  display: flex;
  flex-direction: column;
  transition: transform 0.3s ease, box-shadow 0.3s ease;
}

.resource-card:hover {
  transform: translateY(-10px);
  box-shadow: 0 10px 25px rgba(0, 0, 0, 0.15);
}

.card-image-container {
  height: 180px;
  overflow: hidden;
}

.card-img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  transition: transform 0.3s ease;
}

.resource-card:hover .card-img {
  transform: scale(1.05);
}

.card-content {
  padding: 1.5rem;
  display: flex;
  flex-direction: column;
  flex-grow: 1;
}

.card-content h3 {
  color: #2C3E50;
  font-size: 1.3rem;
  margin-bottom: 0.8rem;
}

.card-content p {
  color: #666;
  font-size: 1rem;
  margin-bottom: 1.5rem;
  flex-grow: 1;
}

.button-container {
  margin-top: auto;
  text-align: center;
}

.resource-button {
  display: inline-block;
  background-color: #FF8A5B;
  color: white;
  padding: 8px 20px;
  border-radius: 30px;
  text-decoration: none;
  font-weight: bold;
  transition: background-color 0.3s ease, transform 0.3s ease;
}

.resource-button:hover {
  background-color: #FF6B35;
  transform: scale(1.05);
  text-decoration: none;
  color: white;
}

/* Fun Facts Section */
.fun-facts-section {
  padding: 2rem 0;
}

.fact-bubble {
  border-radius: 30px;
  padding: 1.5rem;
  height: 100%;
  box-shadow: 0 5px 15px rgba(0, 0, 0, 0.1);
}

.fact-bubble p {
  font-size: 1.1rem;
  line-height: 1.5;
  margin: 0;
}

.fact-bubble-1 {
  background-color: #DFF6FF;
  border: 3px solid #9DDCFF;
}

.fact-bubble-2 {
  background-color: #FFF3EB;
  border: 3px solid #FFCE87;
}

.fact-bubble-3 {
  background-color: #F0FFE6;
  border: 3px solid #AEF78E;
}

/* Action Section */
.action-section {
  padding: 2rem 0;
}

.action-card {
  background-color: #FFF0F0;
  border-radius: 20px;
  padding: 2rem;
  box-shadow: 0 5px 15px rgba(0, 0, 0, 0.1);
  border: 3px dashed #FFA7A7;
}

.action-card h3 {
  color: #FF6B6B;
  margin-bottom: 1.5rem;
  font-size: 1.5rem;
}

.action-list {
  padding-left: 2rem;
  margin-bottom: 1rem;
}

.action-list li {
  font-size: 1.2rem;
  padding: 0.5rem 0;
  color: #555;
}

.pledge-button {
  display: inline-block;
  background-color: #4CAF50;
  color: white;
  padding: 12px 30px;
  border-radius: 30px;
  font-size: 1.2rem;
  text-decoration: none;
  font-weight: bold;
  transition: background-color 0.3s ease, transform 0.3s ease;
  box-shadow: 0 3px 10px rgba(0, 0, 0, 0.2);
}

.pledge-button:hover {
  background-color: #3E8E41;
  transform: scale(1.05);
  text-decoration: none;
  color: white;
}

/* Responsive Adjustments */
@media (max-width: 768px) {
  .hero-section h1 {
    font-size: 2.5rem;
  }
  
  .hero-subtitle {
    font-size: 1.2rem;
  }
  
  .section-title {
    font-size: 1.8rem;
  }
  
  .intro-card h2 {
    font-size: 1.7rem;
  }
  
  .intro-card p {
    font-size: 1.1rem;
  }
  
  .action-list li {
    font-size: 1.1rem;
  }
}
</style>