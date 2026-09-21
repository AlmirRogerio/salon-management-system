export function getApiErrorMessage(error, fallback = 'Ocorreu um erro inesperado.') {
  if (!error?.response) {
    return 'Não foi possível conectar ao servidor. Verifique sua conexão.'
  }

  const detail = error.response.data?.detail

  if (typeof detail === 'string') {
    return detail
  }

  if (Array.isArray(detail) && detail.length > 0) {
    return detail
      .map((item) => item.msg || item.message)
      .filter(Boolean)
      .join(' ')
  }

  return fallback
}
