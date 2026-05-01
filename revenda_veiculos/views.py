from django.contrib import messages
from django.db.models import Sum
from django.shortcuts import get_object_or_404, redirect, render
from rest_framework.exceptions import ValidationError

from compradores.models import Comprador
from veiculos.models import Veiculo
from vendas.models import Venda
from vendas.services import (
    cancelar_venda,
    concluir_venda,
    confirmar_pagamento,
    gerar_codigo_pagamento,
    reservar_veiculo,
    selecionar_veiculo,
)

from .forms import (
    CancelarVendaForm,
    CompradorForm,
    ConfirmarPagamentoForm,
    IniciarVendaForm,
    VeiculoForm,
)


def dashboard(request):
    context = {
        "total_veiculos": Veiculo.objects.count(),
        "veiculos_disponiveis": Veiculo.objects.filter(
            status=Veiculo.StatusVeiculo.DISPONIVEL
        ).count(),
        "veiculos_reservados": Veiculo.objects.filter(
            status=Veiculo.StatusVeiculo.RESERVADO
        ).count(),
        "veiculos_vendidos": Veiculo.objects.filter(status=Veiculo.StatusVeiculo.VENDIDO).count(),
        "total_compradores": Comprador.objects.filter(ativo=True).count(),
        "vendas_em_andamento": Venda.objects.exclude(
            status__in=[Venda.StatusVenda.CONCLUIDO, Venda.StatusVenda.CANCELADO]
        ).count(),
        "vendas_concluidas": Venda.objects.filter(status=Venda.StatusVenda.CONCLUIDO).count(),
        "faturamento_total": Venda.objects.filter(status=Venda.StatusVenda.CONCLUIDO).aggregate(
            total=Sum("preco_venda")
        )["total"]
        or 0,
        "ultimas_vendas": Venda.objects.select_related("veiculo", "comprador").order_by(
            "-criado_em"
        )[:5],
        "veiculos_recentes": Veiculo.objects.filter(
            status=Veiculo.StatusVeiculo.DISPONIVEL
        ).order_by("-criado_em")[:5],
    }
    return render(request, "dashboard.html", context)


def devsecops_dashboard(request):
    branch = "feature/fase-5"
    encoded_branch = branch.replace("/", "%2F")
    repo_url = "https://github.com/MelloLipe/tech-fase-5-service-revenda-automotores"
    workflow_url = f"{repo_url}/actions/workflows/ci.yml"
    workflow_runs_url = f"{workflow_url}?query=branch%3A{encoded_branch}"
    badge_url = f"{workflow_url}/badge.svg?branch={encoded_branch}"
    context = {
        "repo_url": repo_url,
        "workflow_url": workflow_url,
        "workflow_runs_url": workflow_runs_url,
        "badge_url": badge_url,
        "branch": branch,
        "quality_gates": [
            {
                "name": "Code Quality",
                "icon": "bi-braces",
                "status": "Gate obrigatorio",
                "description": "Ruff valida lint e Black valida formatacao padronizada.",
                "command": "ruff check ... / black --check ...",
                "variant": "primary",
            },
            {
                "name": "Testes + Coverage",
                "icon": "bi-check2-square",
                "status": "Minimo 70%",
                "description": "Testes Django executados com coverage report e artifact XML.",
                "command": "coverage report --fail-under=70",
                "variant": "success",
            },
            {
                "name": "SAST",
                "icon": "bi-shield-lock",
                "status": "Bandit",
                "description": "Analise estatica de seguranca no codigo Python da aplicacao.",
                "command": "bandit -r compradores veiculos vendas revenda_veiculos",
                "variant": "danger",
            },
            {
                "name": "SCA",
                "icon": "bi-box-seam",
                "status": "pip-audit + SBOM",
                "description": "Varredura de CVEs e geracao de SBOM CycloneDX.",
                "command": "pip-audit --format=json / cyclonedx-json",
                "variant": "warning",
            },
            {
                "name": "Deploy Readiness",
                "icon": "bi-rocket-takeoff",
                "status": "Render simulation",
                "description": "Check de producao, migrations, collectstatic e migrate.",
                "command": "check --deploy / collectstatic / migrate",
                "variant": "info",
            },
        ],
        "validated_results": [
            ("Testes automatizados", "9 testes Django executados com sucesso"),
            ("Cobertura", "73% de coverage total, acima do gate minimo de 70%"),
            ("SAST", "Bandit executado sem bloquear a pipeline"),
            ("SCA", "pip-audit sem vulnerabilidades conhecidas localmente"),
            ("SBOM", "Inventario CycloneDX gerado como evidencia de supply chain"),
            ("Deploy readiness", "check --deploy validado com variaveis de producao"),
        ],
        "artifacts": [
            {
                "name": "coverage-xml",
                "description": "Relatorio XML de cobertura dos testes automatizados.",
                "url": workflow_runs_url,
            },
            {
                "name": "bandit-sast-report",
                "description": "Resultado JSON da analise estatica de seguranca.",
                "url": workflow_runs_url,
            },
            {
                "name": "pip-audit-sca-report",
                "description": "Relatorio JSON de vulnerabilidades em dependencias.",
                "url": workflow_runs_url,
            },
            {
                "name": "sbom-cyclonedx-json",
                "description": "Inventario SBOM em formato CycloneDX JSON.",
                "url": workflow_runs_url,
            },
        ],
        "summaries": [
            "Resumo consolidado no GitHub Actions Summary",
            "Tabela de status por stage",
            "Metricas de coverage, SAST, SCA e SBOM",
        ],
    }
    return render(request, "devsecops/dashboard.html", context)


