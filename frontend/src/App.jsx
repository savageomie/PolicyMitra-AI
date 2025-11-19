import React from 'react'
import { Routes, Route, Link } from 'react-router-dom'
import ChatPage from './pages/ChatPage'
import SurveyPage from './pages/SurveyPage'
import RecommendPage from './pages/RecommendPage'
import PolicyPage from './pages/PolicyPage'
import ClaimPage from './pages/ClaimPage'
import DashboardPage from './pages/DashboardPage'

export default function App() {
  return (
    <div className="app">
      <nav className="nav">
        <Link to="/">🏠 Home</Link>
        <Link to="/chat">💬 Chat</Link>
        <Link to="/survey">📋 Survey</Link>
        <Link to="/recommend">🔍 Recommend</Link>
        <Link to="/policy">📄 Policy</Link>
        <Link to="/claim">🧾 Claim</Link>
        <Link to="/dashboard">📊 Dashboard</Link>
      </nav>
      <main className="main">
        <Routes>
          <Route path="/" element={<div style={{padding:20}}>Welcome to PolicyMitra Frontend</div>} />
          <Route path="/chat" element={<ChatPage />} />
          <Route path="/survey" element={<SurveyPage />} />
          <Route path="/recommend" element={<RecommendPage />} />
          <Route path="/policy" element={<PolicyPage />} />
          <Route path="/claim" element={<ClaimPage />} />
          <Route path="/dashboard" element={<DashboardPage />} />
        </Routes>
      </main>
    </div>
  )
}
