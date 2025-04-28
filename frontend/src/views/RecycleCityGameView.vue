<template>
    <div class="game-container">
        <div class="game-header">
            <router-link to="/resources/kids-learning" class="back-button">← Back to Climate Kids Corner</router-link>
        </div>
        <iframe src="/games/recyclecity/index.htm" width="1024px" height="700px" frameborder="0"
            allowfullscreen></iframe>
    </div>
</template>

<style scoped>
.game-container {
    width: 100%;
    margin: 20px auto;
    background: white;
    border-radius: 10px;
    box-shadow: 0 5px 15px rgba(0, 0, 0, 0.1);
    overflow: hidden;
}

.game-header {
    background: linear-gradient(135deg, #9DDCFF 0%, #AEF78E 100%);
    padding: 15px;
    text-align: left;
}

.back-button {
    color: #2C3E50;
    font-weight: bold;
    text-decoration: none;
    font-size: 16px;
    transition: color 0.3s;
    font-family: 'Comic Sans MS', 'Chalkboard SE', 'Marker Felt', sans-serif;
}

.back-button:hover {
    color: #FF8A5B;
}

iframe {
    border: none;
    display: block;
}
</style>