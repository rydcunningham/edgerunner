import fs from "fs";
import path from "path";
import matter from "gray-matter";
import type { PostMeta } from "./types";

// The one markdown loader (replaces the three dead copies in the old repo).
// content/writing holds the local archive; Machine Yearning's canonical home
// is machineyearning.io.

const DIR = path.join(process.cwd(), "content", "writing");

export function getAllPosts(): PostMeta[] {
  if (!fs.existsSync(DIR)) return [];
  return fs
    .readdirSync(DIR)
    .filter((f) => f.endsWith(".md"))
    .map((f) => {
      const slug = f.replace(/\.md$/, "");
      const { data } = matter(fs.readFileSync(path.join(DIR, f), "utf8"));
      return {
        slug,
        title: data.title ?? slug,
        subtitle: data.subtitle,
        date: data.date ?? "",
        excerpt: data.excerpt,
      };
    })
    .sort((a, b) => (a.date < b.date ? 1 : -1));
}

export function getPost(slug: string): (PostMeta & { content: string }) | null {
  const file = path.join(DIR, `${slug}.md`);
  if (!fs.existsSync(file)) return null;
  const { data, content } = matter(fs.readFileSync(file, "utf8"));
  return {
    slug,
    title: data.title ?? slug,
    subtitle: data.subtitle,
    date: data.date ?? "",
    excerpt: data.excerpt,
    content,
  };
}
