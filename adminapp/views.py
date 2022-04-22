from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import render

# Create your views here.
from django.urls import reverse, reverse_lazy
from django.contrib.auth.decorators import user_passes_test
from django.views.generic import DetailView, ListView, DeleteView, UpdateView, CreateView, TemplateView

from adminapp.forms import UserAdminRegisterForm, AdminUserChange, AdminCategoryChange, \
    AdminProductCreate
from adminapp.mixin import AdminContextMixin, SuperuserDispatchMixin
from authapp.models import User
from mainapp.models import ProductCategory, Products


class AdminIndexView(TemplateView, SuperuserDispatchMixin, AdminContextMixin):
    template_name = 'adminapp/admin.html'
    title = 'GeekShop | Админка'


# @user_passes_test(lambda u: u.is_superuser, login_url='/login')
# def index(request):
#     context = {
#         'title': 'GeekShop | Админка'
#     }
#     return render(request, 'adminapp/admin.html', context)


class AdminShowUsersView(ListView, SuperuserDispatchMixin, AdminContextMixin):
    model = User
    template_name = 'adminapp/admin-users-read.html'
    title = 'Список пользователей'
    context_object_name = 'users'


# @user_passes_test(lambda u: u.is_superuser, login_url='/login')
# def admin_show_users(request):
#     context = {
#         'title': 'Список пользователей',
#         'users': User.objects.all()
#     }
#
#     return render(request, 'adminapp/admin-users-read.html', context)


class AdminCreateUserView(CreateView, SuperuserDispatchMixin, AdminContextMixin):
    model = User
    template_name = 'adminapp/admin-users-create.html'
    title = 'Создание пользователя'
    form_class = UserAdminRegisterForm
    success_url = reverse_lazy('adminapp:users')


# @user_passes_test(lambda u: u.is_superuser, login_url='/login')
# def admin_create_user(request):
#     if request.method == 'POST':
#         form = UserAdminRegisterForm(data=request.POST)
#         if form.is_valid():
#             form.save()
#             return HttpResponseRedirect(reverse('adminapp:users'))
#         else:
#             print(form.errors)
#     else:
#         form = UserAdminRegisterForm()
#
#     context = {
#         'title': 'Создание пользователя',
#         'form': form
#     }
#
#     return render(request, 'adminapp/admin-users-create.html', context=context)


class AdminUserUpdateView(UpdateView, SuperuserDispatchMixin, AdminContextMixin):
    form_class = AdminUserChange
    model = User
    template_name = 'adminapp/admin-users-update-delete.html'
    title = 'Профиль'
    success_url = reverse_lazy('adminapp:users')


# def admin_update_user(request, id):
#     if request.method == 'POST':
#         form = AdminUserChange(instance=request.user, data=request.POST, files=request.FILES)
#         if form.is_valid():
#             form.save()
#         else:
#             errors = [error for error in form.errors.values()]
#             messages.error(request, *errors)
#     else:
#         form = AdminUserChange()
#
#     context = {
#         'title': 'Профиль',
#         'form': form,
#     }
#
#     return render(request, 'adminapp/admin-users-update-delete.html', context)


class AdminUserDeleteView(DeleteView, SuperuserDispatchMixin, AdminContextMixin):
    form_class = AdminUserChange
    model = User
    template_name = 'adminapp/admin-users-update-delete.html'
    title = 'Удаление пользователя'
    success_url = reverse_lazy('adminapp:users')

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.is_active = False
        self.object.save()

        return HttpResponseRedirect(self.success_url)


# @user_passes_test(lambda u: u.is_superuser, login_url='/login')
# def admin_delete_user(request, id):
#     user_select = User.objects.get(id=id)
#     user_select.is_active = False
#     user_select.save()
#
#     return HttpResponseRedirect(reverse('adminapp:users'))


class AdminCategoryView(ListView, SuperuserDispatchMixin, AdminContextMixin):
    template_name = 'adminapp/admin_category_read.html'
    title = 'GeekShop | Админка'
    model = ProductCategory
    context_object_name = 'categories'
    success_url = reverse_lazy('adminapp:categories')


# @user_passes_test(lambda u: u.is_superuser, login_url='/login')
# def admin_category_show(request):
#     context = {
#         'title': 'Категории',
#         'categories': ProductCategory.objects.all(),
#     }
#
#     return render(request, 'adminapp/admin_category_read.html', context)


class AdminCategoryUpdateView(UpdateView, SuperuserDispatchMixin, AdminContextMixin):
    model = ProductCategory
    template_name = 'adminapp/admin_category_update-delete.html'
    form_class = AdminCategoryChange
    title = 'Обновление категории'
    context_object_name = 'product_cat_select'
    success_url = reverse_lazy('adminapp:categories')


