from upload_machine.utils.uploader.piggo_upload import piggo_upload
from upload_machine.utils.uploader.hdsky_upload import hdsky_upload
from upload_machine.utils.uploader.audience_upload import audience_upload
from upload_machine.utils.uploader.ssd_upload import ssd_upload
from upload_machine.utils.uploader.pter_upload import pter_upload
from upload_machine.utils.uploader.hhclub_upload import hhclub_upload
from upload_machine.utils.uploader.lemonhd_upload import lemonhd_upload
from upload_machine.utils.uploader.hdpt_upload import hdpt_upload
from upload_machine.utils.uploader.wintersakura_upload import wintersakura_upload
from upload_machine.utils.uploader.carpt_upload import carpt_upload
from upload_machine.utils.uploader.hdfans_upload import hdfans_upload
from upload_machine.utils.uploader.hdkylin_upload import hdkylin_upload
from upload_machine.utils.uploader.ptvicomo_upload import ptvicomo_uploadc
from upload_machine.utils.uploader.hares_upload import hares_upload
from upload_machine.utils.uploader.zmpt_upload import zmpt_upload
from upload_machine.utils.uploader.hdvideo_upload import hdvideo_upload
from upload_machine.utils.uploader.ihdbits_upload import ihdbits_upload
from upload_machine.utils.uploader.redleaves_upload import redleaves_upload
from upload_machine.utils.uploader.mteam_upload import mteam_upload
from upload_machine.utils.uploader.sharkpt_upload import sharkpt_upload
from upload_machine.utils.uploader.zhuque_upload import zhuque_upload
from upload_machine.utils.uploader.dajiao_upload import dajiao_upload
from upload_machine.utils.uploader.pandapt_upload import pandapt_upload
from upload_machine.utils.uploader.rousi_upload import rousi_upload





def auto_upload(siteitem,file,record_path,qbinfo,basic,hashlist):
    return eval(siteitem.sitename+'_upload(siteitem,file,record_path,qbinfo,basic,hashlist)')