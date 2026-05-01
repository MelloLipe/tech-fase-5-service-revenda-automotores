"""Gera diagramas de arquitetura e fluxo SAGA como imagens PNG."""
import os

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch


DOCS_DIR = os.path.dirname(__file__)


def desenhar_arquitetura():
    fig, ax = plt.subplots(1, 1, figsize=(16, 12))
    ax.set_xlim(0, 16)
    ax.set_ylim(0, 12)
    ax.axis('off')
    fig.patch.set_facecolor('#f8f9fa')

    # Title
    ax.text(8, 11.5, 'Arquitetura da Plataforma - Revenda de Veiculos',
            fontsize=18, fontweight='bold', ha='center', va='center', color='#1a1a2e')
    ax.text(8, 11.0, 'Tech Challenge SOAT - Fase 5',
            fontsize=12, ha='center', va='center', color='#666')

    # --- CLIENT LAYER ---
    client_box = FancyBboxPatch((1, 9.2), 14, 1.4, boxstyle="round,pad=0.15",
                                 facecolor='#e3f2fd', edgecolor='#1565c0', linewidth=2)
    ax.add_patch(client_box)
    ax.text(8, 10.1, 'CLIENTE (Browser)', fontsize=13, fontweight='bold', ha='center', color='#1565c0')
    ax.text(4, 9.6, 'Django Templates\n+ Bootstrap 5 (CDN)', fontsize=10, ha='center', color='#333')
    ax.text(12, 9.6, 'API REST\n(JSON)', fontsize=10, ha='center', color='#333')

    # Arrow client -> render
    ax.annotate('', xy=(8, 8.5), xytext=(8, 9.2),
                arrowprops=dict(arrowstyle='->', color='#1565c0', lw=2))
    ax.text(8.5, 8.85, 'HTTPS / TLS', fontsize=9, color='#1565c0', fontstyle='italic')

    # --- RENDER PLATFORM ---
    render_box = FancyBboxPatch((0.5, 1.5), 15, 7, boxstyle="round,pad=0.2",
                                 facecolor='#fff3e0', edgecolor='#e65100', linewidth=2.5)
    ax.add_patch(render_box)
    ax.text(8, 8.2, 'RENDER (PaaS - Free Tier)', fontsize=14, fontweight='bold',
            ha='center', color='#e65100')
    ax.text(8, 7.8, 'Deploy automatico via GitHub | SSL gratuito | Gerenciavel',
            fontsize=9, ha='center', color='#bf360c', fontstyle='italic')

    # --- GUNICORN ---
    gunicorn_box = FancyBboxPatch((2, 6.8), 12, 0.8, boxstyle="round,pad=0.1",
                                   facecolor='#e8f5e9', edgecolor='#2e7d32', linewidth=1.5)
    ax.add_patch(gunicorn_box)
    ax.text(8, 7.2, 'Gunicorn (WSGI) - 2 Workers', fontsize=11, fontweight='bold',
            ha='center', color='#2e7d32')

    # Arrow gunicorn -> django
    ax.annotate('', xy=(8, 6.5), xytext=(8, 6.8),
                arrowprops=dict(arrowstyle='->', color='#2e7d32', lw=1.5))

    # --- DJANGO APP ---
    django_box = FancyBboxPatch((1.5, 3.8), 13, 2.7, boxstyle="round,pad=0.15",
                                 facecolor='#e8eaf6', edgecolor='#283593', linewidth=2)
    ax.add_patch(django_box)
    ax.text(8, 6.25, 'Django Application', fontsize=13, fontweight='bold',
            ha='center', color='#283593')

    # App boxes inside Django
    apps = [
        (2.5, 5.0, 3.2, 1.0, 'Veiculos (App)\nCRUD + Filtros\nOrdenacao por preco', '#c8e6c9', '#388e3c'),
        (6.4, 5.0, 3.2, 1.0, 'Compradores (App)\nCadastro seguro\nHash CPF/RG', '#ffcdd2', '#c62828'),
        (10.3, 5.0, 3.5, 1.0, 'Vendas (App)\nSAGA Coreografada\nMaquina de estados', '#fff9c4', '#f9a825'),
    ]
    for x, y, w, h, text, fc, tc in apps:
        box = FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.1",
                              facecolor=fc, edgecolor=tc, linewidth=1.5)
        ax.add_patch(box)
        ax.text(x + w/2, y + h/2, text, fontsize=8.5, ha='center', va='center',
                color=tc, fontweight='bold')

    # DRF + WhiteNoise bar
    drf_box = FancyBboxPatch((2.5, 4.0), 5.5, 0.7, boxstyle="round,pad=0.08",
                              facecolor='#f3e5f5', edgecolor='#6a1b9a', linewidth=1)
    ax.add_patch(drf_box)
    ax.text(5.25, 4.35, 'Django REST Framework\nSerializers | ViewSets | Paginacao',
            fontsize=8, ha='center', va='center', color='#6a1b9a')

    wn_box = FancyBboxPatch((8.5, 4.0), 5.3, 0.7, boxstyle="round,pad=0.08",
                             facecolor='#fce4ec', edgecolor='#880e4f', linewidth=1)
    ax.add_patch(wn_box)
    ax.text(11.15, 4.35, 'Seguranca\nCSRF | HSTS | XSS | Clickjacking | UUIDs',
            fontsize=8, ha='center', va='center', color='#880e4f')

    # Arrow django -> DB
    ax.annotate('', xy=(8, 3.0), xytext=(8, 3.8),
                arrowprops=dict(arrowstyle='->', color='#283593', lw=2))

    # --- DATABASE ---
    db_box = FancyBboxPatch((3, 2.0), 10, 0.9, boxstyle="round,pad=0.1",
                             facecolor='#e0f7fa', edgecolor='#00695c', linewidth=2)
    ax.add_patch(db_box)
    ax.text(8, 2.55, 'PostgreSQL (Render Managed - Free Tier)', fontsize=12,
            fontweight='bold', ha='center', color='#00695c')
    ax.text(8, 2.2, 'Veiculos | Compradores (hash) | Vendas | Historico Auditoria | SSL',
            fontsize=9, ha='center', color='#004d40')

    plt.tight_layout()
    plt.savefig(os.path.join(DOCS_DIR, 'diagrama_arquitetura.png'),
                dpi=150, bbox_inches='tight', facecolor='#f8f9fa')
    plt.close()
    print('diagrama_arquitetura.png gerado')


