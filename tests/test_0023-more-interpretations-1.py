# BSD 3-Clause License; see https://github.com/scikit-hep/uproot4/blob/master/LICENSE

from __future__ import absolute_import

import sys
import json

import numpy
import pytest
import skhep_testdata

import uproot4
import uproot4.interpretation.library
import uproot4.interpretation.jagged
import uproot4.interpretation.numerical


def test_formula_with_dot():
    with uproot4.open(
        skhep_testdata.data_path("uproot-small-evnt-tree-fullsplit.root")
    )["tree"] as tree:
        assert tree.arrays("P3.Py - 50", library="np")["P3.Py - 50"].tolist() == list(
            range(-50, 50)
        )


def test_formula_with_slash():
    with uproot4.open(
        skhep_testdata.data_path("uproot-small-evnt-tree-fullsplit.root")
    )["tree"] as tree:
        assert tree.arrays("get('evt/P3/P3.Py') - 50", library="np")[
            "get('evt/P3/P3.Py') - 50"
        ].tolist() == list(range(-50, 50))


def test_formula_with_missing():
    with uproot4.open(
        skhep_testdata.data_path("uproot-small-evnt-tree-fullsplit.root")
    )["tree"] as tree:
        with pytest.raises(KeyError):
            tree.arrays("wonky", library="np")


def test_strings1():
    with uproot4.open(
        skhep_testdata.data_path("uproot-sample-6.20.04-uncompressed.root")
    )["sample/str"] as branch:
        result = branch.array(library="np")
        assert result.tolist() == ["hey-{0}".format(i) for i in range(30)]


def test_strings4():
    with uproot4.open(
        skhep_testdata.data_path("uproot-small-evnt-tree-fullsplit.root")
    )["tree/StlVecStr"] as branch:
        result = branch.array(library="np")
        assert [result.tolist() for x in result] == [
            ["vec-{0:03d}".format(i)] * (i % 10) for i in range(100)
        ]


@pytest.mark.skip(reason="FIXME: implement unsplit object")
def test_strings4():
    with uproot4.open(skhep_testdata.data_path("uproot-small-evnt-tree-nosplit.root"))[
        "tree/evt"
    ] as branch:
        result = branch.array(library="np")
        assert [result.member("StlVecStr").tolist() for x in result] == [
            ["vec-{0:03d}".format(i)] * (i % 10) for i in range(100)
        ]


def test_strings4():
    with uproot4.open(skhep_testdata.data_path("uproot-vectorVectorDouble.root"))[
        "t/x"
    ] as branch:
        result = branch.array(library="np")
        assert [x.tolist() for x in result] == [
            [],
            [[], []],
            [[10.0], [], [10.0, 20.0]],
            [[20.0, -21.0, -22.0]],
            [[200.0], [-201.0], [202.0]],
        ]


def test_double32():
    with uproot4.open(skhep_testdata.data_path("uproot-demo-double32.root"))["T"] as t:
        fD64 = t["fD64"].array(library="np")
        fF32 = t["fF32"].array(library="np")
        fI32 = t["fI32"].array(library="np")
        fI30 = t["fI30"].array(library="np")
        fI28 = t["fI28"].array(library="np")
        ratio_fF32 = fF32 / fD64
        ratio_fI32 = fI32 / fD64
        ratio_fI30 = fI30 / fD64
        ratio_fI28 = fI28 / fD64
        assert ratio_fF32.min() > 0.9999 and ratio_fF32.max() < 1.0001
        assert ratio_fI32.min() > 0.9999 and ratio_fI32.max() < 1.0001
        assert ratio_fI30.min() > 0.9999 and ratio_fI30.max() < 1.0001
        assert ratio_fI28.min() > 0.9999 and ratio_fI28.max() < 1.0001


def test_double32_2():
    with uproot4.open(skhep_testdata.data_path("uproot-issue187.root"))["fTreeV0"] as t:
        assert numpy.all(t["fMultiplicity"].array(library="np") == -1)
        assert t["V0s.fEtaPos"].array(library="np")[-3].tolist() == [
            -0.390625,
            0.046875,
        ]


def test_double32_3():
    with uproot4.open(skhep_testdata.data_path("uproot-issue232.root"))["fTreeV0"] as t:
        assert t["V0Hyper.fNsigmaHe3Pos"].array(library="np")[-1].tolist() == [
            19.38658905029297,
            999.0,
        ]
        assert t["V0Hyper.fDcaPos2PrimaryVertex"].array(library="np")[-1].tolist() == [
            0.256,
            0.256,
        ]


