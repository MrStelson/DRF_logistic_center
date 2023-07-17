from rest_framework.routers import DefaultRouter

from api.views import UserModelViewSet, StorageModelViewSet, ProductModelViewSet, OrderModelViewSet

router = DefaultRouter()
router.register('users', UserModelViewSet)
router.register('storages', StorageModelViewSet)
router.register('products', ProductModelViewSet)
router.register('order', OrderModelViewSet)


urlpatterns = [

]

urlpatterns.extend(router.urls)
