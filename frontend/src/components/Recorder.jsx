import React, { useEffect, useState } from 'react'
import useMicrophone from '../hooks/useMicrophone'

export default function Recorder() {
  const { start, stop, recording, audioBlob, error } = useMicrophone()
  const [audioUrl, setAudioUrl] = useState(null)

  useEffect(() => {
    if (audioBlob) {
      const url = URL.createObjectURL(audioBlob)
      setAudioUrl(url)
      return () => URL.revokeObjectURL(url)
    }
    setAudioUrl(null)
  }, [audioBlob])

  return (
    <div style={{ padding: 12, border: '1px solid #eee', borderRadius: 8, maxWidth: 480 }}>
      <h3>Voice Recorder</h3>
      <div style={{ display: 'flex', gap: 8 }}>
        <button onClick={start} disabled={recording}>
          Start
        </button>
        <button onClick={stop} disabled={!recording}>
          Stop
        </button>
      </div>

      <div style={{ marginTop: 12 }}>
        <strong>Status:</strong>{' '}
        {error ? <span style={{ color: 'red' }}>{String(error.message || error)}</span> : recording ? <span style={{ color: 'green' }}>Recording…</span> : <span>Idle</span>}
      </div>

      {audioUrl && (
        <div style={{ marginTop: 12 }}>
          <strong>Playback</strong>
          <div>
            <audio src={audioUrl} controls />
          </div>
          <div style={{ marginTop: 8 }}>
            <a href={audioUrl} download="recording.webm">Download recording</a>
          </div>
        </div>
      )}
    </div>
  )
}
