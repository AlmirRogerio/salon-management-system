<script setup>
const props = defineProps({
  id: { type: String, required: true },
  label: { type: String, required: true },
  modelValue: { type: String, default: '' },
  type: { type: String, default: 'text' },
  autocomplete: { type: String, default: 'off' },
  placeholder: { type: String, default: '' },
  error: { type: String, default: '' },
  required: { type: Boolean, default: false },
  inputmode: { type: String, default: undefined },
  maxlength: { type: [String, Number], default: undefined },
  formatter: { type: Function, default: null },
})

const emit = defineEmits(['update:modelValue'])

function onInput(event) {
  const raw = event.target.value
  const value = props.formatter ? props.formatter(raw) : raw
  if (props.formatter && event.target.value !== value) {
    event.target.value = value
  }
  emit('update:modelValue', value)
}
</script>

<template>
  <div class="field">
    <label :for="id">{{ label }}</label>
    <input
      :id="id"
      :type="type"
      :value="modelValue"
      :autocomplete="autocomplete"
      :placeholder="placeholder"
      :required="required"
      :inputmode="inputmode"
      :maxlength="maxlength"
      :aria-invalid="Boolean(error)"
      :aria-describedby="error ? `${id}-error` : undefined"
      @input="onInput"
    >
    <span
      v-if="error"
      :id="`${id}-error`"
      class="field-error"
    >{{ error }}</span>
  </div>
</template>

<style scoped src="./FormField.css"></style>
