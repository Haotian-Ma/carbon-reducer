<template>
    <div class="tree-container">
        <svg class="tree-svg" viewBox="0 0 400 500" xmlns="http://www.w3.org/2000/svg">
            <!-- 地面 -->
            <path d="M0,480 L400,480" stroke="brown" stroke-width="5" />

            <!-- 树干 -->
            <path class="tree-trunk"
                d="M200,480 L200,400 Q200,350 190,320 Q180,290 200,260 Q220,230 210,200 Q230,160 200,120" stroke="brown"
                stroke-width="15" fill="none" stroke-dasharray="1000" stroke-dashoffset="1000" />

            <!-- 小枝干 -->
            <path class="tree-branch branch-1" d="M200,380 Q230,370 260,385" stroke="brown" stroke-width="8" fill="none"
                stroke-dasharray="500" stroke-dashoffset="500" />

            <path class="tree-branch branch-2" d="M200,330 Q170,310 150,325" stroke="brown" stroke-width="6" fill="none"
                stroke-dasharray="500" stroke-dashoffset="500" />

            <path class="tree-branch branch-3" d="M200,260 Q230,240 245,255" stroke="brown" stroke-width="5" fill="none"
                stroke-dasharray="500" stroke-dashoffset="500" />

            <path class="tree-branch branch-4" d="M200,210 Q170,190 140,200" stroke="brown" stroke-width="4" fill="none"
                stroke-dasharray="500" stroke-dashoffset="500" />

            <!-- 树叶组 -->
            <g class="leaf-group leaf-group-1">
                <circle cx="260" cy="385" r="0" fill="#54a05c" class="leaf" />
                <circle cx="270" cy="375" r="0" fill="#54a05c" class="leaf" />
                <circle cx="255" cy="370" r="0" fill="#54a05c" class="leaf" />
            </g>

            <g class="leaf-group leaf-group-2">
                <circle cx="150" cy="325" r="0" fill="#54a05c" class="leaf" />
                <circle cx="140" cy="315" r="0" fill="#54a05c" class="leaf" />
                <circle cx="160" cy="310" r="0" fill="#54a05c" class="leaf" />
            </g>

            <g class="leaf-group leaf-group-3">
                <circle cx="245" cy="255" r="0" fill="#54a05c" class="leaf" />
                <circle cx="255" cy="245" r="0" fill="#54a05c" class="leaf" />
                <circle cx="240" cy="235" r="0" fill="#54a05c" class="leaf" />
            </g>

            <g class="leaf-group leaf-group-4">
                <circle cx="140" cy="200" r="0" fill="#54a05c" class="leaf" />
                <circle cx="130" cy="190" r="0" fill="#54a05c" class="leaf" />
                <circle cx="150" cy="180" r="0" fill="#54a05c" class="leaf" />
            </g>

            <!-- 顶部树冠 -->
            <g class="crown">
                <circle cx="200" cy="120" r="0" fill="#307338" class="crown-center" />
                <circle cx="170" cy="110" r="0" fill="#307338" class="crown-part" />
                <circle cx="230" cy="110" r="0" fill="#307338" class="crown-part" />
                <circle cx="200" cy="90" r="0" fill="#307338" class="crown-part" />
                <circle cx="180" cy="70" r="0" fill="#54a05c" class="crown-part" />
                <circle cx="220" cy="70" r="0" fill="#54a05c" class="crown-part" />
                <circle cx="200" cy="50" r="0" fill="#54a05c" class="crown-part" />
            </g>

            <!-- 小花点缀 -->
            <g class="flowers">
                <circle cx="210" cy="80" r="0" fill="#ff7eb9" class="flower" />
                <circle cx="240" cy="100" r="0" fill="#ff7eb9" class="flower" />
                <circle cx="160" cy="100" r="0" fill="#ff7eb9" class="flower" />
                <circle cx="190" cy="60" r="0" fill="#ff7eb9" class="flower" />
            </g>

            <!-- 太阳 -->
            <circle cx="50" cy="50" r="30" fill="#ffeb3b" class="sun">
                <animate attributeName="opacity" values="0.7;1;0.7" dur="5s" repeatCount="indefinite" />
            </circle>

            <!-- 云朵 -->
            <g class="cloud" opacity="0">
                <ellipse cx="320" cy="60" rx="25" ry="15" fill="white" />
                <ellipse cx="340" cy="50" rx="20" ry="13" fill="white" />
                <ellipse cx="300" cy="50" rx="20" ry="10" fill="white" />
            </g>
        </svg>

        <div class="controls">
            <button @click="startAnimation" :disabled="isAnimating">生长</button>
            <button @click="resetAnimation" :disabled="!hasGrown">重置</button>
        </div>
    </div>
