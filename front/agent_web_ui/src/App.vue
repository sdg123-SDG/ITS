<template>
  <div class="app-container">
    <div v-if="!isLoggedIn" class="login-container">
      <div class="login-form">
        <div class="its-logo-flat login-logo">
            <img src="/its-logo.svg" alt="ITS Logo" width="60" height="60"/>
          </div>
        <h1 class="login-title">ITS系统登录</h1>
        <div class="login-input-group">
          <label for="username">用户名</label>
          <input
            id="username"
            v-model="username"
            type="text"
            placeholder="请输入用户名"
            @keyup.enter="handleLogin"
          />
        </div>
        <div class="login-input-group">
          <label for="password">密码</label>
          <input
            id="password"
            v-model="password"
            type="password"
            placeholder="请输入密码"
            @keyup.enter="handleLogin"
          />
        </div>
        <div v-if="loginError" class="login-error">
          {{ loginError }}
        </div>
        <button class="login-button btn-primary" @click="handleLogin">
          登录
        </button>
        <div class="login-hint">
          <p>测试用户：root1, root2, root3</p>
          <p>密码：123456</p>
        </div>
      </div>
    </div>

    <template v-else>
      <div class="main-content">
        <div class="sidebar-wrapper">
          <div class="sidebar-content" :class="{ 'expanded': isSidebarExpanded }">
            <div class="app-branding">
              <div class="its-logo-flat">
                <img src="/its-logo.svg" alt="ITS Logo" width="40" height="40"/>
              </div>

              <button
                class="toggle-sidebar-btn"
                @click="toggleSidebar"
                :title="isSidebarExpanded ? '收起侧边栏' : '展开侧边栏'"
              >
                {{ isSidebarExpanded ? '‹' : '›' }}
              </button>
            </div>

            <div class="session-button-container" v-show="isSidebarExpanded">
              <a href="/" class="new-chat-btn" @click.prevent="createNewSession">
                <span class="icon">
                  <svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" role="img" style="" width="20" height="20" viewBox="0 0 1024 1024" name="AddConversation" class="iconify new-icon" data-v-9f34fd85="">
                    <path d="M475.136 561.152v89.74336c0 20.56192 16.50688 37.23264 36.864 37.23264s36.864-16.67072 36.864-37.23264v-89.7024h89.7024c20.60288 0 37.2736-16.54784 37.2736-36.864 0-20.39808-16.67072-36.864-37.2736-36.864H548.864V397.63968A37.0688 37.0688 0 0 0 512 360.448c-20.35712 0-36.864 16.67072-36.864 37.2736v89.7024H385.4336a37.0688 37.0688 0 0 0-37.2736 36.864c0 20.35712 16.67072 36.864 37.2736 36.864h89.7024z" fill="currentColor"></path>
                    <path d="M512 118.784c-223.96928 0-405.504 181.57568-405.504 405.504 0 78.76608 22.44608 152.3712 61.35808 214.6304l-44.27776 105.6768a61.44 61.44 0 0 0 56.68864 85.1968H512c223.92832 0 405.504-181.53472 405.504-405.504 0-223.92832-181.57568-405.504-405.504-405.504z m-331.776 405.504a331.776 331.776 0 1 1 331.73504 331.776H198.656l52.59264-125.5424-11.59168-16.62976A330.09664 330.09664 0 0 1 180.224 524.288z" fill="currentColor"></path>
                  </svg>
                </span>
                <span class="text">新建会话</span>
                <span class="shortcut">
                  <span class="key">Ctrl</span>
                  <span>+</span>
                  <span class="key">K</span>
                </span>
              </a>
            </div>

            <div class="navigation-container" v-show="isSidebarExpanded">
              <div class="navigation-item" :class="{ 'selected': selectedNavItem === 'knowledge' }" @click="handleKnowledgeBase">
                <svg xmlns="http://www.w3.org/2000/svg" width="1em" height="1em" fill="none" viewBox="0 0 24 24" class="nav-icon">
                  <path fill="currentColor" fill-rule="evenodd" d="M3.75 7h16.563c0 .48-.007 1.933-.016 3.685.703.172 1.36.458 1.953.837V5.937a2 2 0 0 0-2-2h-6.227a3 3 0 0 1-1.015-.176L9.992 2.677A3 3 0 0 0 8.979 2.5h-5.23a2 2 0 0 0-1.999 2v14.548a2 2 0 0 0 2 2h10.31a6.5 6.5 0 0 1-1.312-2H3.75S3.742 8.5 3.75 7m15.002 14.5a.514.514 0 0 0 .512-.454c.24-1.433.451-2.169.907-2.625.454-.455 1.186-.666 2.611-.907a.513.513 0 0 0-.002-1.026c-1.423-.241-2.155-.453-2.61-.908-.455-.457-.666-1.191-.906-2.622a.514.514 0 0 0-.512-.458.52.52 0 0 0-.515.456c-.24 1.432-.452 2.167-.907 2.624-.454.455-1.185.667-2.607.909a.514.514 0 0 0-.473.513.52.52 0 0 0 .47.512c1.425.24 2.157.447 2.61.9.455.454.666 1.19.907 2.634a.52.52 0 0 0 .515.452" clip-rule="evenodd"></path>
                </svg>
                <span class="nav-text">知识库查询</span>
              </div>
              <div class="navigation-item" :class="{ 'selected': selectedNavItem === 'service' }" @click="handleServiceStation">
                <svg xmlns="http://www.w3.org/2000/svg" width="1em" height="1em" fill="none" viewBox="0 0 24 24" class="nav-icon">
                  <path fill="currentColor" fill-rule="evenodd" d="M12 20.571a8.5 8.5 0 0 1 2.5-6.08c1.43-1.429 3.5-2.49 6.071-2.491-2.571.002-4.617-1.075-6.05-2.508S12 6 12 3.428C12 6 10.954 8.095 9.517 9.532 8.081 10.968 6 12 3.428 12a8.52 8.52 0 0 1 6.082 2.516c1.43 1.43 2.487 3.484 2.49 6.055m-9.853-7.314c3.485.588 5.053 1.331 6.163 2.44s1.847 2.667 2.435 6.198c.105.627.603 1.105 1.26 1.105.664 0 1.156-.479 1.25-1.11.588-3.502 1.329-5.085 2.441-6.2 1.111-1.114 2.677-1.845 6.16-2.433.638-.075 1.144-.586 1.144-1.253 0-.668-.5-1.188-1.147-1.254-3.481-.59-5.026-1.347-6.137-2.46-1.112-1.115-1.872-2.674-2.46-6.171C13.16 1.482 12.671 1 12.003 1c-.66 0-1.155.481-1.259 1.114-.588 3.5-1.323 5.087-2.435 6.203C7.2 9.43 5.632 10.159 2.156 10.75 1.503 10.816 1 11.333 1 12.004c0 .68.52 1.17 1.147 1.253" clip-rule="evenodd"></path>
                </svg>
                <span class="nav-text">服务站查询</span>
              </div>
              <div class="navigation-item" :class="{ 'selected': selectedNavItem === 'network' }" @click="handleNetworkSearch">
                <svg xmlns="http://www.w3.org/2000/svg" width="1em" height="1em" fill="none" viewBox="0 0 24 24" class="nav-icon">
                  <path fill="currentColor" fill-rule="evenodd" d="M11 4a7 7 0 1 0 6.993 7.328c-.039-.53-.586-.93-1.131-.891a5.5 5.5 0 1 1-6.203-6.203.75.75 0 0 0-1.317-.63C4.617 5.458 2.75 8.425 2.75 12c0 4.418 3.582 8 8 8s8-3.582 8-8a7.961 7.961 0 0 0-1.996-5.38" clip-rule="evenodd"></path>
                  <path stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="m21 21-3.5-3.5"></path>
                </svg>
                <span class="nav-text">联网搜索</span>
              </div>
            </div>

            <div v-show="isSidebarExpanded" class="sidebar-main">
              <div class="navigation-item" @click="toggleSessions">
                <svg xmlns="http://www.w3.org/2000/svg" width="1em" height="1em" viewBox="0 0 1024 1024" class="nav-icon">
                  <path d="M512 81.066667c-233.301333 0-422.4 189.098667-422.4 422.4s189.098667 422.4 422.4 422.4 422.4-189.098667 422.4-422.4-189.098667-422.4-422.4-422.4z m-345.6 422.4a345.6 345.6 0 1 1 691.2 0 345.6 345.6 0 1 1-691.2 0z m379.733333-174.933334a38.4 38.4 0 0 0-76.8 0v187.733334a38.4 38.4 0 0 0 11.264 27.136l93.866667 93.866666a38.4 38.4 0 1 0 54.272-54.272L546.133333 500.352V328.533333z" fill="currentColor"></path>
                </svg>
                <span class="nav-text">历史会话</span>
              </div>
              <div class="sessions-list" v-show="showSessions">
                <div v-if="isLoadingSessions" class="loading-sessions">
                  加载历史对话中...
                </div>
                <div v-else-if="sessions.length === 0" class="no-sessions">
                  暂无历史对话
                </div>
                <div
                  v-for="session in sessions"
                  :key="session.session_id"
                  :class="['session-item', { 'selected': session.session_id === selectedSessionId }]"
                  @click="selectSession(session.session_id)"
                >
                  <div class="session-info">
                    <div style="display: flex; align-items: center; gap: 8px;">
                      <img alt="豆包" src="//lf-flow-web-cdn.doubao.com/obj/flow-doubao/doubao/chat/static/image/default.light.2ea4b2b4.png" class="session-icon" style="width: 24px; height: 24px; border-radius: 4px; object-fit: cover;">
                      <div class="session-preview">{{ session.memory[0]?.content || '空对话' }}</div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>

        <div class="main-container">
          <div class="result-container" :class="{ 'processing': isProcessing }">
            <div class="top-user-section">
              <div class="user-avatar-container" ref="avatarContainerRef">
                <img
                  src="https://p3-flow-imagex-sign.byteimg.com/user-avatar/assets/e7b19241fb224cea967dfaea35448102_1080_1080.png~tplv-a9rns2rl98-icon-tiny.png?rcl=202511070904143F9B891FA2E40D7123F0&rk3s=8e244e95&rrcfp=76e58463&x-expires=1765155855&x-signature=nqQBx1W9ABfrm%2FRKkEYZUzsYjE0%3D"
                  class="user-avatar"
                  alt="用户头像"
                  @click="toggleUserInfo"
                  tabindex="0"
                />

                <div class="user-info-dropdown" v-show="showUserInfo">
                  <template v-if="currentUser">
                    <span class="user-name">{{ currentUser }}</span>
                    <button data-testid="setup_logout" class="btn-tertiary" style="width: 100%; justify-content: flex-start;" @click="handleLogout"><span role="img" class="semi-icon semi-icon-default text-16"><svg xmlns="http://www.w3.org/2000/svg" width="1em" height="1em" fill="none" viewBox="0 0 24 24"><path fill="currentColor" fill-rule="evenodd" d="M14 3H4.5v18H14v-5h2v5a2 2 0 0 1-2 2H4.5a2 2 0 0 1-2-2V3a2 2 0 0 1 2-2H14a2 2 0 0 1 2 2v5h-2zm5.207 4.793a1 1 0 1 0-1.414 1.414L19.586 11H10.5a1 1 0 1 0 0 2h9.086l-1.793 1.793a1 1 0 0 0 1.414 1.414l3.5-3.5a1 1 0 0 0 0-1.414z" clip-rule="evenodd"></path></svg></span>退出登录</button>
                  </template>
                  <template v-else>
                    <span class="user-name">当前未登录</span>
                    <button class="login-button btn-primary" @click="goToLogin">请登录</button>
                  </template>
                </div>
              </div>
            </div>

            <div class="chat-message-container" ref="processContent">
              <div v-for="(msg, index) in chatMessages" :key="index" :class="['message-wrapper', msg.type]">

                 <div class="chat-avatar ai-avatar" v-if="msg.type === 'assistant' || msg.type === 'THINKING'">
                   <img src="/its-logo.svg" alt="AI" />
                 </div>

                 <div class="message-body">
                   <div class="message-role-label" v-if="msg.type === 'THINKING'" @click="toggleThinking(index)">
                     <div class="thinking-header">
                       <span class="thinking-text">{{ isProcessing && index === chatMessages.length - 1 ? '深度思考中...' : '已完成思考' }}</span>
                       <svg
                         xmlns="http://www.w3.org/2000/svg"
                         width="16"
                         height="16"
                         viewBox="0 0 24 24"
                         fill="none"
                         stroke="currentColor"
                         stroke-width="2"
                         stroke-linecap="round"
                         stroke-linejoin="round"
                         class="thinking-icon"
                         :class="{ 'collapsed': msg.collapsed }"
                       >
                         <polyline points="6 9 12 15 18 9"></polyline>
                       </svg>
                     </div>
                   </div>

                   <div class="message-bubble" v-show="msg.type !== 'THINKING' || !msg.collapsed">
                     <div class="markdown-body" v-html="renderMarkdown(msg.content)"></div>
                   </div>
                 </div>

                 <div class="chat-avatar user-avatar-msg" v-if="msg.type === 'user'">
                   <img src="https://p3-flow-imagex-sign.byteimg.com/user-avatar/assets/e7b19241fb224cea967dfaea35448102_1080_1080.png~tplv-a9rns2rl98-icon-tiny.png?rcl=202511070904143F9B891FA2E40D7123F0&rk3s=8e244e95&rrcfp=76e58463&x-expires=1765155855&x-signature=nqQBx1W9ABfrm%2FRKkEYZUzsYjE0%3D" alt="User" />
                 </div>

              </div>
            </div>

            <div class="input-container">
              <div class="textarea-with-button">
                <textarea
                  v-model="userInput"
                  placeholder="请输入您的请求..."
                  @keyup.enter.exact="handleSend($event)"
                  :disabled="isProcessing"
                ></textarea>
                <button
                  class="send-button btn-primary"
                  :class="{ 'cancel-button': isProcessing, 'disabled': !userInput.trim() && !isProcessing }"
                  :disabled="!userInput.trim() && !isProcessing"
                  @click="isProcessing ? handleCancel() : handleSend()"
                >
                  {{ isProcessing ? '■' : '发送' }}
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </template>
  </div>
