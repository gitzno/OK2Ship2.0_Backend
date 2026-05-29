<template>
  <div class="upload-container">
    <el-button style="margin-bottom: 20px" type="primary" @click="Upload()">Upload</el-button>
    <el-upload
      ref="uploadRef"
      v-model:file-list="fileList"
      class="upload-demo"
      drag
      :auto-upload="false"
      action="#"
      directory
      multiple
      :http-request="handleCustomUpload"
      :on-change="handleChange"
    >
      <el-icon class="el-icon--upload"><upload-filled /></el-icon>
      <div class="el-upload__text">Thả folder hoặc <em>click để upload</em></div>
    </el-upload>
  </div>
</template>

<script setup lang="ts">
import { onMounted } from 'vue'
import { useHeaderStore } from '@/stores/Header'
const uploadRef = ref<UploadInstance>()

const headerStore = useHeaderStore()
onMounted(() => {
  headerStore.title = 'Upload Folder'
})
import { ref } from 'vue'

import { UploadFilled } from '@element-plus/icons-vue'

import type { UploadFile, UploadFiles, UploadProps, UploadUserFile } from 'element-plus'

const isUploading = ref(false)

const handleChange = (uploadFile: UploadFile, uploadFiles: UploadFiles) => {
  console.log('ADDRESS ' + uploadFile.raw.webkitRelativePath)
}

const Upload = () => {
  if (!uploadRef.value) return
  isUploading.value = true

  // Lệnh này bắt đầu kích hoạt hàm handleCustomUpload tuần tự cho từng file trong danh sách
  uploadRef.value.submit()
}

const handleCustomUpload = (options: UploadProps['httpRequest']) => {
  console.log(options.file)
}

const fileList = ref<UploadUserFile[]>([])
</script>
