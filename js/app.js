// ============================================
// GENIUS Hortifruit - Carrinho (localStorage)
// ============================================

const Carrinho = {
  get() {
    return JSON.parse(localStorage.getItem('genius_carrinho') || '[]');
  },

  salvar(itens) {
    localStorage.setItem('genius_carrinho', JSON.stringify(itens));
    Carrinho.atualizarBadge();
  },

  adicionar(produto) {
    const itens = Carrinho.get();
    const idx = itens.findIndex(i => i.produto.id === produto.id);
    if (idx >= 0) {
      itens[idx].quantidade += 1;
    } else {
      itens.push({ produto, quantidade: 1 });
    }
    Carrinho.salvar(itens);
    mostrarToast(`🛒 ${produto.nome} adicionado!`, 'verde');
  },

  remover(produtoId) {
    const itens = Carrinho.get().filter(i => i.produto.id !== produtoId);
    Carrinho.salvar(itens);
  },

  atualizarQtd(produtoId, novaQtd) {
    if (novaQtd <= 0) { Carrinho.remover(produtoId); return; }
    const itens = Carrinho.get();
    const idx = itens.findIndex(i => i.produto.id === produtoId);
    if (idx >= 0) itens[idx].quantidade = novaQtd;
    Carrinho.salvar(itens);
  },

  limpar() {
    localStorage.removeItem('genius_carrinho');
    Carrinho.atualizarBadge();
  },

  totalItens() {
    return Carrinho.get().reduce((s, i) => s + i.quantidade, 0);
  },

  totalPreco() {
    return Carrinho.get().reduce((s, i) => s + i.produto.preco * i.quantidade, 0);
  },

  totalCalorias() {
    return Carrinho.get().reduce((s, i) => s + i.produto.calorias * i.quantidade, 0);
  },

  totaisNutricionais() {
    return Carrinho.get().reduce((acc, i) => {
      acc.calorias   += (i.produto.calorias       || 0) * i.quantidade;
      acc.proteina   += (i.produto.proteina        || 0) * i.quantidade;
      acc.carboidratos += (i.produto.carboidratos  || 0) * i.quantidade;
      acc.gordura    += (i.produto.gordura         || 0) * i.quantidade;
      return acc;
    }, { calorias: 0, proteina: 0, carboidratos: 0, gordura: 0 });
  },

  atualizarBadge() {
    const badge = document.getElementById('badge-carrinho');
    if (!badge) return;
    const total = Carrinho.totalItens();
    badge.textContent = total;
    badge.style.display = total > 0 ? 'flex' : 'none';
  }
};

// ============================================
// AUTH (localStorage)
// ============================================
const Auth = {
  get() {
    return JSON.parse(localStorage.getItem('genius_usuario') || 'null');
  },

  salvar(usuario) {
    localStorage.setItem('genius_usuario', JSON.stringify(usuario));
  },

  sair() {
    localStorage.removeItem('genius_usuario');
  },

  logado() {
    return !!Auth.get();
  },

  admin() {
    const u = Auth.get();
    return u && u.admin === true;
  }
};

// ============================================
// API (fetch para Flask backend)
// ============================================
const API_BASE = 'geniushortifruit-production.up.railway.app';

const Api = {
  async get(rota) {
    const res = await fetch(API_BASE + rota);
    if (!res.ok) throw new Error(await res.text());
    return res.json();
  },

  async post(rota, dados) {
    const res = await fetch(API_BASE + rota, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(dados)
    });
    if (!res.ok) throw new Error(await res.text());
    return res.json();
  },

  async put(rota, dados) {
    const res = await fetch(API_BASE + rota, {
      method: 'PUT',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(dados)
    });
    if (!res.ok) throw new Error(await res.text());
    return res.json();
  },

  async del(rota) {
    const res = await fetch(API_BASE + rota, { method: 'DELETE' });
    if (!res.ok) throw new Error(await res.text());
    return res.json();
  }
};

// ============================================
// PRODUTOS_DEMO – começa vazio; será preenchido
// pela API ao carregar cada página que precisar
// ============================================
let PRODUTOS_DEMO = [];

// ============================================
// UTILITÁRIOS
// ============================================
function mostrarToast(msg, tipo = '') {
  const container = document.getElementById('toast-container');
  if (!container) return;
  const toast = document.createElement('div');
  toast.className = `toast ${tipo}`;
  toast.textContent = msg;
  container.appendChild(toast);
  setTimeout(() => {
    toast.style.animation = 'slideOut 0.3s ease forwards';
    setTimeout(() => toast.remove(), 300);
  }, 3000);
}

function formatarMoeda(valor) {
  return `R$ ${valor.toFixed(2).replace('.', ',')}`;
}

function formatarCPF(v) {
  v = v.replace(/\D/g, '').slice(0, 11);
  return v.replace(/(\d{3})(\d{3})(\d{3})(\d{2})/, '$1.$2.$3-$4');
}

function formatarTelefone(v) {
  v = v.replace(/\D/g, '').slice(0, 11);
  if (v.length <= 10) return v.replace(/(\d{2})(\d{4})(\d+)/, '($1) $2-$3');
  return v.replace(/(\d{2})(\d{5})(\d{4})/, '($1) $2-$3');
}

function formatarCEP(v) {
  return v.replace(/\D/g, '').slice(0, 8).replace(/(\d{5})(\d+)/, '$1-$2');
}

function formatarCartao(v) {
  return v.replace(/\D/g, '').slice(0, 16).replace(/(.{4})/g, '$1 ').trim();
}

function formatarExpiry(v) {
  v = v.replace(/\D/g, '').slice(0, 4);
  if (v.length >= 3) return v.slice(0, 2) + '/' + v.slice(2);
  return v;
}

// Atualiza badge ao carregar qualquer página
document.addEventListener('DOMContentLoaded', () => {
  Carrinho.atualizarBadge();

  // Menu mobile
  const btnMenu = document.getElementById('btn-mobile-menu');
  const mobileNav = document.getElementById('mobile-nav');
  if (btnMenu && mobileNav) {
    btnMenu.addEventListener('click', () => {
      mobileNav.classList.toggle('aberto');
    });
  }

  // Renderiza usuario no header
  const usuario = Auth.get();
  const spanNomeUsuario = document.getElementById('nome-usuario');
  const btnSair = document.getElementById('btn-sair');
  const linkAdmin = document.getElementById('link-admin');
  const linkCliente = document.getElementById('link-cliente');
  const linkLogin = document.getElementById('link-login');

  if (usuario) {
    if (spanNomeUsuario) spanNomeUsuario.textContent = usuario.nome;
    if (btnSair) {
      btnSair.style.display = 'inline-flex';
      btnSair.addEventListener('click', () => {
        Auth.sair();
        window.location.href = 'index.html';
      });
    }
    if (linkCliente) linkCliente.style.display = 'block';
    if (linkAdmin && usuario.admin) linkAdmin.style.display = 'flex';
    if (linkLogin) linkLogin.style.display = 'none';
  } else {
    if (btnSair) btnSair.style.display = 'none';
    if (linkCliente) linkCliente.style.display = 'none';
    if (linkAdmin) linkAdmin.style.display = 'none';
  }
});
