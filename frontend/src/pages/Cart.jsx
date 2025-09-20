import React, {useState, useEffect} from 'react'

export default function Cart(){
  const [cart, setCart] = useState([])
  useEffect(()=>{
    const raw = localStorage.getItem('cart')
    if(raw) setCart(JSON.parse(raw))
  },[])

  return (
    <div className="max-w-4xl mx-auto p-4">
      <h1 className="text-2xl font-bold mb-4">Cart</h1>
      {cart.length===0 ? <div>Cart is empty</div> : (
        <div className="space-y-3">
          {cart.map((it,idx)=> (
            <div key={idx} className="p-3 bg-white rounded shadow">
              <div className="font-semibold">{it.name}</div>
              <div>Qty: {it.quantity}</div>
            </div>
          ))}
        </div>
      )}
    </div>
  )
}
