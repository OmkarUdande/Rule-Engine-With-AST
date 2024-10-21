from django.db import models

class Rule(models.Model):
    rule_text = models.TextField() 
    ast = models.JSONField()       

    def __str__(self):
        return self.rule_text

class User(models.Model):
    age = models.IntegerField()          
    department = models.CharField(max_length=155)  
    salary = models.FloatField()          
    experience = models.IntegerField()    

    def __str__(self):
        return f"{self.department} - Age: {self.age}"
