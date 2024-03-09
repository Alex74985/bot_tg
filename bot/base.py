from models import session
from models import Base as BaseObj
from models import engine as BaseEngine


class DataBase:
	def select_all(self,Model,**filter_s):
		with session() as ses:
			query = ses.query(Model)
			if len(filter_s) > 0:
				query = query.filter_by(**filter_s)
		return query.all()


	def get_one(self,Model,**filter_s):
		with session() as ses:
			query = ses.query(Model)
			if len(filter_s) > 0:
				query = query.filter_by(**filter_s)
		return query.first()


	def test(self,Model,**filter_s):
		if self.get_one(Model,**filter_s):
			return True
		else:
			return False


	def new(self,Model,*args):
		tmp_new = Model(*args)
		with session() as ses:
			ses.add(tmp_new)
			ses.commit()
		return tmp_new


	def delete(self,Model,**filter_s):
		with session() as ses:
			obj = self.select_all(Model,**filter_s)
			if obj:
				for i in obj:
					ses.delete(i)
				ses.commit()
				return True
			else:
				return False


	def update(self,Model,set,**filter_s):
		with session() as ses:
			query = ses.query(Model)
			if len(filter_s) > 0:
				query = query.filter_by(**filter_s)
			query.update(set)
			ses.commit()
		return True


	def set_state(self, Model, *args):
		to_byte = Model(*args)
		with session() as ses:
			ses.add(to_byte)
			ses.commit()


	def base_init(self):
		BaseObj.metadata.create_all(BaseEngine)



d = DataBase()
d.base_init()
print('ok')
