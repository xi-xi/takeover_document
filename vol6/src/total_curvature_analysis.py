"""全曲率を用いた軌道の解析を行います

Command line::

Usage:
    total_curvature_analysis.py <input> [<output>]
    total_curvature_analysis.py -h
Options:
    -h, --help  Show this help
"""
import os
import sys
import json
import numpy as np
import scipy.optimize as so
import scipy.integrate as si
from docopt import docopt
import bspline.base as bspline
import projected_bspline as pb
import total_curvature
import viewport.viewport as vp
from io_util import io_arg_file


UNDER_TOTAL_CURVATURE = np.deg2rad(50.0)
"""float: 取り出す全曲率の下限値
"""

BEST_TOTAL_CURVATURE = np.deg2rad(75.0)
"""float: 全曲率がこの値になるように取り出されます．
"""


class SecondDimensionalize:
    """３次元軌道を2次元上に落とします

    3次元軌道のうち，0,1要素を取り出すことで2次元軌道の関数にします．
    何か特別な何かをすることで2次元化するわけではありません．

    Args:
        func (function): 3次元軌道の関数

    Attributes:
        func (function): 3次元軌道の関数
        mat (matrix): 3次元軌道の0, 1要素を取り出して2次元に落とす行列
    """

    def __init__(self, func):
        self.mat = np.array(
            [[1.0, 0.0, 0.0],
             [0.0, 1.0, 0.0]]
        )
        self.func = func

    def __call__(self, t):
        return np.dot(self.mat, self.func(t))

    def diff(self):
        """微分値を返します

        微分関数は3次元軌道の微分値を2次元に落としたものです．

        Returns:
            SecondDimensionalize: 2次元軌道
        """
        return(
            SecondDimensionalize(self.func.diff())
        )


def get_dances():
    """舞踊名のリストを返します

    Returns:
        list: 舞踊名のリスト
    """
    return [
        "hula",
        "india",
        "jawa",
        "myan",
        "nichibu"
    ]


def build_viewport_axis_str(dancename):
    """舞踊名から投影平面を返します.

    Args:
        dancename (str): ファイル名

    Returns:
        str: 舞踊名
            "hula", "india", "jawa", "myan", "nichibu"

    """
    if dancename == "hula":
        return "-zy"
    elif dancename == "india":
        return "-zy"
    elif dancename == "jawa":
        return "xy"
    elif dancename == "myan":
        return "xy"
    elif dancename == "nichibu":
        return "xy"
    else:
        return None


def get_dancename(filename):
    """ファイル名から舞踊名を返します

    Args:
        filename (str): ファイル名

    Returns:
        str: 舞踊名
    """
    dances = get_dances()
    for d in dances:
        if d in filename:
            return d


def get_viewport_axis(filename):
    """視点方向の行列を返します

    Args:
        filename (str): ファイル名

    Returns:
        matrix: 視点方向を表す行列
    """
    dancename = get_dancename(filename.lower())
    axis_str = build_viewport_axis_str(dancename)
    axis_matrix = vp.get_plane_matrix(axis_str)
    return np.r_[
        axis_matrix,
        [np.cross(axis_matrix[0], axis_matrix[1])]
    ]


def load_json(filename):
    with open(filename) as f:
        return json.load(f)


def calc_inflection_points(pbsp, trange=None, n_splits=None, ts=None):
    cf = total_curvature.Curvature(pbsp)
    if ts is None:
        if trange is None:
            trange = (0.0, 1.0)
        if n_splits is None:
            n_splits = 100000
        ts = np.linspace(trange[0], trange[1], n_splits)
    dsts = []
    for a, b in zip(ts, ts[1:]):
        try:
            dsts.append(so.brentq(cf, a, b))
        except ValueError as e:
            pass
    return dsts


def search_trim_point(total_curvature_func, ts):
    """ 軌道中から、切り取るべきポイントを探します

    Args:
        total_curvature_func (function): 軌道の全曲率がどの程度理想に近いかを示す値．
                                         この値が0になる場所を探索します
        ts (list[float]): 探索範囲
    """
    return so.brentq(total_curvature_func, ts[0], ts[1])


def calc_length(pbsp, trange):
    diff = pbsp.diff()
    length_func = (lambda t: np.sum(diff(t) * diff(t)) ** 0.5)
    length, err = si.quad(length_func, trange[0], trange[1], limit=10000)
    return length


