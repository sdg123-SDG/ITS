<template>
  <div class="chat-wrapper">
    <div class="model-dashboard glass-card tech-corners">
      <div class="dash-header">PARAMS</div>
      <div class="dash-block">
        <div class="dash-label">CORE_TMP</div>
        <div class="dash-value text-green">42.1°C</div>
        <div class="progress-bar"><div class="fill" style="width: 42%"></div></div>
      </div>
      <div class="dash-block">
        <div class="dash-label">TOKEN_USE</div>
        <div class="dash-value text-blue">14,204 / 32K</div>
        <div class="progress-bar"><div class="fill" style="width: 45%; background: var(--neon-blue)"></div></div>
      </div>
      <div class="dash-block">
        <div class="dash-label">RAG_STATE</div>
        <div class="dash-value text-purple">ACTIVE</div>
        <div class="radar-scan"></div>
      </div>
    </div>

    <div class="chat-container">
      <div class="chat-box glass-card tech-corners">
        <div class="top-deco-line"></div>
        <div class="messages" ref="messagesRef">
          <div v-if="messages.length === 0" class="empty-state">
            <div class="hex-grid-bg"></div>
            <div class="ai-core-icon">
              <div class="core-ring"></div>
              <el-icon :size="40" color="#00f0ff"><ChatDotRound /></el-icon>
            </div>
            <p class="greeting-text">等待指令输入 // AWAITING INPUT</p>
          </div>
          
          <div 
            v-for="(msg, index) in messages" 
            :key="index" 
            class="message-item"
            :class="msg.role"
          >
            <div class="avatar-wrap">
              <el-avatar class="tech-avatar" :icon="msg.role === 'user' ? 'User' : 'Service'" />
            </div>
            <div class="content">
              <div class="bubble tech-bubble">
                <div v-if="msg.loading" class="cyber-typing">
                  <span></span><span></span><span></span>
                </div>
                <div v-else class="md-content" v-html="formatContent(msg.content)"></div>
              </div>
            </div>
          </div>
        </div>
        
        <div class="input-area glass-input-area">
          <el-input
            v-model="input"
            placeholder="[输入指令]..."
            :rows="3"
            type="textarea"
            resize="none"
            class="cyber-input"
            @keydown.enter.prevent="handleSend"
          />
          <el-button type="primary" class="cyber-btn" @click="handleSend" :loading="loading" :disabled="!input.trim()">
            <el-icon><Position /></el-icon> <span>EXEC</span>
          </el-button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, nextTick } from 'vue'
import { queryKnowledge } from '@/api/knowledge'
import { User, Service, Position, ChatDotRound } from '@element-plus/icons-vue'
import { marked } from 'marked'

const input = ref('')
const loading = ref(false)
const messages = ref([])
const messagesRef = ref(null)

const scrollToBottom = () => {
  nextTick(() => {
    if (messagesRef.value) {
      messagesRef.value.scrollTop = messagesRef.value.scrollHeight
    }
  })
}

const formatContent = (text) => marked(text)

const handleSend = async () => {
  if (!input.value.trim() || loading.value) return
  
  const question = input.value
  input.value = ''
  
  messages.value.push({ role: 'user', content: question })
  scrollToBottom()
  
  loading.value = true
  messages.value.push({ role: 'assistant', content: '', loading: true })
  scrollToBottom()
  
  try {
    const res = await queryKnowledge({ question })
    const botMsg = messages.value[messages.value.length - 1]
    botMsg.loading = false
    botMsg.content = res.answer
  } catch (error) {
    const botMsg = messages.value[messages.value.length - 1]
    botMsg.loading = false
    botMsg.content = 'SYS_ERR: 连接中止。'
  } finally {
    loading.value = false
    scrollToBottom()
  }
}
</script>

<style lang="scss" scoped>
.chat-wrapper {
  display: flex; gap: 20px; height: calc(100vh - 50px);
}

.glass-card {
  background: var(--glass-bg); backdrop-filter: blur(10px);
  border: 1px solid var(--glass-border); box-shadow: var(--glass-shadow);
}