def desenhar_saga():
    fig, ax = plt.subplots(1, 1, figsize=(18, 10))
    ax.set_xlim(0, 18)
    ax.set_ylim(0, 10)
    ax.axis('off')
    fig.patch.set_facecolor('#f8f9fa')

    ax.text(9, 9.5, 'Fluxo de Compra - SAGA Coreografada',
            fontsize=18, fontweight='bold', ha='center', color='#1a1a2e')
    ax.text(9, 9.0, 'Cada etapa e uma transacao independente com compensacao em caso de falha',
            fontsize=11, ha='center', color='#666', fontstyle='italic')

    # --- HAPPY PATH ---
    ax.text(1, 8.2, 'FLUXO DE SUCESSO (Happy Path)', fontsize=13, fontweight='bold', color='#2e7d32')

    steps = [
        (1.0, 'SELECIONADO', 'Cliente seleciona\no veiculo', '#bbdefb', '#1565c0'),
        (4.2, 'RESERVADO', 'Veiculo reservado\npor 30 minutos', '#c8e6c9', '#2e7d32'),
        (7.4, 'PGTO PENDENTE', 'Codigo de\npagamento gerado', '#fff9c4', '#f57f17'),
        (10.6, 'PAGO', 'Pagamento\nconfirmado', '#e1bee7', '#7b1fa2'),
        (13.8, 'CONCLUIDO', 'Veiculo retirado\nBaixa no estoque', '#c8e6c9', '#1b5e20'),
    ]

    for i, (x, title, desc, fc, tc) in enumerate(steps):
        box = FancyBboxPatch((x, 6.5), 2.8, 1.5, boxstyle="round,pad=0.15",
                              facecolor=fc, edgecolor=tc, linewidth=2)
        ax.add_patch(box)
        ax.text(x + 1.4, 7.6, title, fontsize=9, fontweight='bold', ha='center', color=tc)
        ax.text(x + 1.4, 7.0, desc, fontsize=8, ha='center', va='center', color='#333')

        if i < len(steps) - 1:
            ax.annotate('', xy=(steps[i+1][0], 7.25), xytext=(x + 2.8, 7.25),
                        arrowprops=dict(arrowstyle='->', color='#2e7d32', lw=2.5))

    # --- COMPENSATION PATHS ---
    ax.text(1, 5.5, 'FLUXOS DE COMPENSACAO (Unhappy Paths)', fontsize=13, fontweight='bold', color='#c62828')

    # Cancelado box
    cancel_box = FancyBboxPatch((13.8, 3.0), 3.0, 1.8, boxstyle="round,pad=0.15",
                                 facecolor='#ffcdd2', edgecolor='#c62828', linewidth=2.5)
    ax.add_patch(cancel_box)
    ax.text(15.3, 4.3, 'CANCELADO', fontsize=11, fontweight='bold', ha='center', color='#c62828')
    ax.text(15.3, 3.7, 'Compensacoes:\n- Libera veiculo\n- Registra motivo\n- Log auditoria',
            fontsize=8, ha='center', va='center', color='#b71c1c')

    # Scenarios
    scenarios = [
        (1.0, 4.2, 'Desistencia\ndo cliente', '#ffcdd2', '#c62828'),
        (4.0, 4.2, 'Outro cliente\nreservou antes', '#ffe0b2', '#e65100'),
        (7.0, 4.2, 'Reserva\nexpirada (30min)', '#fff9c4', '#f57f17'),
        (10.0, 4.2, 'Pagamento\nnao efetuado', '#e1bee7', '#7b1fa2'),
    ]

    for x, y, text, fc, tc in scenarios:
        box = FancyBboxPatch((x, y - 0.6), 2.5, 1.2, boxstyle="round,pad=0.1",
                              facecolor=fc, edgecolor=tc, linewidth=1.5)
        ax.add_patch(box)
        ax.text(x + 1.25, y, text, fontsize=8.5, ha='center', va='center',
                color=tc, fontweight='bold')
        ax.annotate('', xy=(13.8, 3.9), xytext=(x + 2.5, y),
                    arrowprops=dict(arrowstyle='->', color='#c62828', lw=1.5,
                                   linestyle='dashed', connectionstyle='arc3,rad=0.15'))

    # --- SAGA INFO ---
    info_box = FancyBboxPatch((1, 1.0), 15.5, 1.8, boxstyle="round,pad=0.15",
                               facecolor='#e8eaf6', edgecolor='#283593', linewidth=1.5)
    ax.add_patch(info_box)
    ax.text(8.75, 2.4, 'SAGA COREOGRAFADA - Justificativa', fontsize=12, fontweight='bold',
            ha='center', color='#283593')

    info_text = ('- Cada servico conhece suas regras de transicao e compensacao (sem orquestrador central)\n'
                 '- Transacoes atomicas com SELECT_FOR_UPDATE (locks pessimistas) para evitar condicoes de corrida\n'
                 '- Historico de auditoria imutavel registra cada transicao | Ideal para fluxo linear com poucos participantes')
    ax.text(8.75, 1.6, info_text, fontsize=9, ha='center', va='center', color='#1a237e')

    plt.tight_layout()
    plt.savefig(os.path.join(DOCS_DIR, 'diagrama_saga.png'),
                dpi=150, bbox_inches='tight', facecolor='#f8f9fa')
    plt.close()
    print('diagrama_saga.png gerado')


