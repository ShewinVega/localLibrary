from django.shortcuts import render
from .models import Book, BookInstance, BookLanguague, Author, Genre
from django.views.generic import ListView, DetailView
# Create your views here.


def index(request):
  """
  Funcion vista para la pagina de inicio del sitio
  """
  # Generar contadores de algunos de los objetos principales
  num_books = Book.objects.all().count()
  num_instances = BookInstance.objects.all().count()
  num_genre = Genre.objects.all().count()

  # Libros disponibles (status='a')
  num_instances_available = BookInstance.objects.filter(status__exact='a').count()

  num_authors=Author.objects.count() # El all() esta implicito en la linea de consulta

  # Books that contain 'hush' in the name

  num_name_books = Book.objects.filter(title__icontains='hush').count()

  return render(
    request,
    'catalog/index.html',
    {
      'num_books':num_books,
      'num_instances':num_instances,
      'num_instances_available':num_instances_available,
      'num_authors':num_authors,
      'num_genre':num_genre,
       'num_name_books':num_name_books,
    }
  )

# Lista de libros usando vistas basadas en clases
class BookListView(ListView):
  model = Book
  paginate_by = 4
  #Cambio de nombre de variable a utilizar en la plantilla renderizada
  context_object_name = 'my_book_list'

#############################
  """Indicarle que me mande una consulta en especifica
    y unicamente 3 datos de esta
   """
  #queryset = Book.objects.filter(title__icontains='hush')[:3]

  """
    Aunque el queryset lo podemos pedir de estaforma
     sobreescribiendo metodos en este tipo de vista
  """

  # def get_queryset(self):
      #return Book.objects.filter(title__icontains='hush')[:3]

#############################

  """
    Pasar variables de contexto adicionales a la
    plantilla sobreescribiendo el metodo get_context_data()
  """
  def get_context_data(self,**kwargs):
    # Llamando la implementacion base para obtener el contexto
    context = super().get_context_data(**kwargs)
    # escribimos el nombre de la clave del diccionario y le agregamos
    # el valor o contenido de nuestra conveniencia
    context['some_data'] = 'This is just some data' 
    return context

  """
    especificar nuestro propio template, o si la vista
    sera utilizada en varias plantillas o templates
  """
  # template_name = 'libros_list.html'


# Vista basada en clases de Detalle de libros
class BookDetailView(DetailView):
  model = Book    