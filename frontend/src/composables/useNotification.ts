// ── useNotification.ts ── Singleton-Toast
import { ref } from 'vue'

const text    = ref('')
const visible = ref(false)
let timeout: ReturnType<typeof setTimeout> | null = null

export function useNotification() {
  function show(message: string) {
    if (timeout) clearTimeout(timeout)
    text.value    = message
    visible.value = true
    timeout = setTimeout(() => {
      visible.value = false
    }, 2800)
  }

  return { text, visible, show }
}
