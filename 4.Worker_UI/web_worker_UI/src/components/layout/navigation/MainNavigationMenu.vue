<template>
  <el-menu
    default-active="2"
    class="el-menu-vertical-demo"
    :collapse="stageMenu.state"
    @open="handleOpen"
    @close="handleClose"
  >
    <el-menu-item index="1">
      <template #title>
        <el-icon><icon-menu /></el-icon>
        <span>Dashboard</span>
      </template>
    </el-menu-item>
    <el-menu-item index="2">
      <el-icon><icon-menu /></el-icon>
      <template #title>Upload Image</template>
    </el-menu-item>
    <el-menu-item index="3" disabled>
      <el-icon><document /></el-icon>
      <template #title>Navigator Three</template>
    </el-menu-item>
    <el-menu-item index="4">
      <el-icon><setting /></el-icon>
      <template #title>Navigator Four</template>
    </el-menu-item>
  </el-menu>
</template>

<script lang="ts" setup>
import { ref } from 'vue'
import { Document, Expand, Menu as IconMenu, Location, Setting } from '@element-plus/icons-vue'

import { useStageMenu } from '@/stores/stageMenu'
const stageMenu = useStageMenu()

const handleOpen = (key: string, keyPath: string[]) => {
  console.log(key, keyPath)
}
const handleClose = (key: string, keyPath: string[]) => {
  console.log(key, keyPath)
}
</script>

<style>
.el-menu-vertical-demo:not(.el-menu--collapse) {
  width: 200px;
  min-height: 400px;
}
</style>
