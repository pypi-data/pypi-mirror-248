import asyncio
import uuid
from dataclasses import dataclass, field
from typing import (
    Dict,
    List,
    Callable,
    Optional,
    Iterator,
    SupportsIndex,
    Union,
    overload,
)

from arcGisFeatureCash.models.attributes import FeatureAttributes, FeatureField
from arcGisFeatureCash.models.geometry import (
    EsriGeometryTypeEnum,
    parse_point,
    parse_line,
    parse_polygon,
)
from arcGisFeatureCash.utils.helpers import clear_temp_data


@dataclass
class Feature:
    _data: Optional[Dict]

    attributes: FeatureAttributes = field(init=False)
    geometry: str = field(init=False)
    uuid: str = field(init=False)
    dataset: Optional[str] = field(init=False)

    def __post_init__(self):
        self.uuid = str(uuid.uuid4())
        self.attributes = FeatureAttributes(self._data["attributes"])
        if "geometry" in self._data.keys():
            self.geometry = self._data["geometry"]
        else:
            self.geometry = ""

        # clear_temp_data(self)

    def __repr__(self) -> str:
        return f"<Feature {self.attributes.__dict__}>"

    async def set_geometry(self, function: Callable) -> None:
        self.geometry = await function(self.geometry)


@dataclass
class Features(list):
    _data: Optional[Dict]
    _items: List[Feature] = field(init=False)

    def __post_init__(self):
        self._items = [Feature(item) for item in self._data]
        clear_temp_data(self)

    def __iter__(self) -> Iterator[Feature]:
        yield from self._items

    @overload
    def __getitem__(self, idx: SupportsIndex) -> Feature:
        ...

    @overload
    def __getitem__(self, idx: slice) -> list[Feature]:
        ...

    def __getitem__(
        self, idx: Union[SupportsIndex, slice]
    ) -> Union[Feature, list[Feature]]:
        return self._items[idx]

    def __repr__(self) -> str:
        return str(self._items)

    def _set_value(self, field_list: List[FeatureField], function: Callable) -> None:
        for feature in self._items:
            [
                feature.attributes.set_attribute(field_item, function)
                for field_item in field_list
            ]

    async def set_geometry(self, geometry_type: EsriGeometryTypeEnum) -> None:
        match geometry_type:
            case EsriGeometryTypeEnum.esriGeometryPoint:
                function = parse_point
            case EsriGeometryTypeEnum.esriGeometryPolyline:
                function = parse_line
            case EsriGeometryTypeEnum.esriGeometryPolygon:
                function = parse_polygon
            case _:
                raise NotImplementedError

        tasks = [feature.set_geometry(function) for feature in self._items]
        await asyncio.gather(*tasks)


if __name__ == "__main__":
    pass
