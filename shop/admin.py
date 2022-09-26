from django.contrib.admin import (
    ModelAdmin,
    site,
    register,
)
from django.contrib.contenttypes.models import ContentType

from .models import (
    Category,
    Blender,
    Combine,
    Fridge,
    Mixer,
    Panel,
    Teapot,
)

site.register(Category)


class AdminManageProduct(ModelAdmin):
    search_fields = ('name',)
    ordering = ('price',)
    fieldsets = None

    @staticmethod
    def set_connections(form, c_type):
        form.base_fields['content_type'].initial = c_type
        form.base_fields['content_type'].disabled = True
        form.base_fields['content_type'].widget.can_add_related = False
        form.base_fields['content_type'].widget.can_change_related = False

    def get_form(self, request, obj=None, change=False, **kwargs):
        form = super().get_form(request, obj, change, **kwargs)

        if hasattr(obj, 'content_type_id'):
            content_type = obj.content_type_id
        else:
            content_type = ContentType.objects.get(model=self.__class__.model.__name__.lower()).id

        self.set_connections(form, str(content_type))
        return form


@register(Blender)
class AdminManageBlender(AdminManageProduct):
    model = Blender
    list_display = ('name', 'price', 'in_stock', 'description', 'volume', 'fan_speed')


@register(Combine)
class AdminManageCombine(AdminManageProduct):
    model = Combine
    list_display = ('name', 'price', 'in_stock', 'description', 'volume', 'max_power')


@register(Fridge)
class AdminManageFridge(AdminManageProduct):
    model = Fridge
    list_display = ('name', 'price', 'in_stock', 'description', 'height', 'width', 'length')


@register(Mixer)
class AdminManageMixer(AdminManageProduct):
    model = Mixer
    list_display = ('name', 'price', 'in_stock', 'description', 'mixer_type', 'fan_speed', 'bowl_size')


@register(Panel)
class AdminManagePanel(AdminManageProduct):
    model = Panel
    list_display = ('name', 'price', 'in_stock', 'description', 'height', 'width', 'length')


@register(Teapot)
class AdminManageTeapot(AdminManageProduct):
    model = Teapot
    list_display = ('name', 'price', 'in_stock', 'description', 'volume', 'max_power')