def set_length_field(func, arc_dict):
    arc_dict["original_length"] = calc_length(func, arc_dict["original_ts"])
    arc_dict["trim_length"] = calc_length(func, arc_dict["trim_ts"])
    return arc_dict


def analysis(pbsp):
    dst = {
        "desc": ("total_curvature_analysisによって作られたデータ\n" +
                 "変曲点3つを一つのS字とし，ホガースの示した美の線に近づくように一部を取り出すような処理をします．"),
        "curves": []
    }
    inf_points = calc_inflection_points(pbsp)
    dst["inflection_points"] = inf_points
    if 0.0 not in inf_points:
        inf_points.insert(0, 0.0)
    if 1.0 not in inf_points:
        inf_points.append(1.0)
    total_curvature_func = total_curvature.TotalCurvature(pbsp)
    for tb, tc, te in zip(inf_points, inf_points[1:], inf_points[2:]):
        curve = {
            "ts": (tb, tc, te),
            "is_valid": None,
            "arcs": []
        }
        total_curvature_begin = total_curvature_func(tb, tc)
        arc_begin = {
            "original_ts": (tb, tc),
            "trim_ts": None,
            "total_curvature": total_curvature_begin,
            "is_trimed": False,
            "trimed_total_curvature": None
        }
        total_curvature_end = total_curvature_func(tc, te)
        arc_end = {
            "original_ts": (tc, te),
            "trim_ts": None,
            "total_curvature": total_curvature_end,
            "is_trimed": False,
            "trimed_total_curvature": None
        }
        if (total_curvature_begin >= UNDER_TOTAL_CURVATURE and
                total_curvature_end >= UNDER_TOTAL_CURVATURE):
            curve["is_valid"] = True
            if total_curvature_begin >= BEST_TOTAL_CURVATURE:
                tc_func = (
                    lambda t: (
                        total_curvature_func(t, tc) -
                        BEST_TOTAL_CURVATURE
                    )
                )
                tb_dash = search_trim_point(
                    tc_func,
                    (tb, tc)
                )
                arc_begin["is_trimed"] = True
                arc_begin["trimed_total_curvature"] = BEST_TOTAL_CURVATURE
            else:
                tb_dash = tb
            arc_begin["trim_ts"] = (tb_dash, tc)

            if total_curvature_end >= BEST_TOTAL_CURVATURE:
                tc_func = (
                    lambda t: (
                        total_curvature_func(tc, t) -
                        BEST_TOTAL_CURVATURE
                    )
                )
                te_dash = search_trim_point(
                    tc_func,
                    (tc, te)
                )
                arc_end["is_trimed"] = True
                arc_end["trimed_total_curvature"] = BEST_TOTAL_CURVATURE
            else:
                te_dash = te
            arc_end["trim_ts"] = (tc, te_dash)
        else:
            arc_begin["trim_ts"] = (tb, tc)
            arc_end["trim_ts"] = (tc, te)
            curve["is_valid"] = False
        arc_begin = set_length_field(pbsp, arc_begin)
        curve["arcs"].append(arc_begin)
        arc_end = set_length_field(pbsp, arc_end)
        curve["arcs"].append(arc_end)
        dst["curves"].append(curve)
    return dst


def build_bspline(bspline_dict):
    return bspline.BSpline(
        int(bspline_dict["degree"]),
        np.array(bspline_dict["knot_vector"]),
        np.array(bspline_dict["control_point"])
    )


def main(input_arg, output_arg):
    for i, o in io_arg_file(input_arg, output_arg, ".json"):
        print(i, o)
        json_data = load_json(i)
        traj_func = SecondDimensionalize(
            pb.ProjectedBSpline(
                build_bspline(json_data["bspline"]),
                get_viewport_axis(i)
            )
        )
        result = analysis(traj_func)
        result["axis"] = traj_func.func.axis.tolist()
        json_data["total_curvature_analysis"] = result
        dst_string = json.dumps(json_data, sort_keys=True, indent=4)
        if o is None:
            print(dst_string)
        else:
            if not os.path.exists(os.path.dirname(o)):
                os.makedirs(os.path.dirname(o))
            with open(o, "w") as f:
                f.write(dst_string)

if __name__ == '__main__':
    args = docopt(__doc__)
    main(args["<input>"], args["<output>"])
