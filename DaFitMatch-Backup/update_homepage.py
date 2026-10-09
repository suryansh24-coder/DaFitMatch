import re

with open('index.html', 'r') as f:
    content = f.read()

# 1. Replace the CSS block
css_pattern = r'/\* ====(.*?)\n  </style>'
new_css = """/* ==================================================
       HOMEPAGE STYLES (EDITORIAL)
       ================================================= */
    .hp-wrapper {
      position: relative;
      z-index: 100;
      background: #000;
      color: #fff;
      font-family: 'Manrope', system-ui, sans-serif;
    }
    
    .hp-nav {
      position: absolute;
      top: 0;
      left: 0;
      width: 100%;
      padding: 40px 60px;
      display: flex;
      justify-content: space-between;
      align-items: center;
      z-index: 200;
    }
    .hp-nav-left { font-size: 16px; font-weight: 700; letter-spacing: 0.1em; text-transform: uppercase; }
    .hp-nav-right { display: flex; gap: 48px; font-size: 13px; font-weight: 500; text-transform: uppercase; letter-spacing: 0.1em; }
    .hp-nav-right a { color: #fff; text-decoration: none; opacity: 0.6; transition: opacity 0.4s ease; }
    .hp-nav-right a:hover { opacity: 1; }

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
      transform: scale(1.02);
      animation: ambientDrift 30s ease-in-out infinite alternate;
    }
    .hp-hero-bg::after {
      content: ''; position: absolute; inset: 0;
      background: radial-gradient(circle at center, rgba(0,0,0,0) 0%, rgba(0,0,0,0.5) 100%);
    }
    @keyframes ambientDrift {
      0% { transform: scale(1.02) translateY(0); }
      100% { transform: scale(1.06) translateY(-2%); }
    }
    
    .hp-hero-content {
      position: relative;
      z-index: 2;
      max-width: 1200px;
      padding: 0 40px;
      margin-top: 10vh;
      animation: editorialFade 2s cubic-bezier(0.22, 1, 0.36, 1) forwards;
    }
    @keyframes editorialFade {
      0% { opacity: 0; filter: blur(10px); transform: translateY(40px); }
      100% { opacity: 1; filter: blur(0); transform: translateY(0); }
    }
    
    .hp-hero h1 {
      font-size: clamp(60px, 12vw, 160px);
      font-weight: 500;
      line-height: 0.85;
      letter-spacing: -0.06em;
      text-transform: uppercase;
      margin: 0 0 32px 0;
      color: rgba(255,255,255,0.95);
      position: static;
      transform: none;
      width: auto;
    }
    .hp-hero-subtitle {
      font-size: 14px;
      font-weight: 400;
      letter-spacing: 0.2em;
      text-transform: uppercase;
      color: rgba(255, 255, 255, 0.6);
      margin-bottom: 64px;
    }
    
    .hp-hero-actions {
      display: flex;
      justify-content: center;
    }
    .hp-btn-text {
      font-size: 13px;
      font-weight: 600;
      text-transform: uppercase;
      letter-spacing: 0.1em;
      color: #fff;
      text-decoration: none;
      border-bottom: 1px solid rgba(255,255,255,0.3);
      padding-bottom: 8px;
      transition: border-color 0.4s ease, opacity 0.4s ease;
    }
    .hp-btn-text:hover {
      border-color: #fff;
      opacity: 0.8;
    }

    .hp-section {
      padding: 240px 80px;
      max-width: 1600px;
      margin: 0 auto;
    }
    .hp-section-header {
      display: flex;
      justify-content: space-between;
      align-items: flex-end;
      margin-bottom: 120px;
      border-bottom: 1px solid rgba(255,255,255,0.1);
      padding-bottom: 40px;
    }
    .hp-section-title {
      font-size: clamp(40px, 6vw, 80px);
      font-weight: 500;
      letter-spacing: -0.04em;
      margin: 0;
      text-transform: uppercase;
    }
    .hp-section-meta {
      font-size: 13px;
      letter-spacing: 0.1em;
      text-transform: uppercase;
      color: rgba(255,255,255,0.5);
    }

    /* Catalog blocks - Editorial style */
    .hp-catalog-grid {
      display: grid;
      grid-template-columns: repeat(4, 1fr);
      gap: 2px;
      background: rgba(255,255,255,0.05); /* creates thin borders between items */
    }
    .hp-card {
      position: relative;
      height: 600px;
      background: #000;
      display: flex;
      flex-direction: column;
      justify-content: space-between;
      padding: 40px;
      transition: background 0.6s ease;
      cursor: pointer;
    }
    .hp-card:hover {
      background: #0a0a0a;
    }
    .hp-card-number { 
      font-size: 80px; 
      font-weight: 400; 
      color: rgba(255,255,255,0.05); 
      letter-spacing: -0.05em; 
      line-height: 1;
      transition: color 0.6s ease;
    }
    .hp-card:hover .hp-card-number { color: rgba(255,255,255,0.15); }
    .hp-card-bottom {
      transform: translateY(20px);
      opacity: 0.6;
      transition: all 0.6s cubic-bezier(0.22, 1, 0.36, 1);
    }
    .hp-card:hover .hp-card-bottom {
      transform: translateY(0);
      opacity: 1;
    }
    .hp-card h3 { 
      font-size: 24px; 
      font-weight: 500; 
      margin: 0 0 16px 0; 
      letter-spacing: 0.02em; 
      text-transform: uppercase; 
    }
    .hp-card p { 
      font-size: 14px; 
      color: rgba(255,255,255,0.5); 
      margin: 0; 
      line-height: 1.6;
      position: static; width: auto; transform: none;
    }

    /* About Section */
    .hp-about-grid {
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 120px;
    }
    .hp-about-left h2 {
      font-size: clamp(48px, 6vw, 80px);
      font-weight: 500;
      letter-spacing: -0.04em;
      line-height: 1.05;
      margin: 0 0 60px 0;
      text-transform: uppercase;
    }
    .hp-about-left p {
      font-size: 20px; 
      color: rgba(255,255,255,0.6); 
      line-height: 1.6; 
      margin: 0;
      font-weight: 400;
    }
    .hp-features {
      display: flex;
      flex-direction: column;
      gap: 0;
    }
    .hp-feature {
      padding: 40px 0;
      border-bottom: 1px solid rgba(255,255,255,0.1);
      display: grid;
      grid-template-columns: 1fr 2fr;
      gap: 40px;
    }
    .hp-feature:first-child { border-top: 1px solid rgba(255,255,255,0.1); }
    .hp-feature h4 { font-size: 13px; margin: 0; letter-spacing: 0.1em; text-transform: uppercase; color: #fff; font-weight: 600; }
    .hp-feature p { font-size: 15px; color: rgba(255,255,255,0.5); margin: 0; line-height: 1.6; position: static; transform: none; width: auto; }

    /* Fair Section */
    .hp-fair {
      text-align: center;
      padding: 240px 40px;
      background: #000;
    }
    .hp-fair h2 { font-size: clamp(60px, 10vw, 120px); font-weight: 500; letter-spacing: -0.05em; margin: 0 0 60px 0; text-transform: uppercase; line-height: 0.9; }
    .hp-fair p { font-size: 20px; color: rgba(255,255,255,0.5); max-width: 600px; margin: 0 auto; line-height: 1.6; position: static; transform: none; width: auto; font-weight: 400; }

    /* Transition Section */
    .hp-transition {
      height: 60vh;
      display: flex;
      flex-direction: column;
      align-items: center;
      justify-content: flex-end;
      padding-bottom: 80px;
      background: linear-gradient(to bottom, #000 0%, #030303 100%);
    }
    .hp-transition h2 {
      font-size: 13px; 
      font-weight: 500; 
      letter-spacing: 0.2em; 
      text-transform: uppercase; 
      color: rgba(255,255,255,0.4);
      margin: 0 0 60px 0;
    }
    .hp-scroll-indicator {
      width: 1px; height: 120px; background: rgba(255,255,255,0.05); position: relative; overflow: hidden;
    }
    .hp-scroll-indicator::after {
      content: ''; position: absolute; top: 0; left: 0; width: 100%; height: 40%; background: rgba(255,255,255,0.8);
      animation: scrollDown 2.5s infinite cubic-bezier(0.65, 0, 0.35, 1);
    }
    @keyframes scrollDown {
      0% { transform: translateY(-100%); }
      100% { transform: translateY(300%); }
    }

    @media (max-width: 1200px) {
      .hp-catalog-grid { grid-template-columns: 1fr 1fr; }
      .hp-card { height: 400px; }
      .hp-about-grid { grid-template-columns: 1fr; gap: 80px; }
    }
    @media (max-width: 700px) {
      .hp-nav { padding: 32px 24px; }
      .hp-nav-right a:not(:last-child) { display: none; }
      .hp-section { padding: 120px 24px; }
      .hp-catalog-grid { grid-template-columns: 1fr; }
      .hp-feature { grid-template-columns: 1fr; gap: 16px; }
      .hp-fair { padding: 160px 24px; }
    }
\n  </style>"""
content = re.sub(css_pattern, new_css, content, flags=re.DOTALL)

