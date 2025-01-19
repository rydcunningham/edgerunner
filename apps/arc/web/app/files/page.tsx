import React from 'react'
import { Rajdhani } from 'next/font/google'
import Image from 'next/image'

const rajdhani = Rajdhani({
  weight: ['300', '400', '500', '600', '700'],
  subsets: ['latin'],
  display: 'swap',
})

export default function FilesPage() {
  return (
    <div className={`min-h-screen p-8 bg-black text-white ${rajdhani.className}`}>
      <div className="p-4">
        <div className="flex justify-between items-center mb-4">
          <h2 className="text-2xl text-[#5EF6FF]">FILES</h2>
          <div className="flex space-x-4">
            <button className="text-[#5EF6FF] hover:text-white">
              <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" strokeWidth="1.5" stroke="currentColor" className="w-6 h-6">
                <path strokeLinecap="round" strokeLinejoin="round" d="M3 8.25V3h18v5.25M12 21V9m0 0l-3 3m3-3l3 3" />
              </svg>
            </button>
            <button className="text-[#5EF6FF] hover:text-white">
              <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" strokeWidth="1.5" stroke="currentColor" className="w-6 h-6">
                <path strokeLinecap="round" strokeLinejoin="round" d="M21 12.75V21H3v-8.25M12 3v12m0 0l-3-3m3 3l3-3" />
              </svg>
            </button>
          </div>
        </div>
        <div className="bg-black/50 p-4 rounded-lg">
          <div className="flex items-center mb-2">
            <span className="text-[#5EF6FF]">files /</span>
            <input type="text" className="bg-transparent border-none text-white/50 ml-2 flex-grow" placeholder="Search..." />
          </div>
          <div className="grid grid-cols-4 gap-8">
            {/* Example files */}
            {Array.from({ length: 12 }).map((_, index) => (
              <div key={index} className="flex flex-col mt-8 items-center justify-left">
                <Image src="/sd_icon.svg" alt="File Icon" width={48} height={48} className="mb-2 opacity-50 hover:opacity-100 transition-opacity duration-200" />
                <span className="text-white/50 text-xs">file{index + 1}.txt</span>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  )
} 