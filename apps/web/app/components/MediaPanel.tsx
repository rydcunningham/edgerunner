'use client'

import { useEffect, useState } from 'react'
import Image from 'next/image'
import type { MediaItem } from '../../lib/content/types'
import { MEDIA_RAIL_SIZES } from '../../lib/layout'

// Media gallery for the right-hand rail of company and product pages.
// One item at a time with prev/next arrows; YouTube stays a click-to-load
// facade so a page with three videos still ships zero third-party JS.

function Slide({ item, onPlay, playing }: { item: MediaItem; playing: boolean; onPlay: () => void }) {
  if (item.kind === 'video') {
    return playing ? (
      <iframe
        className="absolute inset-0 h-full w-full"
        src={`https://www.youtube-nocookie.com/embed/${item.youtubeId}?autoplay=1`}
        title={item.title}
        allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
        allowFullScreen
      />
    ) : (
      <button
        type="button"
        onClick={onPlay}
        className="group absolute inset-0 flex flex-col items-center justify-center gap-3 transition-colors hover:bg-k-raise"
        aria-label={`Play ${item.title}`}
      >
        <span className="flex h-12 w-12 items-center justify-center border border-k-accent text-k-accent transition-colors group-hover:bg-k-accent group-hover:text-k-bg">
          <svg width="14" height="16" viewBox="0 0 14 16" aria-hidden="true">
            <path d="M0 0L14 8L0 16Z" fill="currentColor" />
          </svg>
        </span>
        <span className="px-6 text-center font-display text-sm font-semibold uppercase tracking-[0.16em] text-k-dim">
          {item.title}
        </span>
      </button>
    )
  }

  if (item.fit === 'contain') {
    // Whole image visible, own aspect ratio preserved, letterboxed on true
    // black — deliberately not var(--k-sunken), which is a theme tone, not
    // black on every colorway. Wrapped in an inset div rather than styling
    // the frame directly, so the border/corner-tick chrome around it is
    // unaffected.
    return (
      <div className="absolute inset-0 bg-black flex items-center justify-center">
        <Image
          src={item.src}
          alt={item.alt}
          fill
          sizes={MEDIA_RAIL_SIZES}
          className="object-contain"
          unoptimized={item.kind === 'gif'}
          priority
        />
      </div>
    )
  }

  return (
    <Image
      src={item.src}
      alt={item.alt}
      fill
      sizes={MEDIA_RAIL_SIZES}
      className={`object-cover ${item.position === 'center' ? 'object-center' : 'object-top'}`}
      // GIFs must bypass the optimizer or they render as a still frame.
      unoptimized={item.kind === 'gif'}
      priority
    />
  )
}

export default function MediaPanel({ items }: { items?: MediaItem[] }) {
  const [i, setI] = useState(0)
  const [playing, setPlaying] = useState(false)

  // Never leave a video running when the slide changes.
  useEffect(() => setPlaying(false), [i])

  if (!items?.length) return null

  const total = items.length
  const item = items[i]
  const caption = item.kind === 'video' ? item.caption : item.caption
  const go = (d: number) => setI((prev) => (prev + d + total) % total)

  return (
    // order-first below lg: stacked, the rail would otherwise sit under the
    // whole left column (measured: the /about portrait landed at y=991 of a
    // 1515px page). Above lg it returns to its natural right-column slot.
    <aside className="order-first lg:order-none lg:sticky lg:top-24 self-start">
      <div className="flex items-center gap-3 mb-4">
        <span className="k-label">Media</span>
        <span className="flex-1 h-px bg-k-line-strong" />
        {total > 1 && (
          <>
            <span className="font-mono text-[10px] tracking-[0.1em] text-k-faint tabular-nums">
              {String(i + 1).padStart(2, '0')} / {String(total).padStart(2, '0')}
            </span>
            <div className="flex">
              <button
                type="button"
                onClick={() => go(-1)}
                aria-label="Previous"
                className="border border-k-line px-2.5 py-1 text-k-dim hover:text-k-accent hover:border-k-line-strong transition-colors leading-none"
              >
                ‹
              </button>
              <button
                type="button"
                onClick={() => go(1)}
                aria-label="Next"
                className="border border-k-line border-l-0 px-2.5 py-1 text-k-dim hover:text-k-accent hover:border-k-line-strong transition-colors leading-none"
              >
                ›
              </button>
            </div>
          </>
        )}
      </div>

      <figure>
        <div className="relative aspect-[16/10] overflow-hidden border border-k-line bg-k-sunken">
          <Slide item={item} playing={playing} onPlay={() => setPlaying(true)} />
        </div>
        {caption && (
          <figcaption className="mt-2 font-mono text-[10px] tracking-[0.1em] uppercase text-k-faint">
            {caption}
          </figcaption>
        )}
      </figure>

      {total > 1 && (
        <div className="mt-3 flex gap-1.5" role="tablist" aria-label="Media">
          {items.map((_, n) => (
            <button
              key={n}
              type="button"
              role="tab"
              aria-selected={n === i}
              aria-label={`Item ${n + 1}`}
              onClick={() => setI(n)}
              className={`h-0.5 flex-1 transition-colors ${
                n === i ? 'bg-k-accent' : 'bg-k-line hover:bg-k-line-strong'
              }`}
            />
          ))}
        </div>
      )}
    </aside>
  )
}
