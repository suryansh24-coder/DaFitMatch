import re

with open('index.html', 'r') as f:
    content = f.read()

# Fix global h1 and p in CSS
content = content.replace('    h1 {', '    .stage h1 {')
content = content.replace('    h1 span {', '    .stage h1 span {')
content = content.replace('    h1 span:nth-child', '    .stage h1 span:nth-child')
content = content.replace('    p {', '    .stage p {')
content = content.replace('      h1 {', '      .stage h1 {')
content = content.replace('      p {', '      .stage p {')

# Inject new CSS before </style>
new_css = """
    /* ==================================================
       HOMEPAGE STYLES
       ================================================= */
    .hp-wrapper {
      position: relative;
      z-index: 100;
      background: #000;
      color: #fff;
      font-family: 'Manrope', system-ui, sans-serif;
    }
    
    .hp-nav {
      position: fixed;
      top: 0;
      left: 0;
      width: 100%;
      padding: 24px 40px;
      display: flex;
      justify-content: space-between;
      align-items: center;
      z-index: 200;
      background: rgba(0, 0, 0, 0.1);
      backdrop-filter: blur(12px);
      -webkit-backdrop-filter: blur(12px);
      border-bottom: 1px solid rgba(255, 255, 255, 0.05);
    }
    .hp-nav-left { font-size: 20px; font-weight: 700; letter-spacing: -0.04em; text-transform: uppercase; }
    .hp-nav-center { display: flex; gap: 40px; font-size: 14px; font-weight: 500; text-transform: uppercase; letter-spacing: 0.05em; }
    .hp-nav-center a { color: #fff; text-decoration: none; opacity: 0.7; transition: opacity 0.3s; }
    .hp-nav-center a:hover { opacity: 1; }
    .hp-nav-right .signin-btn {
      padding: 12px 24px; border-radius: 999px; background: rgba(255, 255, 255, 0.1);
      border: 1px solid rgba(255, 255, 255, 0.2); color: #fff; font-size: 14px; cursor: pointer; transition: all 0.3s ease; text-transform: uppercase; letter-spacing: 0.05em; font-weight: 600;
    }
    .hp-nav-right .signin-btn:hover { background: #fff; color: #000; }

    .hp-hero {
      position: relative;
      height: 100vh;
      display: flex;
      align-items: center;
      justify-content: center;
      text-align: center;
      overflow: hidden;
    }
    .hp-hero-bg {
      position: absolute;
      inset: 0;
      background-image: url('hero-bg.png');
      background-size: cover;
      background-position: center;
      background-repeat: no-repeat;
      z-index: 1;
      animation: slowZoom 25s ease-out infinite alternate;
    }
    .hp-hero-bg::after {
      content: ''; position: absolute; inset: 0;
      background: linear-gradient(to bottom, rgba(0,0,0,0.1) 0%, rgba(0,0,0,0.7) 100%);
    }
    @keyframes slowZoom {
      0% { transform: scale(1); }
      100% { transform: scale(1.08); }
    }
    
    .hp-hero-content {
      position: relative;
      z-index: 2;
      max-width: 900px;
      padding: 0 20px;
      animation: fadeUp 1.2s ease-out;
    }
    @keyframes fadeUp {
      from { opacity: 0; transform: translateY(30px); }
      to { opacity: 1; transform: translateY(0); }
    }
    .hp-hero h1 {
      font-size: clamp(56px, 8vw, 110px);
      font-weight: 700;
      line-height: 0.9;
      letter-spacing: -0.05em;
      margin-bottom: 24px;
      text-transform: uppercase;
      margin-top: 60px; /* offset navbar */
      text-shadow: 0 4px 32px rgba(0,0,0,0.8);
    }
    .hp-hero p {
      font-size: clamp(16px, 2vw, 22px);
      font-weight: 400;
      line-height: 1.5;
      color: rgba(255, 255, 255, 0.85);
      margin-bottom: 48px;
      max-width: 650px;
      margin-left: auto;
      margin-right: auto;
      text-shadow: 0 2px 12px rgba(0,0,0,0.8);
    }
    .hp-hero-actions {
      display: flex;
      gap: 16px;
      justify-content: center;
    }
    .hp-btn-primary, .hp-btn-secondary {
      padding: 18px 36px;
      border-radius: 999px;
      font-size: 14px;
      font-weight: 600;
      text-transform: uppercase;
      letter-spacing: 0.05em;
      cursor: pointer;
      text-decoration: none;
      transition: all 0.3s ease;
    }
    .hp-btn-primary {
      background: #fff;
      color: #000;
      border: 1px solid #fff;
    }
    .hp-btn-primary:hover {
      background: rgba(255,255,255,0.8);
    }
    .hp-btn-secondary {
      background: rgba(0, 0, 0, 0.3);
      color: #fff;
      border: 1px solid rgba(255, 255, 255, 0.3);
      backdrop-filter: blur(12px);
      -webkit-backdrop-filter: blur(12px);
    }
    .hp-btn-secondary:hover {
      background: rgba(255, 255, 255, 0.1);
    }

    .hp-section {
      padding: 160px 40px;
      max-width: 1400px;
      margin: 0 auto;
    }
    .hp-section-title {
      font-size: clamp(36px, 5vw, 56px);
      font-weight: 700;
      letter-spacing: -0.05em;
      margin-bottom: 80px;
      text-transform: uppercase;
    }

    .hp-catalog-grid {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
      gap: 24px;
    }
    .hp-card {
      position: relative;
      height: 480px;
      border-radius: 12px;
      overflow: hidden;
      background: #0a0a0a;
      border: 1px solid rgba(255,255,255,0.05);
      display: flex;
      flex-direction: column;
      justify-content: flex-end;
      padding: 40px;
      transition: transform 0.5s cubic-bezier(0.22, 1, 0.36, 1), border-color 0.5s ease;
      cursor: pointer;
    }
    .hp-card:hover {
      transform: translateY(-12px);
      border-color: rgba(255,255,255,0.2);
    }
    .hp-card-bg {
      position: absolute; inset: 0; background: linear-gradient(180deg, #1a1a1a 0%, #050505 100%); z-index: 0;
      transition: opacity 0.5s ease;
    }
    .hp-card:hover .hp-card-bg { opacity: 0.6; }
    .hp-card-content { position: relative; z-index: 1; }
    .hp-card-number { font-size: 14px; color: rgba(255,255,255,0.4); margin-bottom: 12px; font-weight: 600; letter-spacing: 0.05em; }
    .hp-card h3 { font-size: 32px; font-weight: 700; margin: 0 0 16px 0; letter-spacing: -0.03em; text-transform: uppercase; }
    .hp-card p { font-size: 16px; color: rgba(255,255,255,0.6); margin: 0; line-height: 1.5; }

    .hp-about-grid {
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 100px;
      align-items: center;
    }
    .hp-about-left h2 {
      font-size: clamp(40px, 6vw, 64px);
      font-weight: 700;
      letter-spacing: -0.05em;
      line-height: 1.1;
      margin: 0 0 32px 0;
      text-transform: uppercase;
    }
    .hp-about-left p {
      font-size: 22px; color: rgba(255,255,255,0.7); line-height: 1.6; margin: 0;
    }
    .hp-features {
      display: grid; grid-template-columns: 1fr 1fr; gap: 60px 40px;
    }
    .hp-feature {
      padding-top: 24px;
      border-top: 1px solid rgba(255,255,255,0.1);
    }
    .hp-feature h4 { font-size: 16px; margin: 0 0 16px 0; letter-spacing: 0.05em; text-transform: uppercase; color: #fff; }
    .hp-feature p { font-size: 16px; color: rgba(255,255,255,0.5); margin: 0; line-height: 1.6; }

    .hp-fair {
      text-align: center;
      padding: 200px 40px;
      background: radial-gradient(circle at center, rgba(30,30,30,0.4) 0%, #000 60%);
      border-top: 1px solid rgba(255,255,255,0.05);
      border-bottom: 1px solid rgba(255,255,255,0.05);
    }
    .hp-fair h2 { font-size: clamp(48px, 8vw, 80px); font-weight: 700; letter-spacing: -0.05em; margin: 0 0 40px 0; text-transform: uppercase; }
    .hp-fair p { font-size: 24px; color: rgba(255,255,255,0.7); max-width: 900px; margin: 0 auto; line-height: 1.6; }

    .hp-transition {
      height: 40vh;
      display: flex;
      flex-direction: column;
      align-items: center;
      justify-content: flex-end;
      padding-bottom: 60px;
      background: #000;
    }
    .hp-transition h2 {
      font-size: 24px; font-weight: 600; letter-spacing: 0.05em; text-transform: uppercase; color: rgba(255,255,255,0.4);
      margin: 0 0 40px 0;
    }
    .hp-scroll-indicator {
      width: 1px; height: 80px; background: rgba(255,255,255,0.1); position: relative; overflow: hidden;
    }
    .hp-scroll-indicator::after {
      content: ''; position: absolute; top: 0; left: 0; width: 100%; height: 50%; background: rgba(255,255,255,0.6);
      animation: scrollDown 2s infinite cubic-bezier(0.65, 0, 0.35, 1);
    }
    @keyframes scrollDown {
      0% { transform: translateY(-100%); }
      100% { transform: translateY(200%); }
    }

    @media (max-width: 900px) {
      .hp-nav { padding: 20px; }
      .hp-nav-center { display: none; }
      .hp-about-grid { grid-template-columns: 1fr; gap: 60px; }
      .hp-section { padding: 100px 24px; }
      .hp-hero-actions { flex-direction: column; }
      .hp-fair { padding: 120px 24px; }
    }
"""
content = content.replace('  </style>', new_css + '\n  </style>')

