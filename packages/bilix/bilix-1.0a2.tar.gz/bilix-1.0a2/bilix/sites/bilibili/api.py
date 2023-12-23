import asyncio
import json
import re
from urllib.parse import quote
import httpx
from pydantic import BaseModel, Field, validator
from typing import Union, List, Tuple, Dict, Optional
import json5
from danmakuC.bilibili import parse_view
from bilix.download.utils import req_retry, raise_api_error
from bilix.sites.bilibili.utils import parse_ids_from_url
from bilix.utils import legal_title
from bilix.exception import APIInvalidError, APIError, APIResourceError, APIUnsupportedError
import hashlib
import time

dft_client_settings = {
    'headers': {'user-agent': 'PostmanRuntime/7.29.0', 'referer': 'https://www.bilibili.com'},
    'cookies': {'CURRENT_FNVAL': '4048'},
    'http2': True
}


@raise_api_error
async def get_cate_meta(client: httpx.AsyncClient) -> dict:
    """
    获取b站分区元数据

    :param client:
    :return:
    """
    cate_info = {}
    res = await req_retry(client, 'https://s1.hdslb.com/bfs/static/laputa-channel/client/assets/index.c0ea30e6.js')
    cate_data = re.search('Za=([^;]*);', res.text).groups()[0]
    cate_data = json5.loads(cate_data)['channelList']
    for i in cate_data:
        if 'sub' in i:
            for j in i['sub']:
                cate_info[j['name']] = j
            cate_info[i['name']] = i
    return cate_info


@raise_api_error
async def get_list_info(client: httpx.AsyncClient, url_or_sid: str, ):
    """
    获取视频列表信息

    :param url_or_sid:
    :param client:
    :return:
    """
    if url_or_sid.startswith('http'):
        sid = re.search(r'sid=(\d+)', url_or_sid).groups()[0]
    else:
        sid = url_or_sid
    res = await req_retry(client, f'https://api.bilibili.com/x/series/series?series_id={sid}')  # meta api
    meta = json.loads(res.text)
    mid = meta['data']['meta']['mid']
    params = {'mid': mid, 'series_id': sid, 'ps': meta['data']['meta']['total']}
    list_res, up_res = await asyncio.gather(
        req_retry(client, 'https://api.bilibili.com/x/series/archives', params=params),
        req_retry(client, f'https://api.bilibili.com/x/space/acc/info?mid={mid}'))
    list_info, up_info = json.loads(list_res.text), json.loads(up_res.text)
    list_name, up_name = meta['data']['meta']['name'], up_info['data']['name']
    bvids = [i['bvid'] for i in list_info['data']['archives']]
    return list_name, up_name, bvids


@raise_api_error
async def get_collect_info(client: httpx.AsyncClient, url_or_sid: str):
    """
    获取合集信息

    :param url_or_sid:
    :param client:
    :return:
    """
    sid = re.search(r'sid=(\d+)', url_or_sid).groups()[0] if url_or_sid.startswith('http') else url_or_sid
    params = {'season_id': sid}
    res = await req_retry(client, 'https://api.bilibili.com/x/space/fav/season/list', params=params)
    data = json.loads(res.text)
    medias = data['data']['medias']
    info = data['data']['info']
    col_name, up_name = info['title'], medias[0]['upper']['name']
    bvids = [i['bvid'] for i in data['data']['medias']]
    return col_name, up_name, bvids


@raise_api_error
async def get_favour_page_info(client: httpx.AsyncClient, url_or_fid: str, pn=1, ps=20, keyword=''):
    """
    获取收藏夹信息（分页）

    :param url_or_fid:
    :param pn:
    :param ps:
    :param keyword:
    :param client:
    :return:
    """
    if url_or_fid.startswith('http'):
        fid = re.findall(r'fid=(\d+)', url_or_fid)[0]
    else:
        fid = url_or_fid
    params = {'media_id': fid, 'pn': pn, 'ps': ps, 'keyword': keyword, 'order': 'mtime'}
    res = await req_retry(client, 'https://api.bilibili.com/x/v3/fav/resource/list', params=params)
    data = json.loads(res.text)['data']
    fav_name, up_name = data['info']['title'], data['info']['upper']['name']
    bvids = [i['bvid'] for i in data['medias'] if i['title'] != '已失效视频']
    total_size = data['info']['media_count']
    return fav_name, up_name, total_size, bvids


