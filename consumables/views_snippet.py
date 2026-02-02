@login_required
def stock_history(request):
    if not request.user.is_superuser:
        messages.error(request, "Access denied.")
        return redirect('home')
        
    # Get all items ordered by usage_count (Most Popular first)
    items = Item.objects.filter(usage_count__gt=0).order_by('-usage_count')
    
    return render(request, 'consumables/stock_history.html', {'items': items})
