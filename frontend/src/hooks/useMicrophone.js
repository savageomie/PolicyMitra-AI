import { useState, useRef, useEffect } from 'react'

// useMicrophone hook
// - start(): request mic permission and begin recording
// - stop(): stop recording and produce audio blob
// - returns { start, stop, recording, audioBlob, error }
export default function useMicrophone() {
  const [recording, setRecording] = useState(false)
  const [audioBlob, setAudioBlob] = useState(null)
  const [error, setError] = useState(null)

  const mediaRecorderRef = useRef(null)
  const streamRef = useRef(null)
  const chunksRef = useRef([])

  const start = async () => {
    setError(null)
    if (recording) return
    try {
      const stream = await navigator.mediaDevices.getUserMedia({ audio: true })
      streamRef.current = stream

      const options = { mimeType: 'audio/webm' }
      const mediaRecorder = new MediaRecorder(stream, options)
      chunksRef.current = []

      mediaRecorder.ondataavailable = (e) => {
        if (e.data && e.data.size > 0) chunksRef.current.push(e.data)
      }

      mediaRecorder.onstop = () => {
        const blob = new Blob(chunksRef.current, { type: 'audio/webm' })
        setAudioBlob(blob)
        // clean up stream tracks
        try {
          if (streamRef.current) {
            streamRef.current.getTracks().forEach((t) => t.stop())
            streamRef.current = null
          }
        } catch (err) {
          // ignore
        }
      }

      mediaRecorderRef.current = mediaRecorder
      mediaRecorder.start()
      setRecording(true)
    } catch (err) {
      // permission denied or not available
      setError(err)
      setRecording(false)
    }
  }

  const stop = () => {
    if (!recording) return
    try {
      if (mediaRecorderRef.current && mediaRecorderRef.current.state !== 'inactive') {
        mediaRecorderRef.current.stop()
      }
    } catch (err) {
      setError(err)
    }
    setRecording(false)
  }

  // cleanup on unmount
  useEffect(() => {
    return () => {
      try {
        if (mediaRecorderRef.current && mediaRecorderRef.current.state !== 'inactive') {
          mediaRecorderRef.current.stop()
        }
      } catch (e) {
        // ignore
      }
      try {
        if (streamRef.current) {
          streamRef.current.getTracks().forEach((t) => t.stop())
        }
      } catch (e) {
        // ignore
      }
    }
  }, [])

  return { start, stop, recording, audioBlob, error }
}
