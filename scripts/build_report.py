"""Build the Avaloka hackathon report page (report/index.html).

Single source of truth for every number, verified 20 Nov 2026 against
expected_findings.md, the Avaloka goal_analysis.json files, and the raw
World Bank CSV (re-checked from data/worldbank_health_panel.csv).
Charts are inline SVG — no CDN, no JS dependency, renders anywhere.
"""
import math
import os

# ---------------------------------------------------------------- data
# Bands: (label, mean spend in band [2023, PPP $/person], mean life exp, n)
# Source: data/wb_2023_snapshot.csv + avaloka-analysis/3f4239cb0ea1/goal_analysis.json
BANDS = [
    ("$0–250", 151, 65.0, 45),
    ("$250–500", 363, 67.5, 17),
    ("$500–1,000", 738, 72.2, 30),
    ("$1,000–2,000", 1422, 74.1, 37),
    ("$2,000–4,000", 2893, 77.5, 30),
    ("$4,000–8,000", 6004, 82.6, 25),
    ("$8,000+", 9762, 83.0, 8),
]

# (country, spend 2023 PPP $/person, life expectancy 2023, yrs per $1,000)
# Source: expected_findings.md, re-verified from the raw CSV.
COUNTRIES = [
    ("China", 1487, 78.0, 52.43),
    ("Costa Rica", 1928, 80.8, 41.91),
    ("South Korea", 4798, 83.4, 17.39),
    ("Japan", 5365, 84.0, 15.66),
    ("United Kingdom", 6365, 81.2, 12.76),
    ("Germany", 8306, 81.0, 9.76),
    ("Switzerland", 10602, 84.2, 7.94),
    ("United States", 13473, 78.4, 5.82),
]

# Global (unweighted) mean life expectancy by year.
# Source: avaloka-analysis/25e4a968d919/goal_analysis.json (monthly_values).
TREND = [
    (2000, 67.6), (2001, 67.9), (2002, 68.2), (2003, 68.6), (2004, 68.9),
    (2005, 69.2), (2006, 69.5), (2007, 69.9), (2008, 70.2), (2009, 70.3),
    (2010, 70.8), (2011, 71.1), (2012, 71.5), (2013, 71.8), (2014, 71.9),
    (2015, 72.1), (2016, 72.3), (2017, 72.5), (2018, 72.9), (2019, 73.0),
    (2020, 72.5), (2021, 71.8), (2022, 73.1), (2023, 73.8),
]

TEAL = "#0e7c6b"
TEAL_DARK = "#0a5c50"
INK = "#1c2430"
MUTED = "#5b6774"
GRID = "#e3e6ea"
RED = "#c0392b"
AMBER = "#b7791f"


