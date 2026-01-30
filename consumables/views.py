from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.forms import AuthenticationForm
from django.utils import timezone
from datetime import timedelta
from django.db.models import Sum, F, Q
from django.contrib.auth.models import User
from .models import Category, SubCategory, Item, ConsumptionRecord
from django.contrib import messages

# Authentication
def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
    else:
        form = AuthenticationForm()
    return render(request, 'consumables/login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('login')

# Core Navigation
@login_required
def home(request):
    # Only fetch categories to display main menu
    categories = Category.objects.all()
    return render(request, 'consumables/home.html', {'categories': categories})

@login_required
def view_category(request, category_id):
    category = get_object_or_404(Category.objects.prefetch_related('items', 'subcategories'), pk=category_id)
    subcategories = category.subcategories.all()
    # Direct items are those without a subcategory
    direct_items = category.items.filter(subcategory__isnull=True)
    
    return render(request, 'consumables/view_category.html', {
        'category': category,
        'subcategories': subcategories,
        'direct_items': direct_items
    })

@login_required
def view_subcategory(request, subcategory_id):
    subcategory = get_object_or_404(SubCategory, pk=subcategory_id)
    items = subcategory.items.all()
    return render(request, 'consumables/view_subcategory.html', {
        'subcategory': subcategory,
        'items': items
    })

@login_required
def take_item(request, item_id):
    item = get_object_or_404(Item, pk=item_id)
    if request.method == 'POST':
        qty = int(request.POST.get('quantity', 0))
        if qty > 0:
            if item.current_stock >= qty:
                item.current_stock -= qty
                item.save()
                ConsumptionRecord.objects.create(
                    user=request.user,
                    item=item,
                    quantity=qty
                )
                messages.success(request, f"Took {qty} {item.name}")
            else:
                 messages.error(request, f"Cannot take {qty}! Only {item.current_stock} available.")
        return redirect('home')
    # If GET, show confirmation page/modal? 
    # The UI flow says "When press Take button next page It will ask Quantity... |Confirm|"
    return render(request, 'consumables/take_item.html', {'item': item})

@login_required
def today(request):
    # Show ALL records for today? Or just user's?
    # "user will reach into Today section... and can see that day Took element list"
    # "Edit delete option too."
    records = ConsumptionRecord.objects.filter(date=timezone.now().date()).order_by('-timestamp')
    return render(request, 'consumables/today.html', {'records': records})

@login_required
def delete_consumption(request, record_id):
    record = get_object_or_404(ConsumptionRecord, pk=record_id)
    # Restore stock
    item = record.item
    item.current_stock += record.quantity
    item.save()
    record.delete()
    messages.success(request, "Record deleted and stock restored.")
    return redirect('today')

@login_required
def stock_list(request):
    categories = Category.objects.prefetch_related('items').all()
    return render(request, 'consumables/stock_list.html', {'categories': categories})

@login_required
def low_stock_list(request):
    # Filter for items where stock is 0 or less than 25% of average
    # We must exclude items with 0 average_stock to avoids division issues, 
    # though model defaults to 0. Logic: if average is 0, it's never low stock unless we explicitly want it.
    # But model says if average <= 0 return 100% (Green). So we only care if average > 0.
    
    low_stock_items = Item.objects.filter(
        average_stock__gt=0
    ).filter(
        Q(current_stock__lte=0) | 
        Q(current_stock__lt=F('average_stock') * 0.25)
    ).order_by('category__name', 'name')
    
    return render(request, 'consumables/low_stock_list.html', {'items': low_stock_items})

@login_required
def update_stock(request, item_id):
    item = get_object_or_404(Item, pk=item_id)
    if request.method == 'POST':
        new_stock = request.POST.get('current_stock')
        if new_stock:
            item.current_stock = int(new_stock)
            item.save()
            messages.success(request, f"Stock updated for {item.name}")
    return redirect('stock_list')

# Management
@login_required
# Manage Categories
@login_required
def manage_categories(request):
    categories = Category.objects.all()
    return render(request, 'consumables/manage_categories.html', {'categories': categories})

@login_required
def add_category(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        if name:
            Category.objects.create(name=name)
            return redirect('manage_categories')
    return render(request, 'consumables/add_category.html')

@login_required
def edit_category(request, category_id):
    category = get_object_or_404(Category, pk=category_id)
    if request.method == 'POST':
        name = request.POST.get('name')
        if name:
            category.name = name
            category.save()
            messages.success(request, f"Category updated to '{name}'")
            return redirect('manage_categories')
    # Reuse add_category template or create new? Let's use a generic simple form 
    # But user wants 3-dot menu. This view handles the POST.
    # We need a template for editing category.
    return render(request, 'consumables/edit_category.html', {'category': category})

@login_required
def delete_category(request, category_id):
    if not request.user.is_superuser:
        messages.error(request, "Only admins can delete categories.")
        return redirect('manage_categories')
    category = get_object_or_404(Category, pk=category_id)
    name = category.name
    category.delete()
    messages.success(request, f"Category '{name}' deleted.")
    return redirect('manage_categories')


@login_required
def category_detail(request, category_id):
    category = get_object_or_404(Category.objects.prefetch_related('items', 'subcategories', 'subcategories__items'), pk=category_id)
    return render(request, 'consumables/category_detail.html', {'category': category})

@login_required
def add_subcategory(request, category_id):
    category = get_object_or_404(Category, pk=category_id)
    if request.method == 'POST':
        name = request.POST.get('name')
        if name:
            SubCategory.objects.create(name=name, category=category)
            messages.success(request, f"SubCategory '{name}' created.")
            return redirect('category_detail', category_id=category.id)
    return render(request, 'consumables/add_subcategory.html', {'category': category})

@login_required
def edit_subcategory(request, subcategory_id):
    subcategory = get_object_or_404(SubCategory, pk=subcategory_id)
    if request.method == 'POST':
        name = request.POST.get('name')
        if name:
            subcategory.name = name
            subcategory.save()
            messages.success(request, f"SubCategory updated.")
            return redirect('category_detail', category_id=subcategory.category.id)
    return render(request, 'consumables/edit_subcategory.html', {'subcategory': subcategory})

@login_required
def delete_subcategory(request, subcategory_id):
    if not request.user.is_superuser:
        messages.error(request, "Only admins can delete subcategories.")
        # Find category to redirect to
        subcategory = get_object_or_404(SubCategory, pk=subcategory_id)
        return redirect('category_detail', category_id=subcategory.category.id)
        
    subcategory = get_object_or_404(SubCategory, pk=subcategory_id)
    cat_id = subcategory.category.id
    subcategory.delete()
    messages.success(request, "SubCategory deleted.")
    return redirect('category_detail', category_id=cat_id)

@login_required
def add_item(request, category_id):
    category = get_object_or_404(Category, pk=category_id)
    subcategories = category.subcategories.all()
    
    if request.method == 'POST':
        name = request.POST.get('name')
        avg_stock = int(request.POST.get('average_stock', 0))
        cur_stock = int(request.POST.get('current_stock', 0))
        score = int(request.POST.get('score', 1))
        
        subcategory_id = request.POST.get('subcategory')
        subcategory = None
        if subcategory_id:
            subcategory = get_object_or_404(SubCategory, pk=subcategory_id)

        Item.objects.create(
            category=category,
            subcategory=subcategory,
            name=name,
            average_stock=avg_stock,
            current_stock=cur_stock,
            score=score
        )
        return redirect('category_detail', category_id=category.id)
    return render(request, 'consumables/add_item.html', {'category': category, 'subcategories': subcategories})

@login_required
def edit_item(request, item_id):
    item = get_object_or_404(Item, pk=item_id)
    subcategories = item.category.subcategories.all()
    
    if request.method == 'POST':
        item.name = request.POST.get('name')
        item.average_stock = int(request.POST.get('average_stock', 0))
        item.current_stock = int(request.POST.get('current_stock', 0))
        item.score = int(request.POST.get('score', 1))
        
        subcategory_id = request.POST.get('subcategory')
        item.subcategory = None # Default to None
        if subcategory_id:
            item.subcategory = get_object_or_404(SubCategory, pk=subcategory_id)
            
        item.save()
        return redirect('category_detail', category_id=item.category.id)
    return render(request, 'consumables/edit_item.html', {'item': item, 'subcategories': subcategories})

@login_required
def delete_item(request, item_id):
    # User requested all users can delete items
    item = get_object_or_404(Item, pk=item_id)
    cat_id = item.category.id
    item.delete()
    messages.success(request, "Item deleted.")
    return redirect('category_detail', category_id=cat_id)

# Profile & Leaderboard
@login_required
@login_required
def profile(request, user_id=None):
    if user_id and request.user.is_superuser:
        profile_user = get_object_or_404(User, pk=user_id)
    else:
        profile_user = request.user
        
    user_records = ConsumptionRecord.objects.filter(user=profile_user).order_by('-date')
    total_credits = sum(r.total_credits() for r in user_records)
    
    return render(request, 'consumables/profile.html', {
        'records': user_records,
        'total_credits': total_credits,
        'profile_user': profile_user
    })

@login_required
def leaderboard(request):
    users = User.objects.all()
    
    # 1. Lifetime Leaderboard
    lifetime_data = []
    for u in users:
        records = ConsumptionRecord.objects.filter(user=u)
        score = sum(r.total_credits() for r in records)
        if score > 0:
            lifetime_data.append({'user': u, 'score': score})
    lifetime_data.sort(key=lambda x: x['score'], reverse=True)
    
    # 2. Weekly Winner Logic
    today = timezone.now().date()
    days_since_friday = (today.weekday() - 4) % 7
    start_date = today - timedelta(days=days_since_friday)
    
    weekly_records = ConsumptionRecord.objects.filter(date__gte=start_date)
    # Calculate weekly scores
    weekly_scores = {}
    for r in weekly_records:
        if r.user not in weekly_scores:
            weekly_scores[r.user] = 0
        weekly_scores[r.user] += r.total_credits()
    
    # Find max score
    weekly_winner = None
    if weekly_scores:
        winner_user = max(weekly_scores, key=weekly_scores.get)
        weekly_winner = {'user': winner_user, 'score': weekly_scores[winner_user]}
        
    is_friday = (today.weekday() == 4)
    # FOR TESTING: Uncomment next line to force Friday view
    # is_friday = True 
    
    return render(request, 'consumables/leaderboard.html', {
        'lifetime_leaderboard': lifetime_data,
        'weekly_winner': weekly_winner,
        'is_friday': is_friday,
        'start_date': start_date
    })

# Staff Management
@login_required
def manage_staff(request):
    if not request.user.is_superuser:
        messages.error(request, "Access restricted to admins.")
        return redirect('home')
    staff_members = User.objects.all().order_by('username')
    return render(request, 'consumables/manage_staff.html', {'staff_members': staff_members})

@login_required
def add_staff(request):
    if not request.user.is_superuser:
        return redirect('home')
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '').strip()
        if username and password:
            if User.objects.filter(username=username).exists():
                messages.error(request, "Username already exists.")
            else:
                User.objects.create_user(username=username, password=password)
                messages.success(request, f"Staff {username} created.")
                return redirect('manage_staff')
    return render(request, 'consumables/add_staff.html')

@login_required
def edit_staff(request, user_id):
    if not request.user.is_superuser:
        return redirect('home')
    user_to_edit = get_object_or_404(User, pk=user_id)
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '').strip()
        
        # Edit Username
        if username and username != user_to_edit.username:
            if User.objects.filter(username=username).exists():
                messages.error(request, "Username taken.")
                return render(request, 'consumables/edit_staff.html', {'staff': user_to_edit})
            user_to_edit.username = username
        
        # Edit Password (Directly)
        if password:
            user_to_edit.set_password(password)
        
        user_to_edit.save()
        messages.success(request, f"Staff {user_to_edit.username} updated.")
        return redirect('manage_staff')
    return render(request, 'consumables/edit_staff.html', {'staff': user_to_edit})

@login_required
def delete_staff(request, user_id):
    if not request.user.is_superuser:
        return redirect('home')
    user_to_delete = get_object_or_404(User, pk=user_id)
    if user_to_delete == request.user:
        messages.error(request, "Cannot delete yourself.")
    else:
        user_to_delete.delete()
        messages.success(request, "Staff deleted.")
    return redirect('manage_staff')
