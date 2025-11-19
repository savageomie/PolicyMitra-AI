import React, { useState } from 'react'
import axios from 'axios'

export default function RecommendPage(){
  const [occupation, setOccupation] = useState('')
  const [income, setIncome] = useState('')
  const [familySize, setFamilySize] = useState('')
  const [result, setResult] = useState(null)

  async function getRecommend(){
    try{
      const r = await axios.post('http://127.0.0.1:8000/recommend', { occupation, income: Number(income), family_size: Number(familySize) })
      setResult(r.data)
    }catch(err){
      setResult({ error: err.message })
    }
  }

  return (
    <div className="card">
      <h2>🔍 Recommend</h2>
      <input className="input" placeholder="Occupation" value={occupation} onChange={e=>setOccupation(e.target.value)} />
      <input className="input" placeholder="Monthly income" value={income} onChange={e=>setIncome(e.target.value)} />
      <input className="input" placeholder="Family size" value={familySize} onChange={e=>setFamilySize(e.target.value)} />
      <div className="row">
        <button className="button" onClick={getRecommend}>Get Recommendations</button>
      </div>
      <div style={{marginTop:12}}>
        <pre style={{whiteSpace:'pre-wrap'}}>{result ? JSON.stringify(result, null, 2) : 'No recommendations yet'}</pre>
      </div>
    </div>
  )
}
