import { defineEventHandler, getQuery, setResponseHeader } from 'h3'
import { $fetch } from 'ofetch'
import * as cheerio from 'cheerio'

function toPortalDate(dateStr?: string) {
  const now = dateStr ? new Date(dateStr) : new Date()
  const y = now.getUTCFullYear()
  const monthNames = [
    'January','February','March','April','May','June','July','August','September','October','November','December'
  ]
  const m = monthNames[now.getUTCMonth()]
  const d = now.getUTCDate()
  return `${y}_${m}_${d}`
}

export default defineEventHandler(async (event) => {
  const { date, limit } = getQuery(event) as { date?: string; limit?: string }
  const portalDate = toPortalDate(date)
  const pageTitle = `Portal:Current_events/${portalDate}`

  const url = 'https://en.wikipedia.org/w/api.php'
  const params = {
    action: 'parse',
    format: 'json',
    formatversion: '2',
    prop: 'text',
    page: pageTitle,
    origin: '*'
  }

  const { parse } = await $fetch(url, { params }) as any
  const html: string = parse?.text ?? ''
  const $ = cheerio.load(html)

  // Select list items under .current-events-content (nested in category sections)
  const items: Array<{ title: string; summary: string; url: string; date: string }> = []
  $('.current-events-content ul > li').each((_, el) => {
    const $li = $(el)
    // Skip nested list items (those are sub-bullets)
    if ($li.parent().parent().is('li')) return
    
    const text = $li.text().replace(/\s+/g, ' ').trim()
    const a = $li.find('a[href^="/wiki/"]:not([href*="redlink"])').first()
    const href = a.attr('href') || ''
    const url = href ? `https://en.wikipedia.org${href}` : `https://en.wikipedia.org/wiki/${encodeURIComponent(pageTitle)}`
    
    // Extract a cleaner title (first sentence or first link text)
    let title = a.text() || text.split('.')[0] || text.substring(0, 100)
    title = title.trim()
    
    if (text && text.length > 20) { // Filter out very short items
      items.push({
        title,
        summary: text.substring(0, 300), // Limit summary length
        url,
        date: (date || new Date().toISOString().slice(0,10))
      })
    }
  })

  const n = Math.min(parseInt(limit || '10', 10) || 10, items.length)
  const result = items.slice(0, n)

  setResponseHeader(event, 'Cache-Control', 'public, max-age=300, s-maxage=300')
  return { date: date || null, page: pageTitle, count: result.length, items: result }
})