def test_double32_float16():
    with uproot4.open(skhep_testdata.data_path("uproot-double32-float16.root"))[
        "tree"
    ] as t:
        assert repr(t["double32_32"].interpretation) == "AsDouble32(-2.71, 10.0, 32)"
        assert repr(t["double32_30"].interpretation) == "AsDouble32(-2.71, 10.0, 30)"
        assert repr(t["double32_20"].interpretation) == "AsDouble32(-2.71, 10.0, 20)"
        assert repr(t["double32_10"].interpretation) == "AsDouble32(-2.71, 10.0, 10)"
        assert repr(t["double32_5"].interpretation) == "AsDouble32(-2.71, 10.0, 5)"
        assert repr(t["double32_3"].interpretation) == "AsDouble32(-2.71, 10.0, 3)"
        assert repr(t["float16_16"].interpretation) == "AsFloat16(-2.71, 10.0, 16)"
        assert repr(t["float16_10"].interpretation) == "AsFloat16(-2.71, 10.0, 10)"
        assert repr(t["float16_5"].interpretation) == "AsFloat16(-2.71, 10.0, 5)"
        assert repr(t["float16_3"].interpretation) == "AsFloat16(-2.71, 10.0, 3)"
        assert (
            repr(t["array_30"].interpretation)
            == "AsDouble32(-2.71, 10.0, 30, to_dims=(3,))"
        )
        assert (
            repr(t["array_10"].interpretation)
            == "AsFloat16(-2.71, 10.0, 10, to_dims=(3,))"
        )

        assert t["double32_32"].array(library="np").tolist() == [
            -1.9999999994342215,
            -1.4999999998277052,
            -1.0000000002211891,
            -0.50000000061467276,
            -0.10000000329688152,
            -1.0081566692576871e-09,
            0.10000000128056863,
            0.49999999859835986,
            0.99999999820487595,
            2.0000000003771863,
            2.9999999995902185,
            3.9999999988032506,
            4.9999999980162837,
            5.9999999972293159,
            6.9999999964423489,
            7.9999999986146593,
            8.9999999978276897,
        ]

        assert t["double32_30"].array(library="np").tolist() == [
            -2.0000000023934987,
            -1.5000000057462601,
            -0.99999999726191158,
            -0.50000000061467276,
            -0.10000000329688152,
            -3.9674339369355494e-09,
            0.10000000719912361,
            0.50000000451691484,
            1.0000000011641537,
            1.9999999944586309,
            2.9999999995902185,
            4.0000000047218061,
            4.9999999980162837,
            6.0000000031478704,
            6.9999999964423489,
            8.0000000015739374,
            8.9999999948684142,
        ]

        assert t["double32_20"].array(library="np").tolist() == [
            -2.0000006771087646,
            -1.5000011539459228,
            -1.0000016307830808,
            -0.50000210762023922,
            -0.10000248908996578,
            -2.5844573974254104e-06,
            0.099997320175170934,
            0.49999693870544437,
            0.99999646186828661,
            1.9999955081939698,
            2.9999945545196534,
            4.0000057220458993,
            5.0000047683715829,
            6.0000038146972665,
            7.0000028610229501,
            8.0000019073486328,
            9.0000009536743164,
        ]

        assert t["double32_10"].array(library="np").tolist() == [
            -2.0025097656249997,
            -1.5060253906249998,
            -0.99712890624999995,
            -0.50064453124999986,
            -0.10345703124999961,
            -0.0041601562499997691,
            0.095136718750000071,
            0.50473632812500036,
            1.0012207031250004,
            1.9941894531250002,
            2.9995703125000004,
            4.0049511718750006,
            4.9979199218750008,
            6.0033007812500001,
            6.9962695312500012,
            8.0016503906250023,
            8.9946191406250016,
        ]

        assert t["double32_5"].array(library="np").tolist() == [
            -1.9156249999999999,
            -1.5184374999999999,
            -1.1212499999999999,
            -0.3268749999999998,
            0.0703125,
            0.0703125,
            0.0703125,
            0.46750000000000025,
            0.8646875000000005,
            2.0562500000000004,
            2.850625,
            4.0421875000000007,
            4.8365625000000003,
            6.0281250000000002,
            6.8225000000000007,
            8.0140625000000014,
            8.8084375000000001,
        ]

        assert t["double32_3"].array(library="np").tolist() == [
            -2.71,
            -1.1212499999999999,
            -1.1212499999999999,
            -1.1212499999999999,
            0.46750000000000025,
            0.46750000000000025,
            0.46750000000000025,
            0.46750000000000025,
            0.46750000000000025,
            2.0562500000000004,
            3.6450000000000005,
            3.6450000000000005,
            5.233750000000001,
            5.233750000000001,
            6.822500000000001,
            8.411249999999999,
            8.411249999999999,
        ]

        assert t["float16_16"].array(library="np").tolist() == [
            -1.9999885559082031,
            -1.5000133514404297,
            -1.0000380277633667,
            -0.50006270408630371,
            -0.099966049194335938,
            -8.7499618530273438e-05,
            0.099985122680664062,
            0.50008177757263184,
            1.0000569820404053,
            2.0000076293945312,
            2.9999580383300781,
            3.9999089241027832,
            5.0000534057617188,
            6.0000038146972656,
            6.9999542236328125,
            7.9999046325683594,
            9.0000495910644531,
        ]

        assert t["float16_10"].array(library="np").tolist() == [
            -2.0025098323822021,
            -1.5060254335403442,
            -0.99712896347045898,
            -0.50064444541931152,
            -0.10345697402954102,
            -0.0041601657867431641,
            0.095136642456054688,
            0.50473618507385254,
            1.001220703125,
            1.9941892623901367,
            2.999570369720459,
            4.004951000213623,
            4.997920036315918,
            6.003300666809082,
            6.9962692260742188,
            8.0016508102416992,
            8.9946193695068359,
        ]

        assert t["float16_5"].array(library="np").tolist() == [
            -1.9156250953674316,
            -1.5184375047683716,
            -1.1212500333786011,
            -0.32687497138977051,
            0.0703125,
            0.0703125,
            0.0703125,
            0.46749997138977051,
            0.86468744277954102,
            2.0562500953674316,
            2.8506250381469727,
            4.0421876907348633,
            4.8365626335144043,
            6.0281248092651367,
            6.8225002288818359,
            8.0140628814697266,
            8.8084373474121094,
        ]

        assert t["float16_3"].array(library="np").tolist() == [
            -2.7100000381469727,
            -1.1212500333786011,
            -1.1212500333786011,
            -1.1212500333786011,
            0.46749997138977051,
            0.46749997138977051,
            0.46749997138977051,
            0.46749997138977051,
            0.46749997138977051,
            2.0562500953674316,
            3.6449999809265137,
            3.6449999809265137,
            5.2337498664855957,
            5.2337498664855957,
            6.8225002288818359,
            8.411250114440918,
            8.411250114440918,
        ]

        assert t["array_30"].array(library="np").tolist() == [
            [-2.0000000023934987, -2.0000000023934987, -2.0000000023934987],
            [-1.5000000057462601, -1.5000000057462601, -1.5000000057462601],
            [-0.99999999726191158, -0.99999999726191158, -0.99999999726191158],
            [-0.50000000061467276, -0.50000000061467276, -0.50000000061467276],
            [-0.10000000329688152, -0.10000000329688152, -0.10000000329688152],
            [-3.9674339369355494e-09, -3.9674339369355494e-09, -3.9674339369355494e-09],
            [0.10000000719912361, 0.10000000719912361, 0.10000000719912361],
            [0.50000000451691484, 0.50000000451691484, 0.50000000451691484],
            [1.0000000011641537, 1.0000000011641537, 1.0000000011641537],
            [1.9999999944586309, 1.9999999944586309, 1.9999999944586309],
            [2.9999999995902185, 2.9999999995902185, 2.9999999995902185],
            [4.0000000047218061, 4.0000000047218061, 4.0000000047218061],
            [4.9999999980162837, 4.9999999980162837, 4.9999999980162837],
            [6.0000000031478704, 6.0000000031478704, 6.0000000031478704],
            [6.9999999964423489, 6.9999999964423489, 6.9999999964423489],
            [8.0000000015739374, 8.0000000015739374, 8.0000000015739374],
            [8.9999999948684142, 8.9999999948684142, 8.9999999948684142],
        ]

        assert t["array_10"].array(library="np").tolist() == [
            [-2.0025098323822021, -2.0025098323822021, -2.0025098323822021],
            [-1.5060254335403442, -1.5060254335403442, -1.5060254335403442],
            [-0.99712896347045898, -0.99712896347045898, -0.99712896347045898],
            [-0.50064444541931152, -0.50064444541931152, -0.50064444541931152],
            [-0.10345697402954102, -0.10345697402954102, -0.10345697402954102],
            [-0.0041601657867431641, -0.0041601657867431641, -0.0041601657867431641],
            [0.095136642456054688, 0.095136642456054688, 0.095136642456054688],
            [0.50473618507385254, 0.50473618507385254, 0.50473618507385254],
            [1.001220703125, 1.001220703125, 1.001220703125],
            [1.9941892623901367, 1.9941892623901367, 1.9941892623901367],
            [2.999570369720459, 2.999570369720459, 2.999570369720459],
            [4.004951000213623, 4.004951000213623, 4.004951000213623],
            [4.997920036315918, 4.997920036315918, 4.997920036315918],
            [6.003300666809082, 6.003300666809082, 6.003300666809082],
            [6.9962692260742188, 6.9962692260742188, 6.9962692260742188],
            [8.0016508102416992, 8.0016508102416992, 8.0016508102416992],
            [8.9946193695068359, 8.9946193695068359, 8.9946193695068359],
        ]
