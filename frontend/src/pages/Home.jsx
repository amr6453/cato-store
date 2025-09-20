import React, {useEffect, useState} from 'react'
import { Link } from 'react-router-dom'

export default function Home(){
  const [products, setProducts] = useState([])
  useEffect(()=>{
    fetch('/api/products/')
      .then(r=>r.json())
      .then(data=>{
        const items = data.results || data
        setProducts(items)
      })
  },[])

  return (
    <div className="max-w-6xl mx-auto p-4">
      <h1 className="text-3xl font-bold mb-6">Cato Store — Demo</h1>
      <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-6">
        {products.map(p=> (
          <Link key={p.id} to={`/product/${p.slug}`} className="bg-white rounded shadow p-4 block">
            <div className="h-40 bg-gray-100 mb-3 flex items-center justify-center">Image</div>
            <h2 className="font-semibold">{p.name}</h2>
            <p className="text-sm text-gray-600">{p.description}</p>
            <div className="mt-3 font-bold">${p.price}</div>
          </Link>
        ))}
      </div>
    </div>
  )
}
