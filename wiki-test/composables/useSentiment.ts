export type SentimentLabel = 'positive' | 'negative' | 'neutral'

const positiveWords = new Set([
  'win','wins','won','success','secure','growth','improve','improved','improves','record','milestone','peace','ceasefire','cease-fire','joins','member','elected','agreed','agreement','rescued','saves','saved','approval','approves','deal','aid','relief','support','recovery'
])

const negativeWords = new Set([
  'kill','killed','dead','deaths','dies','death','massacre','massacres','storm','hurricane','flood','landslide','stampede','riot','riots','protests','protest','war','conflict','airstrike','attack','attacks','crash','crashes','injured','injures','injury','arrest','arrested','fire','fires','explosion','explosions','collapse','crimes','crime','charged','sentence','sentences','curfew'
])

export function useSentiment() {
  function score(text: string) {
    const tokens = (text || '').toLowerCase().split(/[^a-zA-Z]+/).filter(Boolean)
    let pos = 0, neg = 0
    for (const t of tokens) {
      if (positiveWords.has(t)) pos++
      if (negativeWords.has(t)) neg++
    }
    const score = pos - neg
    let label: SentimentLabel = 'neutral'
    if (score > 0) label = 'positive'
    else if (score < 0) label = 'negative'
    return { score, label, pos, neg }
  }

  function analyze(texts: string[]) {
    const totals = { pos: 0, neg: 0 }
    let sum = 0
    for (const t of texts) {
      const s = score(t)
      totals.pos += s.pos
      totals.neg += s.neg
      sum += s.score
    }
    const label: SentimentLabel = sum > 0 ? 'positive' : sum < 0 ? 'negative' : 'neutral'
    return { score: sum, label }
  }

  return { score, analyze }
}
