<script setup lang="ts">
import { computed } from 'vue'
import { useRoute } from 'vue-router'

const route = useRoute()
</script>

<template>
  <component :is="$route.meta.layout || 'div'">
    <router-view />
  </component>
</template>

<style scoped></style>
