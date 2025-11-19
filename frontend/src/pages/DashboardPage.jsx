import React from 'react'

export default function DashboardPage(){
  // static dashboard UI shell
  return (
    <div className="card">
      <h2>📊 Dashboard</h2>
      <div style={{display:'grid', gridTemplateColumns:'1fr 1fr', gap:12}}>
        <div className="card">Total chats: <strong>1245</strong></div>
        <div className="card">Total surveys: <strong>312</strong></div>
        <div className="card">Top query: <strong>How to file a claim?</strong></div>
        <div className="card">Recommendations: <strong>Crop (420)</strong></div>
      </div>
    </div>
  )
}
