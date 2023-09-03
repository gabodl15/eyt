from django.db import models

# Create your models here.
class Lista(models.Model):
    # GUARDAMOS LA INFORMACION SOBRE UNA LISTA DE YOUTUBE
    name = models.CharField(max_length=200)
    num_videos = models.IntegerField()
    current_video = models.IntegerField(default=0)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def percentage(self):
        # CALCULAMOS EL PROGRESO EN PORCENTAJE DE UNA LISTA DE VIDEOS
        total_percentage = (self.current_video / self.num_videos) * 100
        return total_percentage

    def __str__(self):
        return self.name

class Video(models.Model):
    # GUARDAMOS CADA VIDEO DE UNA LISTA DE YOUTUBE
    # video_number: NUMERO DEL VIDEO DE ESA LISTA
    # video_time: TIEMPO TOTAL DEL VIDEO
    # video_current_time: TIEMPO EN EL QUE EL VIDEO VA EN LA REPRODUCCION
    #   - ESTO EN CASO DE QUE EL VIDEO SEA MUY LARGO Y NO SE PUEDA VER COMPLETO EN UN SOLO MOMENTO
    # is_watched: SI EL VIDEO HA SIDO VISTO COMPLETO, SE MARCA COMO True
    lista = models.ForeignKey(Lista, on_delete=models.CASCADE)
    name = models.CharField(max_length=200, null=False)
    url = models.URLField()
    youtube_id = models.CharField(max_length=50, unique=True)
    video_number = models.IntegerField()
    video_time = models.DurationField()
    video_current_time = models.IntegerField(default=0)
    is_watched = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def percentage(self):
        # CALCULAMOS EL PROGRESO EN PORCENTAJE DE UNA LISTA DE VIDEOS
        total_seconds = self.video_time.total_seconds()
        total_percentage = (self.video_current_time / total_seconds) * 100
        return total_percentage

    def __str__(self):
        return self.name
