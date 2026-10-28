from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import mm
from reportlab.platypus import (SimpleDocTemplate, Paragraph, Spacer, PageBreak,
    Table, TableStyle, KeepTogether, HRFlowable, ListFlowable, ListItem)
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
from reportlab.graphics.shapes import Drawing, Rect, String, Line, Polygon
from reportlab.pdfgen.canvas import Canvas

OUT = "output/pdf/financial_chat_system_design_relearning_roadmap.pdf"
NAVY = colors.HexColor("#14213D")
BLUE = colors.HexColor("#2457C5")
SKY = colors.HexColor("#EAF2FF")
TEAL = colors.HexColor("#168C85")
INK = colors.HexColor("#1F2937")
MUTED = colors.HexColor("#607086")
PALE = colors.HexColor("#F5F7FA")
AMBER = colors.HexColor("#FFF4D6")
RED = colors.HexColor("#A53A3A")

pdfmetrics.registerFont(TTFont("Inter", "/System/Library/Fonts/Supplemental/Arial.ttf"))
pdfmetrics.registerFont(TTFont("Inter-Bold", "/System/Library/Fonts/Supplemental/Arial Bold.ttf"))
pdfmetrics.registerFont(TTFont("Mono", "/System/Library/Fonts/Supplemental/Courier New.ttf"))

styles = getSampleStyleSheet()
styles.add(ParagraphStyle(name="BodyX", fontName="Inter", fontSize=9.6, leading=14.2, textColor=INK, spaceAfter=7))
styles.add(ParagraphStyle(name="SmallX", fontName="Inter", fontSize=8.1, leading=11.2, textColor=MUTED))
styles.add(ParagraphStyle(name="H1X", fontName="Inter-Bold", fontSize=20, leading=24, textColor=NAVY, spaceBefore=2, spaceAfter=10))
styles.add(ParagraphStyle(name="H2X", fontName="Inter-Bold", fontSize=13.2, leading=16, textColor=BLUE, spaceBefore=10, spaceAfter=5))
styles.add(ParagraphStyle(name="H3X", fontName="Inter-Bold", fontSize=10.4, leading=13, textColor=NAVY, spaceBefore=6, spaceAfter=3))
styles.add(ParagraphStyle(name="QuoteX", fontName="Inter", fontSize=10, leading=14.5, leftIndent=10, rightIndent=8, borderColor=BLUE, borderWidth=0, borderPadding=7, backColor=SKY, textColor=NAVY, spaceBefore=5, spaceAfter=9))
styles.add(ParagraphStyle(name="CodeX", fontName="Mono", fontSize=7.7, leading=10.2, leftIndent=7, rightIndent=7, borderPadding=7, backColor=colors.HexColor("#EEF1F5"), textColor=colors.HexColor("#243247"), spaceBefore=4, spaceAfter=8))
styles.add(ParagraphStyle(name="CellX", fontName="Inter", fontSize=7.6, leading=10, textColor=INK))
styles.add(ParagraphStyle(name="CellHeadX", fontName="Inter-Bold", fontSize=7.8, leading=10, textColor=colors.white))

def P(text, style="BodyX"): return Paragraph(text, styles[style])
def bullets(items):
    return ListFlowable([ListItem(P(x), leftIndent=11) for x in items], bulletType='bullet', start='circle', leftIndent=17, bulletFontName='Inter', bulletFontSize=6, spaceAfter=6)
def code(text): return P(text.replace("\n", "<br/>"), "CodeX")
def callout(title, text, color=SKY):
    t = Table([[P(title, "H3X")], [P(text)]], colWidths=[170*mm])
    t.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,-1),color),('BOX',(0,0),(-1,-1),0.5,colors.HexColor('#BCD0EA')),('LEFTPADDING',(0,0),(-1,-1),9),('RIGHTPADDING',(0,0),(-1,-1),9),('TOPPADDING',(0,0),(-1,-1),4),('BOTTOMPADDING',(0,0),(-1,-1),5)]))
    return t
def section(num, title): return [Spacer(1,2*mm), P(f"{num}. {title}", "H1X"), HRFlowable(width="100%", thickness=1, color=colors.HexColor('#D8E0EC')), Spacer(1,2*mm)]

