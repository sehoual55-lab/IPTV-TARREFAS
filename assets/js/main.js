/* IPTV Tarefas — interações (JavaScript puro, sem dependências) */
(function () {
  "use strict";

  var cfg = window.SITE_CONFIG || {};
  var plans = cfg.plans || {};

  /* ---------------- Menu mobile ---------------- */
  var burger = document.querySelector("[data-burger]");
  var mobileNav = document.getElementById("mobile-nav");

  function closeMenu() {
    if (!burger || !mobileNav) return;
    burger.setAttribute("aria-expanded", "false");
    mobileNav.classList.remove("is-open");
  }

  if (burger && mobileNav) {
    burger.addEventListener("click", function () {
      var open = burger.getAttribute("aria-expanded") === "true";
      burger.setAttribute("aria-expanded", String(!open));
      mobileNav.classList.toggle("is-open", !open);
    });

    mobileNav.addEventListener("click", function (e) {
      if (e.target.closest("a")) closeMenu();
    });

    document.addEventListener("keydown", function (e) {
      if (e.key === "Escape" && burger.getAttribute("aria-expanded") === "true") {
        closeMenu();
        burger.focus();
      }
    });

    window.addEventListener("resize", function () {
      if (window.innerWidth >= 980) closeMenu();
    });
  }

  /* ---------------- FAQ (acordeão acessível) ---------------- */
  document.querySelectorAll("[data-faq-q]").forEach(function (btn) {
    btn.addEventListener("click", function () {
      var panel = document.getElementById(btn.getAttribute("aria-controls"));
      var open = btn.getAttribute("aria-expanded") === "true";
      btn.setAttribute("aria-expanded", String(!open));
      if (panel) panel.hidden = open;
      var item = btn.closest(".faq__item");
      if (item) item.setAttribute("data-open", String(!open));
    });
  });

  /* ---------------- Conexões e pedido ---------------- */
  var conexoesCfg = cfg.conexoes || { max: 5, multiplicadores: [1] };
  var MAX = conexoesCfg.max || 5;
  var MULT = conexoesCfg.multiplicadores || [1];
  var conexoes = {};

  function precoBase(chave) {
    var plan = plans[chave];
    if (!plan || !plan.price) return 0;
    var n = plan.price.replace(/[^\d,.-]/g, "").replace(/\./g, "").replace(",", ".");
    return parseFloat(n) || 0;
  }

  function formatar(valor) {
    return valor.toLocaleString("pt-BR", { minimumFractionDigits: 2, maximumFractionDigits: 2 });
  }

  function total(chave) {
    var n = conexoes[chave] || 1;
    var fator = MULT[n - 1] != null ? MULT[n - 1] : n;
    return precoBase(chave) * fator;
  }

  function pintar(chave) {
    var card = document.querySelector('[data-plan-card="' + chave + '"]');
    if (!card) return;
    var n = conexoes[chave] || 1;
    var partes = formatar(total(chave)).split(",");

    var inteiro = card.querySelector("[data-preco-int]");
    var decimal = card.querySelector("[data-preco-dec]");
    if (inteiro) inteiro.textContent = partes[0];
    if (decimal) decimal.textContent = "," + (partes[1] || "00");

    var contador = card.querySelector("[data-conn]");
    if (contador) contador.textContent = String(n);

    card.querySelectorAll("[data-step]").forEach(function (btn) {
      var passo = parseInt(btn.getAttribute("data-step"), 10);
      btn.disabled = (passo < 0 && n <= 1) || (passo > 0 && n >= MAX);
    });
  }

  document.querySelectorAll("[data-stepper]").forEach(function (stepper) {
    var chave = stepper.getAttribute("data-stepper");
    conexoes[chave] = 1;
    stepper.querySelectorAll("[data-step]").forEach(function (btn) {
      btn.addEventListener("click", function () {
        var passo = parseInt(btn.getAttribute("data-step"), 10);
        conexoes[chave] = Math.min(MAX, Math.max(1, (conexoes[chave] || 1) + passo));
        pintar(chave);
      });
    });
    pintar(chave);
  });

  /* ---------------- Guias de instalação ---------------- */
  var picker = document.querySelector("[data-picker]");

  if (picker) {
    var pBtn = picker.querySelector("[data-picker-btn]");
    var pMenu = picker.querySelector("[data-picker-menu]");
    var pLabel = picker.querySelector("[data-picker-label]");
    var pIcone = picker.querySelector("[data-picker-icone]");
    var opcoes = Array.prototype.slice.call(picker.querySelectorAll(".picker__opt"));
    var ativo = 0;

    var marcarAtivo = function (i) {
      ativo = Math.max(0, Math.min(opcoes.length - 1, i));
      opcoes.forEach(function (o, k) { o.classList.toggle("is-active", k === ativo); });
      pMenu.setAttribute("aria-activedescendant", opcoes[ativo].id);
      opcoes[ativo].scrollIntoView({ block: "nearest" });
    };

    var abrirMenu = function (estado) {
      pBtn.setAttribute("aria-expanded", String(estado));
      pMenu.hidden = !estado;
      if (estado) {
        var sel = opcoes.findIndex(function (o) { return o.getAttribute("aria-selected") === "true"; });
        marcarAtivo(sel < 0 ? 0 : sel);
        pMenu.focus();
      }
    };

    var escolher = function (opt) {
      var valor = opt.getAttribute("data-value");
      opcoes.forEach(function (o) {
        o.setAttribute("aria-selected", String(o === opt));
      });
      pLabel.textContent = opt.querySelector("span:nth-child(2)").textContent;
      pIcone.innerHTML = opt.querySelector(".picker__opt-icone").innerHTML;
      document.querySelectorAll("[data-guia]").forEach(function (p) {
        p.hidden = p.getAttribute("data-guia") !== valor;
      });
      abrirMenu(false);
      pBtn.focus();
    };

    pBtn.addEventListener("click", function () {
      abrirMenu(pBtn.getAttribute("aria-expanded") !== "true");
    });

    pBtn.addEventListener("keydown", function (e) {
      if (e.key === "ArrowDown" || e.key === "ArrowUp") { e.preventDefault(); abrirMenu(true); }
    });

    opcoes.forEach(function (opt, i) {
      opt.addEventListener("click", function () { escolher(opt); });
      opt.addEventListener("mousemove", function () { marcarAtivo(i); });
    });

    pMenu.addEventListener("keydown", function (e) {
      if (e.key === "ArrowDown") { e.preventDefault(); marcarAtivo(ativo + 1); }
      else if (e.key === "ArrowUp") { e.preventDefault(); marcarAtivo(ativo - 1); }
      else if (e.key === "Home") { e.preventDefault(); marcarAtivo(0); }
      else if (e.key === "End") { e.preventDefault(); marcarAtivo(opcoes.length - 1); }
      else if (e.key === "Enter" || e.key === " ") { e.preventDefault(); escolher(opcoes[ativo]); }
      else if (e.key === "Escape" || e.key === "Tab") { abrirMenu(false); pBtn.focus(); }
    });

    document.addEventListener("click", function (e) {
      if (pBtn.getAttribute("aria-expanded") === "true" && !picker.contains(e.target)) abrirMenu(false);
    });
  }

  /* ---------------- Popup de pedido ---------------- */
  var modal = document.querySelector("[data-checkout]");
  var obrigado = document.querySelector("[data-obrigado]");
  var atual = null;
  var ultimoFoco = null;
  var pagamento = "";
  var pais = { iso: "BR", nome: "Brasil", ddi: "55" };

  function moeda(v) { return "R$ " + formatar(v); }

  function prender(caixa, e) {
    if (e.key !== "Tab") return;
    var alvos = caixa.querySelectorAll("button:not([disabled]), input, select, [href]");
    var visiveis = Array.prototype.filter.call(alvos, function (el) { return el.offsetParent !== null; });
    if (!visiveis.length) return;
    var primeiro = visiveis[0];
    var ultimo = visiveis[visiveis.length - 1];
    if (e.shiftKey && document.activeElement === primeiro) { e.preventDefault(); ultimo.focus(); }
    else if (!e.shiftKey && document.activeElement === ultimo) { e.preventDefault(); primeiro.focus(); }
  }

  /* ---- seletor de país ---- */
  var paisesCaixa = modal && modal.querySelector("[data-paises]");
  if (paisesCaixa && window.PAISES) {
    var pBtn2 = paisesCaixa.querySelector("[data-paises-btn]");
    var pMenu2 = paisesCaixa.querySelector("[data-paises-menu]");
    var pBusca = paisesCaixa.querySelector("[data-paises-busca]");
    var pLista = paisesCaixa.querySelector("[data-paises-lista]");
    var pVazio = paisesCaixa.querySelector("[data-paises-vazio]");
    var isoEl = paisesCaixa.querySelector("[data-paises-iso]");
    var ddiEl = paisesCaixa.querySelector("[data-paises-ddi]");
    var ativoPais = 0;

    var desenhar = function (termo) {
      var t2 = (termo || "").trim().toLowerCase().replace("+", "");
      var lista = window.PAISES.filter(function (p2) {
        return !t2 || p2.nome.toLowerCase().indexOf(t2) >= 0 ||
               p2.iso.toLowerCase().indexOf(t2) >= 0 || p2.ddi.indexOf(t2) === 0;
      });
      pLista.innerHTML = "";
      lista.forEach(function (p2, i) {
        var li = document.createElement("li");
        li.className = "paises__opt";
        li.setAttribute("role", "option");
        li.setAttribute("data-iso", p2.iso);
        li.setAttribute("aria-selected", String(p2.iso === pais.iso));
        li.innerHTML = "<b>" + p2.iso + "</b><span>" + p2.nome + "</span><span>+" + p2.ddi + "</span>";
        li.addEventListener("click", function () { escolherPais(p2); });
        li.addEventListener("mousemove", function () { marcarPais(i); });
        pLista.appendChild(li);
      });
      pVazio.hidden = lista.length > 0;
      ativoPais = 0;
      marcarPais(0);
      return lista;
    };

    var itens = function () { return pLista.querySelectorAll(".paises__opt"); };

    function marcarPais(i) {
      var els = itens();
      if (!els.length) return;
      ativoPais = Math.max(0, Math.min(els.length - 1, i));
      Array.prototype.forEach.call(els, function (el, k) { el.classList.toggle("is-active", k === ativoPais); });
      els[ativoPais].scrollIntoView({ block: "nearest" });
    }

    function escolherPais(p2) {
      pais = p2;
      isoEl.textContent = p2.iso;
      ddiEl.textContent = "+" + p2.ddi;
      abrirPaises(false);
      var tel = modal.querySelector("#co-tel");
      if (tel) tel.focus();
    }

    function abrirPaises(estado) {
      pBtn2.setAttribute("aria-expanded", String(estado));
      pMenu2.hidden = !estado;
      if (estado) {
        pBusca.value = "";
        desenhar("");
        pBusca.focus();
      }
    }

    pBtn2.addEventListener("click", function () {
      abrirPaises(pBtn2.getAttribute("aria-expanded") !== "true");
    });
    pBusca.addEventListener("input", function () { desenhar(pBusca.value); });
    pBusca.addEventListener("keydown", function (e) {
      var els = itens();
      if (e.key === "ArrowDown") { e.preventDefault(); marcarPais(ativoPais + 1); }
      else if (e.key === "ArrowUp") { e.preventDefault(); marcarPais(ativoPais - 1); }
      else if (e.key === "Enter") {
        e.preventDefault();
        var alvo = els[ativoPais];
        if (alvo) {
          var achado = window.PAISES.filter(function (p2) { return p2.iso === alvo.getAttribute("data-iso"); })[0];
          if (achado) escolherPais(achado);
        }
      } else if (e.key === "Escape") { e.stopPropagation(); abrirPaises(false); pBtn2.focus(); }
    });
    document.addEventListener("click", function (e) {
      if (pBtn2.getAttribute("aria-expanded") === "true" && !paisesCaixa.contains(e.target)) abrirPaises(false);
    });
    desenhar("");
  }

  /* ---- formas de pagamento ---- */
  var grade = modal && modal.querySelector("[data-pagamentos-grade]");
  if (grade) {
    var formas = cfg.formasPagamento || [];
    if (!formas.length) {
      var bloco = modal.querySelector("[data-pagamentos]");
      if (bloco) bloco.remove();
    } else {
      formas.forEach(function (nome, i) {
        var btn = document.createElement("button");
        btn.type = "button";
        btn.className = "pagamento";
        btn.setAttribute("data-pagamento", nome);
        btn.setAttribute("aria-pressed", String(i === 0));
        var marca = (window.PAGAMENTOS || {})[nome];
        var logo = marca
          ? '<span class="pagamento__logo" style="color:' + marca.cor + '">' + marca.svg + "</span>"
          : "";
        btn.innerHTML = logo + "<span>" + nome + "</span>";
        btn.addEventListener("click", function () {
          pagamento = nome;
          grade.querySelectorAll("[data-pagamento]").forEach(function (b2) {
            b2.setAttribute("aria-pressed", String(b2 === btn));
          });
        });
        grade.appendChild(btn);
      });
      pagamento = formas[0];
    }
  }

  /* ---- resumo ---- */
  function pintarModal() {
    if (!modal || !atual) return;
    var plan = plans[atual];
    var n = conexoes[atual] || 1;
    var base = precoBase(atual);
    var tot = total(atual);
    var extra = tot - base;

    modal.querySelector("[data-co-nome]").textContent = plan.name;
    modal.querySelector("[data-co-duracao-topo]").textContent = plan.duration;
    modal.querySelector("[data-co-duracao]").textContent = plan.duration;
    modal.querySelector("[data-co-bonus-linha]").hidden = !plan.bonus;
    modal.querySelector("[data-co-conn]").textContent = String(n);
    modal.querySelector("[data-co-conn-rotulo]").textContent = n > 1 ? "conexões" : "conexão";
    modal.querySelector("[data-co-extra-linha]").hidden = extra <= 0;
    modal.querySelector("[data-co-extra]").textContent = "+ " + moeda(extra);
    modal.querySelector("[data-co-total]").textContent = moeda(tot);

    var seletorPlano = modal.querySelector("[data-co-plano]");
    if (seletorPlano && seletorPlano.value !== atual) seletorPlano.value = atual;

    modal.querySelectorAll("[data-co-step]").forEach(function (btn) {
      var passo = parseInt(btn.getAttribute("data-co-step"), 10);
      btn.disabled = (passo < 0 && n <= 1) || (passo > 0 && n >= MAX);
    });
    pintar(atual);
  }

  function abrirModal(chave) {
    if (!modal) return;
    atual = chave;
    ultimoFoco = document.activeElement;
    modal.hidden = false;
    document.body.classList.add("is-locked");
    var erro = modal.querySelector("[data-co-erro]");
    if (erro) erro.hidden = true;
    pintarModal();
    var nomeEl = modal.querySelector("#co-nome");
    if (nomeEl) nomeEl.focus();
  }

  function fecharModal() {
    if (!modal || modal.hidden) return;
    modal.hidden = true;
    document.body.classList.remove("is-locked");
    if (ultimoFoco) ultimoFoco.focus();
  }

  document.querySelectorAll("[data-buy]").forEach(function (btn) {
    btn.addEventListener("click", function () {
      var chave = btn.getAttribute("data-buy");
      if (plans[chave] && modal) abrirModal(chave);
    });
  });

  if (modal) {
    modal.querySelectorAll("[data-checkout-close]").forEach(function (el) {
      el.addEventListener("click", fecharModal);
    });

    var seletorPlano2 = modal.querySelector("[data-co-plano]");
    if (seletorPlano2) {
      seletorPlano2.addEventListener("change", function () {
        if (!plans[seletorPlano2.value]) return;
        atual = seletorPlano2.value;
        if (!conexoes[atual]) conexoes[atual] = 1;
        pintarModal();
      });
    }

    modal.querySelectorAll("[data-co-step]").forEach(function (btn) {
      btn.addEventListener("click", function () {
        var passo = parseInt(btn.getAttribute("data-co-step"), 10);
        conexoes[atual] = Math.min(MAX, Math.max(1, (conexoes[atual] || 1) + passo));
        pintarModal();
      });
    });

    ["#co-nome", "#co-tel"].forEach(function (sel) {
      var campoEl = modal.querySelector(sel);
      if (!campoEl) return;
      campoEl.addEventListener("input", function () {
        var erroEl = modal.querySelector("[data-co-erro]");
        if (erroEl && !erroEl.hidden && campoEl.value.trim()) erroEl.hidden = true;
      });
    });

    document.addEventListener("keydown", function (e) {
      if (modal.hidden) return;
      if (e.key === "Escape") { fecharModal(); return; }
      prender(modal, e);
    });

    var confirmar = modal.querySelector("[data-co-confirmar]");
    if (confirmar) {
      confirmar.addEventListener("click", function () {
        var plan = plans[atual];
        if (!plan) return;
        var n = conexoes[atual] || 1;
        var campo = function (id) {
          var el = modal.querySelector(id);
          return el && el.value ? el.value.trim() : "";
        };

        var erro = modal.querySelector("[data-co-erro]");
        var faltando = [];
        if (!campo("#co-nome")) faltando.push("o nome");
        if (!campo("#co-tel")) faltando.push("o telefone");
        if (faltando.length) {
          if (erro) {
            erro.textContent = "Informe " + faltando.join(" e ") + " para continuar.";
            erro.hidden = false;
          }
          var vazio = modal.querySelector(campo("#co-nome") ? "#co-tel" : "#co-nome");
          if (vazio) vazio.focus();
          return;
        }
        if (erro) erro.hidden = true;

        var telefone = "+" + pais.ddi + " " + campo("#co-tel");
        var linhas = [
          "Novo pedido — " + (cfg.brand || "IPTV Tarefas"),
          "",
          "Plano: " + plan.name + " (" + plan.duration + (plan.bonus ? " + 3 meses grátis" : "") + ")",
          "Conexões simultâneas: " + n,
          "Total: " + moeda(total(atual)),
          "",
          "Nome: " + campo("#co-nome"),
          "Telefone: " + telefone + " (" + pais.nome + ")"
        ];
        if (campo("#co-email")) linhas.push("E-mail: " + campo("#co-email"));
        if (pagamento) linhas.push("Pagamento preferido: " + pagamento);

        var link = cfg.whatsapp
          ? "https://wa.me/" + cfg.whatsapp + "?text=" + encodeURIComponent(linhas.join("\n"))
          : "";

        // Registro no Google Sheets, se configurado. Enviado em paralelo:
        // uma falha aqui nunca impede o pedido de seguir pelo WhatsApp.
        if (cfg.pedidosEndpoint) {
          var pedido = {
            token: cfg.pedidosToken || "",
            plano: plan.name,
            duracao: plan.duration,
            bonus: !!plan.bonus,
            conexoes: n,
            total: Math.round(total(atual) * 100) / 100,
            nome: campo("#co-nome"),
            telefone: telefone,
            pais: pais.nome,
            email: campo("#co-email"),
            pagamento: pagamento,
            origem: window.location.hostname || "site",
            website: ""
          };
          try {
            fetch(cfg.pedidosEndpoint, {
              method: "POST",
              mode: "no-cors",
              headers: { "Content-Type": "text/plain;charset=utf-8" },
              body: JSON.stringify(pedido)
            })["catch"](function () {});
          } catch (erro) {}
        }

        if (link) window.open(link, "_blank", "noopener");
        fecharModal();

        if (obrigado) {
          obrigado.querySelector("[data-ob-nome]").textContent = campo("#co-nome").split(" ")[0];
          obrigado.querySelector("[data-ob-plano]").textContent = plan.name;
          obrigado.querySelector("[data-ob-conn]").textContent = String(n);
          obrigado.querySelector("[data-ob-total]").textContent = moeda(total(atual));
          var ligacao = obrigado.querySelector("[data-ob-link]");
          if (ligacao) {
            if (link) ligacao.setAttribute("href", link);
            else ligacao.remove();
          }
          obrigado.hidden = false;
          document.body.classList.add("is-locked");
          var fechaOb = obrigado.querySelector("[data-obrigado-close]");
          if (fechaOb) fechaOb.focus();
        }
      });
    }
  }

  if (obrigado) {
    var fecharObrigado = function () {
      obrigado.hidden = true;
      document.body.classList.remove("is-locked");
      if (ultimoFoco) ultimoFoco.focus();
    };
    obrigado.querySelectorAll("[data-obrigado-close]").forEach(function (el) {
      el.addEventListener("click", fecharObrigado);
    });
    document.addEventListener("keydown", function (e) {
      if (obrigado.hidden) return;
      if (e.key === "Escape") { fecharObrigado(); return; }
      prender(obrigado, e);
    });
  }

  /* ---------------- Link de navegação ativo ---------------- */
  var sections = Array.prototype.slice.call(document.querySelectorAll("main section[id]"));
  var navLinks = Array.prototype.slice.call(document.querySelectorAll(".nav__link[href^='#']"));

  if (sections.length && navLinks.length && "IntersectionObserver" in window) {
    var observer = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (!entry.isIntersecting) return;
        navLinks.forEach(function (link) {
          var isCurrent = link.getAttribute("href") === "#" + entry.target.id;
          if (isCurrent) {
            link.setAttribute("aria-current", "true");
          } else {
            link.removeAttribute("aria-current");
          }
        });
      });
    }, { rootMargin: "-45% 0px -50% 0px" });

    sections.forEach(function (section) { observer.observe(section); });
  }

  /* ---------------- Widget de WhatsApp ---------------- */
  var waLinks = document.querySelectorAll("[data-whatsapp]");
  var widget = document.querySelector("[data-wa-widget]");

  if (!cfg.whatsapp) {
    // Sem número configurado: nada de canal de contato quebrado na página.
    waLinks.forEach(function (el) { el.remove(); });
    if (widget) widget.remove();
  } else {
    var link = "https://wa.me/" + cfg.whatsapp;
    waLinks.forEach(function (el) {
      el.setAttribute("href", link);
      el.setAttribute("target", "_blank");
      el.setAttribute("rel", "noopener");
    });
  }

  if (widget && cfg.whatsapp) {
    var fab = widget.querySelector("[data-wa-toggle]");
    var painel = widget.querySelector(".wa__panel");
    var fechar = widget.querySelector("[data-wa-close]");
    var iniciar = widget.querySelector("[data-wa-start]");
    var numero = widget.querySelector("[data-wa-number]");

    if (numero) numero.textContent = cfg.whatsappExibicao || ("+" + cfg.whatsapp);

    if (iniciar) {
      var saudacao = cfg.mensagemInicial || "Olá! Vim pelo site e gostaria de informações sobre os planos de IPTV.";
      iniciar.setAttribute("href", "https://wa.me/" + cfg.whatsapp + "?text=" + encodeURIComponent(saudacao));
    }

    var abrir = function (estado) {
      fab.setAttribute("aria-expanded", String(estado));
      painel.hidden = !estado;
      if (estado && iniciar) iniciar.focus();
    };

    fab.addEventListener("click", function () {
      abrir(fab.getAttribute("aria-expanded") !== "true");
    });

    if (fechar) {
      fechar.addEventListener("click", function () {
        abrir(false);
        fab.focus();
      });
    }

    document.addEventListener("keydown", function (e) {
      if (e.key === "Escape" && fab.getAttribute("aria-expanded") === "true") {
        abrir(false);
        fab.focus();
      }
    });

    document.addEventListener("click", function (e) {
      if (fab.getAttribute("aria-expanded") === "true" && !widget.contains(e.target)) abrir(false);
    });
  }
})();
