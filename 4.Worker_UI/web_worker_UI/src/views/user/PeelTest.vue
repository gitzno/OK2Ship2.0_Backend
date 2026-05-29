<template >
    <div>
        this is peel test
    </div>
</template>
<script lang="ts" setup>
import { onMounted } from 'vue';
import { useHeaderStore } from '@/stores/Header';   
const headerStore = useHeaderStore();
onMounted(() => {
  headerStore.title = 'Peel Test';
});
</script>
<style lang="">
    
</style>