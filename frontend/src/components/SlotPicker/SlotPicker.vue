<script setup>
const props = defineProps({
  slots: { type: Array, required: true },
  state: { type: Object, required: true },
  selected: { type: String, default: '' },
  hasQuery: { type: Boolean, default: true },
})

const emit = defineEmits(['select'])

function formatSlotTime(value) {
  return new Date(value).toLocaleTimeString('pt-BR', {
    hour: '2-digit',
    minute: '2-digit',
  })
}
</script>

<template>
  <p
    v-if="!hasQuery"
    class="muted"
  >
    <slot name="empty-query">
      Selecione os serviços e a data para ver os horários disponíveis.
    </slot>
  </p>
  <p
    v-else-if="state.loading"
    class="muted"
  >
    Buscando horários...
  </p>
  <p
    v-else-if="state.loaded && !state.isOpen"
    class="muted"
  >
    O salão está fechado neste dia. Escolha outra data.
  </p>
  <p
    v-else-if="state.loaded && slots.length === 0"
    class="muted"
  >
    Nenhum horário disponível para este dia. Tente outra data.
  </p>
  <div
    v-else
    class="slots"
  >
    <button
      v-for="slot in slots"
      :key="slot"
      type="button"
      class="slot"
      :class="{ selected: props.selected === slot }"
      @click="emit('select', slot)"
    >
      {{ formatSlotTime(slot) }}
    </button>
  </div>
</template>
