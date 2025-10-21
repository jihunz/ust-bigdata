from __future__ import annotations
import time
from typing import Optional, Dict, List
import requests
from bs4 import BeautifulSoup
import re
from pathlib import Path
from wordcloud import WordCloud, STOPWORDS
import matplotlib

matplotlib.use('TkAgg')
import matplotlib.pyplot as plt

DEFAULT_HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/124.0 Safari/537.36"
    )
}


def fetch(
        url: str,
        params: Optional[Dict[str, str]] = None,
        headers: Optional[Dict[str, str]] = None,
        timeout: int = 15,
) -> str:
    hdrs = {**DEFAULT_HEADERS, **(headers or {})}
    r = requests.get(url, params=params, headers=hdrs, timeout=timeout)
    r.raise_for_status()
    if not r.encoding or r.encoding.lower() == "iso-8859-1":
        r.encoding = r.apparent_encoding
    return r.text


def soup(html: str, parser: str = "html.parser") -> BeautifulSoup:
    return BeautifulSoup(html, parser)


def save_local(titles: List[str], filepath: str = "headlines.txt") -> None:
    with open(filepath, "w", encoding="utf-8") as f:
        for t in titles:
            f.write(t.strip() + "\n")


def create_wordcloud(query) -> str:
    filepath = Path("headlines.txt")
    if not filepath.exists():
        raise FileNotFoundError("headlines.txt 파일이 존재하지 않습니다. 먼저 뉴스 스크래핑을 실행하세요.")

    with open(filepath, "r", encoding="utf-8") as f:
        lines = [line.strip() for line in f if line.strip()]

    joined = " ".join(lines)
    tokens = [tok for tok in re.split(r"[^\w]+", joined) if len(tok) >= 2]

    stopwords = {
        "기자", "특파원", "앵커", "사진", "영상", "포토", "화보", "자료", "전문", "입수",
        "속보", "단독", "종합", "현장", "중계", "인터뷰", "좌담", "토론", "논설", "사설", "칼럼", "오피니언", "해설", "분석",
        "보도", "취재", "제보", "속사정", "단평", "코멘트", "오늘", "내일", "어제", "이번", "지난", "현재", "당일", "금일", "방금", "조금전",
        "방안", "대책", "대응", "논란", "이슈", "핵심", "추가", "속속", "연속", "최신", "업데이트",
        "발표", "공개", "발굴", "확인", "밝혀", "드러나", "전해", "전했다", "밝혔다", "나타나", "관측",
        "정부", "당국", "관계자", "업계", "당", "의회", "위원회", "청와대", "국회", "법원",
        "관련", "제목", "기사", "뉴스", "보도자료", "속보알림", "사진제공", "영상제공",
        "연합뉴스", "뉴시스", "뉴스1", "KBS", "MBC", "SBS", "YTN"
    }
    stopwords.add(query)

    wc = WordCloud(
        width=1400,
        height=900,
        stopwords=set(stopwords),
        background_color="white",
        font_path="/System/Library/Fonts/AppleGothic.ttf",
        collocations=False
    ).generate(" ".join(tokens))

    plt.figure()
    plt.imshow(wc)
    plt.axis("off")
    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    query = input("검색어: ").strip()
    page = int(input("페이지수: ").strip())

    result: List[str] = []
    for start in range(1, page * 10, 10):
        url = (
            "https://search.naver.com/search.naver"
            f"?where=news&sm=tab_pge&query={query}"
            "&sort=0&photo=0&field=0&pd=0&ds=&de=&cluster_rank=32&mynews=0"
            "&office_type=0&office_section_code=0&news_office_checked="
            "&nso=so:r,p:all,a:all"
            f"&start={start}"
        )
        html = fetch(url)
        sp = soup(html)
        title_tags = sp.select(".sds-comps-text-type-headline1")
        titles = [tag.get_text(strip=True) for tag in title_tags]
        result.extend(titles)
        print(f"{start} ~ {start + 9} 수집, 누적 {len(result)}")
        time.sleep(2)

    save_local(result, "headlines.txt")
    create_wordcloud(query)