def box(d, x, y, w, h, label, fill=SKY, stroke=BLUE, fs=8):
    d.add(Rect(x,y,w,h,rx=5,ry=5,fillColor=fill,strokeColor=stroke,strokeWidth=0.8))
    lines=label.split('\n')
    for i,s in enumerate(lines): d.add(String(x+w/2,y+h/2+(len(lines)-1-i)*9-3,s,fontName='Inter-Bold' if i==0 else 'Inter',fontSize=fs,textAnchor='middle',fillColor=NAVY))
def arrow(d,x1,y1,x2,y2):
    d.add(Line(x1,y1,x2,y2,strokeColor=MUTED,strokeWidth=1.1))
    if abs(x2-x1)>abs(y2-y1): pts=[x2,y2,x2-5,y2+3,x2-5,y2-3] if x2>x1 else [x2,y2,x2+5,y2+3,x2+5,y2-3]
    else: pts=[x2,y2,x2-3,y2+5,x2+3,y2+5] if y2<y1 else [x2,y2,x2-3,y2-5,x2+3,y2-5]
    d.add(Polygon(pts,fillColor=MUTED,strokeColor=MUTED))

def architecture():
    d=Drawing(485,335)
    box(d,190,295,105,28,"User / Chat App",colors.HexColor('#DCE9FF'))
    box(d,190,248,105,28,"API Backend") ; arrow(d,242,295,242,276)
    box(d,180,198,125,30,"Query Router / Classifier",colors.HexColor('#E5F7F4'),TEAL); arrow(d,242,248,242,228)
    xs=[20,137,254,371]; labs=["Product\nSupport","Market\nResearch","Stock\nData","Calculation\nJobs"]
    for x,l in zip(xs,labs): box(d,x,137,94,34,l); arrow(d,242,198,x+47,171)
    deps=["Support KB","Vector DB\n+ reports","Market APIs\n+ fundamentals","Code Sandbox\n+ query engine"]
    for x,l in zip(xs,deps): box(d,x,75,94,34,l,PALE,colors.HexColor('#9AA9BD'),7.5); arrow(d,x+47,137,x+47,109)
    box(d,120,15,110,32,"LLM + Answer",colors.HexColor('#EEE9FF'),colors.HexColor('#7159B8'))
    box(d,275,15,110,32,"Safety + Policy",AMBER,colors.HexColor('#C08A16'))
    for x in xs: arrow(d,x+47,75,175,47)
    arrow(d,230,31,275,31)
    d.add(String(430,28,"Sensitive action",fontName='Inter',fontSize=7,fillColor=RED,textAnchor='middle'))
    box(d,405,4,75,20,"Human review",colors.HexColor('#FCE8E8'),RED,7); arrow(d,385,31,405,14)
    return d

def footer(canvas: Canvas, doc):
    canvas.saveState(); w,h=A4
    canvas.setStrokeColor(colors.HexColor('#D8E0EC')); canvas.line(20*mm,15*mm,w-20*mm,15*mm)
    canvas.setFont('Inter',7.5); canvas.setFillColor(MUTED)
    canvas.drawString(20*mm,10*mm,"Financial Chat System Design - Relearning Roadmap")
    canvas.drawRightString(w-20*mm,10*mm,f"{doc.page}")
    canvas.restoreState()

story=[]
story += [Spacer(1,28*mm), P("FINANCIAL CHAT SYSTEM DESIGN", "SmallX"), Spacer(1,4*mm),
          Paragraph("Relearning Roadmap", ParagraphStyle('TitleX',parent=styles['H1X'],fontSize=31,leading=35,textColor=NAVY)),
          Spacer(1,5*mm), Paragraph("A beginner-friendly study guide for rebuilding the software, data, cloud, and AI foundations behind a production financial chat application.", ParagraphStyle('Deck',parent=styles['BodyX'],fontSize=13,leading=19,textColor=MUTED)),
          Spacer(1,14*mm), architecture(), Spacer(1,5*mm),
          callout("The destination", "Explain what every component does, why it exists, how it communicates, what can fail, and why this design is preferable to the alternatives.", colors.HexColor('#E5F7F4')),
          Spacer(1,13*mm), P("Study-guide edition | Built from the complete learning plan", "SmallX"), PageBreak()]

