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

        response = '+CSQ: 99,99'

        signal_quality = SignalQuality.from_quality_query(response)

        assert signal_quality.strength == -999
        assert not signal_quality.is_rscp
        assert signal_quality.bit_error_rate == 99

        response = '+CSQ: 199,99'

        signal_quality = SignalQuality.from_quality_query(response)

        assert signal_quality.strength == -999
        assert signal_quality.is_rscp
        assert signal_quality.bit_error_rate == 99

    def test_from_quality_query_with_exception(self):
        response_1 = '+CSQ: 199,100'
        response_2 = '+CSQ: 255,0'
        response_3 = '+CSQ: 255,100'

        with pytest.raises(ValueError):
            signal_quality = SignalQuality.from_quality_query(response_1)

        with pytest.raises(ValueError):
            signal_quality = SignalQuality.from_quality_query(response_2)

        with pytest.raises(ValueError):
            signal_quality = SignalQuality.from_quality_query(response_3)

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

        signal_quality_7 = SignalQuality(
            strength=-51,
            is_rscp=True,
            bit_error_rate=4,
        )

        # Compare BER if strength is the same
        assert signal_quality_6 < signal_quality_7

    def test_ber_max(self):
        signal_quality = SignalQuality(
            strength=-51,
            is_rscp=False,
            bit_error_rate=0,
        )

        assert signal_quality.ber_max == 0.0001

        signal_quality = SignalQuality(
            strength=-51,
            is_rscp=False,
            bit_error_rate=1,
        )

        assert signal_quality.ber_max == 0.001

        signal_quality = SignalQuality(
            strength=-51,
            is_rscp=False,
            bit_error_rate=2,
        )

        assert signal_quality.ber_max == 0.005

        signal_quality = SignalQuality(
            strength=-51,
            is_rscp=False,
            bit_error_rate=3,
        )

        assert signal_quality.ber_max == 0.01

        signal_quality = SignalQuality(
            strength=-51,
            is_rscp=False,
            bit_error_rate=4,
        )

        assert signal_quality.ber_max == 0.02

        signal_quality = SignalQuality(
            strength=-51,
            is_rscp=False,
            bit_error_rate=5,
        )

        assert signal_quality.ber_max == 0.04

        signal_quality = SignalQuality(
            strength=-51,
            is_rscp=False,
            bit_error_rate=6,
        )

        assert signal_quality.ber_max == 0.08

        signal_quality = SignalQuality(
            strength=-51,
            is_rscp=False,
            bit_error_rate=7,
        )

        assert signal_quality.ber_max == 1
