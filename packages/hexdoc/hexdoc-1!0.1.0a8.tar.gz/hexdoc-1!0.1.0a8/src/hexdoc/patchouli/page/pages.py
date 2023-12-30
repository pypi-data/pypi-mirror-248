from typing import Self

from pydantic import model_validator

from hexdoc.core import Entity, ResourceLocation
from hexdoc.minecraft import LocalizedStr
from hexdoc.minecraft.assets import ItemWithTexture, TagWithTexture, Texture
from hexdoc.minecraft.recipe import (
    BlastingRecipe,
    CampfireCookingRecipe,
    CraftingRecipe,
    SmeltingRecipe,
    SmithingRecipe,
    SmokingRecipe,
    StonecuttingRecipe,
)
from hexdoc.model import HexdocModel

from ..text import FormatTree
from .abstract_pages import Page, PageWithDoubleRecipe, PageWithText, PageWithTitle


class TextPage(Page, type="patchouli:text"):
    title: LocalizedStr | None = None
    text: FormatTree


class BlastingPage(PageWithDoubleRecipe[BlastingRecipe], type="patchouli:blasting"):
    pass


class CampfireCookingPage(
    PageWithDoubleRecipe[CampfireCookingRecipe], type="patchouli:campfire_cooking"
):
    pass


class CraftingPage(PageWithDoubleRecipe[CraftingRecipe], type="patchouli:crafting"):
    pass


class EmptyPage(Page, type="patchouli:empty", template_type="patchouli:page"):
    draw_filler: bool = True


class EntityPage(PageWithText, type="patchouli:entity"):
    entity: Entity
    scale: float = 1
    offset: float = 0
    rotate: bool = True
    default_rotation: float = -45
    name: LocalizedStr | None = None


class ImagePage(PageWithTitle, type="patchouli:image"):
    images: list[Texture]
    border: bool = False

    @property
    def images_with_alt(self):
        for image in self.images:
            if self.title:
                yield image, self.title
            else:
                yield image, str(image)


class LinkPage(TextPage, type="patchouli:link"):
    url: str
    link_text: LocalizedStr


class Multiblock(HexdocModel):
    """https://vazkiimods.github.io/Patchouli/docs/patchouli-basics/multiblocks/"""

    mapping: dict[str, ItemWithTexture | TagWithTexture]
    pattern: list[list[str]]
    symmetrical: bool = False
    offset: tuple[int, int, int] | None = None


class MultiblockPage(PageWithText, type="patchouli:multiblock"):
    name: LocalizedStr
    multiblock_id: ResourceLocation | None = None
    multiblock: Multiblock | None = None
    enable_visualize: bool = True

    @model_validator(mode="after")
    def _check_multiblock(self) -> Self:
        if self.multiblock_id is None and self.multiblock is None:
            raise ValueError(f"One of multiblock_id or multiblock must be set\n{self}")
        return self


class QuestPage(PageWithText, type="patchouli:quest"):
    trigger: ResourceLocation | None = None
    title: LocalizedStr = LocalizedStr.with_value("Objective")


class RelationsPage(PageWithText, type="patchouli:relations"):
    entries: list[ResourceLocation]
    title: LocalizedStr = LocalizedStr.with_value("Related Chapters")


class SmeltingPage(PageWithDoubleRecipe[SmeltingRecipe], type="patchouli:smelting"):
    pass


class SmithingPage(PageWithDoubleRecipe[SmithingRecipe], type="patchouli:smithing"):
    pass


class SmokingPage(PageWithDoubleRecipe[SmokingRecipe], type="patchouli:smoking"):
    pass


class StonecuttingPage(
    PageWithDoubleRecipe[StonecuttingRecipe], type="patchouli:stonecutting"
):
    pass


class SpotlightPage(PageWithTitle, type="patchouli:spotlight"):
    item: ItemWithTexture
    link_recipe: bool = False
