import React, {useEffect, useState} from 'react'
import {useParams} from 'react-router-dom'

export default function ProductDetail(){
  const { slug } = useParams()
  const [product, setProduct] = useState(null)

  useEffect(()=>{
    if(!slug) return
    fetch(`/api/products/?slug=${slug}`)
      .then(r=>r.json())
      .then(data=>{
        const items = data.results || data
        setProduct(items[0])
      })
  },[slug])

  if(!product) return <div className="p-4">Loading...</div>

  return (
    <div className="max-w-4xl mx-auto p-4">
      <h1 className="text-2xl font-bold mb-4">{product.name}</h1>
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <div className="h-80 bg-gray-100">Image</div>
        <div>
          <p className="mb-4">{product.description}</p>
          <div className="font-bold text-xl">${product.price}</div>
          <div className="mt-4">
            <button className="px-4 py-2 bg-blue-600 text-white rounded">Add to cart</button>
          </div>
        </div>
      </div>
    </div>
  )
}
