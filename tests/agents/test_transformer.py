from pathlib import Path

from app.agents.transformers.gb import transform_gb

def test_valid_gb_file():
    ghg_file = Path("/Users/debojit/Documents/ghg-conversion-factors-2025-full-set.xlsx")

    conversion_factors = transform_gb(ghg_file)
    print(conversion_factors)
    assert conversion_factors is not None
    assert len(conversion_factors) != 0