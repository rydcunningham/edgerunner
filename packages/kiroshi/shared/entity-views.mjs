/* ============================================================
   KIROSHI · shared entity-view renderers (ESM port)
   ------------------------------------------------------------
   Verbatim port of upstream shared/entity-views.js. The upstream file is an
   IIFE that registers `window.KIROSHI_renderStructure`; this ESM exports
   `renderStructure` directly so React/Vue/etc. consumers can import it:

     import { renderStructure } from "@edgerunner/kiroshi/shared/entity-views";

   Two opt-in `window` hooks are preserved verbatim (no-op if unset):
     · window.KIROSHI.sectionHex  — section→hue map override
     · window.KIROSHI_SYNC()      — call after a render so EN↔汉字 names resync

   Structure grammar (on-brand, deterministic):
     · self node top-center — accent-outlined corner-tick box, bilingual name,
       type micro-label
     · a horizontal bus dropping from the self node
     · each group is a labelled branch (rel label + its node boxes in a column)
     · section-colored left bar per node (type → sectionHex)
     · hairline --k-line-strong connectors

   Names are .k-name spans/texts (data-en/data-zh); the page's EN↔汉字 toggle
   (window.KIROSHI_SYNC) swaps them, so a lang flip needs no re-render.
   ============================================================ */

const NS = "http://www.w3.org/2000/svg";

/* entity type → Cortex section (drives the FIXED sectionHex data hue).
   Mirrors the map used across the identity pages. */
const TYPE_SECTION = {
  conglomerate: "organizations", "chip-designer": "organizations", "cloud-provider": "organizations",
  fab: "organizations", "semi-equipment-maker": "organizations", telecom: "organizations",
  "ai-lab": "organizations", materials: "organizations", supplier: "organizations",
  integrator: "organizations", operator: "organizations", "robotics-manufacturer": "organizations",
  product: "products", architecture: "products", "programming-language": "products",
  system: "products", toolchain: "products",
  person: "people",
  agency: "governance", ministry: "governance", regulator: "governance",
  policy: "governance", standard: "governance",
  cluster: "infrastructure", program: "infrastructure", facility: "infrastructure",
  datacenter: "infrastructure", substation: "infrastructure", transmission: "infrastructure"
};

function esc(s) {
  return String(s == null ? "" : s)
    .replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;").replace(/"/g, "&quot;");
}
function secOf(t) { return TYPE_SECTION[t] || "products"; }
/* which dossier a node opens (mock has two real pages; others fall back to the
   product exemplar — in the real app each entity routes to its own dossier).
   Consumer can override by setting window.KIROSHI.pageFor. */
function pageFor(name) {
  const K = typeof window !== "undefined" && window.KIROSHI;
  if (K && typeof K.pageFor === "function") return K.pageFor(name);
  return name === "Huawei" ? "huawei.html" : "entity.html";
}
function secHex(t) {
  const K = typeof window !== "undefined" && window.KIROSHI;
  return (K && K.sectionHex && K.sectionHex[secOf(t)]) || "#a1a1aa";
}

/* inject the shared structure CSS once (keeps the visual contract in the
   renderer, so pages don't each carry a divergent copy) */
function ensureCSS() {
  if (typeof document === "undefined") return;
  if (document.getElementById("kev-css")) return;
  const st = document.createElement("style");
  st.id = "kev-css";
  st.textContent = [
    ".kev-struct{width:100%;overflow-x:auto}",
    ".kev-struct svg{width:100%;height:auto;display:block;margin:0 auto}",
    ".kev-node{cursor:pointer}",
    ".kev-node.kev-self{cursor:default}",
    ".kev-box{fill:var(--k-bg-panel);stroke:var(--k-line-strong);stroke-width:1;transition:fill var(--k-dur,170ms) var(--k-ease,ease),stroke var(--k-dur,170ms) var(--k-ease,ease)}",
    ".kev-node:hover .kev-box{fill:var(--k-bg-raise);stroke:var(--k-dim)}",
    ".kev-node.kev-self .kev-box{stroke:var(--k-accent);stroke-width:1.7}",
    ".kev-node.kev-self:hover .kev-box{stroke:var(--k-accent)}",
    ".kev-tick{fill:none;stroke:var(--k-tick);stroke-width:1.4}",
    ".kev-node.kev-self .kev-tick{stroke:var(--k-accent);stroke-width:1.7}",
    ".kev-name{fill:var(--k-text);font:700 12px var(--k-font-display);letter-spacing:.03em}",
    ".kev-node.kev-self .kev-name{fill:var(--k-accent);font-size:13.5px;letter-spacing:.05em}",
    ".kev-type{fill:var(--k-faint);font:400 8.5px var(--k-font-mono);letter-spacing:.09em;text-transform:uppercase}",
    ".kev-edge{fill:none;stroke:var(--k-line-strong);stroke-width:1}",
    ".kev-rel{fill:var(--k-dim);font:700 9.5px var(--k-font-display);letter-spacing:.16em;text-transform:uppercase}",
    ".kev-rel .kev-reln{fill:var(--k-faint);font-weight:400;letter-spacing:.06em}"
  ].join("");
  document.head.appendChild(st);
}

