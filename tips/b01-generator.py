import json
CSS="""*{box-sizing:border-box;margin:0}body{width:1200px;height:630px;font-family:"DejaVu Sans",Arial,sans-serif;background:#eef7f5;color:#1d2433;overflow:hidden;position:relative}
.lab{position:absolute;left:56px;top:44px;font-size:20px;font-weight:700;color:#0f7b6c;letter-spacing:.06em;text-transform:uppercase}
.ttl{position:absolute;left:56px;top:78px;font-size:38px;font-weight:800;width:1090px;line-height:1.15}
.stage{position:absolute;left:56px;right:56px;top:200px;bottom:56px;display:flex;align-items:center;justify-content:center;gap:28px}
.card{background:#fff;border-radius:16px;box-shadow:0 8px 24px rgba(15,42,43,.10);padding:24px 28px}
.pill{display:inline-block;padding:8px 16px;border-radius:999px;font-weight:700;font-size:20px}
.teal{background:#0f7b6c;color:#fff}.soft{background:#d6ece7;color:#0f5f54}.gold{background:#f5b841;color:#1d2433}.red{background:#fde2e1;color:#b42318}.grey{background:#e9ecf1;color:#5b6475}
.arrow{font-size:44px;color:#0f7b6c;font-weight:800}
.big{font-size:30px;font-weight:800}.sm{font-size:19px;color:#5b6475;margin-top:6px}
.col{display:flex;flex-direction:column;align-items:center;gap:12px}
.mail{width:520px}.mail .h{font-size:16px;color:#5b6475;border-bottom:1px solid #e3e7ee;padding-bottom:10px;margin-bottom:14px}
.btn{display:inline-block;background:#0f7b6c;color:#fff;font-weight:700;border-radius:8px;padding:12px 20px;margin-top:16px;font-size:19px}
.phone{width:300px;height:350px;border-radius:36px;background:#1d2433;padding:14px}.scr{background:#f4f6f8;border-radius:26px;height:100%;padding:22px 16px;display:flex;flex-direction:column;gap:12px}
.bub{background:#fff;border-radius:16px;padding:14px;font-size:18px;line-height:1.35;box-shadow:0 2px 6px rgba(0,0,0,.06)}
.x{color:#b42318;font-weight:800}.ok{color:#0f7b6c;font-weight:800}
"""
def page(n,title,body):
    return f'<!doctype html><html><head><meta charset="utf-8"><style>{CSS}</style></head><body><div class="lab">Tip {n}</div><div class="ttl">{title}</div><div class="stage">{body}</div></body></html>'
A='<div class="arrow">&rarr;</div>'
def step(t,s="",cls="card"):
    return f'<div class="{cls} col" style="min-width:230px"><div class="big">{t}</div>{f"<div class=sm>{s}</div>" if s else ""}</div>'
def seq(items):  # list of (label, sub, pillclass)
    return ''.join(f'<div class="card col" style="min-width:150px;padding:18px"><span class="pill {c}">{l}</span><div class="sm">{s}</div></div>' for l,s,c in items)
T={}
T[1]=("Send the first reminder 2 to 4 hours after they leave",
 step("10:00","Leaves the checkout")+A+f'<div class="card col" style="min-width:300px;border:3px solid #0f7b6c"><div class="big">12:00 to 14:00</div><div class="sm">Email 1 goes out</div></div>'+A+step("Comes back","Decision still warm"))
T[2]=("Don't fire the first reminder within minutes",
 f'<div class="card col" style="width:400px"><span class="pill red">1 minute later</span><div class="big" style="margin-top:8px"><span class="x">&#10007;</span> Too soon</div><div class="sm">Still deciding. Feels pushy.</div></div>'
 f'<div class="card col" style="width:400px"><span class="pill teal">A few hours later</span><div class="big" style="margin-top:8px"><span class="ok">&#10003;</span> Well timed</div><div class="sm">They have really gone.</div></div>')
