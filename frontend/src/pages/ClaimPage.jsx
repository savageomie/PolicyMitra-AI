import React, { useState } from 'react'
import axios from 'axios'

export default function ClaimPage(){
  const [policyType, setPolicyType] = useState('crop')
  const [guide, setGuide] = useState(null)

  async function loadGuide(){
    try{
      const r = await axios.get('http://127.0.0.1:8000/claim/guide', { params: { policy_type: policyType } })
      setGuide(r.data)
    }catch(err){
      setGuide({ error: err.message })
    }
  }

  return (
    <div className="card">
      <h2>🧾 Claim Guide</h2>
      <select className="input" value={policyType} onChange={e=>setPolicyType(e.target.value)}>
        <option value="crop">Crop</option>
        <option value="health">Health</option>
        <option value="life">Life</option>
      </select>
      <div className="row">
        <button className="button" onClick={loadGuide}>Load Guide</button>
      </div>
      <div style={{marginTop:12}}>
        <pre style={{whiteSpace:'pre-wrap'}}>{guide ? JSON.stringify(guide, null, 2) : 'No guide loaded'}</pre>
      </div>
    </div>
  )
}