# 2. Replace the HTML block
html_pattern = r'<div class="hp-wrapper">.*?<div id="experience" class="stage">'
new_html = """<div class="hp-wrapper">
    <nav class="hp-nav">
      <div class="hp-nav-left">THE FIT CHECK</div>
      <div class="hp-nav-right">
        <a href="#catalog">Catalog</a>
        <a href="#about">About</a>
        <a href="#">Sign In</a>
      </div>
    </nav>

    <section class="hp-hero">
      <div class="hp-hero-bg"></div>
      <div class="hp-hero-content">
        <div class="hp-hero-subtitle">Visual Intelligence</div>
        <h1>YOUR STYLE.<br>YOUR FIT.<br>THE FIT CHECK.</h1>
        <div class="hp-hero-actions">
          <a href="#experience" class="hp-btn-text">Experience the platform &rarr;</a>
        </div>
      </div>
    </section>

    <section id="catalog" class="hp-section">
      <div class="hp-section-header">
        <h2 class="hp-section-title">Explore<br>Your Fit</h2>
        <div class="hp-section-meta">Curated Collections</div>
      </div>
      <div class="hp-catalog-grid">
        <div class="hp-card">
          <div class="hp-card-number">01</div>
          <div class="hp-card-bottom">
            <h3>MEN</h3>
            <p>Classic, contemporary and effortless style language.</p>
          </div>
        </div>
        <div class="hp-card">
          <div class="hp-card-number">02</div>
          <div class="hp-card-bottom">
            <h3>WOMEN</h3>
            <p>Explore silhouettes, high-end aesthetics and trends.</p>
          </div>
        </div>
        <div class="hp-card">
          <div class="hp-card-number">03</div>
          <div class="hp-card-bottom">
            <h3>STREET</h3>
            <p>Bold fits. Unapologetic individual expression.</p>
          </div>
        </div>
        <div class="hp-card">
          <div class="hp-card-number">04</div>
          <div class="hp-card-bottom">
            <h3>FORMAL</h3>
            <p>Sharp, refined and exclusively occasion-ready.</p>
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
            <h4>Personal Stylist</h4>
            <p>Advanced algorithmic recommendations tailored exclusively to your visual preferences.</p>
          </div>
          <div class="hp-feature">
            <h4>Virtual Try-On</h4>
            <p>Visualize outfits dynamically on your fully reconstructed 3D digital avatar.</p>
          </div>
          <div class="hp-feature">
            <h4>Smart Discovery</h4>
            <p>Search entire collections seamlessly using natural language or image references.</p>
          </div>
          <div class="hp-feature">
            <h4>Shop Your Fit</h4>
            <p>Locate the exact products online instantly and curate your definitive shopping list.</p>
          </div>
        </div>
      </div>
    </section>

    <section id="fair" class="hp-fair">
      <h2>Fashion,<br>Made Personal.</h2>
      <p>Instead of endlessly scrolling through thousands of products, tell us where you're going, how you want to look, and what you like. The Fit Check handles the rest.</p>
    </section>

    <section class="hp-transition">
      <h2>Now, let's build your fit</h2>
      <div class="hp-scroll-indicator"></div>
    </section>
  </div>

  <div id="experience" class="stage">"""
content = re.sub(html_pattern, new_html, content, flags=re.DOTALL)

with open('index.html', 'w') as f:
    f.write(content)
