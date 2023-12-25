from sqlalchemy import Column, DateTime, Boolean, Float, func, BigInteger

from afeng_tools.sqlalchemy_tools import sqlalchemy_settings
from afeng_tools.sqlalchemy_tools.core.sqlalchemy_meta_class import ModelMetaClass


def get_base_model(db_code: str = 'default') -> type:
    """获取基础Model"""
    Base = sqlalchemy_settings.get_database(db_code).Base

    class Model(Base, metaclass=ModelMetaClass):
        """模型根类"""
        __abstract__ = True

        id = Column(BigInteger, comment='主键', primary_key=True, index=True, autoincrement=True)
        add_time = Column(DateTime, comment='添加时间', default=func.now())
        update_time = Column(DateTime, comment='修改时间', default=func.now(), onupdate=func.now())
        is_enable = Column(Boolean, comment='是否可用', default=True)
        order_num = Column(Float, comment='排序值', default=100)

    return Model