/* 侧边仪表盘 */
.model-dashboard {
  width: 220px; display: flex; flex-direction: column; padding: 20px;
  background: rgba(10, 14, 23, 0.8);
  .dash-header { font-family: monospace; color: #fff; border-bottom: 1px solid rgba(255,255,255,0.1); padding-bottom: 10px; margin-bottom: 20px; font-weight: bold;}
  .dash-block { margin-bottom: 25px; }
  .dash-label { font-size: 11px; color: var(--text-muted); font-family: monospace; margin-bottom: 5px; }
  .dash-value { font-size: 16px; font-family: monospace; font-weight: bold; margin-bottom: 5px; }
  .text-green { color: var(--neon-green); text-shadow: 0 0 5px rgba(0, 255, 163, 0.3); }
  .text-blue { color: var(--neon-blue); text-shadow: 0 0 5px rgba(0, 240, 255, 0.3); }
  .text-purple { color: var(--neon-purple); text-shadow: 0 0 5px rgba(138, 43, 226, 0.3); }
  
  .progress-bar { height: 4px; background: rgba(255,255,255,0.1); width: 100%; border-radius: 2px; }
  .fill { height: 100%; background: var(--neon-green); border-radius: 2px; box-shadow: 0 0 5px currentColor; }
  
  .radar-scan {
    width: 60px; height: 60px; border: 1px solid rgba(138, 43, 226, 0.5); border-radius: 50%;
    margin-top: 10px; position: relative; overflow: hidden;
    &::after {
      content: ''; position: absolute; top: 50%; left: 50%; width: 50%; height: 50%;
      background: conic-gradient(transparent, rgba(138, 43, 226, 0.8));
      transform-origin: 0 0; animation: radar 2s linear infinite;
    }
  }
}
@keyframes radar { 100% { transform: rotate(360deg); } }

/* 主聊天区 */
.chat-container { flex: 1; display: flex; flex-direction: column; }
.chat-box { flex: 1; display: flex; flex-direction: column; overflow: hidden; position: relative; }
.top-deco-line { position: absolute; top: 0; left: 0; height: 2px; width: 100%; background: linear-gradient(90deg, transparent, var(--neon-blue), transparent); opacity: 0.5; }

.messages {
  flex: 1; padding: 25px; overflow-y: auto; scroll-behavior: smooth;
  .empty-state {
    height: 100%; display: flex; flex-direction: column; justify-content: center; align-items: center; position: relative;
    .hex-grid-bg {
      position: absolute; width: 300px; height: 300px; opacity: 0.05;
      background-image: radial-gradient(var(--neon-blue) 2px, transparent 2px); background-size: 20px 20px;
    }
    .ai-core-icon {
      position: relative; width: 80px; height: 80px; display: flex; align-items: center; justify-content: center;
      .core-ring { position: absolute; width: 100%; height: 100%; border: 1px dashed var(--neon-blue); border-radius: 50%; animation: radar 10s linear infinite; }
    }
    .greeting-text { margin-top: 15px; color: var(--text-muted); font-family: monospace; letter-spacing: 1px; }
  }
}

.message-item {
  display: flex; margin-bottom: 25px; animation: slideIn 0.3s ease-out forwards;
  .avatar-wrap { width: 36px; height: 36px; flex-shrink: 0; }
  .tech-avatar { background: rgba(0,0,0,0.5); border: 1px solid rgba(255,255,255,0.2); }

  &.user {
    flex-direction: row-reverse;
    .avatar-wrap { margin-left: 15px; }
    .tech-bubble {
      background: rgba(138, 43, 226, 0.1); border: 1px solid rgba(138, 43, 226, 0.4);
      border-top-right-radius: 0; box-shadow: inset 0 0 10px rgba(138, 43, 226, 0.1);
    }
  }
  
  &.assistant {
    .avatar-wrap { margin-right: 15px; }
    .tech-bubble {
      background: rgba(0, 240, 255, 0.05); border: 1px solid rgba(0, 240, 255, 0.2);
      border-top-left-radius: 0; box-shadow: inset 0 0 10px rgba(0, 240, 255, 0.05);
    }
  }
}
@keyframes slideIn { from { opacity: 0; transform: translateY(10px); } to { opacity: 1; transform: translateY(0); } }

.tech-bubble { padding: 12px 18px; border-radius: 8px; line-height: 1.6; font-size: 14px; color: var(--text-main); }

/* Markdown 样式保持原样 */
.md-content {
  :deep(p) { margin: 0 0 10px 0; &:last-child { margin-bottom: 0; } }
  :deep(a) { color: var(--neon-blue); text-decoration: none; }
  :deep(code) { background: rgba(255,255,255,0.1); padding: 2px 4px; border-radius: 4px; font-family: monospace; color: var(--neon-blue); }
  :deep(pre) { background: #000; border: 1px solid #333; padding: 12px; border-radius: 6px; overflow-x: auto; border-left: 2px solid var(--neon-blue); code { background: transparent; color: #ccc;} }
}

.glass-input-area {
  padding: 15px 25px; background: rgba(0, 0, 0, 0.4); border-top: 1px solid var(--glass-border);
  display: flex; gap: 15px; align-items: flex-end;
  
  .cyber-input :deep(.el-textarea__inner) {
    background: rgba(0, 0, 0, 0.5); border: 1px solid rgba(255,255,255,0.1); color: #fff;
    border-radius: 4px; font-size: 14px; font-family: monospace;
    &:focus { border-color: var(--neon-blue); box-shadow: 0 0 10px rgba(0, 240, 255, 0.1); }
  }
  
  .cyber-btn {
    height: 52px; padding: 0 20px; border-radius: 4px; background: rgba(0, 240, 255, 0.1);
    border: 1px solid var(--neon-blue); color: var(--neon-blue); font-family: monospace; font-weight: bold;
    &:hover:not(:disabled) { background: var(--neon-blue); color: #000; box-shadow: 0 0 15px rgba(0, 240, 255, 0.5); }
    &:disabled { background: transparent; border-color: #333; color: #555; }
  }
}

.cyber-typing span {
  display: inline-block; width: 6px; height: 6px; background-color: var(--neon-blue); border-radius: 50%; margin: 0 3px; animation: cyberBounce 1.4s infinite ease-in-out both;
  &:nth-child(1) { animation-delay: -0.32s; } &:nth-child(2) { animation-delay: -0.16s; }
}
@keyframes cyberBounce { 0%, 80%, 100% { transform: scale(0); opacity: 0.3; } 40% { transform: scale(1); opacity: 1; } }
</style>