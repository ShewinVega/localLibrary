from django.db import models
from django.urls import reverse #Used to generate URLs by reversing the URL patterns
import uuid # Requerida para las instancias de libros únicos

# Create your models here.



class Genre(models.Model):
    name = models.CharField(max_length=200, help_text="Ingrese el nombre del género (p. ej. Ciencia Ficción, Poesía Francesa etc.)")

    def __str__(self):
        return self.name


class Author(models.Model):
    """
    Modelo que representa un autor
    """
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    date_of_birth = models.DateField(null=True, blank=True)
    date_of_death = models.DateField('Died', null=True, blank=True)

    def get_absolute_url(self):
        """
        Retorna la url para acceder a una instancia particular de un autor.
        """
        return reverse('author-detail', args=[str(self.id)])


    def __str__(self):
        """
        String para representar el Objeto Modelo
        """
        textContent = '{0},{1}'
        return textContent.format(self.last_name, self.first_name)


class BookLanguague(models.Model):
    name: models.CharField('Lenguaje', max_length= 20, help_text="Enter the book's natural language (e.g. English, French, Japanese etc.)")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Creado')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Modificado')

    def __str__(self):
        return self.name
    

class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.ForeignKey('Author', on_delete=models.SET_NULL, null=True)
    summary = models.TextField(max_length=1000, help_text="Ingrese una breve descripción del libro")

    isbn = models.CharField('ISBN',max_length=13, help_text='13 Caracteres <a href="https://www.isbn-international.org/content/what-isbn">ISBN number</a>')

    genre = models.ManyToManyField(Genre, help_text="Seleccione un genero para este libro")

    def __str__(self):
        """
        String que representa al objeto Book
        """
        return self.title
 

    def get_absolute_url(self):
        """
        Devuelve el URL a una instancia particular de Book
        """
        return reverse('book-detail', args=[str(self.id)])

    # Agregando funcion para mandar a llamar Genre al Admin
    def display_genre(self):
        """
            Crea un string para el genre, requerido 'Ver comentario arriba'
        """
        return ','.join([Genre.name for Genre in self.genre.all()[:3]])
    display_genre.short_description = 'Genre'

class BookInstance(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, help_text="ID único para este libro particular en toda la biblioteca")
    book = models.ForeignKey('Book', on_delete=models.SET_NULL, null=True)
    imprint = models.CharField(max_length=200)
    due_back = models.DateField(null=True, blank=True)

    LOAN_STATUS = (
        ('m', 'Maintenance'),
        ('o', 'On loan'),
        ('a', 'Available'),
        ('r', 'Reserved'),
    )

    status = models.CharField(max_length=1, choices=LOAN_STATUS, blank=True, default='m', help_text='Disponibilidad del libro')

    class Meta:
        ordering = ["due_back"]


    def __str__(self):
        """
        String para representar el Objeto del Modelo
        """
        textContent = '{0} ({1})'
        return textContent.format(self.id,self.book.title)