# @user_passes_test(lambda u: u.is_superuser, login_url='/login')
# def admin_category_update(request, id):
#     product_cat_select = ProductCategory.objects.get(id=id)
#     if request.method == 'POST':
#         form = AdminCategoryChange(instance=product_cat_select, data=request.POST)
#         if form.is_valid():
#             form.save()
#             return HttpResponseRedirect(reverse('adminapp:categories'))
#         else:
#             print(form.errors)
#     else:
#         form = AdminCategoryChange(instance=product_cat_select)
#
#     context = {
#         'title': 'Обновление категории',
#         'form': form,
#         'product_cat_select': product_cat_select
#     }
#     return render(request, 'adminapp/admin_category_update-delete.html', context)


class AdminCategoryDeleteView(DeleteView, SuperuserDispatchMixin, AdminContextMixin):
    model = ProductCategory
    template_name = 'adminapp/admin_category_update-delete.html'
    success_url = reverse_lazy('adminapp:categories')

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.is_active = False
        self.object.save()

        return HttpResponseRedirect(self.success_url)


# @user_passes_test(lambda u: u.is_superuser, login_url='/login')
# def admin_category_delete(request, id):
#     category_select = ProductCategory.objects.get(id=id)
#     category_select.is_active = False
#     category_select.save()
#
#     return HttpResponseRedirect(reverse('adminapp:categories'))


class AdminCategoryCreateView(CreateView, SuperuserDispatchMixin, AdminContextMixin):
    model = ProductCategory
    title = 'Создание категории'
    template_name = 'adminapp/admin_category_create.html'
    form_class = AdminCategoryChange
    success_url = reverse_lazy('adminapp:categories')



# @user_passes_test(lambda u: u.is_superuser, login_url='/login')
# def admin_category_create(request):
#     if request.method == 'POST':
#         form = AdminCategoryChange(data=request.POST)
#         if form.is_valid():
#             form.save()
#             return HttpResponseRedirect(reverse('adminapp:categories'))
#         else:
#             errors = [error for error in form.errors.values()]
#             messages.error(request, *errors)
#     else:
#         form = AdminCategoryChange()
#
#     context = {
#         'title': 'Создание категории',
#         'form': form,
#     }
#
#     return render(request, 'adminapp/admin_category_create.html', context)


class AdminProductsShowView(ListView, SuperuserDispatchMixin, AdminContextMixin):
    title = 'Товары'
    model = Products
    context_object_name = 'products'
    template_name = 'adminapp/admin_products_show.html'



# @user_passes_test(lambda u: u.is_superuser, login_url='/login')
# def admin_products_show(request):
#     context = {
#         'title': 'Товары',
#         'products': Products.objects.all(),
#     }
#
#     return render(request, 'adminapp/admin_products_show.html', context)


class AdminProductCreateView(CreateView, SuperuserDispatchMixin, AdminContextMixin):
    title = 'Создание товара'
    template_name = 'adminapp/admin_products_create.html'
    form_class = AdminProductCreate
    model = Products



# @user_passes_test(lambda u: u.is_superuser, login_url='/login')
# def admin_product_create(request):
#     if request.method == 'POST':
#         form = AdminProductCreate(data=request.POST)
#         if form.is_valid():
#             form.save()
#             return HttpResponseRedirect(reverse('adminapp:admin_products_show'))
#         else:
#             errors = [error for error in form.errors.values()]
#             messages.error(request, *errors)
#     else:
#         form = AdminProductCreate()
#
#     context = {
#         'title': 'Создание товара',
#         'form': form,
#     }
#
#     return render(request, 'adminapp/admin_products_create.html', context)


class AdminProductChangeView(UpdateView, SuperuserDispatchMixin, AdminContextMixin):
    template_name = 'adminapp/admin_products_update-delete.html'
    title = 'Изменение товара'
    form_class = AdminProductCreate
    model = Products
    context_object_name = 'product_select'
    success_url = reverse_lazy('adminapp:admin_products_show')


# @user_passes_test(lambda u: u.is_superuser, login_url='/login')
# def admin_product_change(request, id):
#     product_select = Products.objects.get(id=id)
#     if request.method == 'POST':
#         form = AdminProductCreate(instance=product_select, data=request.POST)
#         if form.is_valid():
#             form.save()
#             return HttpResponseRedirect(reverse('adminapp:admin_products_show'))
#         else:
#             print(form.errors)
#     else:
#         form = AdminProductCreate(instance=product_select)
#
#     context = {
#         'title': 'Изменение товара',
#         'form': form,
#         'product_select': product_select
#     }
#     return render(request, 'adminapp/admin_products_update-delete.html', context)


class AdminProductDeleteView(DeleteView, SuperuserDispatchMixin, AdminContextMixin):
    model = Products
    success_url = reverse_lazy('adminapp:admin_products_show')

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.is_active = False
        self.object.save()

        return HttpResponseRedirect(self.success_url)


# @user_passes_test(lambda u: u.is_superuser, login_url='/login')
# def admin_product_delete(request, id):
#     product_select = Products.objects.get(id=id)
#     product_select.is_active = False
#     product_select.save()
#
#     return HttpResponseRedirect(reverse('adminapp:admin_products_show'))
