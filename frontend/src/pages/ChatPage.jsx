import React, { useState } from 'react'
import axios from 'axios'

export default function ChatPage(){
  const [sessionId, setSessionId] = useState('sess1')
  const [message, setMessage] = useState('')
  const [response, setResponse] = useState(null)
  const [loading, setLoading] = useState(false)

  async function send(){
    setLoading(true)
    try{
      const r = await axios.post('http://127.0.0.1:8000/chat', { session_id: sessionId, message, language: 'en' })
      setResponse(r.data)
    }catch(err){
      setResponse({ error: err.message })
    }
    setLoading(false)
  }

  return (
    <div className="card">
      <h2>💬 Chat</h2>
      <div className="row">
        <input className="input" value={sessionId} onChange={e=>setSessionId(e.target.value)} />
        <div className="text-muted">Session ID</div>
      </div>
      <textarea rows={4} className="input" value={message} onChange={e=>setMessage(e.target.value)} placeholder="Type your message..." />
      <div className="row">
        <button className="button" onClick={send} disabled={loading}>{loading ? 'Sending...' : 'Send'}</button>
        <button className="button secondary" onClick={()=>{setMessage(''); setResponse(null)}}>Clear</button>
      </div>
      <div style={{marginTop:12}}>
        <h3>Response</h3>
        <pre style={{whiteSpace:'pre-wrap'}}>{response ? JSON.stringify(response, null, 2) : 'No response yet'}</pre>
      </div>
    </div>
  )
}
