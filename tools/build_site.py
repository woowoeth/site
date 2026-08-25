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
     "desc": "70+ 个人物与典籍的生存智慧，跨越 2600 年。每一条写清这个人真正留下的那一个想法，以及今天怎么用。"},
    {"repo": "skill",  "path": "/skill/",  "icon": "/skill/icon.svg",
     "zh": "品味", "en": "Taste",
     "desc": "叫 SKILL.md 的文件已经百万量级，没人数得清。我们只挑值得装的，并且把挑它的理由写下来。"},
    # zouni 的图标内联成 data URI，不再跨站取 —— 导航页七条里只有它是
    # 跨站取图（其余都是 /skill/icon.svg 这样的同源路径），也只有它不显示。
    # 实测 https://zouni.app/icon.svg 在部分网络下被 302 到 urlblock.php。
    # 根因是过滤还是 CORS 不重要：**跨站依赖去掉了，这条就不会再坏。**
    {"repo": "zouni",  "path": "https://zouni.app/", "icon": "data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHZpZXdCb3g9IjAgMCAxMDAgMTAwIiByb2xlPSJpbWciPjx0aXRsZT7otbDkvaA8L3RpdGxlPjxyZWN0IHdpZHRoPSIxMDAiIGhlaWdodD0iMTAwIiByeD0iMjIiIGZpbGw9IiMwYTBhMGEiLz48cGF0aCBkPSJNMjggNjIgUTUwIDMwIDcyIDYyIiBzdHJva2U9IiNmZmZmZmYiIHN0cm9rZS13aWR0aD0iOCIgZmlsbD0ibm9uZSIgc3Ryb2tlLWxpbmVjYXA9InJvdW5kIi8+PGNpcmNsZSBjeD0iNzIiIGN5PSIzOCIgcj0iNyIgZmlsbD0iI2ZmZmZmZiIvPjwvc3ZnPg==",
     "zh": "走你", "en": "Zouni",
     "desc": "计划赶得上变化。输入去哪儿、几天、多少预算，出一份能直接照着走的攻略；路上有变，它把后面重排一遍。"},
    {"repo": "ai",     "path": "/ai/",     "icon": "/ai/icon.svg",
     "zh": "AI 泡沫检测仪", "en": "AI Bubble Monitor",
     "desc": "AI 泡沫监测面板：环境 / 结构 / 引爆三层，20 条红线，破了就标出来。"},
    # podcast 一直在线上 index.html 里，却**从来没进过 PROJECTS** ——
    # 也就是说这个生成器相对线上页是旧的。2026-08-25 我照它跑了一次构建，
    # 就把「原声」整条挤掉了，是店主发现的。补回来，并在 main() 末尾加了闸。
    {"repo": "podcast", "path": "/podcast/", "icon": "/podcast/icon.svg",
     "zh": "原声", "en": "Podcast",
     "desc": "世界太吵，来原声听播客。每天从 61 档中英文播客里挑出值得记住的判断，要点和金句都带时间戳。"},
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


# 已下架的条目 —— **只有写在这里的才允许从页面上消失。**
#
# 2026-08-25 加的，起因是我把「原声」弄丢了：podcast 一直在线上 index.html 里，
# 却从来没进过 PROJECTS。我照着这个生成器跑了一次构建，它就按 PROJECTS 重生成，
# 把 podcast 整条挤掉了 —— **生成器相对线上页是旧的，而我假设它是源头。**
# 是店主发现的，不是我。
#
# 所以这道闸比「记得别漏」可靠：写入前拿当前 index.html 的条目比一遍，
# 任何会消失的条目都必须在 REMOVED 里显式列出，否则拒绝写。
# **删东西要动手写一行；漏东西什么都不用做 —— 闸门必须装在漏的那一侧。**
REMOVED = {
    "/idea/":  "2026-08-25 店主下架，仓库同期删除",
    "/pixel/": "2026-08-25 店主下架，仓库同期删除",
}


