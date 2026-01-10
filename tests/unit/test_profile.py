"""Unit tests for Profile dataclass."""

import pytest

from pykabutan.profile import Profile


class TestProfile:
    """Test Profile dataclass."""

    def test_create_profile(self):
        """Test creating a Profile."""
        profile = Profile(
            code="7203",
            name="トヨタ自動車",
            market="東証Ｐ",
            industry="輸送用機器",
        )

        assert profile.code == "7203"
        assert profile.name == "トヨタ自動車"
        assert profile.market == "東証Ｐ"
        assert profile.industry == "輸送用機器"

    def test_optional_fields_default_to_none(self):
        """Test that optional fields default to None."""
        profile = Profile(code="7203")

        assert profile.name is None
        assert profile.market is None
        assert profile.industry is None
        assert profile.description is None
        assert profile.themes is None
        assert profile.per is None
        assert profile.pbr is None

    def test_dict_conversion(self):
        """Test converting Profile to dict."""
        profile = Profile(
            code="7203",
            name="トヨタ自動車",
            per=15.1,
        )

        d = dict(profile)

        assert d["code"] == "7203"
        assert d["name"] == "トヨタ自動車"
        assert d["per"] == 15.1
        assert d["pbr"] is None

    def test_to_dict_method(self):
        """Test to_dict() method."""
        profile = Profile(code="7203", name="Toyota")

        d = profile.to_dict()

        assert isinstance(d, dict)
        assert d["code"] == "7203"
        assert d["name"] == "Toyota"

    def test_all_fields(self):
        """Test Profile with all fields populated."""
        profile = Profile(
            code="7203",
            name="トヨタ自動車",
            market="東証Ｐ",
            industry="輸送用機器",
            description="世界首位級の自動車メーカー",
            themes=["EV", "自動運転"],
            website="https://toyota.co.jp",
            english_name="TOYOTA MOTOR CORPORATION",
            per=15.1,
            pbr=1.18,
            market_cap=535134000000000,
            dividend_yield=2.5,
            margin_ratio=3.2,
        )

        d = dict(profile)
        assert len(d) == 13  # All 13 fields

    def test_themes_as_list(self):
        """Test that themes is a list."""
        profile = Profile(
            code="7203",
            themes=["EV", "自動運転", "水素"],
        )

        assert isinstance(profile.themes, list)
        assert len(profile.themes) == 3
        assert "EV" in profile.themes

    def test_numeric_fields_can_be_float(self):
        """Test that numeric fields accept float values."""
        profile = Profile(
            code="7203",
            per=15.123,
            pbr=1.1876,
            market_cap=535134.5,
            dividend_yield=2.567,
            margin_ratio=3.234,
        )

        assert profile.per == 15.123
        assert profile.pbr == 1.1876
