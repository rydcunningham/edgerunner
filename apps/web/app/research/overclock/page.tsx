import type { Metadata } from 'next'
import ProductDossier from '../ProductDossier'

export const metadata: Metadata = {
  title: 'Overclock',
  description: 'Energy-compute digital twins. Compose a stack, run the Sovereign Equation.',
}

export default function OverclockPage() {
  return <ProductDossier slug="overclock" />
}
