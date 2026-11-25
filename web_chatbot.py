"""
Mini AI Chatbot - BROWSER version (made by Mahesh Oli)
Run:  python web_chatbot.py
It opens http://localhost:8000 in your browser. No extra install needed.
"""

import json
import threading
import webbrowser
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

import mini_chatbot
from mini_chatbot import ask_stream  # same AI brain (asks for your key once)

PORT = 8000

PAGE = r"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>Mini AI Chatbot</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Baloo+2:wght@600;700&family=Plus+Jakarta+Sans:wght@400;500;600&family=Noto+Sans+Devanagari:wght@400;600&display=swap" rel="stylesheet">
<style>
:root{--ink:#0F2347;--muted:#5B6B86;--bg:#F3F6FB;--card:#fff;--line:#DCE3EF;--brand:#0B3D91;--accent:#C8102E;--bot:#F7F9FD;--code:#E9EEF7}
@media (prefers-color-scheme:dark){:root{--ink:#E7ECF6;--muted:#92A3C2;--bg:#0A1222;--card:#0F192D;--line:#243250;--brand:#2B5FC7;--accent:#FF4D63;--bot:#14213B;--code:#1B2A4A}}
*{box-sizing:border-box}
html,body{height:100%}
body{margin:0;background:var(--bg);color:var(--ink);font:16px/1.6 "Plus Jakarta Sans","Noto Sans Devanagari",system-ui,sans-serif}
.shell{max-width:820px;height:100%;margin:0 auto;display:flex;flex-direction:column;background:var(--card);box-shadow:0 0 0 1px var(--line)}
header{position:relative;flex:none;height:140px;padding:20px 22px 0;overflow:hidden;color:#fff;background:linear-gradient(180deg,#0A2459,#1D56A8)}
header svg{position:absolute;left:0;right:0;bottom:0;width:100%;height:90px}
.head{position:relative;z-index:1}
h1{margin:0;font:700 27px/1.15 "Baloo 2","Noto Sans Devanagari",sans-serif}
.sub{margin:3px 0 0;font-size:14px;opacity:.88}
.new{position:absolute;z-index:2;top:16px;right:16px;padding:7px 14px;font:500 14px inherit;font-family:inherit;color:#fff;background:rgba(255,255,255,.14);border:1px solid rgba(255,255,255,.45);border-radius:999px;cursor:pointer}
.new:hover{background:rgba(255,255,255,.26)}
#chat{flex:1;overflow-y:auto;padding:22px 20px 10px;display:flex;flex-direction:column;gap:14px;scroll-behavior:smooth}
.welcome h2{margin:0 0 2px;font:700 26px/1.2 "Baloo 2","Noto Sans Devanagari",sans-serif}
.welcome p{margin:0 0 18px;color:var(--muted)}
.chips{display:grid;grid-template-columns:repeat(2,1fr);gap:10px}
.chip{padding:12px 14px;text-align:left;font:inherit;font-size:15px;color:var(--ink);background:var(--bg);border:1px solid var(--line);border-radius:14px;cursor:pointer;transition:border-color .15s}
.chip:hover{border-color:var(--accent)}
.row{display:flex;gap:10px;align-items:flex-start}
.row.me{justify-content:flex-end}
.av{flex:none;width:34px;height:34px;display:grid;place-items:center;background:var(--brand);border-radius:50%}
.bubble{padding:11px 15px;max-width:min(88%,640px);overflow-wrap:anywhere;border-radius:18px}
.me .bubble{color:#fff;background:var(--brand);border-bottom-right-radius:6px;white-space:pre-wrap}
.bot .col{min-width:0;max-width:calc(100% - 44px)}
.bot .bubble{background:var(--bot);border:1px solid var(--line);border-top-left-radius:6px}
.bot .bubble.err{border-left:4px solid var(--accent)}
.bubble p{margin:0 0 .6em}.bubble p:last-child{margin:0}
.bubble ul,.bubble ol{margin:.2em 0 .6em;padding-left:1.3em}
.bubble h4{margin:.4em 0 .3em;font-size:1em}
pre{margin:.5em 0;padding:12px;overflow-x:auto;background:var(--code);border-radius:10px;font-size:14px}
code{padding:1px 5px;font:.9em ui-monospace,Consolas,monospace;background:var(--code);border-radius:5px}
pre code{padding:0;background:none}
.tools{margin-top:4px;display:flex;gap:14px}
.tools button,.retry{padding:2px 0;font:inherit;font-size:13px;color:var(--muted);background:none;border:0;cursor:pointer}
.tools button:hover,.retry:hover{color:var(--accent)}
.retry{margin-top:6px;color:var(--accent);font-weight:600}
.dots{display:flex;gap:5px;padding:6px 2px}
.dots i{width:8px;height:8px;background:var(--muted);border-radius:50%;animation:b 1.2s infinite}
.dots i:nth-child(2){animation-delay:.15s}.dots i:nth-child(3){animation-delay:.3s}
@keyframes b{0%,60%,100%{opacity:.3;transform:none}30%{opacity:1;transform:translateY(-4px)}}
.composer{flex:none;padding:10px 16px calc(10px + env(safe-area-inset-bottom,0px));background:var(--card);border-top:1px solid var(--line)}
.field{display:flex;align-items:flex-end;gap:8px;padding:6px 6px 6px 18px;background:var(--bg);border:1.5px solid var(--line);border-radius:24px;transition:border-color .15s}
.field:focus-within{border-color:var(--brand)}
textarea{flex:1;max-height:140px;padding:8px 0;font:inherit;line-height:1.5;color:inherit;background:none;border:0;outline:0;resize:none}
textarea::placeholder{color:var(--muted)}
.send{flex:none;width:42px;height:42px;display:grid;place-items:center;color:#fff;background:var(--accent);border:0;border-radius:50%;cursor:pointer}
.send:disabled{opacity:.4;cursor:default}
.note{margin:8px 0 0;text-align:center;font-size:12px;color:var(--muted)}
.photos{display:grid;grid-template-columns:repeat(auto-fit,minmax(150px,1fr));gap:10px;margin-top:8px}
.photos figure{margin:0}
.photos img{display:block;width:100%;aspect-ratio:4/5;object-fit:cover;background:var(--code);border-radius:12px}
.photos figcaption{margin-top:4px;font-size:12px;line-height:1.4;color:var(--muted)}
.photos a{color:var(--accent)}
:focus-visible{outline:3px solid var(--accent);outline-offset:2px}
@media (max-width:560px){.chips{grid-template-columns:1fr}h1{font-size:24px}}
@media (prefers-reduced-motion:reduce){*{animation:none!important;transition:none!important;scroll-behavior:auto!important}}
</style>
</head>
<body>
<div class="shell">
  <header>
    <div class="head"><h1>Mini AI Chatbot</h1><p class="sub">Ask any question. Get a simple answer.</p></div>
    <button class="new" id="new" type="button">New chat</button>
    <svg viewBox="0 0 800 90" preserveAspectRatio="xMidYMax slice" aria-hidden="true">
      <circle cx="660" cy="30" r="15" fill="#FF4D63" opacity=".9"/>
      <path d="M0 90V52L90 22l60 26 90-36 90 44 90-30 100 36 90-30 90 20 60-14 40 6v36z" fill="#fff" opacity=".13"/>
      <path d="M0 90V70l120-24 80 22 130-34 120 36 130-28 120 30v18z" fill="#fff" opacity=".22"/>
    </svg>
  </header>
  <main id="chat" aria-live="polite"></main>
  <form class="composer" id="form">
    <div class="field">
      <textarea id="box" rows="1" placeholder="Type your question here" aria-label="Your question"></textarea>
      <button class="send" id="send" type="submit" aria-label="Send question">
        <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"><path d="M12 19V5M5 12l7-7 7 7"/></svg>
      </button>
    </div>
    <p class="note">Made by Mahesh Oli. AI can make mistakes, so check important answers.</p>
  </form>
</div>
<script>
const $=s=>document.querySelector(s);
const chat=$("#chat"),box=$("#box"),send=$("#send");
const AV='<svg width="20" height="20" viewBox="0 0 22 22" fill="#fff"><path d="M1 18 8 6l3.5 6L14 9l7 9z"/></svg>';
const CHIPS=["Explain photosynthesis simply","Solve 2x + 5 = 15 step by step","What is demand in economics?","नेपालको राजधानी के हो?","Write a leave application letter","Show a photo of Mount Everest"];
let busy=false;

function el(tag,cls,html){const e=document.createElement(tag);if(cls)e.className=cls;if(html!=null)e.innerHTML=html;return e}
function down(){chat.scrollTop=chat.scrollHeight}

function md(src){
  const esc=s=>s.replace(/&/g,"&amp;").replace(/</g,"&lt;").replace(/>/g,"&gt;");
  const blocks=[];
  src=src.replace(/```(?:\w+)?\n?([\s\S]*?)```/g,(m,c)=>{blocks.push("<pre><code>"+esc(c.trim())+"</code></pre>");return "\u0000"+(blocks.length-1)+"\u0000"});
  let h=esc(src).replace(/`([^`\n]+)`/g,"<code>$1</code>").replace(/\*\*([^*\n]+)\*\*/g,"<strong>$1</strong>");
  let out="",list=null;
  const close=()=>{if(list){out+="</"+list+">";list=null}};
  for(const l of h.split("\n")){
    let m;
    if(m=l.match(/^\s*[*-]\s+(.*)/)){if(list!=="ul"){close();out+="<ul>";list="ul"}out+="<li>"+m[1]+"</li>"}
    else if(m=l.match(/^\s*\d+[.)]\s+(.*)/)){if(list!=="ol"){close();out+="<ol>";list="ol"}out+="<li>"+m[1]+"</li>"}
    else if(m=l.match(/^#{1,6}\s+(.*)/)){close();out+="<h4>"+m[1]+"</h4>"}
    else if(!l.trim()){close()}
    else{close();out+="<p>"+l+"</p>"}
  }
  close();
  return out.replace(/\u0000(\d+)\u0000/g,(m,i)=>blocks[i]);
}

function userRow(t){const r=el("div","row me");const b=el("div","bubble");b.textContent=t;r.append(b);chat.append(r);down()}
function botRow(){
  const r=el("div","row bot",'<div class="av">'+AV+'</div><div class="col"><div class="bubble"></div><div class="tools"></div></div>');
  chat.append(r);down();return r;
}
function addCopy(r,text){
  const b=el("button",null,"Copy");b.type="button";
  b.onclick=()=>{navigator.clipboard&&navigator.clipboard.writeText(text);b.textContent="Copied";setTimeout(()=>b.textContent="Copy",1500)};
  r.querySelector(".tools").append(b);
}
function fail(q,msg){
  let t=msg.replace(/^Error:\s*/,"")||"The AI did not give an answer. Please try again or ask in other words.";
  if(/503|UNAVAILABLE|high demand/i.test(msg))t="Google’s AI is busy right now. Wait a few seconds, then try again.";
  else if(/401|403|API key|PERMISSION/i.test(msg))t="The API key was not accepted. Check your Gemini key, then restart the chatbot.";
  else if(msg==="offline")t="The chatbot is not responding. Check that python web_chatbot.py is still running in the terminal.";
  const r=botRow(),bub=r.querySelector(".bubble");bub.classList.add("err");
  bub.innerHTML="<p>"+t.replace(/</g,"&lt;")+"</p>";
  const b=el("button","retry","Try again");b.type="button";
  b.onclick=()=>{r.remove();ask(q)};bub.append(b);down();
}
async function ask(q){
  busy=true;send.disabled=true;
  const r=botRow(),bub=r.querySelector(".bubble");
  bub.innerHTML='<div class="dots" role="status" aria-label="Thinking"><i></i><i></i><i></i></div>';
  try{
    const res=await fetch("/chat",{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify({message:q})});
    const reader=res.body.getReader(),dec=new TextDecoder();
    let text="";
    for(;;){
      const {done,value}=await reader.read();
      if(done)break;
      text+=dec.decode(value,{stream:true});
      if(text.charAt(0)==="\u0001")continue;   // error marker: wait for the full message
      bub.innerHTML=md(text);down();            // show the answer while it is still arriving
    }
    text+=dec.decode();
    if(text.charAt(0)==="\u0001"){r.remove();fail(q,text.slice(5))}
    else if(!text.trim()){r.remove();fail(q,"")}
    else{bub.innerHTML=md(text);addCopy(r,text);down()}
  }catch(e){r.remove();fail(q,"offline")}
  busy=false;send.disabled=false;box.focus();
}
const PHOTO_WORD=/\b(photos?|pictures?|images?|pics?)\b/i;
function wantsPhoto(q){return PHOTO_WORD.test(q)&&(q.split(/\s+/).length<=6||/\b(show|give|send|see|display)\b/i.test(q))}
function photoTerm(q){return q.replace(/\b(show|give|send|see|display|me|please|a|an|the|of|photos?|pictures?|images?|pics?|and)\b/gi," ").replace(/\s+/g," ").trim()}
async function photos(q){
  busy=true;send.disabled=true;
  const term=photoTerm(q),r=botRow(),bub=r.querySelector(".bubble");
  if(!term){bub.textContent="Which picture do you want? Try: Show a photo of Mount Everest";busy=false;send.disabled=false;return}
  bub.innerHTML='<div class="dots" role="status" aria-label="Searching"><i></i><i></i><i></i></div>';
  try{
    const url="https://commons.wikimedia.org/w/api.php?action=query&generator=search&gsrnamespace=6&gsrlimit=8&gsrsearch="+encodeURIComponent(term+" filetype:bitmap")+"&prop=imageinfo&iiprop=url|extmetadata&iiurlwidth=500&format=json&formatversion=2&origin=*";
    const data=await (await fetch(url)).json();
    const pages=((data.query&&data.query.pages)||[]).filter(p=>p.imageinfo&&p.imageinfo[0].thumburl).sort((a,b)=>a.index-b.index).slice(0,3);
    if(!pages.length){bub.textContent="I could not find a free picture of “"+term+"”. Try another name or spelling."}
    else{
      bub.innerHTML="";
      const intro=el("p");intro.textContent="Here are free-to-use pictures of "+term+":";
      const grid=el("div","photos");
      pages.forEach(p=>{
        const i=p.imageinfo[0],m=i.extmetadata||{};
        const fig=el("figure"),img=el("img"),cap=el("figcaption"),a=el("a");
        img.src=i.thumburl;img.alt=term;img.loading="lazy";img.onload=down;
        const artist=m.Artist?new DOMParser().parseFromString(m.Artist.value,"text/html").body.textContent.trim():"unknown";
        const lic=m.LicenseShortName?m.LicenseShortName.value:"see source";
        a.href=i.descriptionurl;a.target="_blank";a.rel="noopener";a.textContent="Source";
        cap.append("Photo by "+artist+", "+lic+". ",a);
        fig.append(img,cap);grid.append(fig);
      });
      bub.append(intro,grid);
    }
  }catch(e){bub.textContent="Could not load pictures. Check your internet and try again."}
  busy=false;send.disabled=false;box.focus();down();
}
function submit(q){
  q=q.trim();if(!q||busy)return;
  const w=$(".welcome");if(w)w.remove();
  userRow(q);box.value="";grow();
  if(wantsPhoto(q))photos(q);else ask(q);
}
function welcome(){
  const w=el("section","welcome",'<h2>Namaste! What do you want to learn today?</h2><p>Pick a question below or type your own.</p><div class="chips"></div>');
  CHIPS.forEach(c=>{const b=el("button","chip");b.type="button";b.textContent=c;b.onclick=()=>submit(c);w.querySelector(".chips").append(b)});
  chat.append(w);
}
function grow(){box.style.height="auto";box.style.height=Math.min(box.scrollHeight,140)+"px"}

$("#form").addEventListener("submit",e=>{e.preventDefault();submit(box.value)});
box.addEventListener("input",grow);
box.addEventListener("keydown",e=>{if(e.key==="Enter"&&!e.shiftKey&&!e.isComposing){e.preventDefault();submit(box.value)}});
$("#new").onclick=()=>{fetch("/reset",{method:"POST"}).catch(()=>{});chat.innerHTML="";busy=false;send.disabled=false;welcome();box.focus()};
welcome();box.focus();
</script>
</body>
</html>
"""


class Handler(BaseHTTPRequestHandler):
    def _send(self, code, body, ctype):
        data = body.encode("utf-8")
        self.send_response(code)
        self.send_header("Content-Type", ctype)
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    def do_GET(self):
        if self.path in ("/", "/index.html"):
            mini_chatbot.history.clear()  # page refresh = fresh conversation
            self._send(200, PAGE, "text/html; charset=utf-8")
        else:
            self._send(404, "Not found", "text/plain")

    def do_POST(self):
        if self.path == "/reset":
            mini_chatbot.history.clear()  # start a fresh conversation
            self._send(200, "{}", "application/json")
        elif self.path == "/chat":
            length = int(self.headers.get("Content-Length", 0))
            message = json.loads(self.rfile.read(length)).get("message", "").strip()
            self.send_response(200)
            self.send_header("Content-Type", "text/plain; charset=utf-8")
            self.send_header("Cache-Control", "no-cache")
            self.end_headers()
            started = False
            try:
                if not message:
                    raise ValueError("Please type a question.")
                for piece in ask_stream(message):  # send each piece as soon as it arrives
                    self.wfile.write(piece.encode("utf-8"))
                    self.wfile.flush()
                    started = True
            except (BrokenPipeError, ConnectionResetError):
                pass
            except Exception as e:
                if not started:  # "\x01ERR:" marks an error for the web page
                    self.wfile.write(f"\x01ERR:Error: {e}".encode("utf-8"))
        else:
            self._send(404, "Not found", "text/plain")

    def log_message(self, *args):
        pass  # keep the terminal clean


def main():
    server = ThreadingHTTPServer(("127.0.0.1", PORT), Handler)
    url = f"http://localhost:{PORT}"
    print(f"\nChatbot is running at {url}")
    print("Keep this window open. Press Ctrl + C to stop.\n")
    threading.Timer(1, lambda: webbrowser.open(url)).start()
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nStopped.")


if __name__ == "__main__":
    main()
