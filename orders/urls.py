from . import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('orders', views.OrderViewSet, base_name='orders')
router.register('customers', views.CustomerViewSet, base_name='customers')
router.register('pizzas', views.PizzaViewSet, base_name='pizzas')

urlpatterns = router.urls
