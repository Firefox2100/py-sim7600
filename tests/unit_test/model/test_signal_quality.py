import pytest

from py_sim7600.model.signal_quality import SignalQuality


class TestSignalQuality:
    def test_init(self):
        signal_quality = SignalQuality(
            strength=-51,
            is_rscp=False,
            bit_error_rate=7,
        )

        assert signal_quality.strength == -51
        assert not signal_quality.is_rscp
        assert signal_quality.bit_error_rate == 7

    def test_from_quality_query(self):
        response = '+CSQ: 31,7'

        signal_quality = SignalQuality.from_quality_query(response)

        assert signal_quality.strength == -51
        assert not signal_quality.is_rscp
        assert signal_quality.bit_error_rate == 7

    def test_rich_comparison(self):
        signal_quality_1 = SignalQuality(
            strength=-51,
            is_rscp=False,
            bit_error_rate=6,
        )

        signal_quality_2 = SignalQuality(
            strength=-51,
            is_rscp=False,
            bit_error_rate=6,
        )

        # Same data
        assert signal_quality_1 == signal_quality_2

        signal_quality_3 = SignalQuality(
            strength=-51,
            is_rscp=False,
            bit_error_rate=99,
        )

        signal_quality_4 = SignalQuality(
            strength=-80,
            is_rscp=False,
            bit_error_rate=6,
        )

        # Max BER should always be worse
        assert signal_quality_1 > signal_quality_3
        assert signal_quality_4 > signal_quality_3
        assert signal_quality_4 < signal_quality_1

        signal_quality_5 = SignalQuality(
            strength=-999,
            is_rscp=False,
            bit_error_rate=4,
        )

        # Unknown strength should always be worse
        assert signal_quality_1 > signal_quality_5

        signal_quality_6 = SignalQuality(
            strength=-51,
            is_rscp=True,
            bit_error_rate=6,
        )

        # RSSI and RSCP are incomparable
        with pytest.raises(TypeError):
            assert signal_quality_1 > signal_quality_6
