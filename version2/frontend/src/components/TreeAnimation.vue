<!-- LottieAnimation.vue -->
<template>
  <div ref="animationContainer" class="lottie-container"></div>
</template>

<script setup>
import { ref, onMounted, onUnmounted, watch } from 'vue';
import lottie from 'lottie-web';

const props = defineProps({
  animationData: {
    type: Object,
    required: true
  },
  loop: {
    type: Boolean,
    default: true
  },
  autoplay: {
    type: Boolean,
    default: true
  },
  speed: {
    type: Number,
    default: 1
  },
  width: {
    type: String,
    default: '100%'
  },
  height: {
    type: String,
    default: '100%'
  }
});

const animationContainer = ref(null);
let animation = null;

onMounted(() => {
  if (animationContainer.value) {
    animation = lottie.loadAnimation({
      container: animationContainer.value,
      renderer: 'svg',
      loop: props.loop,
      autoplay: props.autoplay,
      animationData: props.animationData
    });
    
    animation.setSpeed(props.speed);
  }
});

watch(() => props.animationData, (newData) => {
  if (animation) {
    animation.destroy();
  }
  
  if (animationContainer.value) {
    animation = lottie.loadAnimation({
      container: animationContainer.value,
      renderer: 'svg',
      loop: props.loop,
      autoplay: props.autoplay,
      animationData: newData
    });
    
    animation.setSpeed(props.speed);
  }
}, { deep: true });

watch(() => props.speed, (newSpeed) => {
  if (animation) {
    animation.setSpeed(newSpeed);
  }
});

watch(() => props.loop, (newLoop) => {
  if (animation) {
    animation.loop = newLoop;
  }
});

onUnmounted(() => {
  if (animation) {
    animation.destroy();
  }
});
</script>

<style scoped>
.lottie-container {
  display: block;
  position: relative;
  width: v-bind('width');
  height: v-bind('height');
  overflow: hidden;
}
</style>