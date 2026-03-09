from django.contrib import admin
from .models import TechnicalSpecification, Mission, Task, Agent, Participation

admin.site.register(TechnicalSpecification)
admin.site.register(Mission)
admin.site.register(Task)
admin.site.register(Agent)
admin.site.register(Participation)