// Shared geometry for the two-column pages (research dossiers, portfolio
// company pages): content left, media rail right.
//
// The split lives here so both pages stay in step and it's one edit to
// change. 60:40 over 75:25 because at this page width 75:25 leaves the media
// column ~280px — too small for a screenshot to read as a preview. At 60:40
// the rail is ~475px while the prose column still exceeds its 672px measure.
// To try 75:25, change the grid-cols track below to `75fr_25fr`.

export const TWO_COL_PAGE = 'max-w-[1280px]'

export const TWO_COL_GRID =
  'mt-8 grid grid-cols-1 items-start gap-x-24 gap-y-12 lg:grid-cols-[60fr_40fr]'

/** Matches the rail's rendered width at TWO_COL_PAGE for next/image sizing. */
export const MEDIA_RAIL_SIZES = '(max-width: 1024px) 100vw, 480px'
