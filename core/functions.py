from .models import Product, PurchaseHistory

def purchase_item(uid, item_id, amount):
    """
    購買商品並創建購買記錄的函數
    
    Args:
        uid (str): 使用者ID
        item_id (int): 商品ID
        amount (int): 購買數量
        
    Returns:
        dict: {
            'success': bool,  # 是否成功
            'message': str,   # 訊息
            'data': dict      # 購買記錄資料（如果成功）
        }
    """
    try:
        item = Product.objects.get(id=item_id)

        # 檢查庫存是否足夠
        if item.amount < amount:
            return {
                'success': False,
                'message': '商品庫存不足',
                'data': None
            }

        # 減少商品庫存
        item.amount -= amount
        item.save()

        # 創建購買記錄
        purchase = PurchaseHistory.objects.create(
            uid=uid,
            itemID=item_id,
            amount=amount
        )

        return {
            'success': True,
            'message': '購買成功',
            'data': {
                'id': purchase.id,
                'uid': purchase.uid,
                'itemID': purchase.itemID,
                'purchase_time': purchase.purchase_time
            }
        }
        
    except Product.DoesNotExist:
        return {
            'success': False,
            'message': '商品不存在',
            'data': None
        }
    except Exception as e:
        return {
            'success': False,
            'message': f'購買失敗：{str(e)}',
            'data': None
        } 