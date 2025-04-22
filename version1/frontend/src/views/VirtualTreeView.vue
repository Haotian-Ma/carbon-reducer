<template>
    <div class="container mt-5">
        <div class="row">
            <div class="col-md-12 offset-md-0">
                <section class="about-us">
                    <h2 class="text-center">Virtual Tree</h2>
                    <div class="animation-container">
                        <div ref="animationContainer" class="lottie-animation"></div>
                    </div>
                </section>
            </div>
        </div>
    </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue';
import lottie from 'lottie-web';

const animationContainer = ref(null);
let animation = null;
onMounted(async () => {
    try {
        
        const animationData = await import('../assets/animations/virtual-tree-animation.json');
        
        if (animationContainer.value) {
           
            animation = lottie.loadAnimation({
                container: animationContainer.value,
                renderer: 'svg',
                loop: true,
                autoplay: true,
                animationData: animationData.default || animationData
            });
        }
    } catch (error) {
        console.error('Error', error);
    }
});

onUnmounted(() => {
    if (animation) {
        animation.destroy();
    }
});
</script>

<style>
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
</style>