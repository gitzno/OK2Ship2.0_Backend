<template>
  <el-page-header>
    <template #content>
      <span class="text-large font-600 mr-3"> Title </span>
    </template>
   
  </el-page-header>
</template>

<script lang="ts" setup>
import { Expand, Fold } from '@element-plus/icons-vue'
import { useStageMenu } from '@/stores/stageMenu'
const stageMenu = useStageMenu()
</script>

<style lang=""></style>
