"""External zero-colour VECT files must retain their exact coordinate rows."""
import numpy as np
import pytest
from src.curves.vect import read_vect, VECTParseError


def test_zero_colour_counts_are_consumed_for_every_component(tmp_path):
    path = tmp_path / 'two_triangles.vect'
    path.write_text('VECT\n2 6 0\n-3 -3\n0 0\n'
                    '0 0 0\n1 0 0\n0 1 0\n'
                    '0 0 3\n1 0 3\n0 1 3\n')
    link = read_vect(path)
    np.testing.assert_array_equal(link.components[0].vertices,
                                  [[0, 0, 0], [1, 0, 0], [0, 1, 0]])
    np.testing.assert_array_equal(link.components[1].vertices,
                                  [[0, 0, 3], [1, 0, 3], [0, 1, 3]])


def test_zero_colour_header_rejects_nonzero_component_colour_count(tmp_path):
    path = tmp_path / 'invalid.vect'
    path.write_text('VECT\n1 3 0\n-3\n1\n0 0 0\n1 0 0\n0 1 0\n')
    with pytest.raises(VECTParseError, match='color count'):
        read_vect(path)