story += section(1,"What the assignment is actually testing")
story += [P("You do not need to relearn your entire Electronic and Computer Engineering diploma first. This project is mainly about software systems, backend architecture, databases, cloud infrastructure, APIs, and modern AI systems."),
          P("Imagine one brokerage chat box receiving all of these messages:"),
          code('"What is Apple\'s current share price?"\n"Summarize the latest analyst reports about NVIDIA."\n"How do I request a refund?"\n"Using our historical dataset, calculate Tesla\'s 30-day volatility."\n"Refund my subscription."'),
          P("They look alike because they are all chat messages, but each requires a different technical path."),
          P("The real question is:","H2X"),
          P("How do you build the system behind the chat box so it understands intent, finds the right information, performs calculations, responds quickly, survives heavy traffic, and prevents unsafe actions?", "QuoteX")]

story += section(2,"The big picture")
story += [P("The architecture is a map, not a list to memorize. Use it to connect each requirement to a component."), architecture(),
          P("A query first reaches the backend and router. Product questions use support knowledge; research questions search fresh reports; stock questions use appropriate data sources; calculation requests run in an isolated sandbox. The LLM assembles a grounded answer, while policy checks intercept sensitive actions and route them to a human."),
          callout("Your system-design goal", "For every box, be ready to explain its responsibility, input and output, failure modes, scaling strategy, security boundary, and trade-offs.")]

story += section(3,"Layer 1 - Basic software and computing foundations")
story += [P("Rebuild the mental model of how software works before diving into AI or cloud architecture."),
          bullets(["Client vs server; frontend vs backend", "HTTP and HTTPS; requests and responses", "APIs, REST, and JSON", "Authentication vs authorization", "Processes, CPU, memory, and storage", "IP addresses, DNS, ports, TCP, and latency"]),
          code("Phone  -- HTTPS request -->  Backend server  -- SQL query -->  Database"),
          callout("Checkpoint", "Explain, in plain language, what roughly happens between pressing Send in a chat app and receiving the first words of the reply.", AMBER)]

story += section(4,"Layer 2 - Programming with Python")
story += [P("Python is the most useful primary language for this project. Start with variables, data types, conditions, loops, functions, lists, dictionaries, classes, exceptions, files, modules, and packages."),
          P("Then connect those basics to real systems:","H2X"), bullets(["HTTP requests and APIs", "JSON", "SQL and Pandas", "Asynchronous programming", "Basic backend development"]),
          code("def get_stock_price(symbol):\n    price = stock_api.get(symbol)\n    return price\n\n@app.get('/stock/{symbol}')\ndef stock(symbol):\n    return get_stock_price(symbol)"),
          P("The important step is seeing how a small function becomes part of a backend endpoint that another application can call.")]

story += section(5,"Layer 3 - Databases and data engineering")
story += [P("The 500 GB internal-data requirement is a deliberate clue: the system cannot load everything into Python memory."),
          P("Begin with database fundamentals:","H2X"), bullets(["Tables, rows, columns, primary keys, and foreign keys", "SELECT, WHERE, JOIN, GROUP BY, and indexes", "Relational data and when SQL fits", "Object storage, data warehouses, and data lakes", "Caching, indexing, partitioning, and replication"]),
          code("SELECT price\nFROM stocks\nWHERE symbol = 'AAPL';"),
          code("500 GB dataset -> durable storage -> query engine -> required rows only -> Python sandbox"),
          P("For a request such as calculating AAPL's average return from 2020 to 2025, the query engine should retrieve only the relevant symbol, dates, and columns. This keeps transfer, memory, and compute manageable."),
          callout("Design principle", "Move the computation close to the data when practical, and move only the smallest useful result into the sandbox.")]

