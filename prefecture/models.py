from random import choices
from django.db import models
from django.conf import settings
from .consts import MAX_RATE

RATE_CHOICES = [(x, str(x)) for x in range(0, MAX_RATE + 1)]
PREFECTURES = [
    ("北海道", "北海道"),
    ("青森県", "青森県"),
    ("岩手県", "岩手県"),
    ("宮城県", "宮城県"),
    ("秋田県", "秋田県"),
    ("山形県", "山形県"),
    ("福島県", "福島県"),
    ("茨城県", "茨城県"),
    ("栃木県", "栃木県"),
    ("群馬県", "群馬県"),
    ("埼玉県", "埼玉県"),
    ("千葉県", "千葉県"),
    ("東京都", "東京都"),
    ("神奈川県", "神奈川県"),
    ("新潟県", "新潟県"),
    ("富山県", "富山県"),
    ("石川県", "石川県"),
    ("福井県", "福井県"),
    ("山梨県", "山梨県"),
    ("長野県", "長野県"),
    ("岐阜県", "岐阜県"),
    ("静岡県", "静岡県"),
    ("愛知県", "愛知県"),
    ("三重県", "三重県"),
    ("滋賀県", "滋賀県"),
    ("京都府", "京都府"),
    ("大阪府", "大阪府"),
    ("兵庫県", "兵庫県"),
    ("奈良県", "奈良県"),
    ("和歌山県", "和歌山県"),
    ("鳥取県", "鳥取県"),
    ("島根県", "島根県"),
    ("岡山県", "岡山県"),
    ("広島県", "広島県"),
    ("山口県", "山口県"),
    ("徳島県", "徳島県"),
    ("香川県", "香川県"),
    ("愛媛県", "愛媛県"),
    ("高知県", "高知県"),
    ("福岡県", "福岡県"),
    ("佐賀県", "佐賀県"),
    ("長崎県", "長崎県"),
    ("熊本県", "熊本県"),
    ("大分県", "大分県"),
    ("宮崎県", "宮崎県"),
    ("鹿児島県", "鹿児島県"),
    ("沖縄県", "沖縄県"),
]

PREFECTURES_CODE = [
    ("1", "北海道"),
    ("2", "青森県"),
    ("3", "岩手県"),
    ("4", "宮城県"),
    ("5", "秋田県"),
    ("6", "山形県"),
    ("7", "福島県"),
    ("8", "茨城県"),
    ("9", "栃木県"),
    ("10", "群馬県"),
    ("11", "埼玉県"),
    ("12", "千葉県"),
    ("13", "東京都"),
    ("14", "神奈川県"),
    ("15", "新潟県"),
    ("16", "富山県"),
    ("17", "石川県"),
    ("18", "福井県"),
    ("19", "山梨県"),
    ("20", "長野県"),
    ("21", "岐阜県"),
    ("22", "静岡県"),
    ("23", "愛知県"),
    ("24", "三重県"),
    ("25", "滋賀県"),
    ("26", "京都府"),
    ("27", "大阪府"),
    ("28", "兵庫県"),
    ("29", "奈良県"),
    ("30", "和歌山県"),
    ("31", "鳥取県"),
    ("32", "島根県"),
    ("33", "岡山県"),
    ("34", "広島県"),
    ("35", "山口県"),
    ("36", "徳島県"),
    ("37", "香川県"),
    ("38", "愛媛県"),
    ("39", "高知県"),
    ("40", "福岡県"),
    ("41", "佐賀県"),
    ("42", "長崎県"),
    ("43", "熊本県"),
    ("44", "大分県"),
    ("45", "宮崎県"),
    ("46", "鹿児島県"),
    ("47", "沖縄県"),
]


class Prefecture(models.Model):
    name = models.CharField(verbose_name="都道府県", choices=PREFECTURES, max_length=10)
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Review(models.Model):
    prefecture = models.ForeignKey(Prefecture, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    text = models.TextField()
    rate = models.IntegerField(choices=RATE_CHOICES)
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    image = models.ImageField(null=True, blank=True)

    def __str__(self):
        return self.title