def saturation_chart() -> str:
    """Log-x line chart: mean life expectancy vs health spend per band."""
    W, H = 900, 430
    L, R, T, B = 58, 34, 30, 58
    x0, x1 = math.log10(100), math.log10(20000)
    y0, y1 = 60.0, 86.0

    def X(v):
        return L + (math.log10(v) - x0) / (x1 - x0) * (W - L - R)

    def Y(v):
        return T + (y1 - v) / (y1 - y0) * (H - T - B)

    p = [f'<svg viewBox="0 0 {W} {H}" role="img" '
         f'aria-label="Line chart: mean life expectancy rises steeply with health spending, then flattens after about 4,000 dollars per person.">']
    # gridlines + y labels
    for yv in (65, 70, 75, 80, 85):
        p.append(f'<line x1="{L}" y1="{Y(yv):.1f}" x2="{W-R}" y2="{Y(yv):.1f}" stroke="{GRID}"/>')
        p.append(f'<text x="{L-10}" y="{Y(yv)+4:.1f}" text-anchor="end" font-size="13" fill="{MUTED}">{yv}</text>')
    p.append(f'<text x="{L-44}" y="{T-12}" font-size="12" fill="{MUTED}">years</text>')
    # x ticks
    for xv, lab in ((100, "$100"), (250, "$250"), (500, "$500"), (1000, "$1k"),
                    (2000, "$2k"), (4000, "$4k"), (8000, "$8k"), (16000, "$16k")):
        p.append(f'<line x1="{X(xv):.1f}" y1="{H-B}" x2="{X(xv):.1f}" y2="{H-B+6}" stroke="{MUTED}"/>')
        p.append(f'<text x="{X(xv):.1f}" y="{H-B+22}" text-anchor="middle" font-size="13" fill="{MUTED}">{lab}</text>')
    p.append(f'<text x="{(L+W-R)/2:.0f}" y="{H-6}" text-anchor="middle" font-size="12" fill="{MUTED}">Health spending per person, 2023 (PPP $, log scale) — dot placed at each band\u2019s mean spend</text>')
    # $4,000 ceiling line
    p.append(f'<line x1="{X(4000):.1f}" y1="{T}" x2="{X(4000):.1f}" y2="{H-B}" stroke="{AMBER}" stroke-dasharray="6 5" stroke-width="1.6"/>')
    p.append(f'<text x="{X(4000)+8:.1f}" y="{T+16}" font-size="13" font-weight="700" fill="{AMBER}">the $4,000 ceiling</text>')
    p.append(f'<text x="{X(4000)+8:.1f}" y="{T+34}" font-size="12" fill="{AMBER}">doubling spend past here: +0.4 yrs</text>')
    # line + area
    pts = [(X(s), Y(le)) for _, s, le, _ in BANDS]
    path = "M " + " L ".join(f"{x:.1f},{y:.1f}" for x, y in pts)
    area = path + f" L {pts[-1][0]:.1f},{H-B} L {pts[0][0]:.1f},{H-B} Z"
    p.append(f'<path d="{area}" fill="{TEAL}" opacity="0.08"/>')
    p.append(f'<path d="{path}" fill="none" stroke="{TEAL}" stroke-width="3" stroke-linejoin="round"/>')
    for (lab, s, le, n), (x, y) in zip(BANDS, pts):
        p.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="6" fill="#fff" stroke="{TEAL}" stroke-width="3"/>')
        p.append(f'<text x="{x:.1f}" y="{y-14:.1f}" text-anchor="middle" font-size="13" font-weight="700" fill="{INK}">{le:.1f} yrs</text>')
        p.append(f'<text x="{x:.1f}" y="{y+26:.1f}" text-anchor="middle" font-size="11.5" fill="{MUTED}">n={n}</text>')
    p.append("</svg>")
    return "".join(p)


