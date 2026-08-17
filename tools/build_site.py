#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""OurWord.ai 导航站 —— 北欧黑白风。每个项目一条，图标取该项目自己的 icon 文件。"""
import html, json, os

SITE = "https://ourword.ai"
SELF = "site"

# 每个项目一条，按仓库名去重；顺序按「有人在用的排前面」
PROJECTS = [
    {"repo": "",       "path": "/",        "icon": "/favicon.svg",
     "zh": "人类世界生存法则", "en": "Human World",
     "desc": "89 位人物与典籍的生存智慧，跨越 2600 年。每一条写清这个人真正留下的那个想法，以及今天怎么用。"},
    {"repo": "idea",   "path": "/idea/",   "icon": "/idea/icon.svg",
     "zh": "痛点雷达", "en": "Idea",
     "desc": "每天读普通人用自己的话说自己问题的地方，把反复出现的缺口写成卡片。痛点足够痛，付费意愿足够强。"},
    {"repo": "skill",  "path": "/skill/",  "icon": "/skill/icon.svg",
     "zh": "Skill 商店", "en": "Skill Store",
     "desc": "每天上新的好玩 Agent Skill 精选店，逐个读过再上架。"},
    {"repo": "zouni",  "path": "https://zouni.app/", "icon": "https://zouni.app/icon.svg",
     "zh": "走你", "en": "Zouni",
     "desc": "输入去哪儿、几天、多少预算，出一份能直接照着走的攻略。"},
    {"repo": "ai",     "path": "/ai/",     "icon": "/ai/icon.svg",
     "zh": "AI 泡沫检测仪", "en": "AI Bubble Monitor",
     "desc": "把「这轮是不是泡沫」拆成可核对的红线，逐条记分，破了就标出来。"},
    {"repo": "pixel",  "path": "/pixel/",  "icon": "/pixel/icon.svg",
     "zh": "像素板", "en": "PixelPad",
     "desc": "24×24 原生像素画 Agent Skill——逐像素落调色板索引，不是生成大图再降采样。"},
]

def e(s): return html.escape(s)

CSS = """
:root{
  color-scheme:light only;
  --ink:#0a0a0a; --ink-70:#404040; --ink-50:#666666; --ink-30:#b3b3b3;
  --hairline:#e5e5e5; --surface:#ffffff; --bg:#fafafa; --tint:#f0f0f0;
  --cta-fill:#0a0a0a; --cta-text:#ffffff;
  --sp-1:4px; --sp-2:8px; --sp-3:12px; --sp-4:16px; --sp-5:24px; --sp-6:32px;
  --fs-micro:10px; --fs-caption:11px; --fs-body:13px; --fs-strong:14px; --fs-heading:16px; --fs-display:20px;
  --h-sm:28px; --h-md:36px; --h-lg:46px;
  --r-block:8px; --r-card:16px;
  --shadow-card:0 1px 2px rgba(10,10,10,.03),0 6px 20px rgba(10,10,10,.06);
  --shadow-pop:0 2px 6px rgba(10,10,10,.05),0 12px 32px rgba(10,10,10,.08);
  --focus:0 0 0 2px var(--ink);
  --font:'Inter','Noto Sans CJK SC','PingFang SC','Hiragino Sans GB','Microsoft YaHei',system-ui,sans-serif;
}
*{box-sizing:border-box}
html,body{margin:0;padding:0;background:var(--bg)}
body{color:var(--ink);font-family:var(--font);font-size:var(--fs-strong);line-height:1.65;-webkit-font-smoothing:antialiased}
.caps{letter-spacing:.07em}
.skip-link{position:absolute;left:var(--sp-3);top:-52px;z-index:100;padding:var(--sp-2) var(--sp-4);
  background:var(--ink);color:var(--cta-text);border-radius:var(--r-block);font-size:var(--fs-body);
  font-weight:700;text-decoration:none;transition:top .2s ease-out}
.skip-link:focus{top:var(--sp-3)}
.wrap{max-width:720px;margin:0 auto;padding:0 var(--sp-5) var(--sp-6)}
header{padding:var(--sp-6) 0 0}
.brand{font-size:var(--fs-micro);letter-spacing:.22em;text-transform:uppercase;color:var(--ink-50);margin-bottom:var(--sp-2)}
h1{font-size:var(--fs-display);font-weight:700;letter-spacing:-.01em;line-height:1.2;margin:0 0 var(--sp-2)}
.lede{margin:0;font-size:var(--fs-body);color:var(--ink-50);max-width:34em}
.sec{font-size:var(--fs-caption);font-weight:700;color:var(--ink-50);text-transform:uppercase;
  letter-spacing:.07em;margin:0 0 var(--sp-3)}
.item{display:flex;align-items:flex-start;gap:var(--sp-4);padding:var(--sp-5);
  background:var(--surface);border-radius:var(--r-card);box-shadow:var(--shadow-card);
  text-decoration:none;color:inherit;margin-bottom:var(--sp-3);
  transition:box-shadow .2s ease-out,transform .12s ease-out}
.item:hover{box-shadow:var(--shadow-pop)}
.item:active{transform:scale(.985)}
.item:focus-visible{outline:0;box-shadow:var(--focus)}
.item .ico{width:var(--h-md);height:var(--h-md);flex:none;border-radius:var(--r-block);
  background:var(--tint);display:grid;place-items:center;color:var(--ink)}
.item .ico img{display:block;width:20px;height:20px}
.item .body{flex:1;min-width:0}
.item h2{margin:0 0 var(--sp-1);font-size:var(--fs-heading);font-weight:700;letter-spacing:-.01em}
.item h2 .en{margin-left:var(--sp-2);font-size:var(--fs-caption);font-weight:700;color:var(--ink-50);letter-spacing:.07em}
.item p{margin:0;font-size:var(--fs-body);color:var(--ink-70);line-height:1.8}
.item .go{flex:none;align-self:center;color:var(--ink-30);font-size:var(--fs-heading);line-height:1}
.item:hover .go{color:var(--ink)}
footer{border-top:1px solid var(--hairline);margin-top:var(--sp-6);padding:var(--sp-5) 0 0;
  font-size:var(--fs-caption);color:var(--ink-50)}
footer a{color:var(--ink-70);display:inline-block;min-height:24px;line-height:24px}
@media(max-width:640px){
  .wrap{padding:0 var(--sp-4) var(--sp-6)}
  .item{padding:var(--sp-4)}
}
@media(prefers-reduced-motion:reduce){*{transition:none!important}}
"""

