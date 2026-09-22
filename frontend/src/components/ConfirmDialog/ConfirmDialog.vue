<script setup>
import { nextTick, ref, watch } from 'vue'

const props = defineProps({
  open: { type: Boolean, default: false },
  title: { type: String, default: 'Confirmar' },
  message: { type: String, default: '' },
  confirmLabel: { type: String, default: 'Confirmar' },
  cancelLabel: { type: String, default: 'Cancelar' },
  variant: {
    type: String,
    default: 'primary',
    validator: (value) => ['primary', 'danger'].includes(value),
  },
  busy: { type: Boolean, default: false },
})

const emit = defineEmits(['confirm', 'cancel'])

const confirmButton = ref(null)

function onConfirm() {
  if (props.busy) return
  emit('confirm')
}

function onCancel() {
  if (props.busy) return
  emit('cancel')
}

function onKeydown(event) {
  if (event.key === 'Escape') onCancel()
}

watch(
  () => props.open,
  async (isOpen) => {
    if (isOpen) {
      await nextTick()
      confirmButton.value?.focus()
    }
  }
)
</script>

<template>
  <Teleport to="body">
    <Transition name="dialog">
      <div
        v-if="open"
        class="dialog-overlay"
        role="presentation"
        @click.self="onCancel"
        @keydown="onKeydown"
      >
        <div
          class="dialog"
          role="alertdialog"
          aria-modal="true"
          :aria-label="title"
        >
          <h2 class="dialog-title">
            {{ title }}
          </h2>
          <p
            v-if="message"
            class="dialog-message"
          >
            {{ message }}
          </p>
          <div class="dialog-actions">
            <button
              type="button"
              class="dialog-btn ghost"
              :disabled="busy"
              @click="onCancel"
            >
              {{ cancelLabel }}
            </button>
            <button
              ref="confirmButton"
              type="button"
              class="dialog-btn"
              :class="variant"
              :disabled="busy"
              @click="onConfirm"
            >
              {{ confirmLabel }}
            </button>
          </div>
        </div>
      </div>
    </Transition>
  </Teleport>
</template>

<style scoped src="./ConfirmDialog.css"></style>
