print(30 + 5 + 2)
print(30 + (5 + 2))
print(30 - 5)
print(30 * 5)
print(30 / 5)
print(30 ** 5)
print(30 // 5)
print(30 % 5)
blocks = db.relationship('Block', backref='subject', lazy='dynamic')