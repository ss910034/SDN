# -*- coding: utf-8 -*- 
#上行為處理中文問題
from ryu.base import app_manager
from ryu.ofproto import ofproto_v1_0

from ryu.controller import ofp_event
from ryu.controller.handler import MAIN_DISPATCHER
from ryu.controller.handler import set_ev_cls
'''
    set_ev_cls為一種裝飾器,主要作用為辨別副程式的以下兩種狀態：
    1. 負責事件
    2. 在何種溝通狀況下執行（RYU與SWITCH之間的溝通狀況）
'''
# Initialize
class L2Switch(app_manager.RyuApp):
    # 管理環境版本設定
    OFP_VERSIONS = [ofproto_v1_0.OFP_VERSION]
    def __init__(self, *_args, **_kwargs):
            super(L2Switch, self).__init__(*_args, **_kwargs)
    
    #負責packet-in事件且在Switch與RYU完成交握的狀況下執行
    @set_ev_cls(ofp_event.EventOFPPacketIn,MAIN_DISPATCHER)
    def packet_in_handler(self,ev):
        msg = ev.msg
        dp = msg.datapath
        ofp = dp.ofproto
        ofp_parser = dp.ofproto_parser
        actions = [ofp_parser.OFPActionOutput(ofp.OFPP_FLOOD)]
        out = ofp_parser.OFPPacketOut(datapath=dp, buffer_id=msg.buffer_id, in_port=msg.in_port)
        dp.send_msg(out)