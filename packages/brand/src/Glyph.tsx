import * as React from "react";

/* The Edgerunner glyph — four bars, bottom one stepped. Geometry is the
   original public/glyph_nobg.svg; fill is currentColor so the parent's
   CSS color decides the hue (red on the site, cyan on cortex). This file
   replaces the per-color asset copies (glyph_nobg / glyph_gray_nobg / …). */
export function Glyph({
  size = 80,
  className,
  title = "Edgerunner",
}: {
  size?: number;
  className?: string;
  title?: string;
}) {
  return (
    <svg
      width={size}
      height={size}
      viewBox="0 0 200 200"
      fill="none"
      xmlns="http://www.w3.org/2000/svg"
      className={className}
      role="img"
      aria-label={title}
    >
      <path fillRule="evenodd" clipRule="evenodd" d="M170 57H30V49H170V57Z" fill="currentColor" />
      <path fillRule="evenodd" clipRule="evenodd" d="M170 79H30V71H170V79Z" fill="currentColor" />
      <path fillRule="evenodd" clipRule="evenodd" d="M170 101H30V93H170V101Z" fill="currentColor" />
      <path
        fillRule="evenodd"
        clipRule="evenodd"
        d="M98.7444 127H30V119H101.256L129.974 139H170V147H127.462L98.7444 127Z"
        fill="currentColor"
      />
    </svg>
  );
}