bar=''.join(f'<div style="flex:1;height:70px;background:{"#0f7b6c" if 6<=h<21 else "#cfd6df"};border-right:2px solid #eef7f5"></div>' for h in range(24))
T[3]=("Only send between 6am and 9pm",
 f'<div class="col" style="width:1000px"><div style="display:flex;width:100%;border-radius:12px;overflow:hidden">{bar}</div><div style="display:flex;justify-content:space-between;width:100%;font-size:20px;color:#5b6475"><span>Midnight</span><span>6am</span><span>Noon</span><span>9pm</span><span>Midnight</span></div><div class="sm" style="font-size:22px">Triggered overnight? It waits for the morning.</div></div>')
T[4]=("Set up a sequence for everyone who starts checkout and doesn't finish",
 step("Starts checkout")+A+step("Doesn't buy")+A+f'<div class="card col" style="min-width:300px;border:3px solid #0f7b6c"><div class="big">Abandon sequence</div><div class="sm">Email 1, 2, 3</div></div>')
T[5]=("Stop the sequence the moment someone buys",
 seq([("Email 1","Sent","soft"),("Purchase","Tag: buyer","gold"),("Email 2","Skipped","grey"),("Email 3","Skipped","grey")])+f'<div class="card col"><div class="big ok">Exit</div><div class="sm">No "you forgot"<br>after paying</div></div>')
T[6]=("End with an email that asks why they didn't buy",
 '<div class="card mail"><div class="h">Subject: Quick question</div><div style="font-size:22px;line-height:1.45">Hi Sam,<br>You didn\'t finish your order, and that\'s fine.<br><b>What stopped you?</b> Just hit reply.</div></div>'+A+step("Replies","Tell you what to fix"))
T[7]=("Give past customers a shorter, lighter reminder",
 f'<div class="col" style="gap:22px"><div style="display:flex;align-items:center;gap:20px"><span class="pill gold" style="width:240px;text-align:center">Past customer</span>{A}{seq([("1 email","Gentle nudge","soft")])}</div>'
 f'<div style="display:flex;align-items:center;gap:20px"><span class="pill grey" style="width:240px;text-align:center">New visitor</span>{A}{seq([("Email 1","","soft"),("Email 2","","soft"),("Email 3","","soft")])}</div></div>')
T[8]=("Run a separate sequence for memberships and subscriptions",
 f'<div class="card col" style="width:420px"><span class="pill soft">One-off course</span><div class="big" style="margin-top:6px">"Get the course"</div><div class="sm">Sell the result</div></div>'
 f'<div class="card col" style="width:420px;border:3px solid #0f7b6c"><span class="pill teal">Membership</span><div class="big" style="margin-top:6px">"Every month you get..."</div><div class="sm">Sell the ongoing value</div></div>')
T[9]=("Hold back anyone with an open support question",
 step("Abandons cart")+A+f'<div class="card col" style="min-width:300px"><span class="pill red">Open support ticket</span><div class="big" style="margin-top:8px">Sequence paused</div><div class="sm">Until it is answered</div></div>')
T[10]=("Test a text message alongside your emails",
 f'<div class="card col" style="width:380px"><span class="pill soft">Version A</span><div class="big" style="margin-top:6px">Email only</div></div><div class="big" style="color:#5b6475">vs</div>'
 f'<div class="card col" style="width:380px;border:3px solid #0f7b6c"><span class="pill teal">Version B</span><div class="big" style="margin-top:6px">Email + 1 text</div><div class="sm">With SMS consent</div></div>')
T[11]=("Send one text, not a series",
 '<div class="phone"><div class="scr"><div class="sm" style="text-align:center">Today 14:05</div><div class="bub">Hi Sam, your order is still waiting. Finish it here: <u>link</u></div><div class="sm" style="text-align:center;margin-top:auto">One message. That\'s it.</div></div></div>')