story += section(6,"Layer 4 - Backend system design")
story += [P("This layer joins the application pieces into services that can handle traffic and failure."),
          bullets(["Servers, APIs, and service boundaries", "Load balancers and horizontal vs vertical scaling", "Caches, queues, and background workers", "Rate limits, timeouts, retries, and circuit breakers", "Health checks, logs, metrics, and alerts"]),
          code("Users -> Load balancer -> [Server A | Server B | Server C]"),
          P("If traffic grows from 100 to 10,000 requests per second during a market event, multiple stateless application servers can share the load. Queues can separate expensive calculation jobs so they do not overwhelm fast chat requests."),
          callout("Requirement connection", "Elastic load handling means scaling capacity, isolating heavy work, applying backpressure, and degrading gracefully when dependencies are overloaded.", AMBER)]

story += section(7,"Layer 5 - AI and LLM fundamentals")
story += [P("Only after the base layers should you go deeper into the AI-specific pieces."),
          bullets(["LLMs, tokens, context windows, prompts, and system prompts", "Hallucination and temperature", "Embeddings, semantic search, and vector databases", "Retrieval-Augmented Generation (RAG)", "Tool or function calling, agents, and structured outputs"]),
          P("RAG is central because the corpus contains more than 5,000 reports and grows by about 100 per day. You cannot paste the entire corpus into every prompt."),
          code("Reports -> split into chunks -> create embeddings -> vector database\n\nQuestion -> query embedding -> vector search -> relevant passages -> LLM -> grounded answer"),
          P("For a question about NVIDIA's AI revenue, retrieval finds the most relevant report passages. The LLM answers using that evidence and should include source metadata or citations so users can verify it."),
          callout("Freshness pipeline", "Ingest new reports, extract text, clean and chunk them, attach metadata, create embeddings, update the index, and monitor failures. Freshness is an operational pipeline, not a one-time upload.")]

story += section(8,"Layer 6 - Routing and orchestration")
story += [P("The system should not treat every message identically. It must classify intent, select tools, and coordinate steps."),
          code('"How do I change my password?" -> PRODUCT SUPPORT\n"What is Tesla trading at?" -> LIVE STOCK DATA\n"What are analysts saying about Tesla?" -> MARKET RESEARCH / RAG\n"Calculate Tesla\'s volatility over 3 years." -> CALCULATION / SANDBOX'),
          bullets(["Classification: what kind of request is this?", "Routing: which subsystem should handle it?", "Tool selection: which API, database, or retrieval system is appropriate?", "Orchestration: what steps run, in what order, and which can run in parallel?"]),
          callout("Practical trade-off", "Use deterministic rules for high-risk boundaries, a small fast classifier for common intent routing, and the larger LLM where language understanding or synthesis adds value.", AMBER)]

story += section(9,"Layer 7 - Reliability, performance, and distributed systems")
story += [P("The target is an average time to first token (TTFT) below two seconds. That is the delay before the user sees the first generated text."),
          code("1 second: fast\n2 seconds: acceptable target\n5 seconds: slow\n15 seconds: appears broken"),
          P("A heavy path may include classification, database lookup, vector search, an external API call, the LLM, and code execution. Useful techniques include:"),
          bullets(["Stream the answer as soon as generation begins", "Cache safe, reusable results with appropriate freshness limits", "Run independent retrievals in parallel", "Use async I/O and connection pooling", "Precompute expensive reusable values", "Use a smaller model for simple classification", "Set timeouts, retry selectively, and provide fallbacks"]),
          code("Sequential: A -> B -> C -> D\nParallelizable: A -> [B and C] -> D"),
          P("Do not force every workload into the same latency promise. A stock quote should be fast; a large computation can acknowledge the job quickly, stream status, and finish asynchronously.")]

story += section(10,"Layer 8 - Security and AI safety")
story += [P("A financial application must assume sensitive data, valuable actions, and adversarial input."),
          bullets(["Authentication, authorization, and role-based access control", "TLS, encryption, and secrets management", "Input validation, audit logs, rate limiting, and least privilege", "Prompt injection defenses and data-leakage controls", "Personally identifiable information (PII)", "Sandboxing and human-in-the-loop approval"]),
          P("The AI may explain the refund policy, but it must not issue a refund by itself."),
          code("User request -> intent detection -> REFUND ACTION -> policy and permission check -> human review -> approve or reject -> refund system"),
          callout("Core principle", "An LLM's ability to understand an instruction does not justify giving it unlimited authority to execute that instruction.", colors.HexColor('#FCE8E8'))]