@raise_api_error
async def get_cate_page_info(client: httpx.AsyncClient, cate_id, time_from, time_to, pn=1, ps=30,
                             order='click', keyword=''):
    """
    获取分区视频信息（分页）

    :param cate_id:
    :param pn:
    :param ps:
    :param order:
    :param keyword:
    :param time_from:
    :param time_to:
    :param client:
    :return:
    """
    params = {'search_type': 'video', 'view_type': 'hot_rank', 'cate_id': cate_id, 'pagesize': ps,
              'keyword': keyword, 'page': pn, 'order': order, 'time_from': time_from, 'time_to': time_to}
    res = await req_retry(client, 'https://s.search.bilibili.com/cate/search', params=params)
    info = json.loads(res.text)
    bvids = [i['bvid'] for i in info['result']]
    return bvids


async def _add_sign(client: httpx.AsyncClient, params: dict):
    """添加b站api签名到params中
    :param params:
    :return:
    """
    OE = [46, 47, 18, 2, 53, 8, 23, 32, 15, 50, 10, 31, 58, 3, 45,
          35, 27, 43, 5, 49, 33, 9, 42, 19, 29, 28, 14, 39, 12, 38,
          41, 13, 37, 48, 7, 16, 24, 55, 40, 61, 26, 17, 0, 1, 60,
          51, 30, 4, 22, 25, 54, 21, 56, 59, 6, 63, 57, 62, 11, 36,
          20, 34, 44, 52]
    res = await req_retry(
        client, "https://api.bilibili.com/x/web-interface/nav"
    )
    info = json.loads(res.text)
    img_val = info['data']['wbi_img']['img_url'].split('/')[-1].split('.')[0]
    sub_val = info['data']['wbi_img']['sub_url'].split('/')[-1].split('.')[0]
    val = img_val + sub_val
    request_token = ''.join([val[v] for v in OE])[:32]

    wts = int(time.time())
    params["wts"] = wts
    data = dict(sorted(params.items()))
    data_str = "&".join([f"{k}={v}" for k, v in data.items()]) + request_token
    md5 = hashlib.md5(data_str.encode("utf-8")).hexdigest()
    params["w_rid"] = md5
    return params


def _find_mid(space_url: str):
    return re.search(r'^https://space.bilibili.com/(\d+)/?', space_url).group(1)


@raise_api_error
async def get_up_video_info(client: httpx.AsyncClient, url_or_mid: str, pn=1, ps=30, order="pubdate", keyword=""):
    """
    获取up主信息

    :param url_or_mid:
    :param pn:
    :param ps:
    :param order:
    :param keyword:
    :param client:
    :return:
    """
    if url_or_mid.startswith("http"):
        mid = _find_mid(url_or_mid)
    else:
        mid = url_or_mid

    params = {"mid": mid, "order": order, "ps": ps, "pn": pn, "keyword": quote(keyword or "")}
    await _add_sign(client, params)

    res = await req_retry(client, "https://api.bilibili.com/x/space/wbi/arc/search", params=params)
    info = json.loads(res.text)
    up_name = info["data"]["list"]["vlist"][0]["author"]
    total_size = info["data"]["page"]["count"]
    bv_ids = [i["bvid"] for i in info["data"]["list"]["vlist"]]
    return up_name, total_size, bv_ids


async def get_up_info(client: httpx.AsyncClient, url_or_mid: str):
    if url_or_mid.startswith("http"):
        mid = _find_mid(url_or_mid)
    else:
        mid = url_or_mid
    params = {"mid": mid}
    await _add_sign(client, params)
    res = await req_retry(client, "https://api.bilibili.com/x/space/wbi/acc/info", params=params)
    data = json.loads(res.text)['data']
    return data


class Media(BaseModel):
    base_url: str
    backup_url: List[str] = None
    size: int = None
    width: int = None
    height: int = None
    suffix: str = None
    quality: str = None
    codec: str = None
    segment_base: dict = None

    @property
    def urls(self):
        """the copy of all url including backup"""
        return [self.base_url, *self.backup_url] if self.backup_url else [self.base_url]


