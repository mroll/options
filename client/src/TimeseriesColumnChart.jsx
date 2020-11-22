import React from 'react'
import { Bar } from '@visx/shape'
import { Group } from '@visx/group'
import { GridRows, GridColumns } from '@visx/grid'
import { AxisLeft, AxisBottom } from '@visx/axis'
import { scaleBand, scaleLinear } from '@visx/scale'
import { timeFormat } from 'd3-time-format'

const getX = (d) => d.date
const getY = (d) => d.value

function TimeseriesColumnChart(props) {
  const { data, title, width, height, margin } = props

  const maxHeight = Math.max(...data.map(d => Math.abs(d.value)))

  const xMax = width - margin.left - margin.right;
  const yMax = height - margin.top - margin.bottom;

  const xScale = scaleBand({
    range: [0, xMax],
    round: false,
    domain: data.map(getX),
    padding: 0.4
  })
  const yScale = scaleLinear({
    range: [0, yMax],
    round: false,
    domain: [maxHeight, -maxHeight]
  })

  return (
    <div>
    <h3>{ title }</h3>
    <svg width={width} height={height}>
      <rect width={width} height={height} fill="white" rx={14} ry={14} />

      <Group left={margin.left} top={margin.top}>
        <GridRows scale={yScale} width={xMax} height={yMax} stroke="#e0e0e0" />
        <GridColumns
          scale={xScale}
          width={xMax}
          height={yMax}
          stroke="#e0e0e0"
        />
        <AxisBottom
          top={yMax}
          scale={xScale}
          tickFormat={timeFormat("%b %d")}
        />
        <AxisLeft scale={yScale} />

        {data.map(d => {
          const date = getX(d)
          const value = getY(d)
          const barWidth = xScale.bandwidth()
          const barHeight = yMax / 2 - yScale(Math.abs(value))
          const barX = xScale(date)
          const barY = value < 0 ? yMax / 2 : yScale(value)

          console.log(date, value)
          if(!value) {
            console.log(data)

          }

          return (
            <Bar
              key={`bar-${date}`}
              x={barX}
              y={barY}
              width={barWidth}
              height={barHeight}
              fill="rgba(23, 233, 217, .5)"
            />
          );
        })}

      </Group>
    </svg>
    </div>
  )
}

export default TimeseriesColumnChart
