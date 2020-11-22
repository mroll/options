import React from 'react'
import { LinePath } from '@visx/shape'
import { Group } from '@visx/group'
import { GradientTealBlue } from '@visx/gradient'
import { GridRows, GridColumns } from '@visx/grid'
import { AxisLeft, AxisBottom } from '@visx/axis'
import { curveNatural } from '@visx/curve'
import { scaleTime, scaleLinear } from '@visx/scale'
import { extent } from 'd3-array'

const getX = (d) => d.date
const getY = (d) => d.value

function RSIChart(props) {
  const { data, width, height, margin } = props

  const xScale = scaleTime({ domain: extent(data, getX) })
  const yScale = scaleLinear({ domain: [0, 100] })

  // bounds
  const xMax = width - margin.left - margin.right;
  const yMax = height - margin.top - margin.bottom;

  // update scale output ranges
  xScale.range([0, xMax]);
  yScale.range([yMax, 0]);

  return (
    <svg width={width} height={height}>
      <rect width={width} height={height} fill="white" rx={14} ry={14} />

      <Group left={margin.left} top={margin.top}>
        <GridRows scale={yScale} width={xMax} height={yMax} stroke="#e0e0e0" />
        <GridColumns scale={xScale} width={xMax} height={yMax} stroke="#e0e0e0" />
        <AxisBottom top={yMax} scale={xScale} numTicks={width > 520 ? 10 : 5} />
        <AxisLeft scale={yScale} />
        <GradientTealBlue id="teal" />
        <LinePath
          curve={curveNatural}
          data={data}
          x={d => xScale(getX(d))}
          y={d => yScale(getY(d))}
          stroke="rgba(23, 233, 217)"
          strokeWidth={2}
          shapeRendering="geometricPrecision"
        />
      </Group>
    </svg>
  )
}

export default RSIChart
