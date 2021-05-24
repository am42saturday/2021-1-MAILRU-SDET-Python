from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class AllRequests(Base):
    __tablename__ = 'all_requests'
    __table_args__ = {'mysql_charset': 'utf8'}

    def __repr__(self):
        return f"<All_requests(" \
               f"id='{self.id}'," \
               f"question='{self.question}'," \
               f"answer='{self.quantity}', " \
               f")>"

    id = Column(Integer, primary_key=True, autoincrement=True)
    question = Column(String(100), nullable=False)
    quantity = Column(Integer, nullable=False)


class RequestsByMethod(Base):
    __tablename__ = 'requests_by_method'
    __table_args__ = {'mysql_charset': 'utf8'}

    def __repr__(self):
        return f"<Requests_by_method(" \
               f"id='{self.id}'," \
               f"method='{self.method}'," \
               f"quantity='{self.quantity}', " \
               f")>"

    id = Column(Integer, primary_key=True, autoincrement=True)
    method = Column(String(300), nullable=False)
    quantity = Column(Integer, nullable=False)


class Top10FrequentRequest(Base):
    __tablename__ = 'top_10_frequent_requests'
    __table_args__ = {'mysql_charset': 'utf8'}

    def __repr__(self):
        return f"<Top_10_frequent_requests(" \
               f"id='{self.id}'," \
               f"url='{self.url}'," \
               f"quantity='{self.quantity}', " \
               f")>"

    id = Column(Integer, primary_key=True, autoincrement=True)
    url = Column(String(500), nullable=False)
    quantity = Column(Integer, nullable=False)


class Top5Largest4xxRequests(Base):
    __tablename__ = 'top_5_largest_4xx_requests'
    __table_args__ = {'mysql_charset': 'utf8'}

    def __repr__(self):
        return f"<Top_5_largest_4xx_requests(" \
               f"id='{self.id}'," \
               f"ip='{self.ip}'," \
               f"url='{self.url}'," \
               f"size='{self.size}'," \
               f"status_code='{self.status_code}'" \
               f")>"

    id = Column(Integer, primary_key=True, autoincrement=True)
    ip = Column(String(15), nullable=False)
    url = Column(String(500), nullable=False)
    size = Column(Integer, nullable=False)
    status_code = Column(String(3), nullable=False)


class Top5Users5xxRequests(Base):
    __tablename__ = 'top_5_users_5xx_requests'
    __table_args__ = {'mysql_charset': 'utf8'}

    def __repr__(self):
        return f"<Top_5_users_5xx_requests(" \
               f"id='{self.id}'," \
               f"ip='{self.ip}'," \
               f"quantity='{self.quantity}', " \
               f")>"

    id = Column(Integer, primary_key=True, autoincrement=True)
    ip = Column(String(15), nullable=False)
    quantity = Column(Integer, nullable=False)

