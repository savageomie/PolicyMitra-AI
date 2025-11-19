import React, { useState, useEffect, useRef } from 'react'
import axios from 'axios'
import useMicrophone from '../hooks/useMicrophone'

export default function ChatPage(){
  const [sessionId, setSessionId] = useState('sess1')
  const [message, setMessage] = useState('')
  const [response, setResponse] = useState(null)
  const [loading, setLoading] = useState(false)
  const [transcript, setTranscript] = useState('')

  const { start, stop, recording, audioBlob, error } = useMicrophone()
  const audioRef = useRef(null)

  // When audioBlob becomes available, send it to backend STT
  useEffect(() => {
    if (!audioBlob) return
    const sendAudio = async () => {
      setLoading(true)
      try {
        const form = new FormData()
        // send as recording.webm; backend will accept bytes
        form.append('file', audioBlob, 'recording.webm')
        form.append('language', 'en')
        const sttRes = await axios.post('http://127.0.0.1:8000/stt/transcribe', form, {
          headers: { 'Content-Type': 'multipart/form-data' }
        })
        const text = sttRes.data?.text || ''
        setTranscript(text)
        setMessage(text)

        // now send to chat
        const chatRes = await axios.post('http://127.0.0.1:8000/chat', { session_id: sessionId, message: text, language: 'en' })
        setResponse(chatRes.data)

        // auto-play TTS if available
        if (chatRes.data && chatRes.data.tts_audio && chatRes.data.tts_audio !== 'tts_error') {
          // chatRes.data.tts_audio should be a URL under /audio
          try {
            if (audioRef.current) {
              audioRef.current.src = chatRes.data.tts_audio
              await audioRef.current.play()
            }
          } catch (e) {
            // play may fail silently (autoplay policy)
            console.warn('Auto-play failed', e)
          }
        }

      } catch (err) {
        console.error(err)
        setResponse({ error: err.message || String(err) })
      }
      setLoading(false)
    }
    sendAudio()
  }, [audioBlob])

  async function send(){
    setLoading(true)
    try{
      const r = await axios.post('http://127.0.0.1:8000/chat', { session_id: sessionId, message, language: 'en' })
      setResponse(r.data)
      // play audio if present
      if (r.data && r.data.tts_audio && r.data.tts_audio !== 'tts_error'){
        try{
          if (audioRef.current){
            audioRef.current.src = r.data.tts_audio
            await audioRef.current.play()
          }
        }catch(e){console.warn('Auto-play failed', e)}
      }
    }catch(err){
      setResponse({ error: err.message })
    }
    setLoading(false)
  }

  return (
    <div className="card">
      <h2>💬 Voice Chat</h2>

      <div style={{marginBottom:8}}>
        <input className="input" value={sessionId} onChange={e=>setSessionId(e.target.value)} />
        <div className="text-muted">Session ID</div>
      </div>

      <div style={{ display: 'flex', gap: 8, alignItems: 'center', marginBottom: 8 }}>
        <button className="button" onClick={start} disabled={recording}>🎤 Start</button>
        <button className="button secondary" onClick={stop} disabled={!recording}>⏹ Stop</button>
        <div style={{ marginLeft: 12 }}>
          { error ? <span style={{color:'red'}}>Mic error: {String(error.message || error)}</span> : recording ? <span style={{color:'green'}}>Recording…</span> : <span>Idle</span> }
        </div>
      </div>

      <div>
        <textarea rows={4} className="input" value={message} onChange={e=>setMessage(e.target.value)} placeholder="Type or record a message..." />
      </div>

      <div className="row" style={{marginTop:8}}>
        <button className="button" onClick={send} disabled={loading}>{loading ? 'Sending...' : 'Send'}</button>
        <button className="button secondary" onClick={()=>{setMessage(''); setResponse(null); setTranscript('')}}>Clear</button>
      </div>

      <div style={{marginTop:12}}>
        <h3>Transcription</h3>
        <div style={{whiteSpace:'pre-wrap'}}>{transcript || 'No transcription yet'}</div>
      </div>

      <div style={{marginTop:12}}>
        <h3>AI Response</h3>
        <pre style={{whiteSpace:'pre-wrap'}}>{response ? JSON.stringify(response, null, 2) : 'No response yet'}</pre>
      </div>

      <audio ref={audioRef} />
    </div>
  )
}
