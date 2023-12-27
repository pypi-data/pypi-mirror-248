from loguru import logger
import time
import os
from upload_machine.utils.uploader.upload_tools import *
import re
import cloudscraper

def hdfans_upload(siteinfo,file1,record_path,qbinfo,basic,hashlist):
    post_url = "https://hdfans.org/takeupload.php"
    tags=[]
    time_out=40
    if (file1.pathinfo.type=='anime' or file1.pathinfo.type=='tv') and file1.pathinfo.collection==0:
        fileinfo=file1.chinesename+'在'+siteinfo.sitename+'第'+file1.episodename+'集'
    else:
        fileinfo=file1.chinesename+'在'+siteinfo.sitename


    #选择类型
    if 'anime' in file1.pathinfo.type.lower():
        select_type='417'
    elif 'tv' in file1.pathinfo.type.lower() :
        select_type='402'
    elif 'movie' in file1.pathinfo.type.lower():
        select_type='401'
    elif 'show' in file1.pathinfo.type.lower():
        select_type='416'
    elif 'doc' in file1.pathinfo.type.lower():
        select_type='403'
    elif 'mv' in file1.pathinfo.type.lower():
        select_type='407'
    elif 'sport' in file1.pathinfo.type.lower():
        select_type='418'
    else:
        select_type='410'
    logger.info('已成功填写类型为'+file1.pathinfo.type)

    #选择媒介
    if file1.type=='WEB-DL':
        medium_sel='5'
    elif ('rip' in file1.type.lower() or file1.type=='bluray' and '1080p' in file1.standard_sel.lower()):
        medium_sel='24'
    elif ('rip' in file1.type.lower() or file1.type=='bluray' and '720p' in file1.standard_sel.lower()):
        medium_sel='25'
    elif file1.type=='HDTV':
        medium_sel='6'
    elif file1.type=='Remux':
        medium_sel='23'
    else:
        medium_sel='10'
    logger.info('已成功选择质量为'+file1.type)



    #选择编码
    if file1.Video_Format=='H264':
        codec_sel='1'
    elif file1.Video_Format=='x264':
        codec_sel='2'
    elif file1.Video_Format=='H265':
        codec_sel='3'
    elif file1.Video_Format=='x265':
        codec_sel='4'
    else:
        codec_sel='1'
    logger.info('已成功选择编码为'+file1.Video_Format)

    #选择音频编码
    if file1.Audio_Format.upper()=='AAC':
        audiocodec_sel='11'
    elif 'DTS-HDMA' in file1.Audio_Format.upper() or 'DTS-HD MA' in file1.Audio_Format.upper():
        audiocodec_sel='4'
    elif 'TRUEHD ATMOS' in file1.Audio_Format.upper():
        audiocodec_sel='1'
    elif 'LPCM' in file1.Audio_Format.upper():
        audiocodec_sel='7'
    elif 'TRUEHD' in file1.Audio_Format.upper():
        audiocodec_sel='6'
    elif 'FLAC' in file1.Audio_Format.upper():
        audiocodec_sel='12'
    elif 'APE' in file1.Audio_Format.upper():
        audiocodec_sel='13'
    elif 'MP3' in file1.Audio_Format.upper():
        audiocodec_sel='17'
    elif 'AC3' in file1.Audio_Format.upper() or 'AC-3' in file1.Audio_Format.upper():
        audiocodec_sel='10'
    elif 'DTS:X' in file1.Audio_Format.upper() or 'DTS-X' in file1.Audio_Format.upper() or 'DTS X' in file1.Audio_Format.upper():
        audiocodec_sel='3'
    elif 'DTS' in file1.Audio_Format.upper():
        audiocodec_sel='2'
    elif 'WAV' in file1.Audio_Format.upper():
        audiocodec_sel='14'
    elif 'M4A' in file1.Audio_Format.upper():
        audiocodec_sel='18'
    else:
        audiocodec_sel='18'
    logger.info('已成功选择音频编码为'+file1.Audio_Format.upper())

    #选择分辨率
    if '8K' in file1.standard_sel:
        standard_sel='1'
    elif '2160' in file1.standard_sel:
        standard_sel='2'
    elif '1080p' in file1.standard_sel.lower():
        standard_sel='3'
    elif '1080i' in file1.standard_sel.lower():
        standard_sel='4'
    elif '720' in file1.standard_sel:
        standard_sel='5'
    elif '480' in file1.standard_sel:
        standard_sel='6'
    else:
        standard_sel='7'
    logger.info('已成功选择分辨率为'+file1.standard_sel)
    
    #选择地区
    if not file1.country=='':
        if '大陆' in file1.country:
            processing_sel='1'
            logger.info('国家信息已选择'+file1.country)
        elif '香港' in file1.country:
            processing_sel='4'
            logger.info('国家信息已选择'+file1.country)
        elif '台湾' in file1.country:
            processing_sel='5'
            logger.info('国家信息已选择'+file1.country)
        elif '美国' in file1.country:
            processing_sel='2'
            logger.info('国家信息已选择'+file1.country)
        elif '英国' in file1.country:
            processing_sel='3'
            logger.info('国家信息已选择'+file1.country)
        elif '法国' in file1.country:
            processing_sel='8'
            logger.info('国家信息已选择'+file1.country)
        elif '韩国' in file1.country:
            processing_sel='7'
            logger.info('国家信息已选择'+file1.country)
        elif '日本' in file1.country:
            processing_sel='6'
            logger.info('国家信息已选择'+file1.country)
        elif '印度' in file1.country:
            processing_sel='10'
            logger.info('国家信息已选择'+file1.country)
        else:
            processing_sel='9'
            logger.info('未找到资源国家信息，已默认日本')
    else:
        processing_sel='6'
        logger.info('未找到资源国家信息，已默认日本')

    #选择制作组
    if 'hdfans' in file1.sub.lower():
        team_sel='9'
    elif 'chd' in file1.sub.lower():
        team_sel='1'
    elif 'hdc' in file1.sub.lower():
        team_sel='2'
    elif 'ttg' in file1.sub.lower():
        team_sel='19'
    elif 'wiki' in file1.sub.lower():
        team_sel='3'
    elif 'beast' in file1.sub.lower():
        team_sel='4'
    elif 'cmct' in file1.sub.lower():
        team_sel='5'
    elif 'frds' in file1.sub.lower():
        team_sel='6'
    elif 'hdsky' in file1.sub.lower():
        team_sel='7'
    elif 'ourbits' in file1.sub.lower():
        team_sel='17'
    elif 'pter' in file1.sub.lower():
        team_sel='20'
    elif 'league' in file1.sub.lower():
        team_sel='26'
    elif 'hdhome' in file1.sub.lower():
        team_sel='18'
    elif 'pthome' in file1.sub.lower():
        team_sel='16'
    elif 'tlf' in file1.sub.lower():
        team_sel='8'
    elif 'btn' in file1.sub.lower() or 'ntb' in file1.sub.lower():
        team_sel='32'
    elif 'hares' in file1.sub.lower():
        team_sel='28'
    elif 'audiences' in file1.sub.lower():
        team_sel='29'
    elif 'epsilon' in file1.sub.lower():
        team_sel='30'
    elif 'framestor' in file1.sub.lower():
        team_sel='31'
    else:
        team_sel='27'
    logger.info('制作组已成功选择为'+file1.sub)
    
    if 'hdfan' in file1.sub.lower():
        tags.append(3)
        logger.info('已选择官方')
    if 'hdfan' in file1.pathinfo.exclusive :
        tags.append(1)
        logger.info('已选择禁转')
    if '国' in file1.language or '中' in file1.language:
        tags.append(5)
        logger.info('已选择国语')
    if not file1.sublan=='' and ('简' in file1.sublan or '繁' in file1.sublan or '中' in file1.sublan):
        tags.append(6)
        logger.info('已选择中字')

    
    tags=list(set(tags))
    tags.sort()
    
    if siteinfo.uplver==1:
        uplver='yes'
    else:
        uplver='no'

    torrent_file = file1.torrentpath
    file_tup = ("file", (os.path.basename(torrent_file), open(torrent_file, 'rb'), 'application/x-bittorrent')),
            

    other_data = {
            "name": file1.uploadname,
            "small_descr": file1.small_descr+file1.pathinfo.exinfo,
            "url" : file1.imdburl,
            "color": "0",
            "font": "0",
            "size": "0",
            "descr": file1.pathinfo.contenthead+'\n'+file1.douban_info+'\n'+file1.screenshoturl+'\n'+file1.pathinfo.contenttail,
            "technical_info" : file1.mediainfo,
            "type": select_type,
            "medium_sel": medium_sel,
            "codec_sel": codec_sel,
            "audiocodec_sel": audiocodec_sel,
            "standard_sel": standard_sel,
            "processing_sel" : processing_sel,
            "team_sel": team_sel,
            "uplver": uplver,
            "tags[]": tags,
            }

    scraper=cloudscraper.create_scraper()
    success_upload=0
    try_upload=0
    while success_upload==0:
        try_upload+=1
        if try_upload>5:
            return False,fileinfo+' 发布种子发生请求错误,请确认站点是否正常运行'
        logger.info('正在发布种子')
        try:
            r = scraper.post(post_url, cookies=cookies_raw2jar(siteinfo.cookie),data=other_data, files=file_tup,timeout=time_out)
            success_upload=1
        except Exception as r:
            logger.warning('发布种子发生错误: %s' %(r))
            success_upload=0
    
    return afterupload(r,fileinfo,record_path,siteinfo,file1,qbinfo,hashlist)