class Dash(BaseModel):
    duration: int
    videos: List[Media]
    audios: List[Media]
    video_formats: Dict[str, Dict[str, Media]]
    audio_formats: Dict[str, Optional[Media]]

    @classmethod
    def from_dict(cls, play_info: dict):
        dash = play_info['data']['dash']  # may raise KeyError
        video_formats = {}
        quality_map = {}
        for d in play_info['data']['support_formats']:
            quality_map[d['quality']] = d['new_description']
            video_formats[d['new_description']] = {}
        videos = []
        for d in dash['video']:
            if d['id'] not in quality_map:
                continue  # https://github.com/HFrost0/bilix/issues/93
            quality = quality_map[d['id']]
            m = Media(quality=quality, codec=d['codecs'], **d)
            video_formats[quality][m.codec] = m
            videos.append(m)

        audios = []
        audio_formats = {}
        if dash.get('audio', None):  # some video have NO audio
            d = dash['audio'][0]
            m = Media(quality="default", suffix='.aac', codec=d['codecs'], **d)
            audios.append(m)
            audio_formats[m.quality] = m
        if dash['dolby']['type'] != 0:
            quality = "dolby"
            audio_formats[quality] = None
            if dash['dolby'].get('audio', None):
                d = dash['dolby']['audio'][0]
                m = Media(quality=quality, suffix='.eac3', codec=d['codecs'], **d)
                audios.append(m)
                audio_formats[m.quality] = m
        if dash.get('flac', None):
            quality = "flac"
            audio_formats[quality] = None
            if d := dash['flac']['audio']:
                m = Media(quality=quality, suffix='.flac', codec=d['codecs'], **d)
                audios.append(m)
                audio_formats[m.quality] = m
        return cls(duration=dash['duration'], videos=videos, audios=audios,
                   video_formats=video_formats, audio_formats=audio_formats)

    def choose_video(self, quality: Union[int, str], video_codec: str) -> Media:
        # 1. absolute choice with quality name like 4k 1080p '1080p 60帧'
        if isinstance(quality, str):
            for k in self.video_formats:
                if k.upper().startswith(quality.upper()):  # incase 1080P->1080p
                    for c in self.video_formats[k]:
                        if c.startswith(video_codec):
                            return self.video_formats[k][c]
        # 2. relative choice
        else:
            keys = [k for k in self.video_formats.keys() if self.video_formats[k]]
            quality = min(quality, len(keys) - 1)
            k = keys[quality]
            for c in self.video_formats[k]:
                if c.startswith(video_codec):
                    return self.video_formats[k][c]
        raise KeyError(f"no match for video quality: {quality} codec: {video_codec}")

    def choose_audio(self, audio_codec: str) -> Optional[Media]:
        if len(self.audios) == 0:  # some video has no audio
            return
        for k in self.audio_formats:
            if self.audio_formats[k] and self.audio_formats[k].codec.startswith(audio_codec):
                return self.audio_formats[k]
        raise KeyError(f'no match for audio codec: {audio_codec}')

    def choose_quality(self, quality: Union[str, int], codec: str = '') -> Tuple[Media, Optional[Media]]:
        if isinstance(quality, str):
            quality = self.parse_quality(quality)
        v_codec, a_codec, *_ = codec.split(':') + [""]
        video, audio = self.choose_video(quality, v_codec), self.choose_audio(a_codec)
        return video, audio

    @staticmethod
    def parse_quality(value: str) -> Union[int, str]:
        """for relative choice (0, 1, 2, ...) return int, else return str"""
        if value.isdigit():
            # some special digit
            if value in {1080, 720, 480, 360}:
                return value
            return int(value)
        else:
            return value


class Status(BaseModel):
    view: int = Field(description="播放量")
    danmaku: int = Field(description="弹幕数")
    coin: int = Field(description="硬币数")
    like: int = Field(description="点赞数")
    reply: int = Field(description="回复数")
    favorite: int = Field(description="收藏数")
    share: int = Field(description="分享数")
    follow: int = Field(default=None, description="追剧数/追番数")

    @validator('view', pre=True)
    def no_view(cls, v):
        return 0 if v == '--' else v


class Page(BaseModel):
    p_name: str
    p_url: str


