from django.db import models

# Create your models here.
class DocType(models.Model):
    """
    """
    value=models.CharField(max_length=50, unique=True)

    def __str__(self):
        """
        """
        return self.value

class Query(models.Model):
    """
    """
    value=models.CharField(max_length=500)
    user=models.CharField(max_length=150)
    created_at=models.DateTimeField()

    def __str__(self):
        """
        """
        return self.value

class Category(models.Model):
    """
    """
    def __str__(self):
        """
        """
        self.value

class Doc(models.Model):
    """
    """
    url=models.URLField(max_length=500)
    target=models.URLField(max_length=500)
    related_queries=models.ManyToManyField("doCatalogue.docs.Query")
    doc_type=models.ForeignKey('doCatalogue.docs.DocType')
    categories=models.ManyToManyField("doCatalogue.docs.Category")

    def __str__(self):
        """
        """
        return self.target+"::"+self.url
