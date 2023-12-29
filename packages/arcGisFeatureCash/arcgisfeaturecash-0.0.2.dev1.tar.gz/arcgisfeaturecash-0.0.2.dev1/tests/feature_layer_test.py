import pytest
from arcGisFeatureCash import ArcGisFeatureService


@pytest.fixture
@pytest.mark.asyncio
async def feature_cash():
    url = "https://mapservices.prorail.nl/arcgis/rest/services/Tekeningen_schematisch_002/FeatureServer"
    return await ArcGisFeatureService.factory(url)


@pytest.mark.asyncio
async def test_get_features(feature_cash):
    pass
    # feature_service = await feature_cash
    # all_features = feature_service.get_all_features()


if __name__ == "__main__":
    pytest.main()