class VideoInfo(BaseModel):
    title: str
    h1_title: str  # for bv same to title, but for tv or bangumi title will be more specific
    aid: int
    cid: int
    p: int
    pages: List[Page]  # [[p_name, p_url], ...]
    img_url: str
    status: Status
    bvid: str = None
    dash: Optional[Dash] = None
    other: Optional[List[Media]] = None  # durl resource: flv, mp4.

    @staticmethod
    def parse_html(url, html: str):
        if "window._riskdata_" in html:
            raise APIInvalidError("web 前端访问被风控", url)
        init_info = re.search(r'<script>window.__INITIAL_STATE__=({.*});\(', html).groups()[0]  # this line may raise
        init_info = json.loads(init_info)
        if len(init_info.get('error', {})) > 0:
            raise APIResourceError("视频已失效", url)  # 啊叻？视频不见了？在分区下载的时候可能产生
        # extract meta
        pages = []
        h1_title = legal_title(re.search('<h1[^>]*title="([^"]*)"', html).groups()[0])
        if 'videoData' in init_info:  # bv视频
            status = Status(**init_info['videoData']['stat'])
            bvid = init_info['bvid']
            aid = init_info['aid']
            (p, cid), = init_info['cidMap'][bvid]['cids'].items()
            p = int(p) - 1
            title = legal_title(init_info['videoData']['title'])
            base_url = url.split('?')[0]
            for idx, i in enumerate(init_info['videoData']['pages']):
                p_url = f"{base_url}?p={idx + 1}"
                p_name = f"P{idx + 1}-{i['part']}" if len(init_info['videoData']['pages']) > 1 else ''
                pages.append(Page(p_name=p_name, p_url=p_url))
        elif 'initEpList' in init_info:  # 动漫，电视剧，电影
            stat = init_info['mediaInfo']['stat']
            status = Status(
                view=stat['views'], danmaku=stat['danmakus'], coin=stat['coins'], like=stat['likes'],
                reply=stat['reply'], favorite=stat['favorite'], follow=stat['favorites'], share=stat['share'],
            )
            bvid = None
            aid = init_info['epInfo']['aid']
            cid = init_info['epInfo']['cid']
            p = init_info['epInfo']['i']
            title = legal_title(re.search('property="og:title" content="([^"]*)"', html).groups()[0])
            for idx, i in enumerate(init_info['initEpList']):
                p_url = i['link']
                p_name = i['title']
                pages.append(Page(p_name=p_name, p_url=p_url))
        else:
            raise APIUnsupportedError("未知视频类型", url)
        # extract dash and flv_url
        dash, other = None, []
        try:
            play_info = re.search('<script>window.__playinfo__=({.*})</script><script>', html).groups()[0]
            play_info = json.loads(play_info)
        except AttributeError:  # AttributeError-动画
            pass
        else:
            try:
                dash = Dash.from_dict(play_info)
            except KeyError:
                pass
            try:
                for i in play_info['data']['durl']:
                    suffix = re.search(r'\.([a-zA-Z0-9]+)\?', i['url']).group(1)
                    other.append(Media(base_url=i['url'], backup_url=i['backup_url'], suffix=suffix))
            except KeyError:
                pass
        # extract img url
        img_url = re.search('property="og:image" content="([^"]*)"', html).groups()[0]
        if not img_url.startswith('http'):  # https://github.com/HFrost0/bilix/issues/52 just for some video
            img_url = 'http:' + img_url.split('@')[0]
        # construct data
        video_info = VideoInfo(title=title, h1_title=h1_title, aid=aid, cid=cid, status=status,
                               p=p, pages=pages, img_url=img_url, bvid=bvid, dash=dash, other=other)
        return video_info


@raise_api_error
async def get_video_info(client: httpx.AsyncClient, url: str) -> VideoInfo:
    try:
        # try to get video info from web front-end first
        return await _get_video_info_from_html(client, url)
    except APIInvalidError:
        # try to get video info from api if web front-end is banned
        return await _get_video_info_from_api(client, url)


async def _get_video_info_from_html(client: httpx.AsyncClient, url: str) -> VideoInfo:
    res = await req_retry(client, url, follow_redirects=True)
    if str(res.url).startswith("https://www.bilibili.com/festival"):
        raise APIInvalidError("特殊节日页面", url)
    video_info = VideoInfo.parse_html(url, res.text)
    return video_info


async def _get_video_info_from_api(client: httpx.AsyncClient, url: str) -> VideoInfo:
    assert '/av' in url or '/BV' in url  # TODO: only support BV or av url
    video_info = await _get_video_basic_info_from_api(client, url)
    # can not be parallelized since we need to get cid first
    await _attach_dash_and_durl_from_api(client, video_info)
    return video_info


async def _attach_dash_and_durl_from_api(client: httpx.AsyncClient, video_info: VideoInfo) \
        -> Tuple[Dash, List[Media]]:
    params = {'cid': video_info.cid, 'bvid': video_info.bvid,
              'qn': 116,  # 1080P60（请求 DASH 会取到所有分辨率的流地址，应该不用设置 qn）
              'fnval': 4048,  # 请求 dash 格式的全部可用流
              'fourk': 1,  # 请求 4k 资源
              'fnver': 0, 'platform': 'pc', 'otype': 'json'}
    dash_response = await req_retry(client, 'https://api.bilibili.com/x/player/playurl',
                                    params=params, follow_redirects=True)
    dash_json = json.loads(dash_response.text)
    if dash_json['code'] != 0:
        raise APIResourceError(dash_json['message'], video_info.bvid)
    dash, other = None, []
    if 'dash' in dash_json['data']:
        dash = Dash.from_dict(dash_json)
    if 'durl' in dash_json['data']:
        # 请求了 dash ，API 应该永远不会返回 durl 资源。解析一下以防万一
        assert len(dash_json['data']['durl']) == 1, "durl 中返回了多个视频流，这可能是错误？请报告"
        for i in dash_json['data']['durl']:
            suffix = re.search(r'\.([a-zA-Z0-9]+)\?', i['url']).group(1)
            other.append(Media(base_url=i['url'], backup_url=i['backup_url'], size=i['size'], suffix=suffix))
    video_info.dash, video_info.other = dash, other


