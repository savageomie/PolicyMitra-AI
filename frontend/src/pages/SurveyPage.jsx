import React from 'react'

export default function SurveyPage(){
  return (
    <div className="card">
      <h2>📋 Survey</h2>
      <p className="text-muted">This page will show survey questions and collect answers.</p>
      <div style={{marginTop:12}}>
        <button className="button">Load Questions</button>
      </div>
    </div>
  )
}