def trend_chart() -> str:
    """Line chart: global mean life expectancy 2000-2023 with the COVID dip."""
    W, H = 900, 360
    L, R, T, B = 58, 34, 34, 52
    y0, y1 = 66.0, 75.0

    def X(yr):
        return L + (yr - 2000) / 23 * (W - L - R)

    def Y(v):
        return T + (y1 - v) / (y1 - y0) * (H - T - B)

    p = [f'<svg viewBox="0 0 {W} {H}" role="img" '
         f'aria-label="Line chart: global mean life expectancy rose from 67.6 years in 2000 to 73.8 in 2023, with a dip in 2020-2021.">']
    for yv in (67, 69, 71, 73, 75):
        p.append(f'<line x1="{L}" y1="{Y(yv):.1f}" x2="{W-R}" y2="{Y(yv):.1f}" stroke="{GRID}"/>')
        p.append(f'<text x="{L-10}" y="{Y(yv)+4:.1f}" text-anchor="end" font-size="13" fill="{MUTED}">{yv}</text>')
    for yr in range(2000, 2024, 2):
        p.append(f'<text x="{X(yr):.1f}" y="{H-B+22}" text-anchor="middle" font-size="12.5" fill="{MUTED}">{yr}</text>')
    pts = [(X(yr), Y(v)) for yr, v in TREND]
    path = "M " + " L ".join(f"{x:.1f},{y:.1f}" for x, y in pts)
    area = path + f" L {pts[-1][0]:.1f},{H-B} L {pts[0][0]:.1f},{H-B} Z"
    p.append(f'<path d="{area}" fill="{TEAL}" opacity="0.08"/>')
    p.append(f'<path d="{path}" fill="none" stroke="{TEAL}" stroke-width="2.6" stroke-linejoin="round"/>')
    # endpoints
    p.append(f'<circle cx="{pts[0][0]:.1f}" cy="{pts[0][1]:.1f}" r="5" fill="#fff" stroke="{TEAL}" stroke-width="3"/>')
    p.append(f'<text x="{pts[0][0]+10:.1f}" y="{pts[0][1]-10:.1f}" font-size="13" font-weight="700" fill="{INK}">67.6 yrs (2000)</text>')
    p.append(f'<circle cx="{pts[-1][0]:.1f}" cy="{pts[-1][1]:.1f}" r="5" fill="#fff" stroke="{TEAL}" stroke-width="3"/>')
    p.append(f'<text x="{pts[-1][0]-10:.1f}" y="{pts[-1][1]-12:.1f}" text-anchor="end" font-size="13" font-weight="700" fill="{INK}">73.8 yrs (2023)</text>')
    # COVID dip annotation
    dx, dy = X(2021), Y(71.8)
    p.append(f'<circle cx="{dx:.1f}" cy="{dy:.1f}" r="5" fill="{RED}" stroke="#fff" stroke-width="2"/>')
    p.append(f'<text x="{W-R}" y="{dy+30:.1f}" text-anchor="end" font-size="12.5" font-weight="700" fill="{RED}">COVID-19: the only reversal in 24 years</text>')
    p.append(f'<text x="{W-R}" y="{dy+47:.1f}" text-anchor="end" font-size="12.5" fill="{RED}">73.0 \u2192 71.8 yrs (2019\u20132021), recovered by 2022</text>')
    p.append("</svg>")
    return "".join(p)


def efficiency_bars() -> str:
    """Horizontal bars: years of life per $1,000 of health spending (2023)."""
    W = 900
    rows = COUNTRIES  # already sorted high -> low
    row_h, top = 40, 14
    H = top + len(rows) * row_h + 30
    L, R = 150, 70
    vmax = 55.0

    def bw(v):
        return v / vmax * (W - L - R)

    p = [f'<svg viewBox="0 0 {W} {H}" role="img" '
         f'aria-label="Bar chart: years of life per 1,000 dollars of health spending, 2023. China 52.4, Costa Rica 41.9, South Korea 17.4, Japan 15.7, United Kingdom 12.8, Germany 9.8, Switzerland 7.9, United States 5.8.">']
    for i, (c, spend, le, eff) in enumerate(rows):
        y = top + i * row_h
        color = RED if c == "United States" else TEAL
        p.append(f'<text x="{L-12}" y="{y+19}" text-anchor="end" font-size="14" font-weight="600" fill="{INK}">{c}</text>')
        p.append(f'<rect x="{L}" y="{y+6}" width="{bw(eff):.1f}" height="22" rx="4" fill="{color}" opacity="0.92"/>')
        p.append(f'<text x="{L+bw(eff)+10:.1f}" y="{y+23}" font-size="14" font-weight="700" fill="{color}">{eff:.2f}</text>')
    p.append(f'<text x="{L}" y="{H-6}" font-size="12" fill="{MUTED}">Years of life per $1,000 of health spending, 2023 \u00b7 countries with population &gt; 5 million</text>')
    p.append("</svg>")
    return "".join(p)


# ---------------------------------------------------------------- html
def band_rows() -> str:
    out = []
    for lab, spend, le, n in BANDS:
        hl = ' class="hl"' if lab in ("$4,000–8,000", "$8,000+") else ""
        out.append(f'<tr{hl}><td>{lab}</td><td>${spend:,}</td><td><strong>{le:.1f}</strong></td><td>{n}</td></tr>')
    return "".join(out)


def country_rows() -> str:
    out = []
    for c, spend, le, eff in sorted(COUNTRIES, key=lambda r: -r[1]):
        cls = ' class="usa"' if c == "United States" else ""
        out.append(f'<tr{cls}><td>{c}</td><td>${spend:,}</td><td>{le:.1f}</td><td><strong>{eff:.2f}</strong></td></tr>')
    return "".join(out)


