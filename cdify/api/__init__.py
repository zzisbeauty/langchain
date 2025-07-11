# 三 注册路由蓝图
from .health import health
from .kbs_kblist import kbs_kblist
from .kbs_kbdetail import kbs_kbdetail
from .kbs_kbcreate_update import kbs_kernel
from .kbs_kbrm import kbs_kbrm
from .kbs_ups import kbs_kbup
from .kbs_kbdoclist import kbs_kbdoclist
from .retrieval import retrieval
from .embeddings import emb_status

# from .chat_base import chat_base
# from .downfiles import downloadfiles

from .document_del import deldoc


all_blueprints = [
    health,
    kbs_kblist,
    kbs_kbdetail,
    kbs_kernel,
    kbs_kbrm,
    kbs_kbup,
    kbs_kbdoclist,
    retrieval,
    emb_status,

    # chat_base,
    # downloadfiles,
    
    deldoc
]