export function renderStructure(container, structure) {
  if (!container || !structure) return;
  ensureCSS();
  const self = structure.self || {}, groups = structure.groups || [];

  /* geometry */
  const NW = 168, NH = 48, STUB = 16, COLGAP = 34, ROWGAP = 14,
      padX = 28, padTop = 18, selfNW = 190, selfNH = 54;
  const pitch = STUB + NW + COLGAP;
  const cols = groups.length;
  const spines = [];
  for (let i = 0; i < cols; i++) spines.push(padX + i * pitch);
  const contentRight = cols ? spines[cols - 1] + STUB + NW : padX + NW;
  const W = contentRight + padX;
  const selfCx = W / 2;
  const selfTop = padTop, selfBottom = selfTop + selfNH;
  const busY = selfBottom + 34;
  const relY = busY + 22;
  const firstMidY = busY + 54;
  let maxNodes = 1;
  groups.forEach(function (g) { maxNodes = Math.max(maxNodes, (g.nodes || []).length); });
  const H = firstMidY + (maxNodes - 1) * (NH + ROWGAP) + NH / 2 + 20;

  function ticks(x, y, w, h) {
    const L = 8;
    return '<path class="kev-tick" d="M' + x + ',' + (y + L) + ' V' + y + ' H' + (x + L) +
      ' M' + (x + w - L) + ',' + y + ' H' + (x + w) + ' V' + (y + L) +
      ' M' + (x + w) + ',' + (y + h - L) + ' V' + (y + h) + ' H' + (x + w - L) +
      ' M' + (x + L) + ',' + (y + h) + ' H' + x + ' V' + (y + h - L) + '"/>';
  }
  function nameText(n, x, y) {
    return '<text class="kev-name k-name" x="' + x + '" y="' + y +
      '" data-en="' + esc(n.en) + '" data-zh="' + esc(n.zh || "") + '">' + esc(n.en) + '</text>';
  }
  function box(x, midY, w, h, n, isSelf) {
    const y = midY - h / 2;
    return '<g class="kev-node' + (isSelf ? ' kev-self' : '') + '"' +
      (isSelf ? '' : ' data-href="' + pageFor(n.en) + '"') + ' data-dt="' +
      esc(n.en) + (n.zh ? ' ' + esc(n.zh) : '') + '" data-desc="' +
      esc(n.type || "entity") + (isSelf ? ' · focus (this dossier)' : ' · ' + secOf(n.type) + ' · open →') + '">' +
      '<rect class="kev-box" x="' + x + '" y="' + y + '" width="' + w + '" height="' + h + '"/>' +
      '<rect x="' + x + '" y="' + y + '" width="3" height="' + h + '" fill="' + secHex(n.type) + '"/>' +
      ticks(x, y, w, h) +
      nameText(n, x + 14, midY - 3) +
      (n.type ? '<text class="kev-type" x="' + (x + 14) + '" y="' + (midY + 13) + '">' + esc(n.type) + '</text>' : '') +
      '</g>';
  }

  let s = '<svg viewBox="0 0 ' + W + ' ' + Math.round(H) + '" xmlns="' + NS +
    '" role="img" aria-label="' + esc(self.en || "") + ' structure">';

  /* connectors (under the boxes): self drop · bus · per-group spine + stubs */
  const busLeft = Math.min(cols ? spines[0] : selfCx, selfCx);
  const busRight = Math.max(cols ? spines[cols - 1] : selfCx, selfCx);
  let e = '<path class="kev-edge" d="M' + selfCx + ',' + selfBottom + ' V' + busY + '"/>' +
          '<path class="kev-edge" d="M' + busLeft + ',' + busY + ' H' + busRight + '"/>';
  groups.forEach(function (g, gi) {
    const sx = spines[gi], nodes = g.nodes || [];
    const lastMid = firstMidY + (nodes.length - 1) * (NH + ROWGAP);
    e += '<path class="kev-edge" d="M' + sx + ',' + busY + ' V' + lastMid + '"/>';
    nodes.forEach(function (nd, j) {
      const midY = firstMidY + j * (NH + ROWGAP);
      e += '<path class="kev-edge" d="M' + sx + ',' + midY + ' H' + (sx + STUB) + '"/>';
    });
  });
  s += e;

  /* rel labels + node boxes */
  let body = '';
  groups.forEach(function (g, gi) {
    const nodeX = spines[gi] + STUB, nodes = g.nodes || [];
    body += '<text class="kev-rel" x="' + nodeX + '" y="' + relY + '">' +
      esc(g.rel || "") + ' <tspan class="kev-reln">·' + nodes.length + '</tspan></text>';
    nodes.forEach(function (nd, j) {
      const midY = firstMidY + j * (NH + ROWGAP);
      body += box(nodeX, midY, NW, NH, nd, false);
    });
  });
  /* self last → sits above the bus junction */
  body += box(selfCx - selfNW / 2, selfTop + selfNH / 2, selfNW, selfNH, self, true);

  container.classList.add("kev-struct");
  container.innerHTML = s + body + '</svg>';
  container.onclick = function (ev) {
    const g = ev.target.closest ? ev.target.closest(".kev-node[data-href]") : null;
    if (g) {
      const href = g.getAttribute("data-href");
      const K = typeof window !== "undefined" && window.KIROSHI;
      if (K && typeof K.navigate === "function") K.navigate(href);
      else if (typeof window !== "undefined") window.location.href = href;
    }
  };
  if (typeof window !== "undefined" && window.KIROSHI_SYNC) window.KIROSHI_SYNC();
}
