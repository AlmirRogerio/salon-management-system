const currencyFormatter = new Intl.NumberFormat('pt-BR', {
  style: 'currency',
  currency: 'BRL',
})

const dateTimeFormatter = new Intl.DateTimeFormat('pt-BR', {
  dateStyle: 'short',
  timeStyle: 'short',
})

export function formatCurrency(value) {
  const number = Number(value)
  return currencyFormatter.format(Number.isNaN(number) ? 0 : number)
}

export function formatDateTime(value) {
  if (!value) return '-'
  const date = new Date(value)
  return Number.isNaN(date.getTime()) ? '-' : dateTimeFormatter.format(date)
}

export function formatDuration(minutes) {
  const total = Number(minutes) || 0
  const hours = Math.floor(total / 60)
  const mins = total % 60
  if (hours && mins) return `${hours}h ${mins}min`
  if (hours) return `${hours}h`
  return `${mins}min`
}

const STATUS_LABELS = {
  pending: 'Pendente',
  confirmed: 'Confirmado',
  in_progress: 'Em andamento',
  completed: 'Concluído',
  canceled: 'Cancelado',
}

export function formatStatus(status) {
  return STATUS_LABELS[status] || status
}