story += section(11,"Financial concepts to learn")
story += [P("You do not need investment-banking expertise, but you do need enough domain vocabulary to choose correct data sources and interpret questions."),
          bullets(["Stocks, shares, ticker symbols, market price, bid and ask", "Market capitalization, revenue, profit, EPS, P/E, and dividends", "Financial statements, returns, volatility, and trading volume", "Historical data vs real-time or near-real-time market data"]),
          Table([[P("Fundamental data","CellHeadX"),P("Market data","CellHeadX")],[P("Revenue, profit, EPS, P/E, balance sheet, cash flow","CellX"),P("Current price, bid, ask, volume, daily high/low, price history","CellX")]],colWidths=[85*mm,85*mm],style=TableStyle([('BACKGROUND',(0,0),(-1,0),NAVY),('GRID',(0,0),(-1,-1),0.4,colors.HexColor('#C8D2E0')),('VALIGN',(0,0),(-1,-1),'TOP'),('LEFTPADDING',(0,0),(-1,-1),7),('RIGHTPADDING',(0,0),(-1,-1),7),('TOPPADDING',(0,0),(-1,-1),6),('BOTTOMPADDING',(0,0),(-1,-1),6)])),
          P("This distinction matters because live prices usually come from a market-data provider with freshness and entitlement constraints, while company fundamentals may come from filings or a financial-data store.")]

story += section(12,"Docker and sandboxing")
story += [P("Generated code must run inside a temporary isolated environment, never directly on production servers."),
          bullets(["Process and container isolation", "CPU and memory limits", "Execution timeouts", "Restricted network access", "Read-only or disposable filesystems", "Allowlisted libraries and data-access interfaces", "Output size limits and audit logs"]),
          code("LLM -> generated Python -> isolated container\n                         CPU: limited\n                         RAM: limited\n                         runtime: limited\n                         network: restricted\n                         filesystem: isolated\n                    -> sanitized result"),
          P("These controls contain infinite loops, excessive memory use, dangerous file operations, and unauthorized network access.")]

story += section(13,"The 14-phase learning roadmap")
road=[
('1','Computer and software fundamentals','Rebuild your mental model'),('2','Python','Learn to build things'),('3','Networking, HTTP, and APIs','Understand system communication'),('4','SQL and databases','Understand data'),('5','Backend development','Build services'),('6','Git, Linux, and Docker','Use a real engineering workflow'),('7','System-design fundamentals','Understand scalable architecture'),('8','LLM fundamentals','Understand the AI'),('9','Embeddings, vector DB, and RAG','Build knowledge retrieval'),('10','Tool calling and routing','Build AI workflows'),('11','Distributed systems and scaling','Handle real traffic'),('12','Security and reliability','Make it production-worthy'),('13','Financial-data basics','Understand the domain'),('14','Build the project','Combine everything')]
data=[[P('Phase','CellHeadX'),P('Learn','CellHeadX'),P('Why','CellHeadX')]]+[[P(a,'CellX'),P(b,'CellX'),P(c,'CellX')] for a,b,c in road]
tbl=Table(data,colWidths=[16*mm,73*mm,81*mm],repeatRows=1)
tbl.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,0),NAVY),('ROWBACKGROUNDS',(0,1),(-1,-1),[colors.white,PALE]),('GRID',(0,0),(-1,-1),0.35,colors.HexColor('#CCD5E1')),('VALIGN',(0,0),(-1,-1),'TOP'),('LEFTPADDING',(0,0),(-1,-1),6),('RIGHTPADDING',(0,0),(-1,-1),6),('TOPPADDING',(0,0),(-1,-1),5),('BOTTOMPADDING',(0,0),(-1,-1),5),('ALIGN',(0,1),(0,-1),'CENTER')]))
story += [P("Do not try to learn everything simultaneously. Progress in order, but overlap adjacent phases and build small projects throughout."),tbl,Spacer(1,4*mm),callout("Important", "You do not need to master Phase 1 before touching Phase 2. Learning becomes stickier when theory and small builds reinforce each other.", colors.HexColor('#E5F7F4'))]

