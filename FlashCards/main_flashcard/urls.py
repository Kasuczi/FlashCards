from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

app_name = 'main_flashcard'

urlpatterns = [
    path('', views.fiszka_main, name='fiszka_main'),
    path('my_account/', views.my_account, name='my_account'),
    path('flashcards/', views.fiszka_proper, name='fiszka_proper'),
    path('signup/', views.sign_up, name='signup'),
    path('FlashcardsModel/create/', views.create_flash),
    path('like/', views.flashcard_like_system, name='like'),
]
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
