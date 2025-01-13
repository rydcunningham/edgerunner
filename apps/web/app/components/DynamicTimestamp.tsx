'use client'

import { useState, useEffect } from 'react'

export default function DynamicTimestamp() {
  const [timestamp, setTimestamp] = useState('')

  useEffect(() => {
    const updateTime = () => {
      const date = new Date()
      const formattedDate = `${date.toISOString().split('T')[0].replace(/-/g, '.')} ${date.toTimeString().split(' ')[0]}`
      setTimestamp(formattedDate)
    }

    // Update immediately
    updateTime()
    
    // Update every second
    const interval = setInterval(updateTime, 1000)

    return () => clearInterval(interval)
  }, [])

  return (
    <div className="fixed left-3 top-32 origin-top-left -rotate-90 z-[100] pointer-events-none">
      <p className="text-[#F75049]/50 text-sm tracking-wider">{timestamp}</p>
    </div>
  )
} 