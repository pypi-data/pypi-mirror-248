from __future__ import annotations

from randovania.games import game
from randovania.games.samus_returns import layout
from randovania.games.samus_returns.layout.preset_describer import MSRPresetDescriber
from randovania.games.samus_returns.pickup_database import progressive_items


def _options():
    from randovania.interface_common.options import PerGameOptions

    return PerGameOptions


def _gui() -> game.GameGui:
    from randovania.games.samus_returns import gui

    return game.GameGui(
        game_tab=gui.MSRGameTabWidget,
        tab_provider=gui.msr_preset_tabs,
        cosmetic_dialog=gui.MSRCosmeticPatchesDialog,
        export_dialog=gui.MSRGameExportDialog,
        progressive_item_gui_tuples=progressive_items.tuples(),
        spoiler_visualizer=(),
    )


def _patch_data_factory():
    from randovania.games.samus_returns.exporter.patch_data_factory import MSRPatchDataFactory

    return MSRPatchDataFactory


def _exporter():
    from randovania.games.samus_returns.exporter.game_exporter import MSRGameExporter

    return MSRGameExporter()


def _generator() -> game.GameGenerator:
    from randovania.games.samus_returns import generator
    from randovania.games.samus_returns.generator.bootstrap import MSRBootstrap
    from randovania.generator.hint_distributor import AllJokesHintDistributor

    return game.GameGenerator(
        pickup_pool_creator=generator.pool_creator,
        bootstrap=MSRBootstrap(),
        base_patches_factory=generator.MSRBasePatchesFactory(),
        hint_distributor=AllJokesHintDistributor(),
    )


game_data: game.GameData = game.GameData(
    short_name="MSR",
    long_name="Metroid: Samus Returns",
    development_state=game.DevelopmentState.EXPERIMENTAL,
    presets=[
        {"path": "starter_preset.rdvpreset"},
    ],
    faq=[
        (
            "Why is this pickup not animating?",
            "While progressive pickups update to have the correct model, "
            "due to limitations these models are not animated.",
        ),
    ],
    layout=game.GameLayout(
        configuration=layout.MSRConfiguration,
        cosmetic_patches=layout.MSRCosmeticPatches,
        preset_describer=MSRPresetDescriber(),
    ),
    options=_options,
    gui=_gui,
    generator=_generator,
    patch_data_factory=_patch_data_factory,
    exporter=_exporter,
    multiple_start_nodes_per_area=True,
)
