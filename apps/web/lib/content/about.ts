import type { MediaItem } from "./types";

// Media rail for /about. Replaces the old fixed abstract-texture panel, so
// adding a lab shot, a talk recording, or a conference GIF is a one-line
// append rather than a layout change.
//
// Portrait is square (995×995, from Machine Yearning's Substack profile) —
// "contain" scales the whole image into the 16:10 frame and letterboxes on
// black instead of cover-cropping the top of the head or the chin.
export const aboutMedia: MediaItem[] = [
  {
    kind: "image",
    src: "/media/about/ryan.jpg",
    alt: "Ryan Cunningham",
    caption: "Ryan Cunningham · founder, Edgerunner Ventures",
    fit: "contain",
  },
];