# Inject new HTML at the start of <body>
new_html = """
  <div class="hp-wrapper">
    <nav class="hp-nav">
      <div class="hp-nav-left">THE FIT CHECK</div>
      <div class="hp-nav-center">
        <a href="#">Home</a>
        <a href="#about">About</a>
        <a href="#fair">Fair</a>
      </div>
      <div class="hp-nav-right">
        <button class="signin-btn">Sign in with Google</button>
      </div>
    </nav>

    <section class="hp-hero">
      <div class="hp-hero-bg"></div>
      <div class="hp-hero-content">
        <h1>YOUR STYLE.<br>YOUR FIT.<br>THE FIT CHECK.</h1>
        <p>Discover what truly suits you. Build your aesthetic, visualize your outfits, and find your perfect fit with AI.</p>
        <div class="hp-hero-actions">
          <a href="#experience" class="hp-btn-primary">Start Your Fit Check</a>
          <a href="#catalog" class="hp-btn-secondary">Explore Styles</a>
        </div>
      </div>
    </section>

    <section id="catalog" class="hp-section">
      <h2 class="hp-section-title">Explore Your Fit</h2>
      <div class="hp-catalog-grid">
        <div class="hp-card">
          <div class="hp-card-bg"></div>
          <div class="hp-card-content">
            <div class="hp-card-number">01</div>
            <h3>MEN</h3>
            <p>Classic, contemporary and effortless.</p>
          </div>
        </div>
        <div class="hp-card">
          <div class="hp-card-bg"></div>
          <div class="hp-card-content">
            <div class="hp-card-number">02</div>
            <h3>WOMEN</h3>
            <p>Explore silhouettes, aesthetics and trends.</p>
          </div>
        </div>
        <div class="hp-card">
          <div class="hp-card-bg"></div>
          <div class="hp-card-content">
            <div class="hp-card-number">03</div>
            <h3>STREETWEAR</h3>
            <p>Bold fits. Individual expression.</p>
          </div>
        </div>
        <div class="hp-card">
          <div class="hp-card-bg"></div>
          <div class="hp-card-content">
            <div class="hp-card-number">04</div>
            <h3>FORMAL</h3>
            <p>Sharp, refined and occasion-ready.</p>
          </div>
        </div>
      </div>
    </section>

    <section id="about" class="hp-section">
      <div class="hp-about-grid">
        <div class="hp-about-left">
          <h2>Fashion is easy.<br>Knowing what suits you isn't.</h2>
          <p>The Fit Check uses AI to understand your occasion, aesthetic, preferences and personal style &mdash; helping you discover outfits that actually feel like you.</p>
        </div>
        <div class="hp-features">
          <div class="hp-feature">
            <h4>AI PERSONAL STYLIST</h4>
            <p>Personalized recommendations based on your preferences.</p>
          </div>
          <div class="hp-feature">
            <h4>3D VIRTUAL TRY-ON</h4>
            <p>Visualize outfits on your digital avatar.</p>
          </div>
          <div class="hp-feature">
            <h4>SMART OUTFIT DISCOVERY</h4>
            <p>Search clothing using text or images.</p>
          </div>
          <div class="hp-feature">
            <h4>SHOP YOUR FIT</h4>
            <p>Find the actual products online and build your shopping list.</p>
          </div>
        </div>
      </div>
    </section>

    <section id="fair" class="hp-fair">
      <h2>FASHION, MADE PERSONAL.</h2>
      <p>Instead of endlessly scrolling through thousands of products, tell us where you're going, how you want to look, and what you like. The Fit Check helps you find the rest.</p>
    </section>

    <section class="hp-transition">
      <h2>NOW, LET'S BUILD YOUR FIT.</h2>
      <div class="hp-scroll-indicator"></div>
    </section>
  </div>
"""

# Inject right after <body>, and add id="experience" to .stage
content = content.replace('<body>\n', f'<body>\n{new_html}\n')
content = content.replace('<div class="stage">', '<div id="experience" class="stage">')

with open('index.html', 'w') as f:
    f.write(content)
