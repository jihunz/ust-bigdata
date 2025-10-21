from __future__ import annotations
import time
from typing import Iterable, List, Optional, Dict
from urllib.parse import urljoin, urlparse
import requests
from bs4 import BeautifulSoup, Tag
from google.colab import drive

drive.mount('/content/drive')

DEFAULT_HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/124.0 Safari/537.36"
    )
}


class FetchError(RuntimeError):
    pass


def fetch(
        url: str,
        params: Optional[Dict[str, str]] = None,
        headers: Optional[Dict[str, str]] = None,
        timeout: int = 15,
        retries: int = 2,
        backoff: float = 1.5,
) -> str:
    """URL에서 HTML 문자열을 가져온다. 간단한 재시도/백오프 포함."""
    hdrs = {**DEFAULT_HEADERS, **(headers or {})}
    last_err = None
    for attempt in range(retries + 1):
        try:
            r = requests.get(url, params=params, headers=hdrs, timeout=timeout)
            r.raise_for_status()
            # 인코딩 힌트 적용(서버가 잘못 보낼 때 대비)
            if not r.encoding or r.encoding.lower() == "iso-8859-1":
                r.encoding = r.apparent_encoding
            return r.text
        except Exception as e:
            last_err = e
            if attempt < retries:
                time.sleep(backoff ** attempt)
            else:
                break
    raise FetchError(f"GET 실패: {url} ({last_err})")


def soup(html: str, parser: str = "html.parser") -> BeautifulSoup:
    """HTML -> BeautifulSoup 객체."""
    return BeautifulSoup(html, parser)


def select(s: BeautifulSoup | Tag, css: str) -> List[Tag]:
    """CSS 셀렉터로 Tag 리스트 반환."""
    return s.select(css)


def text(s: BeautifulSoup | Tag, css: str, sep: str = " ", strip: bool = True) -> str:
    """첫 매칭 요소의 텍스트만 뽑아온다. 없으면 빈 문자열."""
    el = s.select_one(css)
    if not el:
        return ""
    t = el.get_text(separator=sep)
    return t.strip() if strip else t


def texts(s: BeautifulSoup | Tag, css: str, sep: str = " ", strip: bool = True) -> List[str]:
    """여러 요소 텍스트 리스트."""
    out: List[str] = []
    for el in s.select(css):
        t = el.get_text(separator=sep)
        out.append(t.strip() if strip else t)
    return out


def links(s: BeautifulSoup | Tag, base: Optional[str] = None, css: str = "a[href]") -> List[str]:
    """a[href] 링크들을 절대경로로 반환."""
    out: List[str] = []
    for a in s.select(css):
        href = a.get("href")
        if not href:
            continue
        out.append(urljoin(base, href) if base else href)
    return out


def table_rows(s: BeautifulSoup | Tag, css: str = "table tr") -> List[List[str]]:
    """간단한 표 파싱: 각 tr의 셀 텍스트 리스트."""
    rows: List[List[str]] = []
    for tr in s.select(css):
        cells = tr.select("th, td")
        if cells:
            rows.append([c.get_text(strip=True) for c in cells])
    return rows


def same_origin(u1: str, u2: str) -> bool:
    """도메인/스킴 동일성 체크(robots나 범위 제한시 활용)."""
    p1, p2 = urlparse(u1), urlparse(u2)
    return (p1.scheme, p1.netloc) == (p2.scheme, p2.netloc)


def save(title_list):
    file_path = '/content/drive/My Drive/headlines.txt'
    with open(file_path, 'w') as f:
        for title in title_list:
            f.write(title.get_text(strip=True) + '\n')


# 간단 사용 예시 ---------------------------------------------------------------
if __name__ == "__main__":
    query = input('검색어')
    page = int(input('페이지수'))
    result = []
    
    for start in range(1, page * 10, 10):
        url = f"https://search.naver.com/search.naver?where=news&sm=tab_pge&query={query}&sort=0&photo=0&field=0&pd=0&ds=&de=&cluster_rank=32&mynews=0&office_type=0&office_section_code=0&news_office_checked=&nso=so:r,p:all,a:all&start={start}"
        html = fetch(url)
        sp = soup(html)

        title_list = sp.select('.sds-comps-text-type-headline1')
        result.append(title_list)

    save(result)
    for title in result:
        print(title)