HTML = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>The $4,000 Ceiling — Years of Life per Health Dollar | Manesh Sunil Jadhav</title>
<meta name="description" content="Past about $4,000 per person, doubling health spending buys just 0.4 more years of life. An Avaloka analysis of 217 countries, 2000–2023.">
<style>
  :root { --ink:#1c2430; --muted:#5b6774; --teal:#0e7c6b; --teal-dark:#0a5c50;
          --red:#c0392b; --amber:#b7791f; --bg:#faf9f7; --card:#ffffff; --line:#e3e6ea; }
  * { box-sizing:border-box; }
  body { margin:0; background:var(--bg); color:var(--ink);
         font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,Helvetica,Arial,sans-serif;
         line-height:1.65; font-size:17px; }
  .wrap { max-width:960px; margin:0 auto; padding:0 20px 64px; }
  header.hero { background:linear-gradient(160deg,#0a2e29 0%,#0e7c6b 78%,#12937f 100%);
                color:#fff; padding:56px 0 44px; }
  .kicker { font-size:12.5px; letter-spacing:.22em; text-transform:uppercase; opacity:.85; font-weight:700; }
  h1 { font-size:clamp(2.4rem,6vw,3.9rem); line-height:1.05; margin:14px 0 10px; letter-spacing:-.02em; }
  .lede { font-size:clamp(1.15rem,2.6vw,1.45rem); line-height:1.45; max-width:44em; opacity:.96; margin:0 0 8px; }
  .question { font-size:1.05rem; opacity:.85; font-style:italic; }
  .byline { margin-top:26px; padding:16px 18px; background:rgba(255,255,255,.12);
            border:1px solid rgba(255,255,255,.25); border-radius:10px; font-size:.95rem; line-height:1.55; }
  .byline strong { font-size:1.05rem; }
  .byline a { color:#fff; }
  .stats { display:grid; grid-template-columns:repeat(auto-fit,minmax(150px,1fr)); gap:12px; margin:28px 0 8px; }
  .stat { background:var(--card); border:1px solid var(--line); border-radius:10px; padding:16px 18px; }
  .stat b { display:block; font-size:1.7rem; line-height:1.1; color:var(--teal-dark); }
  .stat span { font-size:.85rem; color:var(--muted); }
  h2 { font-size:1.65rem; margin:52px 0 6px; letter-spacing:-.01em; }
  h2 .num { color:var(--teal); margin-right:8px; }
  .sub { color:var(--muted); margin:0 0 18px; font-size:1.02rem; }
  .card { background:var(--card); border:1px solid var(--line); border-radius:12px; padding:22px 22px 14px; margin:16px 0; }
  .card svg { width:100%; height:auto; display:block; }
  .caption { font-size:.85rem; color:var(--muted); margin:10px 0 4px; }
  table { width:100%; border-collapse:collapse; margin:14px 0; font-size:.97rem; }
  th { text-align:left; color:var(--muted); font-size:.82rem; text-transform:uppercase;
       letter-spacing:.06em; border-bottom:2px solid var(--line); padding:8px 10px; }
  td { padding:9px 10px; border-bottom:1px solid var(--line); }
  tr.hl td { background:#fdf6e3; }
  tr.usa td { background:#fdecea; }
  .callout { border-left:4px solid var(--teal); background:#eef7f4; padding:16px 20px;
             border-radius:0 10px 10px 0; margin:20px 0; }
  .callout.red { border-color:var(--red); background:#fdecea; }
  .callout.amber { border-color:var(--amber); background:#fdf6e3; }
  .callout p { margin:0; }
  .grid2 { display:grid; grid-template-columns:repeat(auto-fit,minmax(240px,1fr)); gap:14px; margin:16px 0; }
  .mini { background:var(--card); border:1px solid var(--line); border-radius:10px; padding:16px 18px; }
  .mini b { display:block; font-size:1.5rem; color:var(--teal-dark); line-height:1.15; }
  .mini span { font-size:.88rem; color:var(--muted); }
  .twrap { overflow-x:auto; }
  code { background:#eef1f3; padding:1px 6px; border-radius:5px; font-size:.9em; }
  ul { padding-left:22px; }
  li { margin:6px 0; }
  footer { margin-top:56px; padding-top:22px; border-top:1px solid var(--line);
           color:var(--muted); font-size:.9rem; }
  footer a { color:var(--teal-dark); }
  @media (max-width:640px){ .card{padding:16px 12px 10px;} body{font-size:16px;} }
</style>
</head>
<body>
<header class="hero"><div class="wrap" style="padding-bottom:0">
  <div class="kicker">Avaloka Hackathon &middot; November 2026 &middot; Analysis by Avaloka CLI v1.6</div>
  <h1>The $4,000 Ceiling</h1>
  <p class="lede">Past about $4,000 of health spending per person, doubling the money buys just <strong>+0.4&nbsp;years</strong> of life. The richest health system on Earth buys the least life per dollar &mdash; and India is quietly beating its income peers.</p>
  <p class="question">The question: which countries get the most years of life per health dollar &mdash; and where does India stand?</p>
  <div class="byline">
    <strong>Manesh Sunil Jadhav</strong><br>
    Final-year Diploma in AI &amp; ML, Government Polytechnic Mumbai<br>
    Best Undergraduate, Google Mumbai Data Challenge (Google + Zindi), November 2026<br>
    <a href="https://github.com/maneshdev-cloud">github.com/maneshdev-cloud</a> &middot;
    <a href="https://www.linkedin.com/in/manesh-jadhav04">linkedin.com/in/manesh-jadhav04</a>
  </div>
</div></header>

<main class="wrap">
  <div class="stats">
    <div class="stat"><b>217</b><span>countries, 2000&ndash;2023</span></div>
    <div class="stat"><b>5,208</b><span>country-year rows</span></div>
    <div class="stat"><b>192</b><span>countries in the 2023 snapshot</span></div>
    <div class="stat"><b>r = 0.655</b><span>spending vs life expectancy</span></div>
    <div class="stat"><b>R&sup2; 0.776</b><span>random-forest holdout</span></div>
  </div>

  <h2><span class="num">01</span> The saturation curve</h2>
  <p class="sub">Mean life expectancy by 2023 health-spending band (PPP $ per person). The curve climbs fast, then stops.</p>
  <div class="card">__SAT_CHART__
    <p class="caption">Each dot is a spending band&rsquo;s mean life expectancy, placed at that band&rsquo;s mean spend. n = countries in the band. Source: World Bank, 2023 (n = 192 countries).</p>
  </div>
  <div class="twrap"><table>
    <tr><th>Health spend / person (PPP $, 2023)</th><th>Mean spend in band</th><th>Mean life expectancy</th><th>Countries</th></tr>
    __BAND_ROWS__
  </table></div>
  <div class="callout amber"><p><strong>The ceiling:</strong> countries spending $4,000&ndash;8,000 per person live 82.6 years on average; countries spending over $8,000 live 83.0. Doubling the money past ~$4,000 buys <strong>+0.4 years</strong>. Below the ceiling, every extra dollar still matters enormously &mdash; moving from the $0&ndash;250 band to the $500&ndash;1,000 band is worth +7.2 years.</p></div>

  <h2><span class="num">02</span> The USA paradox</h2>
  <p class="sub">The United States spends more on health per person than any country on Earth &mdash; $13,473 in 2023 &mdash; and gets 78.4 years of life for it. Among 123 countries with population over 5 million, it is <strong>dead last</strong> in years of life per $1,000 spent.</p>
  <div class="card">__EFF_BARS__
    <p class="caption">Efficiency here is measured only among large countries (population &gt; 5 million), so the comparison is between real health systems &mdash; not against tiny or war-affected states. A raw global ranking would be dominated by the poorest countries, where a tiny spend divided into any lifespan looks &ldquo;efficient&rdquo;. That is poverty, not efficiency, and this report does not headline it.</p>
  </div>
  <div class="twrap"><table>
    <tr><th>Country</th><th>Health spend / person (PPP $, 2023)</th><th>Life expectancy (2023)</th><th>Years per $1,000</th></tr>
    __COUNTRY_ROWS__
  </table></div>
  <div class="callout red"><p><strong>Japan spends 40% of what the USA spends &mdash; and lives 5.7 years longer.</strong> Costa Rica spends one-seventh of the USA&rsquo;s budget and lives 2.4 years longer. South Korea spends $4,798 per person and reaches 83.4 years. The two biggest spenders on the planet, the USA and Switzerland, are the two least efficient large countries in the dataset.</p></div>

  <h2><span class="num">03</span> Where India stands</h2>
  <p class="sub">India spends $346 per person on health (2023) and reaches 72.0 years of life. Judged against countries at its own income level, India is ahead of the pack.</p>
  <div class="grid2">
    <div class="mini"><b>$346</b><span>health spend per person, 2023 (PPP $)</span></div>
    <div class="mini"><b>72.0 yrs</b><span>life expectancy, 2023</span></div>
    <div class="mini"><b>#14 of 30</b><span>by life expectancy among income-matched peers (GDP per capita PPP 0.7&times;&ndash;1.4&times; India&rsquo;s $9,853)</span></div>
    <div class="mini"><b>+2.0 yrs</b><span>above the peer mean of 70.0 years</span></div>
  </div>
  <p>India&rsquo;s position is genuinely good for its income &mdash; but the peer table also names the gap: <strong>Bangladesh reaches 74.7 years</strong> at a similar income, 2.7 years ahead of India. The lesson of the ceiling cuts both ways for India: there is still enormous life to be bought cheaply below $4,000 per person, and the countries to learn from are the efficient ones &mdash; Japan, South Korea, Costa Rica &mdash; not the biggest spenders.</p>

  <h2><span class="num">04</span> Twenty-four years of progress</h2>
  <p class="sub">The world&rsquo;s average life expectancy rose from 67.6 years in 2000 to 73.8 in 2023 &mdash; a gain of 6.2 years in a generation.</p>
  <div class="card">__TREND_CHART__
    <p class="caption">Unweighted mean life expectancy across countries, each year 2000&ndash;2023. Every country counts equally, so this is the average country&rsquo;s trajectory &mdash; not a population-weighted global figure.</p>
  </div>

  <h2><span class="num">05</span> Correlation &mdash; and the GDP twist</h2>
  <p class="sub">Health spending correlates with life expectancy at Pearson r = 0.655 across all 5,208 country-years. But so does plain national wealth.</p>
  <div class="grid2">
    <div class="mini"><b>r = 0.655</b><span>health spend per capita (PPP) vs life expectancy</span></div>
    <div class="mini"><b>r = 0.651</b><span>GDP per capita (PPP) vs life expectancy</span></div>
  </div>
  <p>GDP per capita predicts life expectancy about as well as health spending does. That reframes the whole question: the money itself is not the differentiator &mdash; <strong>how a country spends it is</strong>. Two countries at similar income can sit years apart in lifespan. The ceiling, the USA paradox and the Japan/Costa Rica contrast are all the same story: beyond a point, outcomes come from the system, not the budget.</p>

  <h2><span class="num">06</span> The model</h2>
  <p class="sub">A random-forest model trained with Avaloka to predict life expectancy from spending, GDP, population and year.</p>
  <div class="grid2">
    <div class="mini"><b>R&sup2; 0.7762</b><span>holdout (time-based split: 4,166 train / 1,042 test rows)</span></div>
    <div class="mini"><b>CV R&sup2; 0.846 &plusmn; 0.051</b><span>cross-validated; beats the mean baseline (&minus;0.106)</span></div>
    <div class="mini"><b>R&sup2; 0.1139</b><span>linear regression on the same data &mdash; a straight line cannot explain this relationship</span></div>
    <div class="mini"><b>PASS &middot; level 4/4</b><span>Avaloka validation: no target leakage, stable across folds</span></div>
  </div>
  <p>The model comparison is the saturation story in miniature: linear regression manages R&sup2; 0.11, while a random forest that can bend reaches 0.78. Life expectancy does not rise in a straight line with spending &mdash; it curves, and then it flattens.</p>

  <h2><span class="num">07</span> Methodology</h2>
  <ul>
    <li><strong>Data:</strong> World Bank Open Data API (no key required), five indicators joined on country + year &mdash; life expectancy (SP.DYN.LE00.IN), health expenditure per capita PPP (SH.XPD.CHEX.PP.CD) and current US$ (SH.XPD.CHEX.PC.CD), GDP per capita PPP (NY.GDP.PCAP.PP.CD), population (SP.POP.TOTL). 217 real countries, 2000&ndash;2023, 5,208 rows, 4,415 complete. World Bank aggregates (World, High income, regions) were filtered out.</li>
    <li><strong>Analysis:</strong> Avaloka open-source CLI v1.6 (<code>avaloka analyze</code> + <code>avaloka train</code>), deterministic goal-specific calculations &mdash; group comparison, Pearson correlation, time trend, and a random-forest regression with a time-based holdout. No LLM-generated figures anywhere in this report.</li>
    <li><strong>Verification:</strong> every number Avaloka reported was independently re-computed from the raw CSV with a separate script (<code>scripts/verify_numbers.py</code> in the repo). All headline figures matched exactly.</li>
    <li><strong>Reproduce:</strong> <code>python scripts/fetch_worldbank.py</code> re-fetches the data; the Avaloka commands are listed in the repo README.</li>
  </ul>

  <h2><span class="num">08</span> Limitations</h2>
  <ul>
    <li><strong>Ecological data:</strong> country averages hide within-country inequality &mdash; a national mean says nothing about who inside a country lives longest.</li>
    <li><strong>PPP comparability:</strong> purchasing-power-parity dollars make spending comparable across countries, but PPP conversion is approximate, especially for health services.</li>
    <li><strong>Unweighted means:</strong> band and trend averages count each country equally; populous countries do not dominate. Population-weighted figures would differ.</li>
    <li><strong>Correlation &ne; causation:</strong> r = 0.655 describes association. Health spending, wealth, education, sanitation and diet move together; this analysis does not separate their effects.</li>
    <li><strong>Coverage:</strong> 2023 figures reflect the latest World Bank data; 25 of 217 countries lack a 2023 spending or life-expectancy value and are absent from the snapshot (n = 192).</li>
  </ul>

  <footer>
    <p><strong>Manesh Sunil Jadhav</strong> &middot; Final-year Diploma in AI &amp; ML, Government Polytechnic Mumbai &middot; Best Undergraduate, Google Mumbai Data Challenge (Google + Zindi), Nov 2026</p>
    <p>Built for the Avaloka Hackathon (Guruvai Sciences), November 2026, using the open-source <a href="https://github.com/guruvaidev/avaloka">Avaloka CLI</a>. Data: <a href="https://data.worldbank.org/">World Bank Open Data</a>. Full data, code and Avaloka outputs: <a href="https://github.com/maneshdev-cloud/avaloka-health-dollars">github.com/maneshdev-cloud/avaloka-health-dollars</a></p>
  </footer>
</main>
</body>
</html>
"""


def main() -> None:
    html = (HTML
            .replace("__SAT_CHART__", saturation_chart())
            .replace("__TREND_CHART__", trend_chart())
            .replace("__EFF_BARS__", efficiency_bars())
            .replace("__BAND_ROWS__", band_rows())
            .replace("__COUNTRY_ROWS__", country_rows()))
    script_dir = os.path.dirname(os.path.abspath(__file__))
    if os.path.basename(script_dir) == "scripts":
        # Repo layout: scripts/build_report.py -> repo-root index.html
        path = os.path.join(os.path.dirname(script_dir), "index.html")
    else:
        # Project layout: build_report.py -> report/index.html
        outdir = os.path.join(script_dir, "report")
        os.makedirs(outdir, exist_ok=True)
        path = os.path.join(outdir, "index.html")
    with open(path, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"wrote {path} ({len(html):,} bytes)")


if __name__ == "__main__":
    main()
