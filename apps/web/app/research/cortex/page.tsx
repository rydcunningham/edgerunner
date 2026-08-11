import type { Metadata } from 'next'
import ProductDossier from '../ProductDossier'

export const metadata: Metadata = {
  title: 'Cortex',
  description:
    'The Edgerunner Research knowledge base — an encyclopedia of the energy-compute stack.',
}

export default function CortexPage() {
  return <ProductDossier slug="cortex" />
}
