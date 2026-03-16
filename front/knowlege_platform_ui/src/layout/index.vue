<template>
  <div class="app-wrapper">
    <canvas ref="particleCanvas" class="particle-canvas"></canvas>

    <div class="sidebar glass-panel tech-corners">
      <div class="logo">
        <div class="logo-icon">
          <div class="inner-spin"></div>
        </div>
        <span class="logo-text">ITS NEURAL</span>
      </div>
      
      <div class="sidebar-stats">
        <div class="stat-item">
          <span>SYSTEM STATUS</span>
          <span class="status-ok">ONLINE</span>
        </div>
        <div class="stat-item">
          <span>LATENCY</span>
          <span class="text-blue">12ms</span>
        </div>
      </div>

      <el-menu :default-active="activeMenu" class="custom-menu" router>
        <el-menu-item index="/knowledge" class="menu-item">
          <el-icon><Files /></el-icon>
          <span>知识节点库</span>
        </el-menu-item>
        <el-menu-item index="/chat" class="menu-item">
          <el-icon><ChatDotRound /></el-icon>
          <span>智能交互中枢</span>
        </el-menu-item>
      </el-menu>

      <div class="sidebar-footer">
        <div class="grid-deco"></div>
        <span>v2.0.4.build.109</span>
      </div>
    </div>

    <div class="main-container">
      <router-view v-slot="{ Component }">
        <transition name="hologram-transform" mode="out-in">
          <component :is="Component" />
        </transition>
      </router-view>
    </div>
  </div>
</template>

<script setup>
import { computed, ref, onMounted, onBeforeUnmount } from 'vue'
import { useRoute } from 'vue-router'
import { Files, ChatDotRound } from '@element-plus/icons-vue'

const route = useRoute()
const activeMenu = computed(() => route.path)

// ====== Canvas 粒子群引擎逻辑 ======
const particleCanvas = ref(null)
let ctx = null
let particles = []
let animationFrameId = null
let mouse = { x: null, y: null, radius: 150 }

const initParticles = () => {
  const canvas = particleCanvas.value
  ctx = canvas.getContext('2d')
  
  const resize = () => {
    canvas.width = window.innerWidth
    canvas.height = window.innerHeight
  }
  window.addEventListener('resize', resize)
  resize()

  window.addEventListener('mousemove', (event) => {
    mouse.x = event.x
    mouse.y = event.y
  })
  window.addEventListener('mouseout', () => {
    mouse.x = undefined
    mouse.y = undefined
  })

  class Particle {
    constructor(x, y, dx, dy, size) {
      this.x = x; this.y = y; this.dx = dx; this.dy = dy; this.size = size;
    }
    draw() {
      ctx.beginPath()
      ctx.arc(this.x, this.y, this.size, 0, Math.PI * 2, false)
      ctx.fillStyle = 'rgba(0, 240, 255, 0.8)'
      ctx.fill()
    }
    update() {
      if (this.x > canvas.width || this.x < 0) this.dx = -this.dx
      if (this.y > canvas.height || this.y < 0) this.dy = -this.dy

      // 鼠标交互：轻微的排斥与吸引
      if (mouse.x && mouse.y) {
        let dx = mouse.x - this.x
        let dy = mouse.y - this.y
        let distance = Math.sqrt(dx * dx + dy * dy)
        if (distance < mouse.radius) {
          this.x -= dx * 0.01
          this.y -= dy * 0.01
        }
      }

      this.x += this.dx
      this.y += this.dy
      this.draw()
    }
  }

  const createParticles = () => {
    particles = []
    let numberOfParticles = (canvas.width * canvas.height) / 9000 // 根据屏幕大小计算粒子数
    for (let i = 0; i < numberOfParticles; i++) {
      let size = (Math.random() * 1.5) + 0.5
      let x = (Math.random() * ((canvas.width - size * 2) - (size * 2)) + size * 2)
      let y = (Math.random() * ((canvas.height - size * 2) - (size * 2)) + size * 2)
      let dx = (Math.random() - 0.5) * 0.5
      let dy = (Math.random() - 0.5) * 0.5
      particles.push(new Particle(x, y, dx, dy, size))
    }
  }

  const animate = () => {
    requestAnimationFrame(animate)
    ctx.clearRect(0, 0, canvas.width, canvas.height)
    
    for (let i = 0; i < particles.length; i++) {
      particles[i].update()
    }
    connect()
  }

  // 连线逻辑
  const connect = () => {
    let opacityValue = 1
    for (let a = 0; a < particles.length; a++) {
      for (let b = a; b < particles.length; b++) {
        let distance = ((particles[a].x - particles[b].x) * (particles[a].x - particles[b].x))
                     + ((particles[a].y - particles[b].y) * (particles[a].y - particles[b].y))
        if (distance < (canvas.width / 10) * (canvas.height / 10)) {
          opacityValue = 1 - (distance / 10000)
          ctx.strokeStyle = `rgba(0, 240, 255, ${opacityValue * 0.2})`
          ctx.lineWidth = 1
          ctx.beginPath()
          ctx.moveTo(particles[a].x, particles[a].y)
          ctx.lineTo(particles[b].x, particles[b].y)
          ctx.stroke()
        }
      }
    }
  }

  createParticles()
  animate()
}

