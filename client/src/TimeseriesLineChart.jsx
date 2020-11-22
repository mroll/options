import React from 'react'
import { Circle } from '@visx/shape'
import { LinePath } from '@visx/shape'
import { Group } from '@visx/group'
import { GradientTealBlue } from '@visx/gradient'
import { GridRows, GridColumns } from '@visx/grid'
import { AxisLeft, AxisBottom } from '@visx/axis'
import { curveLinear } from '@visx/curve'
import { scaleTime, scaleLinear } from '@visx/scale'
import { extent } from 'd3-array'

const getX = (d) => d.date
const getY = (d) => d.value

function TimeseriesLineChart(props) {
  const {
    data, title, width, height, margin, xMinRange, xMaxRange,
    yMinRange, yMaxRange, markers
  } = props

  const markersWithData = markers ? markers.map((marker) => {
    const correspondingDataPoint = data.find((dp) => {
      return dp.date.getTime() === marker.date.getTime()
    })
    return {
      ...marker,
      value: (correspondingDataPoint || {}).value
    }
  })
  : []

  console.log(markersWithData)

  // bounds
  const xMax = width - margin.left - margin.right;
  const yMax = height - margin.top - margin.bottom;

  const xScale = scaleTime({
    domain: (xMinRange != null && xMaxRange != null)
          ? [xMinRange, xMaxRange]
          : extent(data, getX)
  })
  const yScale = scaleLinear({
    domain: (yMinRange != null && yMaxRange != null)
          ? [yMinRange, yMaxRange]
          : extent(data, getY),
    range: [yMax, 0]
  })

  // update scale output ranges
  xScale.range([0, xMax]);
  yScale.range([yMax, 0]);

  return (
    <div>
    <h3>{ title }</h3>
    <svg width={width} height={height}>
      <rect width={width} height={height} fill="white" rx={14} ry={14} />

      <Group left={margin.left} top={margin.top}>
        <GridRows scale={yScale} width={xMax} height={yMax} stroke="#e0e0e0" />
        <GridColumns scale={xScale} width={xMax} height={yMax} stroke="#e0e0e0" />
        <AxisBottom top={yMax} scale={xScale} numTicks={width > 520 ? 15 : 5} />
        <AxisLeft scale={yScale} />
        <GradientTealBlue id="teal" />
        <LinePath
          curve={curveLinear}
          data={data}
          x={d => xScale(getX(d))}
          y={d => yScale(getY(d))}
          stroke="rgba(23, 233, 217)"
          strokeWidth={2}
          shapeRendering="geometricPrecision"
        />

        {
          markersWithData.map((marker, i) => (
            <Circle
              key={`marker-${i}`}
              cx={xScale(getX(marker))}
              cy={yScale(getY(marker))}
              r={4}
              fill="blue"
            />
          ))
        }

      </Group>
    </svg>
    </div>
  )
}

export default TimeseriesLineChart
