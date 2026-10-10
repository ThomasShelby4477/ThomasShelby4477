"""GitHub-compatible SVG visuals. Local brand assets; no fonts or runtime services."""
import base64
from datetime import date
import html
import json
import mimetypes
from pathlib import Path
import textwrap
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / 'assets'
# A deliberate dark surface in either GitHub colour scheme.
DARK = {'bg':'#10120f','panel':'#10120f','fg':'#f2f3e8','muted':'#aeb5a7','line':'#5d6757','accent':'#c6ff00','warm':'#ff773d','blue':'#8daeff','violet':'#d0a5ff'}
THEMES = {'dark': dict(DARK), 'light': dict(DARK)}



def text(x,y,value,size,color,weight=400,extra=''):
    return f'<text x="{x}" y="{y}" fill="{color}" font-size="{size}" font-weight="{weight}" {extra}>{html.escape(str(value))}</text>'


def svg(w,h,body,title,desc,theme):
    c=THEMES[theme]
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-labelledby="title desc"><title id="title">{html.escape(title)}</title><desc id="desc">{html.escape(desc)}</desc><rect x="1" y="1" width="{w-2}" height="{h-2}" fill="{c['bg']}" stroke="{c['fg']}" stroke-width="2"/><g font-family="ui-monospace, SFMono-Regular, Menlo, Consolas, monospace">{body}</g></svg>'''


def rect(x,y,w,h,fill,stroke='none',r=0):
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="0" fill="{fill}" stroke="{stroke}"/>'


def icon(name,x,y,size,color):
    if name=='maskr':
        path=next(p for p in (ASSETS/'brands').glob('maskr.*') if p.suffix in ['.png','.webp','.jpg'])
        uri=f'data:{mimetypes.guess_type(path.name)[0]};base64,'+base64.b64encode(path.read_bytes()).decode()
        return f'<image x="{x}" y="{y}" width="{size}" height="{size}" href="{uri}"/>'
    root=ET.parse(ASSETS/'brands'/f'{name}.svg').getroot()
    vx,vy,vw,vh=map(float,root.attrib['viewBox'].split())
    scale=min(size/vw,size/vh)
    dx=x+(size-vw*scale)/2-vx*scale;dy=y+(size-vh*scale)/2-vy*scale
    paths=''.join(f'<path d="{html.escape(e.attrib["d"],quote=True)}"/>' for e in root.iter() if e.tag.endswith('path'))
    return f'<g transform="translate({dx:.3f} {dy:.3f}) scale({scale:.5f})" fill="{color}">{paths}</g>'


def write_variants(stem,renderer):
    for theme in THEMES:
        for mobile in [False,True]:
            (ASSETS/f'{stem}-{theme}{"-mobile" if mobile else ""}.svg').write_text(renderer(theme,mobile))


def typed_name(x,y,value,size,color,delay):
    letters=''.join(f'<tspan class="name-letter" style="animation-delay:{delay+i*.09:.2f}s">{html.escape(char)}</tspan>' for i,char in enumerate(value))
    return f'<text x="{x}" y="{y}" fill="{color}" font-size="{size}" font-weight="900" letter-spacing="-4">{letters}</text>'


def typing_taglines(x,y,size,color):
    """Native SVG timing: 1.5s typing, a long reading pause, then deletion.

    Three eight-second slots keep geometry fixed. No script, remote font,
    or animation service is involved. A media query supplies static text.
    """
    lines=['SECURITY × SOFTWARE','PRIVACY BY DESIGN','AI DEVELOPER TOOLS']
    out='<g class="typing-still">'+text(x,y,lines[0],size,color,700)+'</g><g class="typing-motion">'
    for index,line in enumerate(lines):
        start=index*8;advance=size*.6
        events=[(0,0)]
        if start: events.append((start,0))
        events.extend((start+.15+i*.075,i*advance) for i in range(1,len(line)+1))
        events.append((start+6.4,len(line)*advance))
        events.extend((start+6.4+i*.035,(len(line)-i)*advance) for i in range(1,len(line)+1))
        events.append((24,0))
        times=';'.join(f'{t/24:.6f}' for t,_ in events)
        widths=';'.join(f'{width:.2f}' for _,width in events)
        positions=';'.join(f'{x+width+3:.2f}' for _,width in events)
        visible=';'.join('1' if width else '0' for _,width in events)
        timing=f'begin="1.8s" dur="24s" keyTimes="{times}" calcMode="discrete" repeatCount="indefinite"'
        out+=f'<defs><clipPath id="type-{index}"><rect x="{x}" y="{y-size-3}" width="0" height="{size+9}"><animate attributeName="width" values="{widths}" {timing}/></rect></clipPath></defs>'
        out+=f'<g clip-path="url(#type-{index})">'+text(x,y,line,size,color,700,f'textLength="{len(line)*advance:.2f}" lengthAdjust="spacingAndGlyphs"')+'</g>'
        out+=f'<g opacity="0"><animate attributeName="opacity" values="{visible}" {timing}/><rect class="typing-cursor" x="{x+3}" y="{y-size+3}" width="2" height="{size}" fill="{color}"><animate attributeName="x" values="{positions}" {timing}/></rect></g>'
    return out+'</g>'


def hero(config,theme,mobile):
    c=THEMES[theme];w,h=(420,360) if mobile else (960,376);x=24 if mobile else 32
    b=rect(1,1,w-2,40,c['accent'])
    b+=text(x,27,'CYBERSECURITY / DATA / SOFTWARE',10 if mobile else 15,c['bg'],700,'letter-spacing=".5"')
    b+='''<style>
      .name-letter{animation:letter-in .06s ease-out both}
      @keyframes letter-in{from{opacity:0}to{opacity:1}}
      .typing-still{display:none}
      .typing-cursor{animation:cursor-pulse 1.1s ease-in-out infinite}
      @keyframes cursor-pulse{0%,35%,100%{opacity:1}60%,80%{opacity:0}}
      @media(prefers-reduced-motion:reduce){
        .name-letter{animation:none;opacity:1}
        .typing-motion{display:none}.typing-still{display:inline}
      }
    </style>'''
    b+=typed_name(x,126 if mobile else 138,'VAIBHAV',63 if mobile else 88,c['fg'],.18)
    b+=typed_name(x,205 if mobile else 246,'YADAV_',63 if mobile else 88,c['accent'],1)
    divider_y=237 if mobile else 278
    b+=f'<path d="M{x} {divider_y}h{w-2*x if mobile else 460}" stroke="{c["fg"]}" stroke-width="2"/>'
    b+=typing_taglines(x,267 if mobile else 308,18 if mobile else 22,c['fg'])
    b+=text(x,294 if mobile else 336,'Privacy. AI tools. Operational risk.',12 if mobile else 14,c['muted'])
    b+=text(x,337 if mobile else 360,'@'+config['username'],11,c['warm'],600)
    if not mobile:
        b+=rect(573,64,354,280,c['bg'],c['fg'])
        b+=rect(573,64,354,30,c['warm'])+text(590,84,'SYSTEM / BUILDING WITH TRUST',12,c['bg'],700)
        for gx in range(590,911,32):
            b+=f'<path d="M{gx} 112v148" stroke="{c["line"]}" stroke-width=".5"/>'
        for gy in range(112,261,32):
            b+=f'<path d="M590 {gy}h320" stroke="{c["line"]}" stroke-width=".5"/>'
        b+=f'<path d="M750 122l61 22v45l-61 53-61-53v-45Z" fill="{c["bg"]}" stroke="{c["accent"]}" stroke-width="4"/>'
        b+=f'<path d="M723 180l20 20 35-43" fill="none" stroke="{c["accent"]}" stroke-width="7"/>'
        b+=text(590,323,'[ SECURE BY INTENT ]',15,c['fg'],700)
    return svg(w,h,b,config['display_name'],'Vaibhav Yadav. Cybersecurity, data and software. Security-minded engineering. Privacy tools, AI infrastructure and full-stack products.',theme)


def project(p,index,theme,mobile):
    c=THEMES[theme];accent=c['accent'] if index%2==0 else c['warm'];w,h=(420,276) if mobile else (960,240);x=24 if mobile else 32
    category=['PRIVACY ENGINEERING','AI DEVELOPER TOOLS','FULL-STACK PRODUCT','REAL-TIME APPLICATION'][index]
    b=rect(16,16,w-32,24,accent)+text(x,32,f'{index+1:02d} / {category}',9 if mobile else 11,c['bg'],700,'letter-spacing=".5"')
    b+=rect(x,56,42,42,c['bg'],c['line'],11)+icon(p['icon'],x+8,64,26,accent)
    b+=text(x+56,85,p['name'].upper(),22 if mobile else 31,c['fg'],900,'letter-spacing="-.6"')
    head=textwrap.wrap(p['visual_headline'],width=34 if mobile else 59)
    y=130
    for line in head:
        b+=text(x,y,line,15 if mobile else 18,c['fg'],500);y+=23
    for line in textwrap.wrap(p['visual_detail'],width=46 if mobile else 76):
        b+=text(x,y+3,line,12 if mobile else 14,c['muted']);y+=20
    y=h-28
    ix=x
    for name in p['tech_icons']:
        b+=icon(name,ix,y-13,17,accent);ix+=27
    short=p['stack'].split(' · ')
    label=' · '.join(short[:3])
    b+=text(ix+4,y,label,8 if mobile else 11,c['muted'])
    if not mobile:
        action_x=w-x-139
        action_center=action_x+139/2
        b+=rect(action_x,64,139,144,accent)
        b+=icon(p['icon'],action_center-29,87,58,c['bg'])
        b+=text(action_center,190,'OPEN ↗',12,c['bg'],900,'text-anchor="middle"')
    return svg(w,h,b,p['name'],p['description']+' '+p['detail']+' Stack: '+p['stack'],theme)


def overview(data,theme,mobile):
    c=THEMES[theme];w,h=(420,210) if mobile else (960,132);b=''
    metrics=[(data['contributions'],'Contributions','Public profile · rolling year',c['accent']),(data['repositories'],'Public repositories','Owned · non-fork',c['fg']),(data['stars'],'Stars earned','Across public repositories',c['warm']),(data['joined'],'On GitHub since','Building in public',c['fg'])]
    for i,(value,label,detail,color) in enumerate(metrics):
        x=24+(i%2)*210 if mobile else 32+i*224;y=15+(i//2)*105 if mobile else 17
        if i:
            if mobile and i%2:b+=f'<path d="M210 {y+6}v69" stroke="{c["line"]}"/>'
            elif not mobile:b+=f'<path d="M{x-16} 26v79" stroke="{c["line"]}"/>'
        b+=text(x,y+34,f'{value:,}' if isinstance(value,int) else value,33 if mobile else 39,color,650,'letter-spacing="-1"')
        b+=text(x,y+57,label,12 if mobile else 13,c['fg'],500)
        b+=text(x,y+77,detail,9 if mobile else 10,c['muted'])
    return svg(w,h,b,'GitHub at a glance',f'{data["contributions"]} publicly displayed contributions in the rolling year, {data["repositories"]} public repositories, {data["stars"]} earned stars. Joined GitHub in {data["joined"]}.',theme)


def calendar_grid(data,theme,x,y,cell,gap):
    c=THEMES[theme]
    palette=['#242b20','#344518','#657e1e','#9cbe2a','#c6ff00']
    b='';last_month=None
    first=date.fromisoformat(data['calendar'][0]['date'])
    for d in data['calendar']:
        dt=date.fromisoformat(d['date']);offset=(dt-first).days;col=offset//7;row=(dt.weekday()+1)%7
        if dt.month!=last_month and row==0:
            b+=text(x+col*(cell+gap),y-10,dt.strftime('%b'),9,c['muted']);last_month=dt.month
        b+=f'<rect x="{x+col*(cell+gap):.2f}" y="{y+row*(cell+gap):.2f}" width="{cell}" height="{cell}" rx="0" fill="{palette[d["level"]]}"><title>{d["date"]}: {d["count"]} contributions</title></rect>'
    return b


def monthly_chart(data,theme,x,y,w,h):
    c=THEMES[theme];months=list(data['monthly_contributions'].items());step=w/len(months);peak=max((v for _,v in months),default=1) or 1;b=''
    b+=text(x,y-20,'MONTHLY CONTRIBUTIONS',11,c['accent'],600,'letter-spacing="1"')
    for k in range(3):
        gy=y+k*h/2;b+=f'<path d="M{x} {gy}h{w}" stroke="{c["line"]}" stroke-dasharray="2 5"/>'
    for i,(month,count) in enumerate(months):
        bx=x+i*step+4;bh=max(2,h*count/peak);bw=step-8
        b+=rect(round(bx,2),round(y+h-bh,2),round(bw,2),round(bh,2),c['accent'] if count else c['line'],r=3)
        if count:b+=text(bx+bw/2,y+h-bh-6,count,9,c['fg'],500,'text-anchor="middle"')
        b+=text(bx+bw/2,y+h+17,date.fromisoformat(month+'-01').strftime('%b'),8,c['muted'],extra='text-anchor="middle"')
    return b


def activity(data,theme,mobile):
    c=THEMES[theme];w,h=(420,610) if mobile else (960,590);x=24 if mobile else 32
    follower_label='follower' if data['followers']==1 else 'followers'
    b=text(x,34,'GITHUB / ENGINEERING ACTIVITY',11,c['accent'],600,'letter-spacing="1"')
    b+=text(x,57,f'Public snapshot · {data["updated"]}',11,c['muted'])
    metrics=[(data['active_days'],'Active days'),(data['longest_streak'],'Longest streak · days'),(data['most_active_day']['count'],'Peak contributions')]
    for i,(value,label) in enumerate(metrics):
        mx=x+i*((w-2*x)/3)
        b+=text(mx,103,value,32,c['fg'],600)+text(mx,126,label,8 if mobile else 11,c['muted'])
    if mobile:
        # Two chronological strips keep all 53 weeks legible on a phone.
        b+=text(x,164,'CONTRIBUTION CALENDAR',10,c['accent'],600,'letter-spacing="1"')
        original=data['calendar'];middle=27*7
        for start,gy in [(0,194),(middle,301)]:
            chunk=original[start:start+middle]
            b+=calendar_grid({'calendar':chunk},theme,x,gy,10,3)
        b+=text(x,406,'Earlier weeks above · latest weeks below',9,c['muted'])
        b+=f'<path d="M{x} 426h{w-2*x}" stroke="{c["line"]}"/>'
        b+=monthly_chart(data,theme,x,470,w-2*x,72)
        b+=text(x,588,f'{data["followers"]} {follower_label} · {data["forks"]} forks · Current streak: {data["current_streak"]} days',9,c['muted'])
    else:
        b+=text(x,166,'CONTRIBUTION CALENDAR',11,c['accent'],600,'letter-spacing="1"')
        b+=calendar_grid(data,theme,x+28,197,13,3)
        b+=text(x,224,'Mon',8,c['muted'])+text(x,256,'Wed',8,c['muted'])+text(x,288,'Fri',8,c['muted'])
        b+=text(x,331,f'{data["calendar"][0]["date"]} → {data["calendar"][-1]["date"]} · each square is one day',10,c['muted'])
        b+=f'<path d="M32 354h896" stroke="{c["line"]}"/>'
        b+=monthly_chart(data,theme,32,409,896,115)
        b+=text(x,569,f'{data["followers"]} {follower_label} · {data["forks"]} forks · Current streak: {data["current_streak"]} days',10,c['muted'])
    desc=f'{data["active_days"]} active days. Longest streak: {data["longest_streak"]} days. Peak day: {data["most_active_day"]["count"]} contributions on {data["most_active_day"]["date"]}. Calendar total: {data["contributions"]}. Monthly totals: '+json.dumps(data['monthly_contributions'])+'. Monthly bars count contributions across the displayed calendar.'
    return svg(w,h,b,'Contribution calendar and monthly activity',desc,theme)


def toolkit(theme,mobile):
    c=THEMES[theme];w,h=(420,924) if mobile else (960,360);b=''
    groups=[
        ('DETECTION & RESPONSE',[('Elastic SIEM',None),('EQL / KQL',None),('Threat intel',None),('Incident response',None)]),
        ('APPLICATION SECURITY',[('Burp Suite',None),('OWASP ZAP',None),('Nuclei',None),('Nmap',None)]),
        ('PROGRAMMING',[('Python','python'),('TypeScript','typescript'),('JavaScript','javascript'),('SQL',None)]),
        ('WEB & APIs',[('React','react'),('Next.js','nextdotjs'),('Express',None),('Flask','python')]),
        ('DATA & AI',[('PostgreSQL','postgresql'),('Supabase','supabase'),('Tree-sitter',None),('MCP',None)]),
        ('TOOLS & INTERFACES',[('GitHub','github'),('Docker',None),('Linux',None),('Streamlit',None)]),
    ]
    cellw=372 if mobile else 293.33
    cellh=136 if mobile else 148
    for i,(title,items) in enumerate(groups):
        cx=24 if mobile else 24+(i%3)*(cellw+16)
        cy=24+i*(cellh+12) if mobile else 24+(i//3)*(cellh+16)
        accent=c['accent'] if i%2==0 else c['warm']
        b+=rect(cx,cy,cellw,cellh,c['bg'],c['line'])
        b+=text(cx+16,cy+30,title,14,accent,700)
        px=cx+16;py=cy+50
        for label,brand in items:
            labelsize=14 if mobile else 12
            bw=len(label)*labelsize*.6+20+(24 if brand else 0)
            if px+bw>cx+cellw-16:
                px=cx+16;py+=38
            b+=rect(round(px,2),py,round(bw,2),28,c['panel'],c['line'])
            if brand:b+=icon(brand,px+8,py+6,16,c['fg'])
            b+=text(px+(32 if brand else 10),py+18,label,labelsize,c['fg'],500)
            px+=bw+8
    return svg(w,h,b,'Toolkit by area','Detection and response: Elastic SIEM, EQL/KQL, threat intelligence, incident response. Application security: Burp Suite, OWASP ZAP, Nuclei, Nmap. Programming: Python, TypeScript, JavaScript, SQL. Web and APIs: React, Next.js, Express, Flask. Data and AI: PostgreSQL, Supabase, Tree-sitter, MCP. Tools and interfaces: GitHub, Docker, Linux, Streamlit.',theme)


def education(config,theme,mobile):
    c=THEMES[theme];w,h=(420,207) if mobile else (960,129);b=''
    for i,d in enumerate(config['education']['degrees']):
        x=24 if mobile else 32+i*480;y=30+i*91 if mobile else 36;color=c['accent'] if i==0 else c['warm']
        b+=f'<circle cx="{x+8}" cy="{y-6}" r="6" fill="{color}"/>'+text(x+26,y,d['status'].upper(),11,color,600,'letter-spacing="1"')
        b+=text(x,y+30,'B.Tech' if i==0 else 'M.Tech',26,c['fg'],650)
        b+=text(x+103,y+30,'Computer Science Engineering',10 if mobile else 13,c['muted'])
        b+=text(x,y+54,'Cyber Security' + (f' · Expected {d["expected"]}' if d.get('expected') else ''),11,c['muted'])
    return svg(w,h,b,'Education status','B.Tech in Computer Science Engineering completed. M.Tech in Computer Science Engineering in progress, with expected completion in August 2027. Cyber Security specialisation at National Forensic Sciences University, Delhi.',theme)


def link_artwork(label,width,brand=None,primary=False,font_size=12):
    c=DARK;h=52;fill=c['accent'] if primary else c['bg'];fg=c['bg'] if primary else c['fg']
    body=rect(.5,4.5,width-1,43,fill,c['accent'] if primary else c['line'])
    tx=14
    if brand:
        if brand=='linkedin':
            body+=rect(13,14,22,22,'#0a66c2')+icon(brand,17,18,14,'#ffffff')
        else:body+=icon(brand,14,15,20,'#ff918c' if brand=='gmail' else fg)
        tx=46
    body+=text(tx,30,label,font_size,fg,700)
    body+=text(width-12,30,'↗',font_size,fg,700,'text-anchor="end"')
    return f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{h}" viewBox="0 0 {width} {h}" role="img"><title>{html.escape(label)}</title><g font-family="ui-monospace,Menlo,Consolas,monospace">{body}</g></svg>'


def contact_badge(name,label):
    return link_artwork(label,144,name)


def navigation_badge(label):
    width=102;h=52;c=DARK
    body=rect(.5,4.5,width-1,43,c['bg'],c['line'])
    body+=text(width/2,30,label,12,c['fg'],700,'text-anchor="middle"')
    return f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{h}" viewBox="0 0 {width} {h}" role="img"><title>{html.escape(label)}</title><g font-family="ui-monospace,Menlo,Consolas,monospace">{body}</g></svg>'


def project_actions(project,username):
    """Keep destination order, artwork, and accessible link labels together."""
    name=project['name']
    repository=project.get('url') or f'https://github.com/{username}/{project["repo"]}'
    if project.get('extra_label')=='Visit website':
        return [('LIVE SITE',f'Visit {name} live site',project['extra_url'],None),
                ('REPOSITORY',f'View {name} repository',repository,'github')]
    store=project.get('primary_label')=='Chrome Web Store'
    actions=[('CHROME STORE' if store else 'REPOSITORY',
              'Open Chrome Web Store' if store else f'View {name} repository',
              repository,'chrome' if store else 'github')]
    if project.get('extra_url'):
        actions.append(('POLICY' if store else 'ARCHITECTURE',f'{name}: {project["extra_label"]}',project['extra_url'],None))
    return actions


def build_static(config):
    write_variants('hero',lambda t,m:hero(config,t,m))
    write_variants('toolkit',toolkit)
    write_variants('education',lambda t,m:education(config,t,m))
    for i,p in enumerate(config['projects']):
        write_variants(f'project-{i+1}',lambda t,m,i=i,p=p:project(p,i,t,m))
    for name,label in [('linkedin','LINKEDIN'),('gmail','GMAIL'),('github','GITHUB'),('maskr','MASKR')]:
        (ASSETS/f'connect-{name}.svg').write_text(contact_badge(name,label))
    for name,label in [('work','WORK ↓'),('toolkit','TOOLKIT ↓'),('education','EDUCATION ↓'),('activity','ACTIVITY ↓'),('connect','CONNECT ↓')]:
        (ASSETS/f'nav-{name}.svg').write_text(navigation_badge(label))
    if config.get('show_experience',True):
        (ASSETS/'nav-experience.svg').write_text(navigation_badge('EXPERIENCE'))
    else:
        (ASSETS/'nav-experience.svg').unlink(missing_ok=True)
    for i,p in enumerate(config['projects'],1):
        for j,(label,_,_,brand) in enumerate(project_actions(p,config['username'])):
            suffix='primary' if j==0 else 'secondary'
            (ASSETS/f'project-{i}-{suffix}.svg').write_text(link_artwork(label,168,brand,j==0))
    (ASSETS/'activity-calendar.svg').write_text(link_artwork('CALENDAR',168,primary=True))
    (ASSETS/'activity-repositories.svg').write_text(link_artwork('REPOSITORIES',168,'github'))
