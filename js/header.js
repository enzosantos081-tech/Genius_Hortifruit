// ============================================
// Header HTML injetado em todas as páginas
// ============================================
function renderHeader(paginaAtual) {
  const html = `
  <header>
    <div class="header-inner">
      <a href="index.html" class="logo">
        <div class="logo-icon"><img src="img/logo.png" alt="GENIUS logo" style="height:28px;width:28px;object-fit:contain;vertical-align:middle;" /></div>
        <span>GENIUS Hortifruit</span>
      </a>

      <nav class="desktop-nav">
        <a href="index.html" class="${paginaAtual === 'home' ? 'ativo' : ''}">Home</a>
        <a href="loja.html" class="${paginaAtual === 'loja' ? 'ativo' : ''}">Loja Online</a>
        <a href="cliente.html" id="link-cliente" style="display:none;" class="${paginaAtual === 'cliente' ? 'ativo' : ''}">Minha Área</a>
        <a href="admin.html" id="link-admin" style="display:none; align-items:center; gap:0.3rem;" class="${paginaAtual === 'admin' ? 'ativo' : ''}">⚙️ Admin</a>
      </nav>

      <div class="header-actions">
        <a href="carrinho.html" class="btn-carrinho">
          🛒
          <span class="badge-carrinho" id="badge-carrinho" style="display:none;">0</span>
        </a>

        <a href="login.html" id="link-login" class="btn btn-verde btn-sm" style="display:inline-flex;">
          Entrar
        </a>

        <span id="nome-usuario" style="font-size:0.875rem; font-weight:600; color:var(--cinza-700);"></span>
        <button id="btn-sair" class="btn-sair" style="display:none;">Sair</button>

        <button class="btn-mobile-menu" id="btn-mobile-menu">☰</button>
      </div>
    </div>

    <div class="mobile-nav" id="mobile-nav">
      <a href="index.html">🏠 Home</a>
      <a href="loja.html">🛍️ Loja Online</a>
      <a href="carrinho.html">🛒 Carrinho</a>
      <a href="cliente.html" id="link-cliente-mobile">👤 Minha Área</a>
      <a href="admin.html" id="link-admin-mobile">⚙️ Admin</a>
      <a href="login.html" id="link-login-mobile">🔑 Entrar</a>
      <button id="btn-sair-mobile" style="display:none; background:var(--vermelho-claro); color:var(--vermelho); border:none; padding:0.75rem; border-radius:8px; font-weight:700; cursor:pointer; width:100%;">🚪 Sair</button>
    </div>
  </header>
  `;
  document.getElementById('header-placeholder').innerHTML = html;
}
