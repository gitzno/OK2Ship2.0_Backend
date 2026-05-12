<template>
  <el-container class="h-screen w-screen box-border">
    <MainNavigationMenu />
    <el-container>
      <el-header><MainHeader /></el-header>
      <el-main><slot /></el-main>
    </el-container>
  </el-container>
</template>
<script setup lang="ts">
import MainHeader from '@/components/layout/header/MainHeader.vue'
import MainNavigationMenu from '@/components/layout/navigation/MainNavigationMenu.vue'
</script>

<style scoped></style>
