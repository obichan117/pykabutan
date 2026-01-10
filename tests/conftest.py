"""Pytest configuration and fixtures."""

import pytest


def pytest_configure(config):
    """Register custom markers."""
    config.addinivalue_line(
        "markers", "integration: marks tests as integration tests (real HTTP requests)"
    )


@pytest.fixture
def sample_main_page_html():
    """Sample HTML for kabutan main page (simplified)."""
    return """
    <html>
    <head><title>トヨタ自動車（トヨタ）【7203】</title></head>
    <body>
        <h2>7203　トヨタ自動車</h2>
        <span class="market">東証Ｐ</span>
        <div id="stockinfo_i2"><a href="#">輸送用機器</a></div>
        <table>
            <tr><td>概要</td><td>世界首位級の自動車メーカー</td></tr>
            <tr><td>テーマ</td><td>EV 自動運転</td></tr>
        </table>
        <table>
            <tr><th>PER</th><th>PBR</th><th>利回り</th><th>信用倍率</th></tr>
            <tr><td>15.1倍</td><td>1.18倍</td><td>2.5%</td><td>3.2倍</td></tr>
            <tr><td colspan="4">時価総額 535,134億円</td></tr>
        </table>
        <dl class="si_i1_dl2">
            <a href="/stock/?code=7267">Honda</a>
            <a href="/stock/?code=7201">Nissan</a>
        </dl>
    </body>
    </html>
    """


@pytest.fixture
def sample_history_html():
    """Sample HTML for kabutan history page (simplified)."""
    return """
    <html>
    <body>
        <table></table>
        <table></table>
        <table></table>
        <table></table>
        <table></table>
        <table>
            <tr><th>日付</th><th>始値</th><th>高値</th><th>安値</th><th>終値</th><th>前日比</th><th>前日比％</th><th>売買高</th></tr>
            <tr><td>26/01/08</td><td>3301</td><td>3328</td><td>3286</td><td>3294</td><td>-41</td><td>-1.23</td><td>18107700</td></tr>
            <tr><td>26/01/07</td><td>3350</td><td>3360</td><td>3326</td><td>3335</td><td>-94</td><td>-2.74</td><td>21592100</td></tr>
        </table>
    </body>
    </html>
    """


@pytest.fixture
def sample_news_html():
    """Sample HTML for kabutan news page (simplified)."""
    return """
    <html>
    <body>
        <table></table>
        <table></table>
        <table></table>
        <table>
            <tr><td>25/11/05 14:25</td><td>決算</td><td>トヨタ、今期最終を10％上方修正</td></tr>
            <tr><td>25/08/07 14:00</td><td>決算</td><td>トヨタ、今期最終を14％下方修正</td></tr>
        </table>
    </body>
    </html>
    """


@pytest.fixture
def sample_search_html():
    """Sample HTML for kabutan search results page (simplified)."""
    return """
    <html>
    <body>
        <table></table>
        <table></table>
        <table>
            <tr><th>コード</th><th>銘柄名</th><th>市場</th></tr>
            <tr><td>6758</td><td>ソニーグループ</td><td>東Ｐ</td></tr>
            <tr><td>6902</td><td>デンソー</td><td>東Ｐ</td></tr>
        </table>
    </body>
    </html>
    """


@pytest.fixture
def mock_response(mocker):
    """Factory fixture for creating mock HTTP responses."""
    def _mock_response(html_content, status_code=200):
        mock_resp = mocker.Mock()
        mock_resp.text = html_content
        mock_resp.apparent_encoding = "utf-8"
        mock_resp.raise_for_status = mocker.Mock()
        if status_code >= 400:
            mock_resp.raise_for_status.side_effect = Exception(f"{status_code} Error")
        return mock_resp
    return _mock_response
