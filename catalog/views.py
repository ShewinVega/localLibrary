from django.forms import fields
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from .models import Book, BookInstance, BookLanguague, Author, Genre
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from .forms import RenewBookForm
import datetime

#@permission_required('catalog.can_mark_returned')
#@permission_required('catalog.can_edit')
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

  """Numero de Visitas a esta View, como esta contado en session"""

  num_visits = request.session.get('num_visits',0)
  request.session['num_visits'] = num_visits + 1

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
      'num_visits':num_visits
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


class AuthorListView(ListView):
  model = Author
  paginate_by = 2
  context_object_name = 'author_list'


class AuthorDetailView(DetailView):
  model = Author



"""Vista de Libros Prestados"""

class LoanedBooksByUserListView(LoginRequiredMixin,ListView):
  model = BookInstance
  template_name = 'catalog/bookInstance_list_borrowed_user.html'
  paginate_by = 3

  def get_queryset(self):
    return BookInstance.objects.filter(borrower=self.request.user).filter(status__exact='o').order_by('due_back')


"""Vista de libros prestados para unicamente Librarians parte del staff"""

class LoanedBooksForLibrarians(LoginRequiredMixin,ListView):
  model = BookInstance
  template_name = 'catalog/books_borrowed_librarians.html'
  paginate_by=3


  def get_queryset(self):
    return BookInstance.objects.filter(status__exact='o').order_by('due_back')


"""Vistas de Formularios"""
#@permission_required('catalog.can_mark_returned')
def renew_book_librarian(request, pk):
  book_instance = get_object_or_404(BookInstance, pk=pk)

  # If this is a POST request then process the form dta
  if request.method == 'POST':


    # Create a form instance and populate it with data from the request (binding):
    form = RenewBookForm(request.POST)


    # Check if the form is valid:
    if form.is_valid():

      # process the data in form.cleaned_data as required (here we just write it to the model due_back field)
      book_instance.due_back = form.cleaned_data['renewal_date']
      book_instance.save()

      # Redirect to a new URL
      return HttpResponseRedirect(reverse('catalog:librarians'))
  else:
    proposed_renewal_date = datetime.date.today() + datetime.timedelta(weeks=3)
    form = RenewBookForm(initial={'renewal_date': proposed_renewal_date,})

  return render(request, 'catalog/book_renew_librarian.html', {'form': form, 'bookinst':book_instance})



  """CRUD de Authores"""

class AuthorCreate(CreateView):
  model = Author
  fields = '__all__'
  initial = {'date_of_death':'05/01/2018',}
  template_name_suffix = '_suffix'
  success_url = reverse_lazy('catalog:author-detail')

class AuthorUpdate(UpdateView):
  model = Author
  fields = ['first_name','last_name','date_of_birth','date_of_death']
  template_name_suffix = '_suffix'
  success_url = reverse_lazy(' catalog:author-detail',)

class AuthorDelete(DeleteView):
  model = Author
  success_url = reverse_lazy('catalog:authors')