story += section(14,"How engineers translate requirements into design questions")
reqs=[
('500 GB internal dataset','Where is it stored? How is it partitioned and queried? How much data does each job really need? What happens under concurrent load?'),
('TTFT below 2 seconds','Where is latency spent? What can be cached, parallelized, precomputed, streamed, or handled by a smaller model?'),
('100 new reports per day','How are documents ingested, parsed, chunked, embedded, indexed, monitored, and made searchable quickly?'),
('Refunds need human approval','How do we distinguish information from action? Where is the action intercepted? Who approves it? What authority does the AI have?'),
('Sudden traffic spike','Can services scale horizontally? Do heavy jobs need a separate queue? How do we protect lightweight requests and apply backpressure?')]
data=[[P('Requirement','CellHeadX'),P('Engineering questions it should trigger','CellHeadX')]]+[[P(a,'CellX'),P(b,'CellX')] for a,b in reqs]
t=Table(data,colWidths=[48*mm,122*mm],repeatRows=1)
t.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,0),BLUE),('ROWBACKGROUNDS',(0,1),(-1,-1),[colors.white,PALE]),('GRID',(0,0),(-1,-1),0.4,colors.HexColor('#C8D2E0')),('VALIGN',(0,0),(-1,-1),'TOP'),('LEFTPADDING',(0,0),(-1,-1),7),('RIGHTPADDING',(0,0),(-1,-1),7),('TOPPADDING',(0,0),(-1,-1),7),('BOTTOMPADDING',(0,0),(-1,-1),7)]))
story += [P("The deepest lesson is not drawing a beautiful diagram. It is learning to break vague requirements into concrete engineering problems and trade-offs."),t,
          Spacer(1,5*mm),P("That habit - asking where data lives, where latency comes from, where authority is checked, and where failure is contained - is the heart of system design.","QuoteX")]

story += section(15,"Recommended staged learning approach")
stages=[('1','How does a computer program work?','Write small Python programs.'),('2','How do two computers communicate?','Call a public HTTP API.'),('3','How does a backend/API work?','Build a tiny stock endpoint.'),('4','How does a database work?','Build a small stock database.'),('5','How do large systems scale?','Add caching, a queue, and multiple workers.'),('6','How does an LLM work?','Experiment with prompts and structured outputs.'),('7','How does RAG work?','Build a mini report-search system.'),('8','How does an AI use tools?','Route questions to support, stock, research, or calculation.'),('9','How do we make it safe and reliable?','Add permissions, sandbox limits, timeouts, fallbacks, and monitoring.'),('10','Build the financial chat system','Combine the pieces and defend the trade-offs.')]
for n,q,b in stages:
    story.append(KeepTogether([P(f"Stage {n}: {q}","H2X"),P(f"Build: {b}")]))
story += [Spacer(1,3*mm), callout("Why this works", "By the final stage, the architecture is not a diagram you memorized. You understand why each component exists because you encountered the problem that required it.", colors.HexColor('#E5F7F4')),
          PageBreak(),P("Your first practical study cycle", "H1X"),
          P("Use this guide as a loop: learn a concept, build the smallest useful example, explain it without jargon, then connect it back to the financial-chat requirements."),
          P("Suggested first four builds", "H2X"),
          bullets(["A Python script that fetches a stock quote from an API and prints JSON", "A small backend with one stock endpoint and one support endpoint", "A SQL database containing symbols and historical prices, queried by date range", "A rule-based router that labels sample messages as PRODUCT, STOCK, MARKET, or CALCULATION"]),
          P("For each build, write down:","H2X"), bullets(["What problem does this solve?", "What are the inputs and outputs?", "What can fail?", "How would it behave with 1,000 times more traffic or data?", "What security boundary is required?", "What alternative design did you reject, and why?"]),
          callout("Final perspective", "You are rebuilding your technical foundation through one coherent final project. Progress comes from repeatedly connecting a small piece of working software to the larger architecture - not from memorizing every term before you begin.", AMBER)]

doc=SimpleDocTemplate(OUT,pagesize=A4,rightMargin=20*mm,leftMargin=20*mm,topMargin=19*mm,bottomMargin=20*mm,title="Financial Chat System Design - Relearning Roadmap",author="OpenAI Codex")
doc.build(story,onFirstPage=footer,onLaterPages=footer)
print(OUT)
