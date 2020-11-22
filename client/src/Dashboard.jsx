import React, { useEffect, useState } from 'react'
import { Button, Collapse, List, Typography } from 'antd'
import 'antd/dist/antd.css'
import { format, subDays } from 'date-fns'
import _ from 'lodash'

import { fetchTimeseries } from './util'
import './App.css'

const { Panel } = Collapse

function Dashboard() {
  const [markers, setMarkers] = useState([])
  const [dateRange, setDateRange] = useState({
    startDate: subDays(new Date(), 90),
    endDate: new Date()
  })

  const startDate = format(dateRange.startDate, "yyyy-MM-dd")
  const endDate = format(dateRange.endDate, "yyyy-MM-dd")

  useEffect(() => {
    fetchTimeseries('markers', null, startDate, endDate)
      .then(setMarkers)
  }, [startDate, endDate])

  const groupedMarkers = _.groupBy(markers, (marker) => {
    return format(marker.date, "yyyy-MM-dd")
  })
  const dates = _.chain(groupedMarkers)
                 .keys(groupedMarkers)
                 .sort()
                 .reverse()
                 .value()


  return (
    <div style={{ padding: 100 }}>
    <Typography.Title>Recent Put-Selling Opportunities</Typography.Title>
    <Collapse
      defaultActiveKey={[dates[0]]}
      style={{ width: '30%' }}
    >
      {
        dates.map((date) => (
          <Panel header={date} key={date}>
                 <List
                   size="small"
                   dataSource={groupedMarkers[date]}
                   renderItem={marker => (
                     <List.Item>
                       <List.Item.Meta title={(
                         <Button
                           type="link"
                           href={`http://localhost:3000/charts?ticker=${marker.ticker}`}
                         >{ marker.ticker }</Button>
                       )}
                       />
                     </List.Item>
                   )}
                 />
          </Panel>
        ))
      }
    </Collapse>
    </div>
  )
}

export default Dashboard