def assert_no_drop(new_html: str, out: str) -> None:
    """当前页上有、这次要写的页上没有 —— 除非在 REMOVED 里，否则不许写。"""
    import re as _re
    if not os.path.exists(out):
        return
    old = _re.findall(r'class="item" href="([^"]+)"', open(out, encoding="utf-8").read())
    new = set(_re.findall(r'class="item" href="([^"]+)"', new_html))
    dropped = [h for h in old if h not in new and h not in REMOVED]
    if dropped:
        raise SystemExit(
            "拒绝写入：这次构建会让以下条目从导航上消失，而它们不在 REMOVED 里——\n"
            + "".join(f"  {h}\n" for h in dropped)
            + "如果是有意下架，把它写进 build_site.py 的 REMOVED；"
            "如果不是，说明 PROJECTS 比线上页旧了，先把缺的补进 PROJECTS。")



# ---------------------------------------------------------------------------
# 每次构建都去各站取一遍它自己怎么称呼自己 —— **导航里不许存过期的副本。**
#
# 2026-08-25 加的。加之前导航写「89 位人物」而首页自己写 70+，
# 写「49 档播客」而原声自己写 61 档，把 skill 站叫「Skill 商店」
# 而它自己的 <title> 是「品味 — 中文 Agent Skill 精选」。
# **三处全是存副本存出来的**：副本写下来那天是对的，然后项目往前走，副本留在原地。
#
# 为什么不干脆自动抓来直接用：各站的 h1 形态不一致（原声的 h1 是「原声.」带句号，
# 品味压根没有 h1），meta description 动辄一百多字，直接塞进导航会把版式撑烂。
# 导航文案是**编辑过的一行**，该由人写。
#
# 所以取的是「核对」而不是「替换」：抓下来比一遍，对不上就**拒绝构建**并打印差异。
# 这样文案仍然是人写的，但它不可能悄悄过期 —— 和 assert_no_drop 同一个思路：
# **闸门装在「什么都不做就会出错」的那一侧。**
#
# 抓不到的（网络拦截、站临时挂了）打印警告继续，不阻断 —— 抓不到不等于对不上。
LIVE_CHECK = {
    # repo -> 该项目自己页面上，导航这条描述里必须能对上的关键片段
    "":        ["70+", "2600 年"],
    "skill":   ["品味", "只挑值得装的"],
    "zouni":   ["计划赶得上变化"],
    "ai":      ["泡沫"],
    "podcast": ["世界太吵", "61 档"],
}


def _fetch(url, timeout=12):
    import urllib.request
    req = urllib.request.Request(url, headers={"User-Agent": "ourword-site-build"})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return r.read().decode("utf-8", "replace")


def assert_live_copy():
    """各站自称 vs 导航文案。对不上就拒绝构建；抓不到只警告。"""
    import re as _re
    bad, unreachable = [], []
    for pr in PROJECTS:
        need = LIVE_CHECK.get(pr["repo"])
        if not need:
            continue
        url = pr["path"] if pr["path"].startswith("http") else SITE + pr["path"]
        try:
            page = _fetch(url)
        except Exception as e:                       # 网络拦截、站临时挂了
            unreachable.append((url, str(e)[:60]))
            continue
        flat = _re.sub(r"\s+", " ", page)
        miss = [k for k in need if k not in flat]
        if miss:
            bad.append((url, miss))
    for url, why in unreachable:
        print(f"  ! 取不到 {url}（{why}）—— 这条没核对上，不等于它对不上")
    if bad:
        raise SystemExit(
            "拒绝构建：以下项目自己页面上已经找不到导航文案依据的说法了——\n"
            + "".join(f"  {u}  找不到：{'、'.join(m)}\n" for u, m in bad)
            + "去那个站看它现在怎么说自己，把 PROJECTS 的 zh/desc 和 LIVE_CHECK 一起更新。\n"
            "（导航文案是编辑过的一行，该由人写；这里只保证它不会悄悄过期。）")


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
    assert_no_drop(doc, out)          # 漏掉条目是静默的，所以闸装在这里
    if os.environ.get("SKIP_LIVE") != "1":
        assert_live_copy()            # 文案过期也是静默的，闸同样装在这里
    open(out, "w", encoding="utf-8").write(doc)
    print("wrote", out, len(doc), "chars,", len(items), "projects")

if __name__ == "__main__":
    main()