</template>

<script>
export default {
    name: 'TreeGrowthAnimation',
    data() {
        return {
            isAnimating: false,
            hasGrown: false
        }
    },
    methods: {
        startAnimation() {
            if (this.isAnimating) return;

            this.isAnimating = true;

            // 延迟结束后将状态改为已生长
            setTimeout(() => {
                this.isAnimating = false;
                this.hasGrown = true;
            }, 8000); // 动画总时长
        },
        resetAnimation() {
            // 移除动画类
            document.querySelector('.tree-container').classList.remove('animate');

            // 强制回流
            void document.querySelector('.tree-container').offsetWidth;

            this.hasGrown = false;
        }
    },
    watch: {
        isAnimating(newVal) {
            if (newVal) {
                document.querySelector('.tree-container').classList.add('animate');
            }
        }
    }
}
</script>

<style scoped>
.tree-container {
    display: flex;
    flex-direction: column;
    align-items: center;
    width: 100%;
    max-width: 500px;
    margin: 0 auto;
    background-color: #e6f7ff;
    border-radius: 12px;
    padding: 20px;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.tree-svg {
    width: 100%;
    height: auto;
    max-height: 80vh;
}

.controls {
    margin-top: 20px;
    display: flex;
    gap: 16px;
}

button {
    padding: 10px 24px;
    background-color: #4CAF50;
    color: white;
    border: none;
    border-radius: 6px;
    cursor: pointer;
    font-size: 16px;
    transition: background-color 0.3s;
}

button:hover:not(:disabled) {
    background-color: #388E3C;
}

button:disabled {
    background-color: #9E9E9E;
    cursor: not-allowed;
}

/* 动画相关样式 */
.tree-trunk,
.tree-branch {
    stroke-linecap: round;
    transition: stroke-dashoffset 2s ease-in-out;
}

.leaf,
.crown-center,
.crown-part {
    transition: r 2s ease-out;
}

.cloud {
    transition: opacity 2s ease-in-out;
}

.tree-container.animate .tree-trunk {
    stroke-dashoffset: 0;
}

.tree-container.animate .branch-1 {
    stroke-dashoffset: 0;
    transition-delay: 1s;
}

.tree-container.animate .branch-2 {
    stroke-dashoffset: 0;
    transition-delay: 1.5s;
}

.tree-container.animate .branch-3 {
    stroke-dashoffset: 0;
    transition-delay: 2s;
}

.tree-container.animate .branch-4 {
    stroke-dashoffset: 0;
    transition-delay: 2.5s;
}

.tree-container.animate .leaf-group-1 .leaf {
    r: 10;
    transition-delay: 1.5s;
}

.tree-container.animate .leaf-group-2 .leaf {
    r: 8;
    transition-delay: 2s;
}

.tree-container.animate .leaf-group-3 .leaf {
    r: 7;
    transition-delay: 2.5s;
}

.tree-container.animate .leaf-group-4 .leaf {
    r: 6;
    transition-delay: 3s;
}

.tree-container.animate .crown-center {
    r: 40;
    transition-delay: 3.5s;
}

.tree-container.animate .crown-part {
    r: 30;
    transition-delay: 4s;
}

.tree-container.animate .flower {
    r: 5;
    transition: r 1s ease-out;
    transition-delay: 5s;
}

.tree-container.animate .cloud {
    opacity: 0.8;
    transition-delay: 6s;
}

.flowers .flower {
    animation: pulse 3s infinite alternate;
    animation-play-state: paused;
}

.tree-container.animate .flowers .flower {
    animation-play-state: running;
}

@keyframes pulse {
    0% {
        transform: scale(1);
    }

    100% {
        transform: scale(1.2);
    }
}

.sun {
    animation: rise 12s linear infinite;
    animation-play-state: paused;
}

.tree-container.animate .sun {
    animation-play-state: running;
}

@keyframes rise {
    0% {
        transform: translateY(0);
    }

    50% {
        transform: translateY(-20px);
    }

    100% {
        transform: translateY(0);
    }
}
</style>
