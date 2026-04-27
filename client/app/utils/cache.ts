import type { ICard } from "~/types";

const CACHE_KEY = "card_cache";

export function readCache(): Map<string, ICard> {
  if (!import.meta.client) return new Map();

  try {
    const raw = localStorage.getItem(CACHE_KEY);
    return raw ? new Map(JSON.parse(raw)) : new Map();
  } catch{
    return new Map();
  }
}

export function writeCache(cache: Map<string, ICard>) {
    if (!import.meta.client) return  
    try {
        localStorage.setItem(CACHE_KEY , JSON.stringify(Array.from(cache.entries())))
    } catch{
        
    }
}