async def _get_video_basic_info_from_api(client: httpx.AsyncClient, url) -> VideoInfo:
    """通过 view api 获取视频的基本信息，不包括 dash 或 durl(other) 视频流资源"""
    aid, bvid, selected_page_num = parse_ids_from_url(url)
    params = {'bvid': bvid} if bvid else {'aid': aid}
    r = await req_retry(client, 'https://api.bilibili.com/x/web-interface/view',
                        params=params, follow_redirects=True)
    raw_json = json.loads(r.text)
    if raw_json['code'] != 0:
        raise APIResourceError(raw_json['message'], raw_json['message'])
    title = legal_title(raw_json['data']['title'])
    h1_title = title  # TODO: 根据视频类型，使 h1_title 与实际网页标题的格式一致
    aid = raw_json['data']['aid']
    bvid = raw_json['data']['bvid']
    base_url = f"https://www.bilibili.com/video/{bvid}/"
    status = Status(**raw_json['data']['stat'])
    pages = []
    p = None
    cid = None
    for idx, i in enumerate(raw_json['data']['pages']):
        page_num = int(i['page'])
        if page_num == selected_page_num:
            p = idx  # selected_page_num 的分p 在 pages 列表中的 index 位置
            cid = int(i['cid'])  # selected_page_num 的分p 的 cid
        p_url = f"{base_url}?p={page_num}"
        p_name = f"P{page_num}-{i['part']}"
        pages.append(Page(p_name=p_name, p_url=p_url))
    assert p is not None, f"没有找到分P: p{selected_page_num}，请检查输入"  # cid 也会是 None
    img_url = raw_json['data']['pic']
    basic_video_info = VideoInfo(title=title, h1_title=h1_title, aid=aid, cid=cid, status=status,
                                 p=p, pages=pages, img_url=img_url, bvid=bvid, dash=None, other=None)
    return basic_video_info


@raise_api_error
async def get_subtitle_info(client: httpx.AsyncClient, bvid, cid):
    params = {'bvid': bvid, 'cid': cid}
    res = await req_retry(client, 'https://api.bilibili.com/x/player/v2', params=params)
    info = json.loads(res.text)
    if info['code'] == -400:
        raise APIError(f'未找到字幕信息', params)
    return [[f'http:{i["subtitle_url"]}', i['lan_doc']] for i in info['data']['subtitle']['subtitles']]


@raise_api_error
async def get_dm_urls(client: httpx.AsyncClient, aid, cid) -> List[str]:
    params = {'oid': cid, 'pid': aid, 'type': 1}
    res = await req_retry(client, f'https://api.bilibili.com/x/v2/dm/web/view', params=params)
    view = parse_view(res.content)
    total = int(view['dmSge']['total'])
    return [f'https://api.bilibili.com/x/v2/dm/web/seg.so?oid={cid}&type=1&segment_index={i + 1}' for i in range(total)]


@raise_api_error
async def get_up_album_info(client: httpx.AsyncClient, url: str) -> Tuple[Dict, List[Dict]]:
    """todo it seems that page_size is not working, count may be incorrect"""
    uid = re.search(r'^https://space.bilibili.com/(\d+)/?', url).group(1)
    up_meta = asyncio.create_task(get_up_info(client, uid))
    res = await req_retry(client, f'https://api.bilibili.com/x/dynamic/feed/draw/upload_count?uid={uid}')
    count = json.loads(res.text)['data']['all_count']
    sema = asyncio.Semaphore(3)

    async def get_page(p: int):
        async with sema:
            params = {'uid': uid, 'page_num': p, 'page_size': ps, 'biz': 'all'}
            r = await req_retry(client, 'https://api.bilibili.com/x/dynamic/feed/draw/doc_list', params=params)
            data = json.loads(r.text)['data']['items']
            return data

    pn, ps, cur = 0, 30, 0
    cors = []
    while cur < count:
        cors.append(get_page(pn))
        pn += 1
        cur += ps
    lst = await asyncio.gather(*cors)
    lst = [item for d in lst for item in d]
    return await up_meta, lst
