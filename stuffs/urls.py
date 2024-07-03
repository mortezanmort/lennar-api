from django.urls import include, path
from rest_framework_nested import routers

from stuffs import viewsets

router = routers.DefaultRouter()

router.register("specifications", viewsets.SpecificationViewSet, basename="specification")
router.register("groups", viewsets.GroupViewSet, basename="group")
router.register("components", viewsets.ComponentViewSet, basename="component")

# Nested Routes
specifications_router = routers.NestedSimpleRouter(router, "specifications", lookup="specification")
specifications_router.register(r"groups", viewsets.NestedSpecificationGroupViewSet, basename="specification-groups")
specifications_router.register(
    r"components", viewsets.NestedSpecificationComponentsViewSet, basename="specification-components"
)

urlpatterns = [path("", include(router.urls)), path("", include(specifications_router.urls))]