def main():
    items = []
    for p in PROJECTS:
        if p["repo"] == SELF:            # 去重：导航站自己不列自己
            continue
        ext = p["path"].startswith("http")
        items.append(
            '<a class="item" href="%s"%s>'
            '<span class="ico"><img src="%s" alt="" width="20" height="20" loading="lazy"></span>'
            '<span class="body"><h2>%s<span class="en caps">%s</span></h2><p>%s</p></span>'
            '<span class="go" aria-hidden="true">→</span></a>'
            % (e(p["path"]), ' target="_blank" rel="noopener"' if ext else '',
               e(p["icon"]), e(p["zh"]), e(p["en"]), e(p["desc"])))

    ld = {"@context": "https://schema.org", "@type": "ItemList",
          "name": "OurWord AI 导航", "numberOfItems": len(items),
          "itemListElement": [
              {"@type": "ListItem", "position": i + 1, "name": p["zh"],
               "url": p["path"] if p["path"].startswith("http") else SITE + p["path"]}
              for i, p in enumerate([x for x in PROJECTS if x["repo"] != SELF])]}

    doc = """<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>OurWord AI · 导航</title>
<meta name="description" content="OurWord.ai 全部项目索引：人类世界生存法则、痛点雷达、Skill 商店、走你、AI 泡沫检测仪、像素板。">
<link rel="icon" type="image/svg+xml" href="/site/icon.svg">
<link rel="canonical" href="%s/site/">
<script type="application/ld+json">%s</script>
<style>%s</style>
</head>
<body>
<a href="#main" class="skip-link">跳至主内容</a>
<div class="wrap">
<header>
  <div class="brand">OURWORD.AI</div>
  <h1>全部项目</h1>
  <p class="lede">一个人做的几件小东西，各自解决一件具体的事。</p>
</header>
<main id="main">
  <h2 class="sec">项目 · %d</h2>
%s
</main>
<footer>
  每个项目的图标取自该项目自己的仓库 · <a href="https://github.com/woowoeth" target="_blank" rel="noopener">GitHub</a>
</footer>
</div>
</body>
</html>
""" % (SITE, json.dumps(ld, ensure_ascii=False), CSS, len(items), "\n".join(items))
    out = os.environ.get("OUT", "index.html")
    open(out, "w", encoding="utf-8").write(doc)
    print("wrote", out, len(doc), "chars,", len(items), "projects")

if __name__ == "__main__":
    main()
