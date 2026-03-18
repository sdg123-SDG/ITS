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
          登 录
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
                <span class="text">新建简牍</span>
                <span class="shortcut">
                  <span class="key">Ctrl</span>
                  <span>+</span>
                  <span class="key">K</span>
                </span>
              </a>
            </div>

            <div class="navigation-container" v-show="isSidebarExpanded">
              <div class="navigation-item" :class="{ 'selected': selectedNavItem === 'knowledge' }" @click="handleKnowledgeBase">
                <span class="nav-text">藏经阁 (知识库)</span>
              </div>
              <div class="navigation-item" :class="{ 'selected': selectedNavItem === 'service' }" @click="handleServiceStation">
                <span class="nav-text">驿站 (服务站)</span>
              </div>
              <div class="navigation-item" :class="{ 'selected': selectedNavItem === 'network' }" @click="handleNetworkSearch">
                <span class="nav-text">八方听风 (联网)</span>
              </div>
            </div>

            <div v-show="isSidebarExpanded" class="sidebar-main">
              <div class="navigation-item" @click="toggleSessions">
                <span class="nav-text">往期卷宗</span>
              </div>
              <div class="sessions-list" v-show="showSessions">
                <div v-if="isLoadingSessions" class="loading-sessions">
                  翻阅卷宗中...
                </div>
                <div v-else-if="sessions.length === 0" class="no-sessions">
                  尚无笔墨留存
                </div>
                <div
                  v-for="session in sessions"
                  :key="session.session_id"
                  :class="['session-item', { 'selected': session.session_id === selectedSessionId }]"
                  @click="selectSession(session.session_id)"
                >
                  <div class="session-info">
                    <div style="display: flex; align-items: center; gap: 8px;">
                      <div class="session-preview">{{ session.memory[0]?.content || '空白卷宗' }}</div>
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
                  src="/avatar.png"
                  class="user-avatar"
                  alt="用户头像"
                  @click="toggleUserInfo"
                  tabindex="0"
                />

                <div class="user-info-dropdown" v-show="showUserInfo">
                  <template v-if="currentUser">
                    <span class="user-name">{{ currentUser }}</span>
                    <button data-testid="setup_logout" class="btn-tertiary logout-btn" @click="handleLogout">
                      退出登录
                    </button>
                  </template>
                  <template v-else>
                    <span class="user-name">尚未落座</span>
                    <button class="login-button btn-primary" @click="goToLogin">请登录</button>
                  </template>
                </div>
              </div>
            </div>

            <div class="chat-message-container" ref="processContent">
              <div v-for="(msg, index) in chatMessages" :key="index" :class="['message-wrapper', msg.type]">

                 <div class="chat-avatar ai-avatar" v-if="msg.type === 'assistant' || msg.type === 'THINKING'">
                   <span class="ink-avatar-text">智</span>
                 </div>

                 <div class="message-body">
                   <div class="message-role-label" v-if="msg.type === 'THINKING'" @click="toggleThinking(index)">
                     <div class="thinking-header">
                       <span class="thinking-text">{{ isProcessing && index === chatMessages.length - 1 ? '凝神推演中...' : '推演已毕' }}</span>
                     </div>
                   </div>

                   <div class="message-bubble" v-show="msg.type !== 'THINKING' || !msg.collapsed">
                     <div class="markdown-body" v-html="renderMarkdown(msg.content)"></div>
                   </div>
                 </div>

                 <div class="chat-avatar user-avatar-msg" v-if="msg.type === 'user'">
                   <img src="/avatar.png" alt="User" />
                 </div>

              </div>
            </div>

            <div class="input-container">
              <div class="textarea-with-button">
                <textarea
                  v-model="userInput"
                  placeholder="落笔于此..."
                  @keyup.enter.exact="handleSend($event)"
                  :disabled="isProcessing"
                ></textarea>
                <button
                  class="send-button"
                  :class="{ 'cancel-button': isProcessing, 'disabled': !userInput.trim() && !isProcessing }"
                  :disabled="!userInput.trim() && !isProcessing"
                  @click="isProcessing ? handleCancel() : handleSend()"
                >
                  {{ isProcessing ? '停 止' : '发 送' }}
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

    // 核心修复点：将清空输入框的操作提前到获取文本的第一时刻
    const handleSend = async (event) => {
      if (event) event.preventDefault();

      const textToSend = userInput.value.trim(); // 1. 先把输入框的值存起来
      if (!textToSend) return;

      userInput.value = ''; // 2. 瞬间清空输入框，解决残留问题
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
        content: textToSend // 使用存起来的变量
      });

      const userMessage = `<div class="user-message">${textToSend}</div>\n\n`;
      if (selectedSessionId.value && answerText.value) answerText.value += userMessage;
      else answerText.value = userMessage;

      const finalUserId = userId || currentUser.value;
      scrollToBottom();

      const requestData = {
        query: textToSend, // 使用存起来的变量
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
      streamTextToProcess('推演已中止\n');
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
/* 避免样式污染，其余在全局控制 */
</style>