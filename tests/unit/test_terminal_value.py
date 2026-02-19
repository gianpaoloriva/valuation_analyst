"""Test per il modulo del valore terminale."""
import pytest
from valuation_analyst.tools.terminal_value import (
    terminal_value_gordon, terminal_value_exit_multiple,
    terminal_value_con_reinvestimento, verifica_terminal_value,
)


class TestTerminalValueGordon:
    def test_gordon_base(self):
        """TV = 100*(1+0.03)/(0.10-0.03) = 1471.43."""
        tv = terminal_value_gordon(
            cash_flow_ultimo=100, tasso_crescita_stabile=0.03, tasso_sconto=0.10,
        )
        assert tv == pytest.approx(1471.43, abs=1)

    def test_gordon_errore_crescita_maggiore_sconto(self):
        """Crescita >= sconto deve generare errore."""
        with pytest.raises(ValueError):
            terminal_value_gordon(cash_flow_ultimo=100, tasso_crescita_stabile=0.12, tasso_sconto=0.10)


class TestTerminalValueExitMultiple:
    def test_exit_multiple_base(self):
        """TV = EBITDA * multiplo = 50 * 10 = 500."""
        tv = terminal_value_exit_multiple(metrica_ultimo_anno=50, multiplo_uscita=10)
        assert tv == pytest.approx(500.0)

    def test_exit_multiple_errore_negativo(self):
        """Multiplo negativo deve generare errore."""
        with pytest.raises(ValueError):
            terminal_value_exit_multiple(metrica_ultimo_anno=50, multiplo_uscita=-5)


class TestTerminalValueConReinvestimento:
    def test_reinvestimento_base(self):
        """TV con reinvestimento esplicito produce un valore positivo."""
        result = terminal_value_con_reinvestimento(
            ebit_after_tax_ultimo=100, tasso_crescita_stabile=0.025,
            roic_stabile=0.12, tasso_sconto=0.09,
        )
        assert result["tv"] > 0
        assert 0 < result["reinvestment_rate"] < 1


class TestVerificaTerminalValue:
    def test_accettabile(self):
        """Un TV pari al 60% del totale e' accettabile (soglia 80%)."""
        result = verifica_terminal_value(tv=60, valore_totale=100)
        assert result["accettabile"] is True

    def test_non_accettabile(self):
        """Un TV pari al 90% del totale non e' accettabile."""
        result = verifica_terminal_value(tv=90, valore_totale=100)
        assert result["accettabile"] is False
