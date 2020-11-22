const baseUrl = 'http://localhost:8000'

export function fetchTimeseries (func, ticker, startDate, endDate) {
  return fetch(`${baseUrl}/${func}?ticker=${ticker}&start_date=${startDate}&end_date=${endDate}`)
    .then(resp => resp.json())
    .then((response) => {

      const data = response.data.map(dp => {
        return Object.assign({}, dp, { date: new Date(dp.date) })
      })

      return data
    })
}