T[12]=("Skip the matching email when someone gets the text",
 seq([("Text","Replaces email 1","teal")])+f'<div class="card col" style="min-width:150px;padding:18px;opacity:.55"><span class="pill grey"><s>Email 1</s></span><div class="sm">Skipped</div></div>'+seq([("Email 2","Rejoin here","soft"),("Email 3","","soft")]))
T[13]=("Start on the channel each person responds to most",
 f'<div class="col" style="gap:22px"><div style="display:flex;align-items:center;gap:20px"><span class="pill grey" style="width:260px;text-align:center">Clicks emails</span>{A}{seq([("Email first","Then text","soft")])}</div>'
 f'<div style="display:flex;align-items:center;gap:20px"><span class="pill grey" style="width:260px;text-align:center">Clicks texts</span>{A}{seq([("Text first","Then email","teal")])}</div></div>')
bars=[(62,"Email 1"),(48,"Email 2"),(19,"Email 3"),(41,"Email 4")]
bh=''.join(f'<div class="col" style="justify-content:flex-end;height:300px"><div style="width:120px;height:{v*4}px;border-radius:10px 10px 0 0;background:{"#f5b841" if v==19 else "#0f7b6c"}"></div><div class="sm">{l}</div></div>' for v,l in bars)
T[14]=("Find the email where people stop opening",
 f'<div style="display:flex;gap:40px;align-items:flex-end">{bh}</div><div class="card col" style="width:300px"><div class="big">Fix this one first</div><div class="sm">Test its timing, offer or channel</div></div>')
T[15]=("Watch the unsubscribe rate",
 '<div class="card" style="width:640px"><svg width="580" height="250" viewBox="0 0 580 250"><polyline points="20,210 130,200 240,205 350,60 460,195 560,200" fill="none" stroke="#0f7b6c" stroke-width="6" stroke-linejoin="round"/><circle cx="350" cy="60" r="14" fill="#f5b841"/><g font-size="18" fill="#5b6475" font-family="DejaVu Sans"><text x="5" y="243">Email 1</text><text x="210" y="243">Email 2</text><text x="320" y="243">Email 3</text><text x="500" y="243">Email 4</text></g></svg></div><div class="card col" style="width:300px"><div class="big">A spike?</div><div class="sm">Too frequent or too pushy. Soften or space it out.</div></div>')
fld=lambda t,k: f'<div style="border:2px solid #cfd6df;border-radius:8px;padding:10px 14px;font-size:19px;{"text-decoration:line-through;color:#a0a8b4;border-style:dashed" if k else ""}">{t}</div>'
T[16]=("Fix the checkout as well as the emails",
 f'<div class="card" style="width:440px;display:flex;flex-direction:column;gap:10px"><div class="big" style="font-size:24px">Checkout</div>{fld("Name",0)}{fld("Email",0)}{fld("Phone number",1)}{fld("Company name",1)}{fld("Card details",0)}</div><div class="card col" style="width:360px"><div class="big">Cut what you don\'t need</div><div class="sm">Fewer fields, fewer reasons to leave</div></div>')
slugs={1:"first-reminder-2-to-4-hours",2:"not-within-minutes",3:"send-6am-to-9pm",4:"sequence-for-everyone",5:"stop-when-they-buy",6:"ask-why-they-didnt-buy",7:"past-customers-shorter",8:"separate-membership-sequence",9:"hold-back-support-questions",10:"test-a-text-message",11:"one-text-not-a-series",12:"skip-matching-email",13:"start-on-preferred-channel",14:"find-the-drop-off-email",15:"watch-unsubscribes",16:"fix-the-checkout-too"}
meta={}
for n,(t,b) in T.items():
    fn=f"b01-tip{n:02d}-{slugs[n]}"
    open(fn+".html","w").write(page(n,t,b)); meta[n]=(fn,t)
json.dump(meta,open("meta.json","w"))
