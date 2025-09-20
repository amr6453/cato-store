import React from 'react'
import { Link } from 'react-router-dom'

export default function NavBar(){
  return (
    <nav className="bg-white shadow mb-6">
      <div className="max-w-6xl mx-auto p-4 flex justify-between items-center">
        <Link to="/" className="font-bold text-xl">Cato Store</Link>
        <div className="space-x-4">
          <Link to="/cart" className="text-sm">Cart</Link>
          <Link to="/login" className="text-sm">Login</Link>
        </div>
      </div>
    </nav>
  )
}
