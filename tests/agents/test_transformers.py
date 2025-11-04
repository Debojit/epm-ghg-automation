from app.agents.transformers.gb import transform_gb
from app.models.conversion_factors import ConversionFactor


def test_gb_transformer_valid_input():
    """
    Test the UK data transformer function
    """
    file_path = (
        "/mnt/c/Users/Debojit Sinha/Downloads/ghg-conversion-factors-2025-full-set.xlsx"
    )
    ghg_data = transform_gb(file_path)

    assert ghg_data is not None
    assert len(ghg_data) is not 0
