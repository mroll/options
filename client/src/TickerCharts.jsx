import React, { useEffect, useState } from 'react'
import { useLocation } from 'react-router-dom'
import TimeseriesLineChart from './TimeseriesLineChart'
import TimeseriesColumnChart from './TimeseriesColumnChart'
import { fetchTimeseries } from './util'

const width = 1200
const height = 400

const margin = { top: 10, right: 30, bottom: 50, left: 40 };

function useQuery() {
  return new URLSearchParams(useLocation().search);
}

function TickerCharts() {
  let query = useQuery()

  const ticker = query.get("ticker")
  const startDate = "2020-06-01"
  const endDate = "2020-10-01"
  const [dailyData, setDailyData] = useState([])
  const [rsiData, setRsiData] = useState([])
  const [macdData, setMacdData] = useState([])
  const [markers, setMarkers] = useState([])

  useEffect(() => {
    fetchTimeseries('daily_close', ticker, startDate, endDate)
    .then(setDailyData)
  }, [ticker])

  useEffect(() => {
    fetchTimeseries('rsi', ticker, startDate, endDate)
      .then(setRsiData)
  }, [ticker])

  useEffect(() => {
    fetchTimeseries('macd_hist', ticker, startDate, endDate)
      .then(setMacdData)
  }, [ticker])

  useEffect(() => {
    fetchTimeseries('markers', ticker, startDate, endDate)
      .then(setMarkers)
  }, [ticker])

  return rsiData.length > 0 && dailyData.length > 0
    ? (
      <>
        <TimeseriesLineChart
          data={dailyData}
          title="Daily Close"
          width={width}
          height={height}
          margin={margin}
          markers={markers}
        />

        <TimeseriesLineChart
          data={rsiData}
          title="RSI"
          width={width}
          height={200}
          margin={margin}
          yMinRange={0}
          yMaxRange={100}
        />

        <TimeseriesColumnChart
          data={macdData}
          title="MACD Hist."
          width={width}
          height={200}
          margin={margin}
        />
      </>
    )
    : null
}

export default TickerCharts