onMounted(() => {
  initParticles()
})

onBeforeUnmount(() => {
  cancelAnimationFrame(animationFrameId)
})
</script>

<style lang="scss" scoped>
.app-wrapper {
  display: flex; height: 100vh; width: 100vw; position: relative;
}

.particle-canvas {
  position: absolute; top: 0; left: 0; width: 100%; height: 100%; z-index: 0; pointer-events: none;
  background: radial-gradient(circle at center, #0a1118 0%, #030406 100%);
}

.glass-panel {
  background: var(--glass-bg);
  backdrop-filter: blur(12px);
  -webkit-backdrop-filter: blur(12px);
  border-right: 1px solid var(--glass-border);
}

.sidebar {
  width: 260px; display: flex; flex-direction: column; z-index: 10;
  box-shadow: inset -1px 0 0 rgba(0, 240, 255, 0.1), 5px 0 20px rgba(0,0,0,0.5);

  .logo {
    height: 80px; display: flex; align-items: center; padding: 0 20px;
    border-bottom: 1px solid var(--glass-border);
    background: rgba(0, 240, 255, 0.03);
    
    .logo-icon {
      width: 24px; height: 24px; border: 2px solid var(--neon-blue); margin-right: 12px;
      position: relative; transform: rotate(45deg);
      .inner-spin {
        position: absolute; top: 4px; left: 4px; width: 12px; height: 12px;
        background: var(--neon-purple); animation: spin 2s linear infinite;
      }
    }
    
    .logo-text {
      font-size: 18px; font-weight: 900; font-family: 'Courier New', monospace;
      color: var(--text-main); letter-spacing: 2px;
    }
  }

  .sidebar-stats {
    padding: 15px 20px; border-bottom: 1px dashed rgba(255,255,255,0.1);
    font-family: monospace; font-size: 12px;
    .stat-item { display: flex; justify-content: space-between; margin-bottom: 5px; color: var(--text-muted); }
    .status-ok { color: var(--neon-green); text-shadow: 0 0 5px var(--neon-green); }
    .text-blue { color: var(--neon-blue); }
  }

  .custom-menu {
    border-right: none; background: transparent; padding: 15px 10px; flex: 1;

    .menu-item {
      border-radius: 4px; margin-bottom: 5px; color: var(--text-muted);
      border-left: 3px solid transparent; transition: all 0.2s;

      &:hover { background: rgba(0, 240, 255, 0.05); color: #fff; }
      &.is-active {
        background: linear-gradient(90deg, rgba(0,240,255,0.15) 0%, transparent 100%);
        color: var(--neon-blue); border-left-color: var(--neon-blue);
      }
    }
  }

  .sidebar-footer {
    padding: 15px; font-family: monospace; font-size: 11px; color: #555;
    border-top: 1px solid var(--glass-border); text-align: right;
  }
}

.main-container { flex: 1; padding: 25px; overflow-y: auto; z-index: 10; position: relative; }

@keyframes spin { 100% { transform: rotate(360deg); } }

.hologram-transform-enter-active, .hologram-transform-leave-active { transition: all 0.3s cubic-bezier(0.25, 0.8, 0.25, 1); }
.hologram-transform-enter-from { opacity: 0; transform: scale(0.99) translateY(10px); }
.hologram-transform-leave-to { opacity: 0; transform: scale(0.99) translateY(-10px); }
</style>