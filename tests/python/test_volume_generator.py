# test_volume_generator.py
from pathlib import Path

import pytest

from argolid import VolumeGenerator


@pytest.mark.parametrize(
    "input_dir,file_pattern,output_dir,image_name,group_by",
    [
        ("3D", "{z:d}.c{c:d}.ome.tiff", "3D_pyramid_full", "test_volume", "c"),
    ],
)
def test_generate_volume_creates_output(tmp_path: Path, input_dir, file_pattern, output_dir, image_name, group_by):
    """
    Pytest version of the snippet:
    - runs VolumeGenerator.generate_volume()
    - asserts it produced the expected output directory structure
    """
    # Arrange: keep test outputs isolated
    out_dir = tmp_path / output_dir

    vg = VolumeGenerator(
        source_dir=input_dir,
        group_by=group_by,
        file_pattern=file_pattern,
        out_dir=str(out_dir),
        image_name=image_name,
    )

    vg.generate_volume()

    # basic sanity checks that something was created
    root = out_dir / image_name
    assert root.exists(), f"Expected output root to exist: {root}"
    assert root.is_dir(), f"Expected output root to be a directory: {root}"

    # base scale at base_scale_key (default 0)
    base_scale = root / "0"
    assert base_scale.exists(), f"Expected base scale directory to exist: {base_scale}"
    assert base_scale.is_dir(), f"Expected base scale directory to be a directory: {base_scale}"

    # ensure some zarr metadata exists
    zarr_markers = [
        root / ".zgroup",
        root / ".zattrs",
        base_scale / ".zgroup",
        base_scale / ".zattrs",
    ]
    assert any(p.exists() for p in zarr_markers), (
        "Expected at least one zarr metadata marker (.zgroup/.zattrs) "
        f"under {root} or {base_scale}"
    )
