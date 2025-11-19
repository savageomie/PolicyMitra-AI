import React, { useState } from 'react'
import axios from 'axios'

export default function PolicyPage(){
  const [file, setFile] = useState(null)
  const [result, setResult] = useState(null)

  async function upload(){
    if(!file) return
    const fd = new FormData()
    fd.append('pdf', file)
    try{
      const r = await axios.post('http://127.0.0.1:8000/policy/simplify', fd, { headers: { 'Content-Type': 'multipart/form-data' } })
      setResult(r.data)
    }catch(err){
      setResult({ error: err.message })
    }
  }

  return (
    <div className="card">
      <h2>📄 Policy Simplify</h2>
      <input type="file" accept="application/pdf" onChange={e=>setFile(e.target.files[0])} />
      <div style={{marginTop:8}} className="row">
        <button className="button" onClick={upload}>Upload & Simplify</button>
      </div>
      <div style={{marginTop:12}}>
        <pre style={{whiteSpace:'pre-wrap'}}>{result ? JSON.stringify(result, null, 2) : 'No result yet'}</pre>
      </div>
    </div>
  )
}
