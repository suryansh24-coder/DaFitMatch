import os
import re

# Read current file to extract original experience parts
with open('index.html', 'r') as f:
    content = f.read()

# Original Experience HTML starts at <div id="experience" class="stage">
# Wait, let's just write the original code directly. It's safer than parsing.
# The original CSS was all the CSS except the /* HOMEPAGE STYLES */ block.
# The original HTML was everything after <div id="experience" class="stage"> (or just <div class="stage"> originally).

original_head_and_css = content.split('/* ==================================================\n       HOMEPAGE STYLES (EDITORIAL)')[0]
original_html_match = re.search(r'(<div id="experience" class="stage">.*)', content, re.DOTALL)
if original_html_match:
    original_html = original_html_match.group(1).replace('<div id="experience" class="stage">', '<div class="stage">')
else:
    # Fallback if regex fails
    original_html = '<div class="stage">...</div>'

original_full = f"{original_head_and_css}\n  </style>\n</head>\n<body>\n{original_html}"
original_full = original_full.replace('.stage h1', 'h1').replace('.stage p', 'p').replace('.stage.title-hidden', '.stage.title-hidden')

os.makedirs('fit-check', exist_ok=True)
with open('fit-check/index.html', 'w') as f:
    f.write(original_full)

# Now, generate the NEW HOMEPAGE as index.html
new_homepage = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
  <title>THE FIT CHECK</title>
  
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Manrope:wght@300;400;500;600;700&display=swap" rel="stylesheet">

  <style>
    * { box-sizing: border-box; }
    body {
      margin: 0;
      background: #000;
      color: #fff;
      font-family: 'Manrope', system-ui, sans-serif;
      -webkit-font-smoothing: antialiased;
      -moz-osx-font-smoothing: grayscale;
      overflow-x: hidden;
    }
    
    /* Navbar */
    .nav {
      position: absolute;
      top: 0; left: 0; width: 100%;
      padding: 32px 48px;
      display: flex;
      justify-content: space-between;
      align-items: center;
      z-index: 200;
      background: linear-gradient(to bottom, rgba(0,0,0,0.6) 0%, rgba(0,0,0,0) 100%);
    }
    .nav-brand { font-size: 16px; font-weight: 700; letter-spacing: 0.1em; text-transform: uppercase; color: #fff; text-decoration: none; }
    .nav-links { display: flex; gap: 40px; }
    .nav-links a { color: #fff; text-decoration: none; font-size: 13px; font-weight: 500; text-transform: uppercase; letter-spacing: 0.1em; opacity: 0.7; transition: opacity 0.3s; }
    .nav-links a:hover { opacity: 1; }
    
    /* Hero */
    .hero {
      position: relative;
      height: 100vh;
      display: flex;
      flex-direction: column;
      justify-content: center;
      align-items: center;
      text-align: center;
      overflow: hidden;
    }
    .hero-bg {
      position: absolute; inset: 0;
      background-image: url('hero-bg.png');
      background-size: cover;
      background-position: center;
      background-repeat: no-repeat;
      z-index: 1;
    }
    .hero-bg::after {
      content: ''; position: absolute; inset: 0;
      background: rgba(0, 0, 0, 0.4); /* subtle dark overlay */
    }
    .hero-content {
      position: relative; z-index: 2;
      max-width: 900px; padding: 0 24px;
    }
    .hero-subtitle { font-size: 14px; letter-spacing: 0.2em; text-transform: uppercase; color: rgba(255,255,255,0.7); margin-bottom: 24px; }
    .hero h1 {
      font-size: clamp(48px, 8vw, 110px);
      font-weight: 500; line-height: 0.9; letter-spacing: -0.04em; margin: 0 0 32px 0; text-transform: uppercase;
    }
    .hero p {
      font-size: 18px; color: rgba(255,255,255,0.7); max-width: 600px; margin: 0 auto 48px auto; line-height: 1.6; font-weight: 400;
    }
    .hero-actions { display: flex; gap: 16px; justify-content: center; }
    
    .btn {
      padding: 16px 32px; border-radius: 999px; font-size: 13px; font-weight: 600; text-transform: uppercase; letter-spacing: 0.1em;
      text-decoration: none; transition: all 0.3s ease; cursor: pointer;
    }
    .btn-primary { background: #fff; color: #000; border: 1px solid #fff; }
    .btn-primary:hover { background: rgba(255,255,255,0.8); }
    .btn-secondary { background: rgba(255,255,255,0.1); color: #fff; border: 1px solid rgba(255,255,255,0.2); backdrop-filter: blur(10px); }
    .btn-secondary:hover { background: rgba(255,255,255,0.2); }

    /* Sections */
    .section { padding: 160px 48px; max-width: 1400px; margin: 0 auto; }
    .section-title { font-size: clamp(32px, 5vw, 64px); font-weight: 500; letter-spacing: -0.04em; margin: 0 0 80px 0; text-transform: uppercase; }

    /* Catalog Cards */
    .catalog-grid { display: grid; grid-template-columns: repeat(4, 1fr); gap: 24px; }
    .card {
      position: relative; height: 500px; background: #0a0a0a; border-radius: 12px; overflow: hidden;
      padding: 40px; display: flex; flex-direction: column; justify-content: flex-end;
      border: 1px solid rgba(255,255,255,0.05); transition: transform 0.4s ease, border-color 0.4s ease;
      text-decoration: none; color: #fff;
    }
    .card:hover { transform: translateY(-10px); border-color: rgba(255,255,255,0.2); }
    .card h3 { font-size: 32px; font-weight: 500; margin: 0; letter-spacing: -0.02em; text-transform: uppercase; }
    
    /* About */
    .about-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 80px; align-items: center; }
    .about-left h2 { font-size: clamp(40px, 5vw, 72px); font-weight: 500; letter-spacing: -0.04em; line-height: 1.1; margin: 0 0 32px 0; text-transform: uppercase; }
    .about-left p { font-size: 20px; color: rgba(255,255,255,0.6); line-height: 1.6; margin: 0; }
    .features { display: flex; flex-direction: column; gap: 40px; }
    .feature { border-top: 1px solid rgba(255,255,255,0.1); padding-top: 24px; }
    .feature h4 { font-size: 14px; margin: 0 0 12px 0; letter-spacing: 0.1em; text-transform: uppercase; font-weight: 600; }
    .feature p { font-size: 16px; color: rgba(255,255,255,0.5); margin: 0; line-height: 1.6; }

    /* Fair */
    .fair { text-align: center; padding: 200px 48px; background: #050505; border-top: 1px solid rgba(255,255,255,0.05); }
    .fair h2 { font-size: clamp(48px, 8vw, 96px); font-weight: 500; letter-spacing: -0.04em; margin: 0 0 40px 0; text-transform: uppercase; }
    .fair p { font-size: 20px; color: rgba(255,255,255,0.6); max-width: 800px; margin: 0 auto 56px auto; line-height: 1.6; }

    @media (max-width: 1024px) {
      .catalog-grid { grid-template-columns: 1fr 1fr; }
      .about-grid { grid-template-columns: 1fr; }
    }
    @media (max-width: 768px) {
      .nav { padding: 24px; flex-direction: column; gap: 24px; }
      .catalog-grid { grid-template-columns: 1fr; }
      .section { padding: 100px 24px; }
      .hero-actions { flex-direction: column; }
    }
  </style>
</head>
<body>

  <nav class="nav">
    <a href="/" class="nav-brand">THE FIT CHECK</a>
    <div class="nav-links">
      <a href="/">Home</a>
      <a href="#about">About</a>
      <a href="#fair">Fair</a>
      <a href="#">Sign in with Google</a>
    </div>
  </nav>

  <header class="hero">
    <div class="hero-bg"></div>
    <div class="hero-content">
      <div class="hero-subtitle">THE FIT CHECK</div>
      <h1>YOUR STYLE.<br>YOUR FIT.<br>YOUR CHECK.</h1>
      <p>Discover what truly suits you. Build your aesthetic, visualize your outfits, and find your perfect fit with AI.</p>
      <div class="hero-actions">
        <a href="/fit-check" class="btn btn-primary">START YOUR FIT CHECK</a>
        <a href="#explore" class="btn btn-secondary">EXPLORE STYLES</a>
      </div>
    </div>
  </header>

  <section id="explore" class="section">
    <h2 class="section-title">EXPLORE YOUR FIT</h2>
    <div class="catalog-grid">
      <a href="#" class="card"><h3>MEN</h3></a>
      <a href="#" class="card"><h3>WOMEN</h3></a>
      <a href="#" class="card"><h3>STREETWEAR</h3></a>
      <a href="#" class="card"><h3>FORMAL</h3></a>
    </div>
  </section>

  <section id="about" class="section">
    <div class="about-grid">
      <div class="about-left">
        <h2>Fashion is easy.<br>Knowing what suits you isn't.</h2>
        <p>The Fit Check uses AI to understand your occasion, aesthetic, preferences and personal style &mdash; helping you discover outfits that actually feel like you.</p>
      </div>
      <div class="features">
        <div class="feature">
          <h4>AI PERSONAL STYLIST</h4>
        </div>
        <div class="feature">
          <h4>3D VIRTUAL TRY-ON</h4>
        </div>
        <div class="feature">
          <h4>SMART OUTFIT DISCOVERY</h4>
        </div>
        <div class="feature">
          <h4>SHOP YOUR FIT</h4>
        </div>
      </div>
    </div>
  </section>

  <section id="fair" class="fair">
    <h2>FASHION, MADE PERSONAL.</h2>
    <p>Instead of endlessly scrolling through thousands of products, tell us where you're going, how you want to look, and what you like. The Fit Check helps you find the rest.</p>
    <a href="/fit-check" class="btn btn-primary">BUILD MY FIT</a>
  </section>

</body>
</html>
"""

with open('index.html', 'w') as f:
    f.write(new_homepage)

