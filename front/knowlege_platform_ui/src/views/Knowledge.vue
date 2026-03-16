<template>
  <div class="knowledge-container">
    
    <div class="metrics-row">
      <div class="metric-card glass-dashboard tech-corners">
        <div class="m-label">TOTAL VECTORS</div>
        <div class="m-value text-blue">1,482,903</div>
        <div class="m-chart line-chart-1"></div>
      </div>
      <div class="metric-card glass-dashboard tech-corners">
        <div class="m-label">STORAGE USED</div>
        <div class="m-value text-purple">42.8 GB</div>
        <div class="m-chart line-chart-2"></div>
      </div>
      <div class="metric-card glass-dashboard tech-corners">
        <div class="m-label">DB STATUS</div>
        <div class="m-value text-green">HEALTHY</div>
        <div class="m-chart status-pulse"></div>
      </div>
    </div>

    <el-card class="upload-card glass-dashboard tech-corners">
      <template #header>
        <div class="tech-header">
          <div class="status-dot"></div><span>DATA INGESTION PORTAL</span>
        </div>
      </template>
      <div class="upload-area">
        <el-upload
          class="cyber-upload" drag action="" :http-request="handleUpload" multiple :show-file-list="false"
        >
          <div class="upload-visual">
            <el-icon class="upload-icon"><upload-filled /></el-icon>
            <div class="scan-line"></div>
          </div>
          <div class="el-upload__text text-muted">
            DRAG FILES OR <em class="text-blue">CLICK</em>
          </div>
        </el-upload>
      </div>
    </el-card>

    <div v-if="uploadHistory.length > 0" class="history-section glass-dashboard tech-corners">
      <h3 class="tech-title">INGESTION LOGS</h3>
      <el-table :data="uploadHistory" class="cyber-table" :row-class-name="tableRowClassName">
        <el-table-column prop="fileName" label="TARGET_FILE" width="280" />
        <el-table-column prop="chunks" label="VECTORS" width="120" align="center">
          <template #default="scope"><span class="chunk-badge">{{ scope.row.chunks }}</span></template>
        </el-table-column>
        <el-table-column prop="status" label="STATUS" width="120" align="center">
          <template #default="scope">
            <el-tag :type="scope.row.status === 'success' ? 'success' : 'danger'" class="tech-tag">
              {{ scope.row.status.toUpperCase() }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="message" label="DIAGNOSTICS" />
        <el-table-column prop="time" label="TIMESTAMP" width="180" />
      </el-table>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { UploadFilled } from '@element-plus/icons-vue'
import { uploadFile } from '@/api/knowledge'
import { ElMessage } from 'element-plus'

const uploadHistory = ref([])

const handleUpload = async (options) => {
  const { file } = options
  const formData = new FormData()
  formData.append('file', file)

  try {
    const res = await uploadFile(formData)
    uploadHistory.value.unshift({
      fileName: res.file_name, chunks: res.chunks_added, status: res.status, message: res.message, time: new Date().toLocaleString()
    })
    ElMessage.success(`File ${file.name} uploaded successfully`)
  } catch (error) {
    uploadHistory.value.unshift({
      fileName: file.name, chunks: 0, status: 'error', message: error.message || 'Upload failed', time: new Date().toLocaleString()
    })
    ElMessage.error(`Upload failed for ${file.name}`)
  }
}
const tableRowClassName = ({ rowIndex }) => rowIndex === 0 ? 'success-row' : ''
</script>

<style lang="scss" scoped>
.knowledge-container { max-width: 1200px; margin: 0 auto; padding-top: 10px;}

/* 顶部数据统计卡片 */
.metrics-row {
  display: grid; grid-template-columns: repeat(3, 1fr); gap: 20px; margin-bottom: 30px;
}
.metric-card {
  padding: 20px; position: relative; overflow: hidden;
  .m-label { font-size: 12px; font-family: monospace; color: var(--text-muted); margin-bottom: 8px; }
  .m-value { font-size: 24px; font-family: monospace; font-weight: bold; }
  .text-blue { color: var(--neon-blue); } .text-purple { color: var(--neon-purple); } .text-green { color: var(--neon-green); }
  .m-chart { position: absolute; bottom: 0; left: 0; width: 100%; height: 30px; opacity: 0.3; }
  .line-chart-1 { background: linear-gradient(90deg, transparent, var(--neon-blue), transparent); }
  .line-chart-2 { background: repeating-linear-gradient(45deg, var(--neon-purple), var(--neon-purple) 2px, transparent 2px, transparent 8px); }
  .status-pulse { background: var(--neon-green); animation: pulseOpacity 2s infinite; }
}
@keyframes pulseOpacity { 0%, 100% { opacity: 0.1; } 50% { opacity: 0.3; } }

.glass-dashboard {
  background: rgba(10, 14, 23, 0.7); backdrop-filter: blur(8px);
  border: 1px solid var(--glass-border); margin-bottom: 30px;
  :deep(.el-card__header) { border-bottom: 1px dashed rgba(255,255,255,0.1); background: rgba(0,0,0,0.2); }
}

.tech-header {
  display: flex; align-items: center; font-family: monospace; color: var(--text-main); font-size: 14px;
  .status-dot { width: 6px; height: 6px; background: var(--neon-blue); margin-right: 10px; box-shadow: 0 0 8px var(--neon-blue); }
}

.upload-area {
  padding: 20px;
  .cyber-upload :deep(.el-upload-dragger) {
    background: rgba(0, 0, 0, 0.4); border: 1px dashed rgba(0, 240, 255, 0.3); border-radius: 4px;
    transition: all 0.3s; position: relative; overflow: hidden;
    &:hover { border-color: var(--neon-blue); background: rgba(0, 240, 255, 0.05); }
    .upload-visual { margin-bottom: 15px; position: relative; display: inline-block;}
    .upload-icon { font-size: 48px; color: rgba(0, 240, 255, 0.6); }
    .text-muted { color: var(--text-muted); font-family: monospace;}
    .text-blue { color: var(--neon-blue); font-style: normal; }
  }
}

.history-section { padding: 20px; .tech-title { color: var(--text-main); font-family: monospace; font-size: 14px; margin-bottom: 20px; } }

.cyber-table {
  background: transparent !important; --el-table-border-color: rgba(255,255,255,0.05) !important;
  --el-table-header-bg-color: rgba(0,0,0,0.5) !important; --el-table-bg-color: transparent !important; --el-table-tr-bg-color: transparent !important;
  :deep(th.el-table__cell) { color: var(--text-muted); font-family: monospace; font-size: 12px; border-bottom: 1px solid rgba(255,255,255,0.1); }
  :deep(td.el-table__cell) { border-bottom: 1px dashed rgba(255,255,255,0.05); color: var(--text-main); font-family: monospace; font-size: 13px; }
  :deep(tr:hover > td.el-table__cell) { background-color: rgba(0, 240, 255, 0.05) !important; }
}

.chunk-badge { border: 1px solid var(--neon-blue); padding: 2px 8px; border-radius: 2px; color: var(--neon-blue); background: rgba(0,240,255,0.1); }
.tech-tag {
  background: transparent; border-radius: 2px; border: 1px solid;
  &.el-tag--success { border-color: var(--neon-green); color: var(--neon-green); }
  &.el-tag--danger { border-color: #ff4d4f; color: #ff4d4f; }
}
</style>