def desenhar_seguranca():
    fig, ax = plt.subplots(1, 1, figsize=(16, 12))
    ax.set_xlim(0, 16)
    ax.set_ylim(0, 12)
    ax.axis('off')
    fig.patch.set_facecolor('#f8f9fa')

    ax.text(8, 11.5, 'Camadas de Seguranca da Plataforma',
            fontsize=18, fontweight='bold', ha='center', color='#1a1a2e')

    # Layer 1 - Transport
    l1 = FancyBboxPatch((1, 9.5), 14, 1.5, boxstyle="round,pad=0.15",
                         facecolor='#e3f2fd', edgecolor='#1565c0', linewidth=2)
    ax.add_patch(l1)
    ax.text(8, 10.6, 'CAMADA 1: Seguranca de Transporte', fontsize=13, fontweight='bold',
            ha='center', color='#1565c0')
    ax.text(8, 10.0, 'HTTPS obrigatorio (SECURE_SSL_REDIRECT) | HSTS 1 ano | Cookies seguros (Secure + HttpOnly)\n'
            'SSL/TLS gerenciado pelo Render (certificado automatico gratuito)',
            fontsize=9, ha='center', va='center', color='#0d47a1')

    # Layer 2 - Application
    l2 = FancyBboxPatch((1, 7.4), 14, 1.8, boxstyle="round,pad=0.15",
                         facecolor='#e8f5e9', edgecolor='#2e7d32', linewidth=2)
    ax.add_patch(l2)
    ax.text(8, 8.8, 'CAMADA 2: Seguranca de Aplicacao', fontsize=13, fontweight='bold',
            ha='center', color='#2e7d32')

    app_items = [
        (3.5, 8.1, 'CSRF\nProtection', '#c8e6c9', '#1b5e20'),
        (6.5, 8.1, 'XSS\nFilter', '#c8e6c9', '#1b5e20'),
        (9.5, 8.1, 'Clickjacking\nX-Frame: DENY', '#c8e6c9', '#1b5e20'),
        (12.5, 8.1, 'Content-Type\nNosniff', '#c8e6c9', '#1b5e20'),
    ]
    for x, y, text, fc, tc in app_items:
        box = FancyBboxPatch((x - 1.2, y - 0.4), 2.4, 0.8, boxstyle="round,pad=0.08",
                              facecolor=fc, edgecolor=tc, linewidth=1)
        ax.add_patch(box)
        ax.text(x, y, text, fontsize=8, ha='center', va='center', color=tc, fontweight='bold')

    # Layer 3 - Data
    l3 = FancyBboxPatch((1, 5.0), 14, 2.1, boxstyle="round,pad=0.15",
                         facecolor='#fff3e0', edgecolor='#e65100', linewidth=2)
    ax.add_patch(l3)
    ax.text(8, 6.8, 'CAMADA 3: Seguranca de Dados', fontsize=13, fontweight='bold',
            ha='center', color='#e65100')

    data_items = [
        (3.0, 5.9, 'CPF: Hash SHA-256\n(irreversivel)', '#ffe0b2', '#bf360c'),
        (7.0, 5.9, 'RG: Hash SHA-256\n(irreversivel)', '#ffe0b2', '#bf360c'),
        (11.0, 5.9, 'CPF mascarado\n***.***.***-XX', '#ffe0b2', '#bf360c'),
    ]
    for x, y, text, fc, tc in data_items:
        box = FancyBboxPatch((x - 1.5, y - 0.5), 3, 1.0, boxstyle="round,pad=0.08",
                              facecolor=fc, edgecolor=tc, linewidth=1.5)
        ax.add_patch(box)
        ax.text(x, y, text, fontsize=9, ha='center', va='center', color=tc, fontweight='bold')

    ax.text(8, 5.2, 'Serializers controlam exposicao: dados sensiveis nunca retornados na API | Validacao de CPF (digitos verificadores)',
            fontsize=8.5, ha='center', color='#e65100', fontstyle='italic')

    # Layer 4 - Database
    l4 = FancyBboxPatch((1, 3.0), 14, 1.7, boxstyle="round,pad=0.15",
                         facecolor='#f3e5f5', edgecolor='#6a1b9a', linewidth=2)
    ax.add_patch(l4)
    ax.text(8, 4.35, 'CAMADA 4: Seguranca de Banco de Dados', fontsize=13, fontweight='bold',
            ha='center', color='#6a1b9a')

    db_items = [
        (3.0, 3.7, 'ORM Parametrizado\n(Anti SQL Injection)', '#e1bee7', '#4a148c'),
        (7.0, 3.7, 'UUIDs como PKs\n(Anti enumeracao)', '#e1bee7', '#4a148c'),
        (11.0, 3.7, 'SELECT_FOR_UPDATE\n(Locks pessimistas)', '#e1bee7', '#4a148c'),
    ]
    for x, y, text, fc, tc in db_items:
        box = FancyBboxPatch((x - 1.5, y - 0.45), 3, 0.9, boxstyle="round,pad=0.08",
                              facecolor=fc, edgecolor=tc, linewidth=1)
        ax.add_patch(box)
        ax.text(x, y, text, fontsize=9, ha='center', va='center', color=tc, fontweight='bold')

    # Layer 5 - Audit
    l5 = FancyBboxPatch((1, 1.3), 14, 1.4, boxstyle="round,pad=0.15",
                         facecolor='#ffcdd2', edgecolor='#c62828', linewidth=2)
    ax.add_patch(l5)
    ax.text(8, 2.3, 'CAMADA 5: Auditoria e Conformidade (LGPD)', fontsize=13, fontweight='bold',
            ha='center', color='#c62828')
    ax.text(8, 1.7, 'HistoricoVenda: log imutavel de transicoes | Timestamps automaticos em todos os modelos\n'
            'Base legal: execucao de contrato (Art. 7, V) | Minimizacao de dados | Finalidade especifica',
            fontsize=9, ha='center', va='center', color='#b71c1c')

    plt.tight_layout()
    plt.savefig(os.path.join(DOCS_DIR, 'diagrama_seguranca.png'),
                dpi=150, bbox_inches='tight', facecolor='#f8f9fa')
    plt.close()
    print('diagrama_seguranca.png gerado')


if __name__ == '__main__':
    desenhar_arquitetura()
    desenhar_saga()
    desenhar_seguranca()
