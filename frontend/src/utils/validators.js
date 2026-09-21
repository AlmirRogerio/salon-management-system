const EMAIL_RE = /^[^\s@]+@[^\s@]+\.[^\s@]+$/

export function validateName(value) {
  const v = (value || '').trim()
  if (v.length < 2) return 'Informe seu nome (mínimo 2 caracteres).'
  if (v.length > 150) return 'Nome muito longo (máximo 150 caracteres).'
  return ''
}

export function validateEmail(value) {
  const v = (value || '').trim()
  if (!v) return 'Informe seu e-mail.'
  if (!EMAIL_RE.test(v)) return 'Informe um e-mail válido.'
  return ''
}

export function validatePhone(value) {
  const v = (value || '').trim()
  if (v.length < 8) return 'Informe um telefone válido (mínimo 8 dígitos).'
  if (v.length > 30) return 'Telefone muito longo (máximo 30 caracteres).'
  return ''
}

export function validatePassword(value) {
  const v = value || ''
  if (v.length < 8) return 'A senha deve ter no mínimo 8 caracteres.'
  if (v.length > 128) return 'A senha deve ter no máximo 128 caracteres.'
  return ''
}

export function validateRequired(value, message = 'Campo obrigatório.') {
  return (value || '').trim() ? '' : message
}
