import React, { useEffect, useState } from 'react'
import { BrowserRouter as Router, Route, useParams } from 'react-router-dom'
import Dashboard from './Dashboard'
import TickerCharts from './TickerCharts'
import './App.css';

const width = 1200
const height = 400

const margin = { top: 10, right: 30, bottom: 50, left: 40 };

function App() {
  return (
    <Router>
      <Route path="/dashboard" component={Dashboard} />
      <Route path="/charts" component={TickerCharts} />
    </Router>
  )
}

export default App;
