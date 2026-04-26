import hashlib
import re

from django import forms

from compradores.models import Comprador
from veiculos.models import Veiculo


class BootstrapFormMixin:
    def _apply_bootstrap(self):
        for field in self.fields.values():
            field.widget.attrs.setdefault("class", "form-control")


class VeiculoForm(BootstrapFormMixin, forms.ModelForm):
    class Meta:
        model = Veiculo
        fields = [
            "marca",
            "modelo",
            "ano",
            "cor",
            "preco",
            "placa",
            "chassi",
            "quilometragem",
            "descricao",
        ]
        widgets = {
            "descricao": forms.Textarea(attrs={"rows": 3}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._apply_bootstrap()


class CompradorForm(BootstrapFormMixin, forms.ModelForm):
    cpf = forms.CharField(max_length=14, label="CPF")
    rg = forms.CharField(max_length=20, label="RG")

    class Meta:
        model = Comprador
        fields = [
            "nome",
            "email",
            "telefone",
            "cpf",
            "rg",
            "endereco",
            "cidade",
            "estado",
            "cep",
            "data_nascimento",
        ]
        widgets = {
            "endereco": forms.Textarea(attrs={"rows": 2}),
            "data_nascimento": forms.DateInput(attrs={"type": "date"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._apply_bootstrap()
        self.fields["estado"].widget.attrs["maxlength"] = 2

    def clean_cpf(self):
        cpf = re.sub(r"\D", "", self.cleaned_data["cpf"])
        if len(cpf) != 11:
            raise forms.ValidationError("CPF deve ter 11 digitos.")
        if cpf == cpf[0] * 11:
            raise forms.ValidationError("CPF invalido.")
        for i in range(9, 11):
            total = sum(int(cpf[num]) * ((i + 1) - num) for num in range(0, i))
            digit = ((total * 10) % 11) % 10
            if digit != int(cpf[i]):
                raise forms.ValidationError("CPF invalido.")
        return cpf

    def clean_rg(self):
        rg = re.sub(r"\D", "", self.cleaned_data["rg"])
        if len(rg) < 5:
            raise forms.ValidationError("RG deve ter pelo menos 5 digitos.")
        return rg

    def save(self, commit=True):
        comprador = super().save(commit=False)
        cpf = self.cleaned_data["cpf"]
        rg = self.cleaned_data["rg"]
        comprador.cpf_hash = hashlib.sha256(cpf.encode()).hexdigest()
        comprador.cpf_masked = f"***.***.*{cpf[7:9]}-{cpf[9:11]}"
        comprador.rg_hash = hashlib.sha256(rg.encode()).hexdigest()
        if commit:
            comprador.save()
        return comprador


class IniciarVendaForm(BootstrapFormMixin, forms.Form):
    veiculo = forms.ModelChoiceField(
        queryset=Veiculo.objects.none(),
        label="Veiculo disponivel",
    )
    comprador = forms.ModelChoiceField(
        queryset=Comprador.objects.none(),
        label="Comprador",
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["veiculo"].queryset = Veiculo.objects.filter(
            status=Veiculo.StatusVeiculo.DISPONIVEL
        ).order_by("preco")
        self.fields["comprador"].queryset = Comprador.objects.filter(ativo=True).order_by("nome")
        self._apply_bootstrap()


class ConfirmarPagamentoForm(BootstrapFormMixin, forms.Form):
    codigo_pagamento = forms.CharField(max_length=36, label="Codigo de pagamento")

    def __init__(self, *args, **kwargs):
        codigo_inicial = kwargs.pop("codigo_inicial", "")
        super().__init__(*args, **kwargs)
        self.fields["codigo_pagamento"].initial = codigo_inicial
        self._apply_bootstrap()


class CancelarVendaForm(BootstrapFormMixin, forms.Form):
    motivo = forms.CharField(
        required=False,
        initial="Cliente desistiu da compra.",
        widget=forms.Textarea(attrs={"rows": 2}),
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._apply_bootstrap()
