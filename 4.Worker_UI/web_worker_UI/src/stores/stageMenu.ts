import { defineStore } from 'pinia'

export const useStageMenu = defineStore('stageMenu', {
  state: () => {
    return {
      state: false,
    }
  },
  actions: {
    toggle() {
      this.state = !this.state
    },
    open() {
      this.state = true
    },
    close() {
      this.state = false
    },
  },
})