def veiculos_list(request):
    status_filter = request.GET.get("status", "")
    veiculos = Veiculo.objects.all().order_by("preco")
    if status_filter:
        veiculos = veiculos.filter(status=status_filter)
    return render(
        request,
        "veiculos/list.html",
        {
            "veiculos": veiculos,
            "status_filter": status_filter,
        },
    )


def veiculo_create(request):
    form = VeiculoForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Veiculo cadastrado com sucesso.")
        return redirect("veiculos_list")
    return render(
        request,
        "form.html",
        {
            "title": "Cadastrar Veiculo",
            "form": form,
            "back_url": "veiculos_list",
            "submit_label": "Salvar veiculo",
        },
    )


def veiculo_edit(request, pk):
    veiculo = get_object_or_404(Veiculo, pk=pk)
    form = VeiculoForm(request.POST or None, instance=veiculo)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Veiculo atualizado com sucesso.")
        return redirect("veiculo_detail", pk=veiculo.pk)
    return render(
        request,
        "form.html",
        {
            "title": "Editar Veiculo",
            "form": form,
            "back_url": "veiculo_detail",
            "back_kwargs": {"pk": veiculo.pk},
            "submit_label": "Salvar alteracoes",
        },
    )


def veiculo_detail(request, pk):
    veiculo = get_object_or_404(Veiculo, pk=pk)
    vendas = veiculo.vendas.select_related("comprador").order_by("-criado_em")
    return render(
        request,
        "veiculos/detail.html",
        {
            "veiculo": veiculo,
            "vendas": vendas,
        },
    )


def compradores_list(request):
    compradores = Comprador.objects.filter(ativo=True).order_by("nome")
    return render(
        request,
        "compradores/list.html",
        {
            "compradores": compradores,
        },
    )


def comprador_create(request):
    form = CompradorForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Comprador cadastrado com sucesso.")
        return redirect("compradores_list")
    return render(
        request,
        "form.html",
        {
            "title": "Cadastrar Comprador",
            "form": form,
            "back_url": "compradores_list",
            "submit_label": "Salvar comprador",
        },
    )


def vendas_list(request):
    status_filter = request.GET.get("status", "")
    vendas = Venda.objects.select_related("veiculo", "comprador").order_by("-criado_em")
    if status_filter:
        vendas = vendas.filter(status=status_filter)
    return render(
        request,
        "vendas/list.html",
        {
            "vendas": vendas,
            "status_filter": status_filter,
            "status_choices": Venda.StatusVenda.choices,
        },
    )


def venda_create(request):
    form = IniciarVendaForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        try:
            venda = selecionar_veiculo(
                form.cleaned_data["veiculo"].id,
                form.cleaned_data["comprador"].id,
            )
        except ValidationError as exc:
            messages.error(request, _format_validation_error(exc))
        else:
            messages.success(request, "Venda iniciada. Proxima etapa: reservar veiculo.")
            return redirect("venda_detail", pk=venda.pk)
    return render(
        request,
        "form.html",
        {
            "title": "Iniciar Venda",
            "form": form,
            "back_url": "vendas_list",
            "submit_label": "Iniciar venda",
        },
    )


def venda_detail(request, pk):
    venda = get_object_or_404(
        Venda.objects.select_related("veiculo", "comprador").prefetch_related("historico"),
        pk=pk,
    )
    return render(
        request,
        "vendas/detail.html",
        {
            "venda": venda,
            "confirmar_pagamento_form": ConfirmarPagamentoForm(
                codigo_inicial=venda.codigo_pagamento or "",
            ),
            "cancelar_venda_form": CancelarVendaForm(),
        },
    )


def venda_action(request, pk, action):
    if request.method != "POST":
        return redirect("venda_detail", pk=pk)

    try:
        if action == "reservar":
            reservar_veiculo(pk)
            messages.success(request, "Veiculo reservado por 30 minutos.")
        elif action == "gerar-pagamento":
            venda = gerar_codigo_pagamento(pk)
            messages.success(
                request,
                f"Codigo de pagamento gerado: {venda.codigo_pagamento}",
            )
        elif action == "confirmar-pagamento":
            form = ConfirmarPagamentoForm(request.POST)
            if form.is_valid():
                confirmar_pagamento(pk, form.cleaned_data["codigo_pagamento"])
                messages.success(request, "Pagamento confirmado com sucesso.")
            else:
                messages.error(request, "Informe o codigo de pagamento.")
        elif action == "concluir":
            concluir_venda(pk)
            messages.success(request, "Venda concluida. Veiculo marcado como vendido.")
        elif action == "cancelar":
            form = CancelarVendaForm(request.POST)
            if form.is_valid():
                cancelar_venda(pk, form.cleaned_data["motivo"])
                messages.success(request, "Venda cancelada e compensada.")
            else:
                messages.error(request, "Informe um motivo valido para cancelamento.")
        else:
            messages.error(request, "Acao desconhecida.")
    except (ValidationError, Venda.DoesNotExist, Veiculo.DoesNotExist) as exc:
        messages.error(request, _format_validation_error(exc))

    return redirect("venda_detail", pk=pk)


def _format_validation_error(exc):
    detail = getattr(exc, "detail", exc)
    if isinstance(detail, dict):
        parts = []
        for field, errors in detail.items():
            if isinstance(errors, (list, tuple)):
                parts.append(f'{field}: {", ".join(str(error) for error in errors)}')
            else:
                parts.append(f"{field}: {errors}")
        return " ".join(parts)
    return str(detail)
