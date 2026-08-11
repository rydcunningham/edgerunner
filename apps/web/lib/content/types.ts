export type Sector = "ai" | "deep-tech";

/** An outcome worth surfacing on the card and the company page.
    `short` is what the card shows when the full label would crowd it;
    the detail page always shows `label`, linked to `href` when present. */
export type CompanyStatus = {
  kind: "acquired" | "public";
  label: string;
  short?: string;
  href?: string;
};

/** A preview asset. Images and GIFs are served from public/media/<slug>/;
    videos embed by YouTube id (nothing loads until the poster is clicked).
    Rendered as a stacked right-hand rail, so items need no layout hints. */
export type MediaItem =
  | {
      kind: "image" | "gif";
      src: string;
      alt: string;
      caption?: string;
      /** Crop anchor in the 16:10 frame when fit is "cover". "top" (default)
          keeps a UI screenshot's chrome; "center" suits portraits/photos. */
      position?: "top" | "center";
      /** "cover" (default) fills the frame, cropping. "contain" scales the
          whole image in and letterboxes on black — for art with its own
          aspect ratio (a square portrait, a poster) that cropping would cut. */
      fit?: "cover" | "contain";
    }
  | { kind: "video"; youtubeId: string; title: string; caption?: string };

export type Company = {
  slug: string;
  name: string;
  oneLiner: string;
  body: string;
  round: "Angel" | "Pre-seed" | "Seed";
  year: number;
  sector: Sector;
  domain: string;
  /** Explicit path only where a real mark exists in public/portfolio/grayscale.
      Absent → monogram fallback. Never hand-type a path to another company's file. */
  logo?: string;
  links: { label: string; url: string }[];
  affiliations?: {
    universities?: string[];
    companies?: string[];
    investors?: string[];
  };
  /** Exit / listing state. Absent for private, still-independent companies. */
  status?: CompanyStatus;
  /** Optional previews. Panel is omitted entirely when absent. */
  media?: MediaItem[];
};

export type Product = {
  slug: "cortex" | "overclock";
  name: string;
  tagline: string;
  status: string;
  year: number;
  body: string[];
  media?: MediaItem[];
};

export type ArchiveProject = {
  name: string;
  description: string;
  year: number;
  status: "retired" | "absorbed";
};

export type Update = {
  /** YYYY.MM — ordered newest first in the source array. */
  date: string;
  kind: "product" | "investment" | "press";
  title: string;
  href: string;
  external?: boolean;
};

export type PostMeta = {
  slug: string;
  title: string;
  subtitle?: string;
  date: string;
  excerpt?: string;
};