</template>

<script>
import { ref, computed, onMounted, watch, nextTick, onUnmounted } from 'vue';
import { marked } from 'marked';

// Configure marked options
marked.setOptions({
  breaks: true,
  gfm: true,
});

const renderMarkdown = (text) => {
  if (!text) return '';
  try {
    return marked.parse(text);
  } catch (e) {
    console.error('Markdown parsing error:', e);
    return text;
  }
};

export default {
  name: 'App',
  setup() {
    const isLoggedIn = ref(true);
    const isSidebarExpanded = ref(true);
    const username = ref('');
    const password = ref('');
    const currentUser = ref('');
    const loginError = ref('');
    const showUserInfo = ref(false);
    const avatarContainerRef = ref(null);

    const toggleUserInfo = () => {
      showUserInfo.value = !showUserInfo.value;
    };

    const handleClickOutside = (event) => {
      if (showUserInfo.value && avatarContainerRef.value && !avatarContainerRef.value.contains(event.target)) {
        showUserInfo.value = false;
      }
    };

    onMounted(() => {
      document.addEventListener('click', handleClickOutside);
    });

    onUnmounted(() => {
      document.removeEventListener('click', handleClickOutside);
    });

    const savedUserId = localStorage.getItem('currentUserId');
    if (savedUserId) {
      const validUsers = [
        { username: 'root1', password: '123456', userId: 'root1' },
        { username: 'root2', password: '123456', userId: 'root2' },
        { username: 'root3', password: '123456', userId: 'root3' }
      ];
      const savedUser = validUsers.find(u => u.userId === savedUserId);
      if (savedUser) {
        currentUser.value = savedUser.username;
      }
    }

    const userInput = ref('');
    const chatMessages = ref([]);
    const processMessages = ref([]);
    const answerText = ref('');
    const processContent = ref(null);
    const isProcessing = ref(false);
    let reader = null;
    const selectedNavItem = ref('');

    const toggleThinking = (index) => {
      const msg = chatMessages.value[index];
      if (msg && msg.type === 'THINKING') {
        msg.collapsed = !msg.collapsed;
      }
    };

    const handleKnowledgeBase = () => {
      processMessages.value = [];
      answerText.value = '';
      processContent.value = null;
      selectedNavItem.value = 'knowledge';
      selectedSessionId.value = '';
    };

    const handleNetworkSearch = () => {
      selectedNavItem.value = 'network';
      selectedSessionId.value = '';
    };

    const handleServiceStation = () => {
      processMessages.value = [];
      answerText.value = '';
      processContent.value = null;
      selectedNavItem.value = 'service';
      selectedSessionId.value = '';
    };

    const sessions = ref([]);
    const selectedSessionId = ref('');
    const isLoadingSessions = ref(false);
    const showSessions = ref(true);

    const toggleSessions = () => {
      showSessions.value = !showSessions.value;
    };

    const handleLogin = () => {
      loginError.value = '';
      const validUsers = [
        { username: 'root1', password: '123456', userId: 'root1' },
        { username: 'root2', password: '123456', userId: 'root2' },
        { username: 'root3', password: '123456', userId: 'root3' }
      ];
      const user = validUsers.find(u => u.username === username.value && u.password === password.value);

      if (user) {
        isLoggedIn.value = true;
        currentUser.value = user.username;
        localStorage.setItem('currentUserId', user.userId);
        window.scrollTo(0, 0);
        username.value = '';
        password.value = '';
      } else {
        loginError.value = '用户名或密码错误';
      }
    };

    const fetchUserSessions = async () => {
      if (!currentUser.value) return;
      isLoadingSessions.value = true;
      try {
        const response = await fetch('http://127.0.0.1:8000/api/user_sessions', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({"user_id": currentUser.value})
        });
        if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`);
        const data = await response.json();
        if (data.success && data.sessions) {
          sessions.value = data.sessions;
          if (data.sessions.length > 0 && !selectedSessionId.value) {
            selectSession(data.sessions[0].session_id);
          }
        }
      } catch (error) {
        console.error('Error fetching sessions:', error);
      } finally {
        isLoadingSessions.value = false;
        scrollToBottom();
      }
    };

    const createNewSession = () => {
      const newSessionId = `session_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;
      const newSession = {
        session_id: newSessionId,
        create_time: new Date().toISOString(),
        memory: [],
        total_messages: 0
      };
      sessions.value.unshift(newSession);
      processMessages.value = [];
      answerText.value = '';
      userInput.value = '';
      selectSession(newSessionId);
    };

    const selectSession = (sessionId) => {
      selectedSessionId.value = sessionId;
      selectedNavItem.value = '';
      const session = sessions.value.find(s => s.session_id === sessionId);
      chatMessages.value = [];
      processMessages.value = [];
      answerText.value = '';

      if (session && session.memory && Array.isArray(session.memory) && session.memory.length > 0) {
        let lastType = null;
        session.memory.forEach(msg => {
          if (!msg || !msg.content) return;
          let type = msg.role;
          if (type === 'process') type = 'THINKING';

          if (type === 'THINKING' && lastType === 'THINKING') {
            const lastMsg = chatMessages.value[chatMessages.value.length - 1];
            lastMsg.content += '\n' + msg.content;
          } else {
            chatMessages.value.push({ type: type, content: msg.content });
          }
          lastType = type;
        });
        nextTick(() => scrollToBottom());
      }
    };

    const handleLogout = () => {
      isLoggedIn.value = false;
      currentUser.value = '';
      localStorage.removeItem('currentUserId');
      processMessages.value = [];
      answerText.value = '';
      userInput.value = '';
      sessions.value = [];
      selectedSessionId.value = '';
    };

    const goToLogin = () => {
      isLoggedIn.value = false;
      currentUser.value = '';
      localStorage.removeItem('currentUserId');
    };

    const handleSend = async (event) => {
      if (event) event.preventDefault();
      if (!userInput.value.trim()) return;
      window.scrollTo(0, 0);

      const userId = localStorage.getItem('currentUserId');
      if (!userId) {
        isLoggedIn.value = false;
        return;
      }

      isProcessing.value = true;
      chatMessages.value.forEach(msg => {
        if (msg.type === 'THINKING') msg.collapsed = true;
      });

      processMessages.value = [];
      chatMessages.value.push({
        type: 'user',
        content: userInput.value.trim()
      });

      const userMessage = `<div class="user-message">${userInput.value.trim()}</div>\n\n`;
      if (selectedSessionId.value && answerText.value) answerText.value += userMessage;
      else answerText.value = userMessage;

      const finalUserId = userId || currentUser.value;
      scrollToBottom();

      const requestData = {
        query: userInput.value.trim(),
        context: { user_id: finalUserId, session_id: selectedSessionId.value || '' }
      };

      try {
        const response = await fetch('http://127.0.0.1:8000/api/query', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(requestData)
        });

        if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`);

        reader = response.body.getReader();
        const decoder = new TextDecoder();
        let buffer = '';

        while (true) {
          const { done, value } = await reader.read();
          if (done) {
            if (buffer.trim()) {
              processSSEData(buffer);
              buffer = '';
            }
            break;
          }

          const chunk = decoder.decode(value, { stream: true });
          buffer += chunk;
          const lines = buffer.split('\n');

          for (let i = 0; i < lines.length - 1; i++) {
            const line = lines[i];
            if (line.trim()) processSSEData(line);
          }
          buffer = lines[lines.length - 1];
        }
      } catch (error) {
        if (!error.name || error.name !== 'AbortError') {
          const errorMsg = `请求失败: ${error.message}`;
          streamTextToProcess(errorMsg + '\n');
          console.error('Error:', error);
        }
      } finally {
        isProcessing.value = false;
        reader = null;
        scrollToBottom();
        fetchUserSessions();
      }
      userInput.value = '';
    };

    const processSSEData = (data) => {
      try {
        if (typeof data !== 'string') return;
        if (data.startsWith('data:')) {
          const jsonStr = data.substring(5).trim();
          if (jsonStr) {
            try {
              const parsedData = JSON.parse(jsonStr);
              let kind;
              let text;

              if (parsedData.content && typeof parsedData.content === 'object') {
                text = parsedData.content.text;
                if (parsedData.content.kind) kind = parsedData.content.kind;
                else if (parsedData.content.type) kind = parsedData.content.type;
                if (parsedData.status === 'FINISHED' || parsedData.content.contentType === 'sagegpt/finish') return;
              } else if (parsedData.type && parsedData.content) {
                kind = parsedData.type;
                text = parsedData.content;
              }

              if (kind && text) {
                switch (kind) {
                  case 'ANSWER':
                    streamTextToAnswer(text);
                    break;
                  case 'THINKING':
                    streamTextToProcess(text);
                    break;
                  case 'PROCESS':
                    streamTextToProcess(text + '\n');
                    scrollToBottom();
                    break;
                  default:
                    streamTextToProcess(text + '\n');
                }
              }
            } catch (jsonError) {
              console.error('JSON parse error:', jsonError);
            }
          }
        }
      } catch (error) {
        console.error('Error processing SSE data:', error);
      }
    };

    const handleCancel = () => {
      if (reader) {
        reader.cancel();
        reader = null;
      }
      isProcessing.value = false;
      streamTextToProcess('请求已取消\n');
    };

    const streamTextToAnswer = (text) => {
      const lastMsg = chatMessages.value[chatMessages.value.length - 1];
      if ((!text || !text.trim()) && lastMsg && lastMsg.type !== 'assistant') return;

      text = text.replace(/ +/g, ' ').replace(/\n+/g, '\n');

      if (lastMsg && lastMsg.type === 'assistant') {
        lastMsg.content += text;
      } else {
        chatMessages.value.push({ type: 'assistant', content: text });
      }
      chatMessages.value = [...chatMessages.value];
      answerText.value += text;
      scrollToBottom();
    };

    const streamTextToProcess = (text) => {
      const lastMsg = chatMessages.value[chatMessages.value.length - 1];
      if (lastMsg && lastMsg.type === 'THINKING') {
        lastMsg.content += text;
        if (isProcessing.value && lastMsg.collapsed === undefined) lastMsg.collapsed = false;
      } else {
        chatMessages.value.push({
          type: 'THINKING',
          content: text,
          collapsed: false
        });
      }
      chatMessages.value = [...chatMessages.value];
      scrollToBottom();
    };

    const scrollToBottom = () => {
      setTimeout(() => {
        const chatContainer = document.querySelector('.chat-message-container');
        if (chatContainer) chatContainer.scrollTop = chatContainer.scrollHeight;
        window.scrollTo(0, 0);
      }, 0);
    };

    watch(isLoggedIn, (newVal) => {
      if (newVal && currentUser.value) fetchUserSessions();
    });

    onMounted(() => {
      if (isLoggedIn.value && currentUser.value) {
        fetchUserSessions();
        nextTick(() => scrollToBottom());
      }
      document.addEventListener('keydown', handleKeyDown);
    });

    onUnmounted(() => {
      document.removeEventListener('keydown', handleKeyDown);
    });

    const handleKeyDown = (event) => {
      if ((event.ctrlKey || event.metaKey) && event.key === 'k') {
        event.preventDefault();
        createNewSession();
      }
    };

    const toggleSidebar = () => {
      isSidebarExpanded.value = !isSidebarExpanded.value;
    };

    return {
      isLoggedIn,
      username,
      password,
      currentUser,
      loginError,
      showUserInfo,
      toggleUserInfo,
      avatarContainerRef,
      handleLogin,
      handleLogout,
      goToLogin,
      userInput,
      chatMessages,
      processMessages,
      answerText,
      processContent,
      isProcessing,
      handleSend,
      handleCancel,
      renderMarkdown,
      sessions,
      selectedSessionId,
      isLoadingSessions,
      showSessions,
      toggleSessions,
      selectedNavItem,
      handleKnowledgeBase,
      handleNetworkSearch,
      handleServiceStation,
      selectSession,
      fetchUserSessions,
      createNewSession,
      isSidebarExpanded,
      toggleSidebar,
      toggleThinking
    };
  }
};
</script>

<style scoped>
/* Scoped样式精简，大部分由全局style.css接管 */
.app-container {
  width: 100%;
  height: 100%;
  display: flex;
  flex-direction: column;
  gap: 10px;
  padding: 5px;
  padding-bottom: 10px;
  box-sizing: border-box;
  min-height: 100vh;
  overflow: hidden;
}

.main-content {
  display: flex;
  flex: 1;
  gap: 20px;
  overflow: hidden;
}

.sessions-sidebar {
  width: 300px;
  background-color: #fff;
  border: 1px solid #ccc;
  border-radius: 8px;
  display: flex;
  flex-direction: column;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
}

.login-container {
  display: flex;
  justify-content: center;
  align-items: center;
  flex: 1;
  padding: 20px;
}

.login-form {
  background: white;
  border-radius: 12px;
  padding: 40px;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
  width: 100%;
  max-width: 400px;
  text-align: center;
}

.login-logo {
  margin: 0 auto 20px;
}

.login-title {
  margin: 0 0 30px;
  font-size: 28px;
  font-weight: 700;
  color: #333;
  background: linear-gradient(90deg, #4CAF50, #2196F3);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.login-input-group {
  margin-bottom: 20px;
  text-align: left;
}

.login-input-group label {
  display: block;
  margin-bottom: 8px;
  font-weight: 500;
  color: #555;
}

.login-input-group input {
  width: 100%;
  padding: 12px 16px;
  border: 1px solid #ddd;
  border-radius: 6px;
  font-size: 16px;
  transition: border-color 0.3s ease;
  box-sizing: border-box;
}

.login-error {
  color: #f44336;
  margin-bottom: 20px;
  padding: 10px;
  background-color: #ffebee;
  border-radius: 4px;
}

.login-button {
  width: 100%;
  padding: 14px;
  background-color: #2196F3;
  color: white;
  border: none;
  border-radius: 6px;
  font-size: 16px;
  font-weight: 600;
  cursor: pointer;
}

.login-hint {
  margin-top: 20px;
  padding: 15px;
  background-color: #f5f5f5;
  border-radius: 6px;
  font-size: 14px;
  color: #666;
}

.display-container {
  display: flex;
  flex: 1;
  overflow: hidden;
  margin-top: 5px;
  margin-bottom: 5px;
  min-height: 500px;
}

.result-container {
  flex: 1;
  padding: 15px;
  display: flex;
  flex-direction: column;
  overflow: visible;
  height: auto;
  box-sizing: border-box;
  border-radius: 8px;
  border: 1px solid #fff;
}

.result-container.processing {
  animation: gradient-pulse 1.5s infinite ease-in-out;
}

@keyframes gradient-pulse {
  0% { border-color: #fff; }
  50% { border-color: #2196F3; }
  100% { border-color: #fff; }
}

.input-container {
  padding: 0;
  margin-top: auto;
}

.textarea-with-button {
  position: relative;
  display: inline-block;
  width: 100%;
  max-width: 50vw;
}

.textarea-with-button textarea {
  width: 100%;
  padding: 12px 48px 12px 12px;
  border: 1px solid #ccc;
  border-radius: 12px;
  resize: none;
  height: 100px;
  font-size: 16px;
  font-family: inherit;
}

.textarea-with-button .send-button {
  position: absolute;
  bottom: 12px;
  right: 12px;
  width: 32px;
  height: 32px;
  border-radius: 8px;
  border: none;
  background-color: #4CAF50;
  color: white;
  font-size: 12px;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
}

@media (max-width: 768px) {
  .app-container {
    padding: 8px;
    gap: 8px;
  }
  .display-container {
    flex-direction: column;
    gap: 15px;
  }
  .result-container {
    min-height: 180px;
  }
  .input-container textarea {
    height: 80px;
    font-size: 14px;
  }
}
</style>