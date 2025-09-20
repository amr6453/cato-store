import React, {useState} from 'react'
import { useNavigate } from 'react-router-dom'

export default function Login(){
  const [username, setUsername] = useState('')
  const [password, setPassword] = useState('')
  const navigate = useNavigate()

  const submit = async e =>{
    e.preventDefault()
    const res = await fetch('/api/auth/login/', { method: 'POST', headers: {'Content-Type':'application/json'}, body: JSON.stringify({ username, password }) })
    if(res.ok){
      const data = await res.json()
      // if backend returns token (DRF Token), store and redirect
      if(data.token){
        localStorage.setItem('token', data.token)
      }
      navigate('/')
    }else{
      alert('Login failed')
    }
  }

  return (
    <div className="max-w-md mx-auto p-4">
      <h2 className="text-xl font-bold mb-4">Login</h2>
      <form onSubmit={submit} className="space-y-3">
        <input className="w-full p-2 border" placeholder="username" value={username} onChange={e=>setUsername(e.target.value)} />
        <input className="w-full p-2 border" placeholder="password" type="password" value={password} onChange={e=>setPassword(e.target.value)} />
        <button className="px-4 py-2 bg-blue-600 text-white rounded">Login</button>
      </form>
    </div>
  )
}
