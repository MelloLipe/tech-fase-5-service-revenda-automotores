"""
Gera PDF consolidado com os 3 entregáveis do Tech Challenge Fase 5:
1. Desenho de Arquitetura (serverless/gerenciáveis + justificativas + segurança nuvem)
2. Relatório de Segurança de Dados
3. Relatório de Orquestração SAGA
"""
import os
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm, mm
from reportlab.lib.colors import HexColor
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY, TA_LEFT
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Image, Table, TableStyle,
    PageBreak, HRFlowable, ListFlowable, ListItem,
)
from reportlab.lib import colors


def build_pdf():
    output_path = os.path.join(os.path.dirname(__file__), '..', 'Tech_Challenge_Fase5_Entregaveis.pdf')
    doc = SimpleDocTemplate(
        output_path,
        pagesize=A4,
        rightMargin=2*cm, leftMargin=2*cm,
        topMargin=2*cm, bottomMargin=2*cm,
    )

    styles = getSampleStyleSheet()

    # Custom styles
    styles.add(ParagraphStyle(
        'CoverTitle', parent=styles['Title'],
        fontSize=28, spaceAfter=10, textColor=HexColor('#1a1a2e'),
        alignment=TA_CENTER,
    ))
    styles.add(ParagraphStyle(
        'CoverSubtitle', parent=styles['Title'],
        fontSize=16, spaceAfter=30, textColor=HexColor('#666'),
        alignment=TA_CENTER,
    ))
    styles.add(ParagraphStyle(
        'SectionTitle', parent=styles['Heading1'],
        fontSize=18, spaceAfter=12, spaceBefore=20,
        textColor=HexColor('#1a1a2e'), borderWidth=1,
        borderColor=HexColor('#1a1a2e'), borderPadding=5,
    ))
    styles.add(ParagraphStyle(
        'SubSection', parent=styles['Heading2'],
        fontSize=14, spaceAfter=8, spaceBefore=14,
        textColor=HexColor('#283593'),
    ))
    styles.add(ParagraphStyle(
        'SubSubSection', parent=styles['Heading3'],
        fontSize=12, spaceAfter=6, spaceBefore=10,
        textColor=HexColor('#37474f'),
    ))
    styles.add(ParagraphStyle(
        'BodyJustified', parent=styles['BodyText'],
        fontSize=10, leading=14, alignment=TA_JUSTIFY,
        spaceAfter=6,
    ))
    styles.add(ParagraphStyle(
        'BulletItem', parent=styles['BodyText'],
        fontSize=10, leading=14, leftIndent=20,
        spaceAfter=4,
    ))
    styles.add(ParagraphStyle(
        'TableHeader', parent=styles['BodyText'],
        fontSize=9, textColor=colors.white, alignment=TA_CENTER,
    ))
    styles.add(ParagraphStyle(
        'TableCell', parent=styles['BodyText'],
        fontSize=9, alignment=TA_LEFT,
    ))
    styles.add(ParagraphStyle(
        'TableCellCenter', parent=styles['BodyText'],
        fontSize=9, alignment=TA_CENTER,
    ))

    elements = []
    docs_dir = os.path.dirname(__file__)

    # ==================== CAPA ====================
    elements.append(Spacer(1, 4*cm))
    elements.append(Paragraph('Tech Challenge SOAT', styles['CoverTitle']))
    elements.append(Paragraph('Fase 5 - Trabalho de Reposicao', styles['CoverSubtitle']))
    elements.append(Spacer(1, 1*cm))
    elements.append(HRFlowable(width="80%", color=HexColor('#1a1a2e'), thickness=2))
    elements.append(Spacer(1, 1*cm))
    elements.append(Paragraph('Plataforma de Revenda de Veiculos Automotores', styles['Heading2']))
    elements.append(Spacer(1, 2*cm))

    cover_info = [
        '<b>Entregaveis:</b>',
        '1. Desenho de Arquitetura (servicos serverless/gerenciaveis)',
        '2. Relatorio de Seguranca de Dados',
        '3. Relatorio de Orquestracao SAGA',
        '',
        '<b>Tecnologias:</b> Python 3.12, Django 5.x/6 compativel, Django REST Framework',
        '<b>Deploy:</b> Render (PaaS - Free Tier)',
        '<b>Banco:</b> PostgreSQL (Render Managed)',
    ]
    for line in cover_info:
        elements.append(Paragraph(line, styles['BodyJustified']))
    elements.append(Spacer(1, 2*cm))
    elements.append(Paragraph('<b>Link do GitHub:</b> https://github.com/MelloLipe/tech-fase-5-service-revenda-automotores', styles['BodyJustified']))

    elements.append(PageBreak())

    # ==================== 1. ARQUITETURA ====================
    elements.append(Paragraph('1. Desenho de Arquitetura', styles['SectionTitle']))
    elements.append(Spacer(1, 0.5*cm))

    elements.append(Paragraph('1.1 Visao Geral', styles['SubSection']))
    elements.append(Paragraph(
        'A plataforma foi construida como uma aplicacao web utilizando Django + Django REST Framework, '
        'deployada no Render (PaaS gerenciavel na nuvem). A arquitetura prioriza servicos <b>serverless '
        'e gerenciaveis</b> para eliminar a necessidade de gerenciar infraestrutura, reduzir custos e '
        'garantir seguranca automatizada.',
        styles['BodyJustified'],
    ))

    elements.append(Paragraph('1.2 Diagrama de Arquitetura', styles['SubSection']))
    img_arq = os.path.join(docs_dir, 'diagrama_arquitetura.png')
    if os.path.exists(img_arq):
        elements.append(Image(img_arq, width=16*cm, height=12*cm))
    elements.append(Spacer(1, 0.5*cm))

    elements.append(Paragraph(
        'O diagrama apresenta a solucao em 4 camadas: (1) Cliente/Browser acessando via HTTPS, '
        '(2) Render PaaS gerenciando o servidor Gunicorn, (3) Django Application com 3 apps '
        '(Veiculos, Compradores, Vendas/SAGA), e (4) PostgreSQL gerenciado pelo Render.',
        styles['BodyJustified'],
    ))

    elements.append(PageBreak())

    elements.append(Paragraph('1.3 Arquitetura Cloud Serverless de Referencia', styles['SubSection']))
    elements.append(Paragraph(
        'Embora a implementacao deste repositorio rode localmente e possa ser simulada no Render para fins '
        'academicos, a arquitetura foi pensada para uma evolucao em nuvem usando servicos serverless e '
        'gerenciaveis. O objetivo do desenho abaixo e demonstrar como a solucao poderia ser implantada em '
        'producao com menor operacao manual, escalabilidade sob demanda e seguranca nativa da plataforma cloud.',
        styles['BodyJustified'],
    ))
    img_arq_serverless = os.path.join(docs_dir, 'diagrama_arquitetura_serverless.png')
    if os.path.exists(img_arq_serverless):
        elements.append(Image(img_arq_serverless, width=16*cm, height=10.6*cm))
    elements.append(Spacer(1, 0.4*cm))
    elements.append(Paragraph(
        'Neste modelo, CloudFront e WAF protegem e distribuem o frontend; API Gateway publica as rotas REST; '
        'AWS Lambda executa as regras de negocio sob demanda; EventBridge/SQS desacoplam eventos da SAGA; '
        'Aurora Serverless v2 preserva as transacoes relacionais necessarias para reserva e venda; '
        'Secrets Manager, KMS e CloudWatch concentram segredos, criptografia, logs e observabilidade.',
        styles['BodyJustified'],
    ))

    elements.append(PageBreak())

    # Componentes e justificativas
    elements.append(Paragraph('1.4 Servicos Utilizados e Justificativas', styles['SubSection']))

    # Table of services
    service_data = [
        [Paragraph('<b>Servico</b>', styles['TableHeader']),
         Paragraph('<b>Tipo</b>', styles['TableHeader']),
         Paragraph('<b>Justificativa</b>', styles['TableHeader'])],
        [Paragraph('Render Web Service', styles['TableCell']),
         Paragraph('PaaS Gerenciavel', styles['TableCellCenter']),
         Paragraph('Deploy automatico via GitHub, SSL gratuito, escalabilidade automatica. '
                   'Elimina gerenciamento de servidores, patches e infraestrutura. '
                   'Plano gratuito adequado para o projeto.', styles['TableCell'])],
        [Paragraph('Render PostgreSQL', styles['TableCell']),
         Paragraph('Banco Gerenciavel', styles['TableCellCenter']),
         Paragraph('Banco relacional robusto com transacoes ACID (essenciais para SAGA). '
                   'Backups automaticos, conexao SSL, isolamento de rede. '
                   'Suporte nativo a UUIDs. Gerenciado pela nuvem.', styles['TableCell'])],
        [Paragraph('Render SSL/TLS', styles['TableCell']),
         Paragraph('Seguranca na Nuvem', styles['TableCellCenter']),
         Paragraph('Certificados Let\'s Encrypt automaticos e gratuitos. '
                   'Toda comunicacao criptografada sem configuracao manual. '
                   'Previne man-in-the-middle e sniffing.', styles['TableCell'])],
        [Paragraph('Django + DRF', styles['TableCell']),
         Paragraph('Framework Web', styles['TableCellCenter']),
         Paragraph('Framework maduro com ORM, autenticacao integrada, admin automatico. '
                   'Uma unica app serve API REST e frontend, economizando recursos. '
                   'Middlewares de seguranca integrados.', styles['TableCell'])],
        [Paragraph('Gunicorn', styles['TableCell']),
         Paragraph('Servidor WSGI', styles['TableCellCenter']),
         Paragraph('Servidor de producao leve e eficiente. 2 workers para plano gratuito (512MB RAM). '
                   'Pre-fork worker model para concorrencia.', styles['TableCell'])],
        [Paragraph('WhiteNoise', styles['TableCell']),
         Paragraph('Static Files', styles['TableCellCenter']),
         Paragraph('Serve arquivos estaticos sem necessidade de CDN ou Nginx separado. '
                   'Compressao automatica (gzip). Zero custo adicional.', styles['TableCell'])],
    ]
    service_table = Table(service_data, colWidths=[3.5*cm, 3*cm, 10*cm])
    service_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), HexColor('#1a1a2e')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
        ('FONTSIZE', (0, 0), (-1, -1), 9),
        ('GRID', (0, 0), (-1, -1), 0.5, HexColor('#ccc')),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [HexColor('#f8f9fa'), colors.white]),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ('LEFTPADDING', (0, 0), (-1, -1), 6),
        ('RIGHTPADDING', (0, 0), (-1, -1), 6),
    ]))
    elements.append(service_table)
    elements.append(Spacer(1, 0.5*cm))

    elements.append(Paragraph('1.5 Alternativas Consideradas e Decisoes Arquiteturais', styles['SubSection']))
    alternatives = [
        '<b>Render</b>: escolhido para simulacao executavel por ser simples, gratuito e gerenciavel, '
        'permitindo gravar o video e demonstrar a aplicacao sem provisionar cloud paga.',
        '<b>AWS Lambda + API Gateway</b>: arquitetura alvo serverless considerada para producao. '
        'Nao foi implementada no repositorio por aumentar complexidade, custo e tempo de entrega academica, '
        'mas foi modelada no desenho de referencia.',
        '<b>Aurora Serverless v2</b>: alternativa serverless ao PostgreSQL gerenciado, preservando SQL, '
        'transacoes ACID e escalabilidade automatica.',
        '<b>DynamoDB/NoSQL</b>: descartado como banco principal pela necessidade de transacoes relacionais '
        'e locks pessimistas no fluxo de reserva/venda, essenciais para consistencia da SAGA.',
        '<b>AWS ECS/Fargate</b>: alternativa gerenciavel para containers, mas com custo e operacao maiores '
        'que Render para o escopo do trabalho.',
        '<b>Heroku/Railway/Fly.io</b>: alternativas PaaS avaliadas, mas descartadas por custo, limites de '
        'free tier ou exigencia de cartao de credito.',
    ]
    for alt in alternatives:
        elements.append(Paragraph(f'- {alt}', styles['BulletItem']))

    elements.append(PageBreak())

    # Seguranca na nuvem
    elements.append(Paragraph('1.6 Servicos de Seguranca na Nuvem', styles['SubSection']))

    elements.append(Paragraph('1.6.1 Render SSL/TLS (Seguranca de Transporte)', styles['SubSubSection']))
    elements.append(Paragraph(
        '<b>O que e:</b> O Render fornece certificados SSL/TLS gratuitos e automaticos (Let\'s Encrypt) '
        'para todas as aplicacoes deployadas na plataforma.',
        styles['BodyJustified'],
    ))
    elements.append(Paragraph(
        '<b>Por que usamos:</b> Garante que toda comunicacao entre cliente e servidor e criptografada, '
        'prevenindo ataques man-in-the-middle, sniffing de dados e interceptacao de credenciais. '
        'E um servico de seguranca gerenciado pela nuvem - nao requer configuracao manual de certificados, '
        'renovacao ou gerenciamento.',
        styles['BodyJustified'],
    ))
    elements.append(Paragraph(
        '<b>Configuracao:</b> SECURE_SSL_REDIRECT = True redireciona automaticamente HTTP para HTTPS. '
        'HSTS com 1 ano de duracao forca o browser a sempre usar HTTPS.',
        styles['BodyJustified'],
    ))
    elements.append(Paragraph(
        '<b>Observacao:</b> Em desenvolvimento local a aplicacao roda com DEBUG=True para facilitar testes. '
        'Em producao, o Render executa com DEBUG=False e HTTPS/TLS gerenciado pela plataforma.',
        styles['BodyJustified'],
    ))

    elements.append(Paragraph('1.6.2 Render Network Isolation (Seguranca de Rede)', styles['SubSubSection']))
    elements.append(Paragraph(
        '<b>O que e:</b> O PostgreSQL no Render e acessivel apenas internamente, dentro da rede privada.',
        styles['BodyJustified'],
    ))
    elements.append(Paragraph(
        '<b>Por que usamos:</b> O banco de dados nao tem IP publico, prevenindo ataques diretos. '
        'Apenas a aplicacao Django consegue se conectar, via conexao SSL interna.',
        styles['BodyJustified'],
    ))

    elements.append(Paragraph('1.6.3 Django Security Middleware (Seguranca de Aplicacao)', styles['SubSubSection']))
    security_items = [
        '<b>SecurityMiddleware (HSTS)</b>: Strict-Transport-Security forca HTTPS por 1 ano, '
        'prevenindo downgrade attacks.',
        '<b>CsrfViewMiddleware</b>: Token CSRF em cada formulario, prevenindo Cross-Site Request Forgery.',
        '<b>X-Content-Type-Options: nosniff</b>: Previne MIME-type sniffing pelo browser.',
        '<b>X-XSS-Protection</b>: Ativa filtro XSS nativo do browser.',
        '<b>X-Frame-Options: DENY</b>: Previne clickjacking (aplicacao embutida em iframes maliciosos).',
        '<b>Cookies Secure + HttpOnly</b>: Cookies de sessao so transmitidos via HTTPS e inacessiveis '
        'via JavaScript.',
    ]
    for item in security_items:
        elements.append(Paragraph(f'- {item}', styles['BulletItem']))

    elements.append(Paragraph(
        '<b>Justificativa:</b> Sao protecoes padrao da industria contra os ataques web mais comuns '
        '(OWASP Top 10). O Django fornece essas protecoes integradas, bastando habilita-las na configuracao.',
        styles['BodyJustified'],
    ))

    elements.append(Paragraph('1.6.4 Hashing Criptografico de Dados Sensiveis', styles['SubSubSection']))
    elements.append(Paragraph(
        '<b>O que e:</b> CPF e RG sao tratados como dados pessoais identificadores criticos e '
        'armazenados como hashes SHA-256 (funcao de hash criptografica irreversivel). '
        'Apenas o CPF mascarado (***.***.*XX-XX) e visivel na interface.',
        styles['BodyJustified'],
    ))
    elements.append(Paragraph(
        '<b>Por que usamos:</b> Mesmo em caso de vazamento completo do banco de dados, e '
        'computacionalmente inviavel recuperar os documentos originais a partir dos hashes. '
        'Essa e uma medida de protecao alinhada a LGPD para reduzir exposicao e risco de fraude '
        'sobre dados pessoais identificadores.',
        styles['BodyJustified'],
    ))

    elements.append(Paragraph('1.6.5 Variaveis de Ambiente (12-Factor App)', styles['SubSubSection']))
    elements.append(Paragraph(
        '<b>O que e:</b> SECRET_KEY, DATABASE_URL e configuracoes sensiveis sao gerenciadas via '
        'variaveis de ambiente (os.environ), nunca armazenadas no codigo-fonte.',
        styles['BodyJustified'],
    ))
    elements.append(Paragraph(
        '<b>Por que usamos:</b> Seguimos o principio dos 12-Factor Apps. Nenhum segredo e exposto '
        'em repositorios publicos. O Render gerencia as variaveis de ambiente de forma segura.',
        styles['BodyJustified'],
    ))

    elements.append(PageBreak())

    # ==================== 2. RELATORIO DE SEGURANCA ====================
    elements.append(Paragraph('2. Relatorio de Seguranca de Dados', styles['SectionTitle']))
    elements.append(Spacer(1, 0.5*cm))

    # Diagrama de seguranca
    elements.append(Paragraph('2.1 Visao Geral das Camadas de Seguranca', styles['SubSection']))
    img_seg = os.path.join(docs_dir, 'diagrama_seguranca.png')
    if os.path.exists(img_seg):
        elements.append(Image(img_seg, width=15*cm, height=11*cm))
    elements.append(Spacer(1, 0.3*cm))
    elements.append(Paragraph(
        'A plataforma implementa 5 camadas de seguranca independentes e complementares, '
        'desde o transporte de dados ate a conformidade com a LGPD.',
        styles['BodyJustified'],
    ))

    elements.append(PageBreak())

    # Dados armazenados
    elements.append(Paragraph('2.2 Dados Armazenados pela Solucao', styles['SubSection']))

    elements.append(Paragraph('2.2.1 Dados de Veiculos', styles['SubSubSection']))
    veiculo_data = [
        [Paragraph('<b>Campo</b>', styles['TableHeader']),
         Paragraph('<b>Tipo</b>', styles['TableHeader']),
         Paragraph('<b>Sensibilidade</b>', styles['TableHeader'])],
        [Paragraph('Marca, Modelo, Ano, Cor', styles['TableCell']),
         Paragraph('Texto', styles['TableCellCenter']),
         Paragraph('Publica', styles['TableCellCenter'])],
        [Paragraph('Preco', styles['TableCell']),
         Paragraph('Decimal', styles['TableCellCenter']),
         Paragraph('Publica', styles['TableCellCenter'])],
        [Paragraph('Placa', styles['TableCell']),
         Paragraph('Texto (unique)', styles['TableCellCenter']),
         Paragraph('Moderada', styles['TableCellCenter'])],
        [Paragraph('Chassi', styles['TableCell']),
         Paragraph('Texto (unique)', styles['TableCellCenter']),
         Paragraph('Moderada', styles['TableCellCenter'])],
        [Paragraph('Quilometragem', styles['TableCell']),
         Paragraph('Inteiro', styles['TableCellCenter']),
         Paragraph('Publica', styles['TableCellCenter'])],
        [Paragraph('Status', styles['TableCell']),
         Paragraph('Enum', styles['TableCellCenter']),
         Paragraph('Publica', styles['TableCellCenter'])],
    ]
    vt = Table(veiculo_data, colWidths=[6*cm, 4*cm, 4*cm])
    vt.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), HexColor('#283593')),
        ('GRID', (0, 0), (-1, -1), 0.5, HexColor('#ccc')),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [HexColor('#f8f9fa'), colors.white]),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
    ]))
    elements.append(vt)
    elements.append(Spacer(1, 0.3*cm))

    elements.append(Paragraph('2.2.2 Dados de Compradores', styles['SubSubSection']))
    comprador_data = [
        [Paragraph('<b>Campo</b>', styles['TableHeader']),
         Paragraph('<b>Tipo</b>', styles['TableHeader']),
         Paragraph('<b>Sensibilidade</b>', styles['TableHeader']),
         Paragraph('<b>Tratamento</b>', styles['TableHeader'])],
        [Paragraph('Nome', styles['TableCell']),
         Paragraph('Texto', styles['TableCellCenter']),
         Paragraph('Pessoal (LGPD)', styles['TableCellCenter']),
         Paragraph('Texto plano', styles['TableCell'])],
        [Paragraph('Email', styles['TableCell']),
         Paragraph('Texto', styles['TableCellCenter']),
         Paragraph('Pessoal (LGPD)', styles['TableCellCenter']),
         Paragraph('Texto plano', styles['TableCell'])],
        [Paragraph('Telefone', styles['TableCell']),
         Paragraph('Texto', styles['TableCellCenter']),
         Paragraph('Pessoal (LGPD)', styles['TableCellCenter']),
         Paragraph('Texto plano', styles['TableCell'])],
        [Paragraph('<b>CPF</b>', styles['TableCell']),
         Paragraph('<b>Hash SHA-256</b>', styles['TableCellCenter']),
         Paragraph('<b>Identificador critico</b>', styles['TableCellCenter']),
         Paragraph('<b>Hash irreversivel + mascaramento</b>', styles['TableCell'])],
        [Paragraph('<b>RG</b>', styles['TableCell']),
         Paragraph('<b>Hash SHA-256</b>', styles['TableCellCenter']),
         Paragraph('<b>Identificador critico</b>', styles['TableCellCenter']),
         Paragraph('<b>Hash irreversivel</b>', styles['TableCell'])],
        [Paragraph('Endereco', styles['TableCell']),
         Paragraph('Texto', styles['TableCellCenter']),
         Paragraph('Pessoal (LGPD)', styles['TableCellCenter']),
         Paragraph('Texto plano', styles['TableCell'])],
        [Paragraph('Data Nascimento', styles['TableCell']),
         Paragraph('Data', styles['TableCellCenter']),
         Paragraph('Pessoal (LGPD)', styles['TableCellCenter']),
         Paragraph('Texto plano', styles['TableCell'])],
    ]
    ct = Table(comprador_data, colWidths=[3.5*cm, 3*cm, 3.5*cm, 6.5*cm])
    ct.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), HexColor('#c62828')),
        ('GRID', (0, 0), (-1, -1), 0.5, HexColor('#ccc')),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [HexColor('#f8f9fa'), colors.white]),
        ('BACKGROUND', (0, 4), (-1, 5), HexColor('#ffebee')),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
    ]))
    elements.append(ct)
    elements.append(Spacer(1, 0.3*cm))

    elements.append(Paragraph('2.2.3 Dados de Vendas', styles['SubSubSection']))
    venda_data = [
        [Paragraph('<b>Campo</b>', styles['TableHeader']),
         Paragraph('<b>Tipo</b>', styles['TableHeader']),
         Paragraph('<b>Sensibilidade</b>', styles['TableHeader'])],
        [Paragraph('Codigo de Pagamento', styles['TableCell']),
         Paragraph('UUID', styles['TableCellCenter']),
         Paragraph('Confidencial', styles['TableCellCenter'])],
        [Paragraph('Preco de Venda', styles['TableCell']),
         Paragraph('Decimal', styles['TableCellCenter']),
         Paragraph('Comercial', styles['TableCellCenter'])],
        [Paragraph('Status da Venda', styles['TableCell']),
         Paragraph('Enum', styles['TableCellCenter']),
         Paragraph('Operacional', styles['TableCellCenter'])],
        [Paragraph('Timestamps', styles['TableCell']),
         Paragraph('DateTime', styles['TableCellCenter']),
         Paragraph('Operacional', styles['TableCellCenter'])],
        [Paragraph('Historico/Auditoria', styles['TableCell']),
         Paragraph('Texto', styles['TableCellCenter']),
         Paragraph('Operacional', styles['TableCellCenter'])],
    ]
    vdt = Table(venda_data, colWidths=[6*cm, 4*cm, 4*cm])
    vdt.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), HexColor('#e65100')),
        ('GRID', (0, 0), (-1, -1), 0.5, HexColor('#ccc')),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [HexColor('#f8f9fa'), colors.white]),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
    ]))
    elements.append(vdt)

    elements.append(PageBreak())

    # Dados sensiveis
    elements.append(Paragraph('2.3 Dados Sensiveis Identificados', styles['SubSection']))
    elements.append(Paragraph(
        '<b>Dados pessoais identificadores de alta criticidade:</b>',
        styles['BodyJustified'],
    ))
    elements.append(Paragraph(
        '- <b>CPF</b>: Documento de identificacao fiscal. Armazenado como hash SHA-256 (irreversivel). '
        'Apenas os 4 ultimos digitos sao visiveis na interface (mascaramento: ***.***.*XX-XX).',
        styles['BulletItem'],
    ))
    elements.append(Paragraph(
        '- <b>RG</b>: Documento de identificacao civil. Armazenado como hash SHA-256 (irreversivel). '
        'Nunca exibido na interface ou retornado pela API.',
        styles['BulletItem'],
    ))
    elements.append(Paragraph(
        '<b>Dados pessoais (LGPD Art. 5, I):</b> Nome, email, telefone, endereco, data de nascimento, '
        'CPF e RG permitem identificacao do titular. CPF e RG foram tratados com controles reforcados '
        'por risco de fraude e dano ao titular.',
        styles['BodyJustified'],
    ))

    # Politicas de acesso
    elements.append(Paragraph('2.4 Politicas de Acesso a Dados Implementadas', styles['SubSection']))
    access_policies = [
        '<b>Principio do Menor Privilegio</b>: A API de leitura nunca expoe CPF ou RG em texto plano. '
        'Apenas o CPF mascarado e retornado. O hash completo nunca e exposto.',
        '<b>Serializers com Controle de Exposicao</b>: CompradorCreateSerializer aceita CPF/RG em texto '
        'plano (write-only) e gera hashes imediatamente. CompradorSerializer retorna apenas CPF mascarado.',
        '<b>Admin Django com Restricoes</b>: Campos sensiveis (cpf_hash, rg_hash) sao readonly e '
        'nao editaveis, mesmo para administradores.',
        '<b>Validacao de Dados na Entrada</b>: CPF e validado algoritmicamente (digitos verificadores) '
        'antes do armazenamento. RG e validado por formato minimo. Email validado por formato e unicidade.',
        '<b>UUIDs como Chaves Primarias</b>: Previne enumeracao sequencial de recursos (ataques IDOR). '
        'Impossivel adivinhar IDs de outros compradores ou vendas.',
    ]
    for policy in access_policies:
        elements.append(Paragraph(f'- {policy}', styles['BulletItem']))

    # Politicas de seguranca da operacao
    elements.append(Paragraph('2.5 Politicas de Seguranca da Operacao Implementadas', styles['SubSection']))

    elements.append(Paragraph('Seguranca de Transporte:', styles['SubSubSection']))
    transport = [
        'HTTPS obrigatorio: SECURE_SSL_REDIRECT = True em producao.',
        'HSTS: SECURE_HSTS_SECONDS = 31536000 (1 ano), incluindo subdominios e preload.',
        'Cookies seguros: SESSION_COOKIE_SECURE = True, CSRF_COOKIE_SECURE = True.',
        'Ambiente local usa DEBUG=True apenas para demonstracao; ambiente de producao usa DEBUG=False.',
    ]
    for t in transport:
        elements.append(Paragraph(f'- {t}', styles['BulletItem']))

    elements.append(Paragraph('Seguranca de Aplicacao:', styles['SubSubSection']))
    app_sec = [
        'CSRF Protection: Token CSRF em todos os formularios.',
        'XSS Protection: SECURE_BROWSER_XSS_FILTER = True.',
        'Content-Type Sniffing: SECURE_CONTENT_TYPE_NOSNIFF = True.',
        'Clickjacking: X_FRAME_OPTIONS = DENY.',
        'Secret Key: Gerada automaticamente via variavel de ambiente, nunca no codigo.',
    ]
    for a in app_sec:
        elements.append(Paragraph(f'- {a}', styles['BulletItem']))

    elements.append(Paragraph('Seguranca de Banco de Dados:', styles['SubSubSection']))
    db_sec = [
        'Conexao criptografada: PostgreSQL via SSL no Render.',
        'ORM parametrizado: Prevencao de SQL Injection via Django ORM. Nenhuma query raw.',
        'SELECT_FOR_UPDATE: Locks pessimistas para operacoes concorrentes (reservas de veiculos).',
        'Transacoes atomicas: transaction.atomic() garante consistencia em cada etapa da SAGA.',
    ]
    for d in db_sec:
        elements.append(Paragraph(f'- {d}', styles['BulletItem']))

    elements.append(Paragraph('Auditoria:', styles['SubSubSection']))
    audit = [
        'HistoricoVenda: Log imutavel de todas as transicoes de estado (SAGA).',
        'Timestamps automaticos: criado_em e atualizado_em em todos os modelos.',
        'Rastreabilidade completa do fluxo de cada venda, incluindo compensacoes.',
    ]
    for au in audit:
        elements.append(Paragraph(f'- {au}', styles['BulletItem']))

    elements.append(PageBreak())

    # Riscos e mitigacao
    elements.append(Paragraph('2.6 Riscos e Acoes de Mitigacao', styles['SubSection']))

    risks = [
        ('Vazamento de Banco de Dados', 'Alto', 'Dados pessoais expostos',
         'CPF e RG armazenados como hash SHA-256 irreversivel. Mesmo com acesso ao banco, '
         'nao e possivel recuperar os documentos originais. CPF mascarado na interface.'),
        ('Condicao de Corrida na Reserva', 'Medio', 'Dois clientes reservam o mesmo veiculo',
         'SELECT_FOR_UPDATE com locks pessimistas. Transacoes atomicas (transaction.atomic()). '
         'Verificacao de status do veiculo antes de cada operacao.'),
        ('Reserva Sem Pagamento', 'Medio', 'Veiculo fica indisponivel indefinidamente',
         'Expiracao automatica de reservas em 30 minutos. Compensacao SAGA libera o veiculo.'),
        ('Acesso Nao Autorizado a API', 'Alto', 'Manipulacao de dados',
         'Para producao: implementar autenticacao JWT ou OAuth2 via DRF. '
         'Rate limiting para prevenir abuso.'),
        ('Forca Bruta em CPF', 'Medio', 'CPFs tem espaco limitado (11 digitos)',
         'Hash SHA-256 reduz exposicao direta. Para producao: adicionar segredo/salt com HMAC '
         'ou algoritmo resistente como bcrypt/argon2 para reduzir ataques por dicionario.'),
        ('Injecao de SQL', 'Critico', 'Acesso/modificacao de dados',
         'Django ORM com queries parametrizadas. Nenhuma query SQL raw utilizada.'),
    ]

    risk_data = [
        [Paragraph('<b>Risco</b>', styles['TableHeader']),
         Paragraph('<b>Impacto</b>', styles['TableHeader']),
         Paragraph('<b>Descricao</b>', styles['TableHeader']),
         Paragraph('<b>Mitigacao</b>', styles['TableHeader'])],
    ]
    for risk, impact, desc, mitigation in risks:
        risk_data.append([
            Paragraph(risk, styles['TableCell']),
            Paragraph(impact, styles['TableCellCenter']),
            Paragraph(desc, styles['TableCell']),
            Paragraph(mitigation, styles['TableCell']),
        ])
    rt = Table(risk_data, colWidths=[3*cm, 2*cm, 3.5*cm, 8*cm])
    rt.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), HexColor('#c62828')),
        ('GRID', (0, 0), (-1, -1), 0.5, HexColor('#ccc')),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [HexColor('#f8f9fa'), colors.white]),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
        ('LEFTPADDING', (0, 0), (-1, -1), 4),
        ('RIGHTPADDING', (0, 0), (-1, -1), 4),
    ]))
    elements.append(rt)

    elements.append(Spacer(1, 0.5*cm))
    elements.append(Paragraph('2.7 Conformidade LGPD', styles['SubSection']))
    lgpd = [
        '<b>Base Legal</b>: Execucao de contrato (Art. 7, V) - dados necessarios para processo de '
        'compra e documentacao veicular.',
        '<b>Minimizacao</b>: Apenas dados estritamente necessarios sao coletados.',
        '<b>Finalidade</b>: Dados utilizados exclusivamente para o processo de compra e documentacao.',
        '<b>Transparencia</b>: CPF mascarado indica ao titular que seus dados estao protegidos.',
        '<b>Seguranca</b>: Medidas tecnicas de protecao implementadas (hashing, HTTPS, headers).',
    ]
    for l in lgpd:
        elements.append(Paragraph(f'- {l}', styles['BulletItem']))

    elements.append(PageBreak())

    # ==================== 3. RELATORIO SAGA ====================
    elements.append(Paragraph('3. Relatorio de Orquestracao SAGA', styles['SectionTitle']))
    elements.append(Spacer(1, 0.5*cm))

    elements.append(Paragraph('3.1 Tipo de SAGA Escolhido: Coreografia (Choreography)', styles['SubSection']))

    elements.append(Paragraph(
        'Para este projeto, foi escolhida a <b>SAGA Coreografada</b> ao inves da SAGA Orquestrada.',
        styles['BodyJustified'],
    ))

    elements.append(Paragraph('3.2 Diagrama do Fluxo SAGA', styles['SubSection']))
    img_saga = os.path.join(docs_dir, 'diagrama_saga.png')
    if os.path.exists(img_saga):
        elements.append(Image(img_saga, width=16*cm, height=9*cm))
    elements.append(Spacer(1, 0.3*cm))

    elements.append(Paragraph('3.3 Justificativa da Escolha', styles['SubSection']))

    elements.append(Paragraph('Razoes Tecnicas:', styles['SubSubSection']))
    tech_reasons = [
        '<b>Arquitetura Monolitica</b>: Como a aplicacao e um monolito Django (nao microsservicos), '
        'nao ha necessidade de um orquestrador central separado. Cada servico (service layer) '
        'conhece suas proprias regras de transicao e compensacao.',
        '<b>Simplicidade</b>: A coreografia e mais simples de implementar em aplicacoes monoliticas, '
        'onde todas as transacoes ocorrem no mesmo banco de dados.',
        '<b>Economia de Recursos</b>: Nao requer um servico de orquestracao separado (como RabbitMQ, '
        'Kafka), reduzindo custos de infraestrutura - essencial para deploy em plano gratuito.',
        '<b>Acoplamento Baixo</b>: Cada etapa do processo e independente e contem sua propria '
        'logica de compensacao, facilitando manutencao e testes.',
    ]
    for r in tech_reasons:
        elements.append(Paragraph(f'- {r}', styles['BulletItem']))

    elements.append(Paragraph('Razoes de Negocio:', styles['SubSubSection']))
    biz_reasons = [
        '<b>Fluxo Linear</b>: O processo de compra e essencialmente linear '
        '(selecionar -> reservar -> pagar -> retirar), sem ramificacoes complexas.',
        '<b>Poucos Participantes</b>: Apenas 3 entidades participam (Veiculo, Comprador, Venda), '
        'tornando a coreografia gerenciavel.',
        '<b>Compensacoes Simples</b>: As acoes compensatorias sao diretas (liberar reserva, '
        'cancelar venda), sem necessidade de coordenacao complexa.',
    ]
    for r in biz_reasons:
        elements.append(Paragraph(f'- {r}', styles['BulletItem']))

    elements.append(PageBreak())

    # Fluxo detalhado
    elements.append(Paragraph('3.4 Fluxo Detalhado da SAGA', styles['SubSection']))

    elements.append(Paragraph('Fluxo de Sucesso (Happy Path):', styles['SubSubSection']))
    elements.append(Paragraph(
        '1. <b>SELECIONADO</b>: Cliente seleciona o veiculo desejado. Sistema verifica disponibilidade.<br/>'
        '2. <b>RESERVADO</b>: Veiculo e reservado por 30 minutos com lock pessimista (SELECT_FOR_UPDATE).<br/>'
        '3. <b>PAGAMENTO PENDENTE</b>: Codigo de pagamento (UUID) e gerado e enviado ao cliente.<br/>'
        '4. <b>PAGO</b>: Cliente confirma pagamento com o codigo recebido. Sistema valida.<br/>'
        '5. <b>CONCLUIDO</b>: Veiculo e retirado pelo cliente. Status do veiculo muda para VENDIDO.',
        styles['BodyJustified'],
    ))

    elements.append(Paragraph('Cenarios de Compensacao:', styles['SubSubSection']))
    comp_data = [
        [Paragraph('<b>Cenario</b>', styles['TableHeader']),
         Paragraph('<b>Etapa</b>', styles['TableHeader']),
         Paragraph('<b>Compensacao</b>', styles['TableHeader'])],
        [Paragraph('Veiculo ja reservado por outro', styles['TableCell']),
         Paragraph('Reserva', styles['TableCellCenter']),
         Paragraph('Cancela venda automaticamente, registra motivo no historico', styles['TableCell'])],
        [Paragraph('Reserva expirada (>30 min)', styles['TableCell']),
         Paragraph('Pagamento', styles['TableCellCenter']),
         Paragraph('Libera veiculo, cancela venda, registra no historico', styles['TableCell'])],
        [Paragraph('Pagamento nao efetuado', styles['TableCell']),
         Paragraph('Pagamento', styles['TableCellCenter']),
         Paragraph('Libera veiculo, cancela venda', styles['TableCell'])],
        [Paragraph('Cliente desiste', styles['TableCell']),
         Paragraph('Qualquer', styles['TableCellCenter']),
         Paragraph('Libera veiculo (se reservado), cancela venda, registra motivo', styles['TableCell'])],
        [Paragraph('Codigo pagamento invalido', styles['TableCell']),
         Paragraph('Confirmacao', styles['TableCellCenter']),
         Paragraph('Rejeita operacao, mantem status anterior', styles['TableCell'])],
    ]
    comp_table = Table(comp_data, colWidths=[4.5*cm, 3*cm, 9*cm])
    comp_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), HexColor('#c62828')),
        ('GRID', (0, 0), (-1, -1), 0.5, HexColor('#ccc')),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [HexColor('#f8f9fa'), colors.white]),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
        ('LEFTPADDING', (0, 0), (-1, -1), 4),
        ('RIGHTPADDING', (0, 0), (-1, -1), 4),
    ]))
    elements.append(comp_table)

    elements.append(Spacer(1, 0.5*cm))

    elements.append(Paragraph('3.5 Implementacao Tecnica', styles['SubSection']))
    impl = [
        '<b>Transacoes Atomicas</b>: Cada etapa da SAGA e envolvida em transaction.atomic() '
        'com SELECT_FOR_UPDATE para garantir atomicidade, isolamento e consistencia.',
        '<b>Historico de Auditoria</b>: Cada transicao e registrada na tabela HistoricoVenda '
        '(status anterior, novo, descricao, timestamp), permitindo rastreabilidade completa.',
        '<b>Service Layer</b>: Logica de negocio isolada em vendas/services.py com funcoes '
        'especificas para cada etapa e compensacao.',
        '<b>Idempotencia</b>: Cada operacao verifica o status atual antes de executar, '
        'garantindo que transicoes invalidas sejam rejeitadas.',
    ]
    for i in impl:
        elements.append(Paragraph(f'- {i}', styles['BulletItem']))

    elements.append(Spacer(1, 0.5*cm))

    elements.append(Paragraph('3.6 Comparacao: Coreografia vs. Orquestracao', styles['SubSection']))
    comp_vs = [
        [Paragraph('<b>Aspecto</b>', styles['TableHeader']),
         Paragraph('<b>Coreografia (Escolhida)</b>', styles['TableHeader']),
         Paragraph('<b>Orquestracao</b>', styles['TableHeader'])],
        [Paragraph('Complexidade', styles['TableCell']),
         Paragraph('Baixa', styles['TableCellCenter']),
         Paragraph('Alta', styles['TableCellCenter'])],
        [Paragraph('Infraestrutura', styles['TableCell']),
         Paragraph('Nenhuma adicional', styles['TableCellCenter']),
         Paragraph('Message broker necessario', styles['TableCellCenter'])],
        [Paragraph('Custo', styles['TableCell']),
         Paragraph('Zero adicional', styles['TableCellCenter']),
         Paragraph('Servidor de orquestracao', styles['TableCellCenter'])],
        [Paragraph('Acoplamento', styles['TableCell']),
         Paragraph('Baixo', styles['TableCellCenter']),
         Paragraph('Centralizado', styles['TableCellCenter'])],
        [Paragraph('Rastreabilidade', styles['TableCell']),
         Paragraph('Via logs de auditoria', styles['TableCellCenter']),
         Paragraph('Via orquestrador', styles['TableCellCenter'])],
        [Paragraph('Adequacao', styles['TableCell']),
         Paragraph('Ideal (fluxo linear)', styles['TableCellCenter']),
         Paragraph('Excessivo para o escopo', styles['TableCellCenter'])],
    ]
    comp_vs_table = Table(comp_vs, colWidths=[4*cm, 6*cm, 6.5*cm])
    comp_vs_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), HexColor('#283593')),
        ('GRID', (0, 0), (-1, -1), 0.5, HexColor('#ccc')),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [HexColor('#f8f9fa'), colors.white]),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
    ]))
    elements.append(comp_vs_table)

    # Build
    doc.build(elements)
    print(f'PDF gerado: {os.path.abspath(output_path)}')


if __name__ == '__main__':
    build_pdf()
