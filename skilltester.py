import random, operator, i18n, text2num, num2text
class SkillTestingQuestion():
	arith = (operator.add,operator.sub,operator.mul,
			 operator.add,operator.sub,operator.mul)
	logic = (operator.gt,operator.ge,
			 operator.lt,operator.le,
			 operator.eq,operator.ne)
	signs = {'add': ['+','plus'],
			 'sub': ['-', 'minus'],
			 'mul': ['*', 'times','multiplied by'],
			 'gt': ['>', 'greater than'],
			 'ge': ['>=', 'greater than or equal to'],
			 'lt': ['<', 'less than'],
			 'le': ['<=', 'less than or equal to'],
			 'eq': ['=', 'equal to'],
			 'ne': ['!=', 'not equal to']}
	def __init__(self, d=None):
		if d:
			self.x = d['x']
			self.y = d['y']
			self.op = getattr(operator, d['op'])
			self.wo = d['wo']
		else:
			self.x = random.randint(0, 10)
			self.y = random.randint(0, 10)
			self.op = random.choice(SkillTestingQuestion.arith + SkillTestingQuestion.logic)
		self.ans = self.op(self.x, self.y)
		if not d:
			self.wo = False
			# if a number can be unambiguously written out (only one way to write "ten",
			# two ways to write 21: twenty-one, twenty one), give it a chance that it
			# must be written out
			if self.ans in (range(0, 21)+[30,40,50,60,70,80,90]) and self.op in SkillTestingQuestion.arith:
				self.wo = random.choice([True, False])
	@property
	def as_dict(self):
		return {'x': self.x,
				'y': self.y,
				'op': self.op.__name__,
				'wo': self.wo}
	def question(self, lang):
		if self.op in SkillTestingQuestion.arith:
			# what is the result of x op y?
			fmt = random.choice(i18n.i18n[lang]['pages']['register']['question']['arithmetic'])
		elif self.op in SkillTestingQuestion.logic:
			# is x op y?
			fmt = random.choice(i18n.i18n[lang]['pages']['register']['question']['logic'])
		left = num2text.num2text(self.x).strip() if random.choice([True,False]) else self.x
		right = num2text.num2text(self.y).strip() if random.choice([True,False]) else self.y
		s = fmt % dict(left=left, op=random.choice(SkillTestingQuestion.signs[self.op.__name__]), right=right)
		if self.wo:
			s += ' %s' % i18n.i18n[lang]['pages']['register']['question']['wo']
		return s
	def check(self, ans):
		if self.wo:
			try:
				ans = text2num.text2num(str(ans))
			except:
				return False
		else:
			if self.op in SkillTestingQuestion.arith:
				try:
					ans = int(ans)
				except:
					return False
			else:
				try:
					if ans.lower() in ('true','yes','oui'):
						ans = True
					elif ans.lower() in ('false','no','non'):
						ans = False
					else:
						return False
				except:
					return False
		return ans == self.ans

if __name__ == '__main__':
	print SkillTestingQuestion().question('e')