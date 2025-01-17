# Copyright (c) 2022, NVIDIA CORPORATION & AFFILIATES.  All rights reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
import pynini
from nemo_text_processing.text_normalization.zh.graph_utils import GraphFst
from nemo_text_processing.text_normalization.zh.verbalizers.cardinal import Cardinal
from nemo_text_processing.text_normalization.zh.verbalizers.char import Char
from nemo_text_processing.text_normalization.zh.verbalizers.date import Date
from nemo_text_processing.text_normalization.zh.verbalizers.fraction import Fraction
from nemo_text_processing.text_normalization.zh.verbalizers.math_symbol import MathSymbol
from nemo_text_processing.text_normalization.zh.verbalizers.measure import Measure
from nemo_text_processing.text_normalization.zh.verbalizers.money import Money
from nemo_text_processing.text_normalization.zh.verbalizers.time import Time
from nemo_text_processing.text_normalization.zh.verbalizers.whitelist import Whitelist


class VerbalizeFst(GraphFst):
    """
    Composes other verbalizer grammars.
    For deployment, this grammar will be compiled and exported to OpenFst Finite State Archive (FAR) File.
    More details to deployment at NeMo/tools/text_processing_deployment.
    Args:
        deterministic: if True will provide a single transduction option,
            for False multiple options (used for audio-based normalization)
    """

    def __init__(self, deterministic: bool = True):
        super().__init__(name="verbalize", kind="verbalize", deterministic=deterministic)

        date = Date(deterministic=deterministic)
        cardinal = Cardinal(deterministic=deterministic)
        char = Char(deterministic=deterministic)
        fraction = Fraction(deterministic=deterministic)
        math_symbol = MathSymbol(deterministic=deterministic)
        money = Money(deterministic=deterministic)
        measure = Measure(deterministic=deterministic)
        time = Time(deterministic=deterministic)
        whitelist = Whitelist(deterministic=deterministic)

        graph = pynini.union(
            date.fst,
            cardinal.fst,
            fraction.fst,
            char.fst,
            math_symbol.fst,
            money.fst,
            measure.fst,
            time.fst,
            whitelist.fst,
        )

        self.fst = graph.optimize()
