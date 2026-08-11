'use client'

import { useState, useEffect } from 'react'

export default function DynamicTimestamp() {
  const [timestamp, setTimestamp] = useState('')

  useEffect(() => {
    const updateTime = () => {
      const date = new Date()
      const ms = String(date.getMilliseconds()).padStart(3, '0')
      const formattedDate = `${date.toISOString().split('T')[0].replace(/-/g, '.')} ${date.toTimeString().split(' ')[0]}.${ms}`
      setTimestamp(formattedDate)
    }
    updateTime()
    const interval = setInterval(updateTime, 1)
    return () => clearInterval(interval)
  }, [])

  return (
    // rotate(-90deg) then translateX(-100%), in that exact order, not the
    // reverse: percentages in translate resolve against the element's own
    // static (pre-rotation) width, so this combination always relocates the
    // box's rendered top-left to precisely (left, top) as set below — top
    // is therefore a real offset from the sidebar's top edge regardless of
    // string length, not a tuned value that happens to clear it (top-2 is
    // just breathing room; top-0 would sit it flush against the edge).
    // Composing via separate rotate/translate utility classes won't do
    // this — Tailwind always emits translate before rotate, the other
    // composition order, which re-clips upward.
    <div
      className="fixed left-3 top-2 z-[100] pointer-events-none"
      style={{ transformOrigin: 'top left', transform: 'rotate(-90deg) translateX(-100%)' }}
    >
      <p className="text-k-accent/50 text-sm tracking-wider font-mono whitespace-nowrap">
        {timestamp}
      </p>
    </div>
  )
}
