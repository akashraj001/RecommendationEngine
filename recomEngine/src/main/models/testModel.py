from mongoengine import Document, StringField, FloatField, IntField


class TestModel(Document):
    resendOtpSecs = "12345"
    kvUploadImageCount = "4"