<template>
  <el-page-header>
    <template #content>
      <span class="text-large font-600 mr-3"> {{ headerStore.title }} </span>
    </template>
   
  </el-page-header>
</template>

<script lang="ts" setup>
import { Expand, Fold } from '@element-plus/icons-vue'
import { useStageMenu } from '@/stores/stageMenu'
import { useHeaderStore } from '@/stores/Header'

const stageMenu = useStageMenu()
const headerStore = useHeaderStore()
</script>

<style lang=""></style>
