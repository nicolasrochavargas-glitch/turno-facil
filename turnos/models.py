from django.db import models


class Turno(models.Model):
    ESTADOS = [
        ('pendiente', 'Pendiente'),
        ('atendiendo', 'Atendiendo'),
        ('atendido', 'Atendido'),
        ('cancelado', 'Cancelado'),
    ]

    numero = models.IntegerField()
    cliente = models.CharField(max_length=100)
    fecha = models.DateTimeField()
    necesidad = models.TextField()
    estado = models.CharField(
        max_length=20,
        choices=ESTADOS,
        default='pendiente'
    )

    def __str__(self):
        return f"Turno {self.numero} - {self.cliente}"