import { ref, computed } from 'vue'
import { defineStore } from 'pinia'

export const useHeaderStore = defineStore('header',  {
 state: () => {
    return {
      title: "Default Title",
    }
  },
  
})
