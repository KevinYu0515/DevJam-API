from venv import logger
from django.shortcuts import render
from django.http import JsonResponse
from rest_framework import status
from rest_framework.decorators import api_view, parser_classes
from drf_spectacular.utils import extend_schema, OpenApiExample, OpenApiResponse
from rest_framework.response import Response
from rest_framework.parsers import FormParser
from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import *
from core.models import *
from core.functions import *


# 商品列表視圖：處理 GET（獲取所有商品）和 POST（創建新商品）請求
@extend_schema(
    request={
        'application/x-www-form-urlencoded': ProductSerializer,
    },
    responses={
        200: ProductSerializer(many=True),   # GET 回傳多筆資料
        201: ProductSerializer,              # POST 成功回傳單筆資料
        400: OpenApiExample(
            "Bad Request Example",
            value={"price": ["This field is required."]},
            response_only=True
        )
    },
    examples=[
        OpenApiExample(
            "Form Example",
            value={"name": "Apple", "price": 25},
            request_only=True
        )
    ]
)
@api_view(['GET', 'POST'])
def product_list(request):
    # 處理 GET 請求：獲取所有商品
    if request.method == 'GET':
        # 從資料庫獲取所有商品
        products = Product.objects.all()
        # 將商品資料序列化（轉換成 JSON 格式）
        serializer = ProductSerializer(products, many=True)
        # 回傳序列化後的資料
        return Response(serializer.data)

    # 處理 POST 請求：創建新商品
    elif request.method == 'POST':
        # 將請求資料反序列化（轉換成 Python 物件）
        serializer = ProductSerializer(data=request.data)
        # 驗證資料是否有效
        if serializer.is_valid():
            # 儲存商品到資料庫
            serializer.save()
            # 回傳成功訊息和狀態碼 201（已創建）
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        # 如果資料無效，回傳錯誤訊息和狀態碼 400（錯誤請求）
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# 商品詳情視圖：處理 PUT（更新商品）和 DELETE（刪除商品）請求
@extend_schema(
    request={
        'application/x-www-form-urlencoded': ProductSerializer,
    },
    responses=ProductSerializer,
    examples=[
        OpenApiExample(
            "Form Example",
            value={"name": "Apple", "price": 25},
            request_only=True
        )
    ]
)
@api_view(['PUT', 'DELETE'])
def product_detail(request, pk):
    try:
        # 嘗試從資料庫獲取指定 ID 的商品
        product = Product.objects.get(pk=pk)
    except Product.DoesNotExist:
        # 如果商品不存在，回傳狀態碼 404（未找到）
        return Response(status=status.HTTP_404_NOT_FOUND)

    # 處理 PUT 請求：更新商品
    if request.method == 'PUT':
        # 將請求資料反序列化，並更新現有商品
        serializer = ProductSerializer(product, data=request.data)
        # 驗證資料是否有效
        if serializer.is_valid():
            # 儲存更新後的商品到資料庫
            serializer.save()
            # 回傳更新後的商品資料
            return Response(serializer.data)
        # 如果資料無效，回傳錯誤訊息和狀態碼 400（錯誤請求）
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # 處理 DELETE 請求：刪除商品
    elif request.method == 'DELETE':
        # 從資料庫刪除商品
        product.delete()
        # 回傳狀態碼 204（無內容）
        return Response(status=status.HTTP_204_NO_CONTENT)

# 訂單列表視圖：處理 GET（獲取所有訂單）和 POST（創建新訂單）請求
@extend_schema(
    request={
        'application/x-www-form-urlencoded': OrderSerializer,
    },
    responses={
        200: OrderSerializer(many=True),   # GET 回傳多筆訂單
        201: OrderSerializer,               # POST 創建成功回傳單筆訂單
        400: OpenApiResponse(description="Bad Request"),  # 失敗回應
    },
    examples=[
        OpenApiExample(
            name="Create Order Example",
            value={
                "product": 1,
                "user": 5,
                "amount": 2
            },
            request_only=True
        )
    ]
)
@api_view(['GET', 'POST'])
def order_list(request):
    if request.method == 'GET':
        # 獲取所有訂單
        orders = Order.objects.all()
        serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        # 創建新訂單
        serializer = OrderSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# 訂單詳情視圖：處理 DELETE（取消訂單）請求
@api_view(['DELETE'])
def order_detail(request, pk):
    try:
        order = Order.objects.get(pk=pk)
    except Order.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'DELETE':
        order.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

# 商店列表視圖：處理 GET（獲取所有商店）和 POST（創建新商店）請求
@extend_schema(
    request={
        'application/x-www-form-urlencoded': ShopOwnerSerializer,
    },
    responses={
        200: ShopOwnerSerializer(many=True),  # GET 回傳多筆商店資料
        201: ShopOwnerSerializer,              # POST 創建成功回傳單筆商店資料
        400: OpenApiResponse(description="Bad Request"),  # 錯誤回應
    },
    examples=[
        OpenApiExample(
            name="Create ShopOwner Example",
            value={
                "name": "小王便利店",
                "location": "台北市中正區",
                "headimage": "base64 or URL or skip if optional"
            },
            request_only=True
        )
    ]
)
@api_view(['GET', 'POST'])
def shopowner_list(request):
    if request.method == 'GET':
        # 獲取所有商店
        shopowners = ShopOwner.objects.all()
        serializer = ShopOwnerSerializer(shopowners, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        # 創建新商店
        serializer = ShopOwnerSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# 商店詳情視圖：只處理 GET（獲取單一商店）請求
@api_view(['GET'])
def shopowner_detail(request, pk):
    try:
        shopowner = ShopOwner.objects.get(pk=pk)
    except ShopOwner.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = ShopOwnerSerializer(shopowner)
        return Response(serializer.data)

# 商店商品列表視圖：處理 GET（獲取所有商品）和 POST（創建新商品）請求
@extend_schema(
    request={
        'application/x-www-form-urlencoded': ShopItemSerializer,
    },
     responses={
        200: ShopItemSerializer(many=True),  # GET 回傳多筆商品
        201: ShopItemSerializer,              # POST 創建成功回傳單筆商品
        400: OpenApiResponse(description="Bad Request"),
    },
    examples=[
        OpenApiExample(
            name="Create Shop Item Example",
            value={
                "shopID": 1,
                "itemName": "鮮奶茶",
                "price": "45.0"
            },
            request_only=True
        )
    ]
)
@api_view(['GET', 'POST'])
def shopitem_list(request):
    if request.method == 'GET':
        # 獲取所有商店商品
        items = ShopItem.objects.all()
        serializer = ShopItemSerializer(items, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        # 創建新商店商品
        serializer = ShopItemSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# 商店商品詳情視圖：處理 GET（獲取單一商品）、PUT（更新商品）和 DELETE（刪除商品）請求
@extend_schema(
    request={
        'application/x-www-form-urlencoded': ShopItemSerializer,
    },
    responses=ShopItemSerializer,
    examples=[
        OpenApiExample(
            name="Create Shop Item Example",
            value={
                "shopID": 1,
                "itemName": "鮮奶茶",
                "price": "45.0"
            },
            request_only=True
        )
    ]
)
@api_view(['GET', 'PUT', 'DELETE'])
def shopitem_detail(request, pk):
    try:
        item = ShopItem.objects.get(pk=pk)
    except ShopItem.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = ShopItemSerializer(item)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = ShopItemSerializer(item, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        item.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

@extend_schema(
    request={'application/x-www-form-urlencoded': UserSerializer},
    responses={201: UserSerializer},
    examples=[
        OpenApiExample(
            'UserCreateExample',
            summary='User 新增範例',
            request_only=True,
            value={
                "username": "johndoe",
                "password": "SafePass123",
                "email": "johndoe@example.com",
                "user_type": "normal",
                "headImage": "https://example.com/avatar.png",
                "account": "A123456789"
            }
        )
    ]
)
@api_view(['POST'])
def adduser(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@extend_schema(
    responses=UserSerializer(many=True),
    summary="取得 user_type 為 disadvantage 的所有使用者",
    examples=[
        OpenApiExample(
            'DisadvantageUsersExample',
            summary='範例回應',
            value=[
                {
                    "id": 1,
                    "username": "alice123",
                    "email": "alice@example.com",
                    "user_type": "disadvantage"
                },
                {
                    "id": 2,
                    "username": "bob456",
                    "email": "bob@example.com",
                    "user_type": "disadvantage"
                }
            ],
            response_only=True,
        )
    ]
)
@api_view(['GET'])
def getuser_disadv(request):
    users = User.objects.filter(user_type='disadvantage')
    serializer = UserSerializer(users, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

@extend_schema(
    responses=UserSerializer(many=True),
    summary="取得 user_type 為 normal 的所有使用者",
    examples=[
        OpenApiExample(
            'NormalUsersExample',
            summary='範例回應',
            value=[
                {
                    "id": 1,
                    "username": "alice123",
                    "email": "alice@example.com",
                    "user_type": "disadvantage"
                },
                {
                    "id": 2,
                    "username": "bob456",
                    "email": "bob@example.com",
                    "user_type": "disadvantage"
                }
            ],
            response_only=True,
        )
    ]
)
@api_view(['GET'])
def getuser_normal(request):
    users = User.objects.filter(user_type='normal')
    serializer = UserSerializer(users, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

# 商品列表視圖：處理 GET（獲取所有商品）和 POST（創建新商品）請求
@api_view(['GET', 'POST'])
def product_list(request):
    # 處理 GET 請求：獲取所有商品
    if request.method == 'GET':
        # 從資料庫獲取所有商品
        products = Product.objects.all()
        # 將商品資料序列化（轉換成 JSON 格式）
        serializer = ProductSerializer(products, many=True)
        # 回傳序列化後的資料
        return Response(serializer.data)

    # 處理 POST 請求：創建新商品
    elif request.method == 'POST':
        # 將請求資料反序列化（轉換成 Python 物件）
        serializer = ProductSerializer(data=request.data)
        # 驗證資料是否有效
        if serializer.is_valid():
            # 儲存商品到資料庫
            serializer.save()
            # 回傳成功訊息和狀態碼 201（已創建）
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        # 如果資料無效，回傳錯誤訊息和狀態碼 400（錯誤請求）
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# 商品詳情視圖：處理 PUT（更新商品）和 DELETE（刪除商品）請求
@api_view(['PUT', 'DELETE'])
def product_detail(request, pk):
    try:
        # 嘗試從資料庫獲取指定 ID 的商品
        product = Product.objects.get(pk=pk)
    except Product.DoesNotExist:
        # 如果商品不存在，回傳狀態碼 404（未找到）
        return Response(status=status.HTTP_404_NOT_FOUND)

    # 處理 PUT 請求：更新商品
    if request.method == 'PUT':
        # 將請求資料反序列化，並更新現有商品
        serializer = ProductSerializer(product, data=request.data)
        # 驗證資料是否有效
        if serializer.is_valid():
            # 儲存更新後的商品到資料庫
            serializer.save()
            # 回傳更新後的商品資料
            return Response(serializer.data)
        # 如果資料無效，回傳錯誤訊息和狀態碼 400（錯誤請求）
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # 處理 DELETE 請求：刪除商品
    elif request.method == 'DELETE':
        # 從資料庫刪除商品
        product.delete()
        # 回傳狀態碼 204（無內容）
        return Response(status=status.HTTP_204_NO_CONTENT)

# 訂單列表視圖：處理 GET（獲取所有訂單）和 POST（創建新訂單）請求
@api_view(['GET', 'POST'])
def order_list(request):
    if request.method == 'GET':
        # 獲取所有訂單
        orders = Order.objects.all()
        serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        # 創建新訂單
        serializer = OrderSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# 訂單詳情視圖：處理 DELETE（取消訂單）請求
@api_view(['DELETE'])
def order_detail(request, pk):
    try:
        order = Order.objects.get(pk=pk)
    except Order.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'DELETE':
        order.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

# 商店列表視圖：處理 GET（獲取所有商店）和 POST（創建新商店）請求
@api_view(['GET', 'POST'])
def shopowner_list(request):
    if request.method == 'GET':
        # 獲取所有商店
        shopowners = ShopOwner.objects.all()
        serializer = ShopOwnerSerializer(shopowners, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        # 創建新商店
        serializer = ShopOwnerSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# 商店詳情視圖：只處理 GET（獲取單一商店）請求
@api_view(['GET'])
def shopowner_detail(request, pk):
    try:
        shopowner = ShopOwner.objects.get(pk=pk)
    except ShopOwner.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = ShopOwnerSerializer(shopowner)
        return Response(serializer.data)

# 商店商品列表視圖：處理 GET（獲取所有商品）和 POST（創建新商品）請求
@api_view(['GET', 'POST'])
def shopitem_list(request):
    if request.method == 'GET':
        # 獲取所有商店商品
        items = ShopItem.objects.all()
        serializer = ShopItemSerializer(items, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        # 創建新商店商品
        serializer = ShopItemSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# 商店商品詳情視圖：處理 GET（獲取單一商品）、PUT（更新商品）和 DELETE（刪除商品）請求
@api_view(['GET', 'PUT', 'DELETE'])
def shopitem_detail(request, pk):
    try:
        item = ShopItem.objects.get(pk=pk)
    except ShopItem.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = ShopItemSerializer(item)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = ShopItemSerializer(item, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        item.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

# Coin API views
@api_view(['GET', 'POST'])
def coin_list(request):
    """
    處理硬幣的列表和創建
    GET: 獲取所有硬幣
    POST: 創建新硬幣
    """
    if request.method == 'GET':
        coins = Coin.objects.all()
        serializer = CoinSerializer(coins, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = CoinSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
def coin_detail(request, pk):
    """
    處理單個硬幣的獲取、更新和刪除
    GET: 獲取特定硬幣
    PUT: 更新硬幣
    DELETE: 刪除硬幣
    """
    try:
        coin = Coin.objects.get(pk=pk)
    except Coin.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        logger.error(f"Error retrieving coin: {str(e)}")
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    if request.method == 'GET':
        try:
            serializer = CoinSerializer(coin)
            return Response(serializer.data)
        except Exception as e:
            logger.error(f"Error serializing coin: {str(e)}")
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    elif request.method == 'PUT':
        try:
            # 檢查請求資料
            if not request.data:
                return Response({'error': '請求資料不能為空'}, status=status.HTTP_400_BAD_REQUEST)
            
            # 只更新提供的欄位
            serializer = CoinSerializer(coin, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            
            # 返回詳細的驗證錯誤
            error_details = {}
            for field, errors in serializer.errors.items():
                error_details[field] = str(errors[0])
            return Response({
                'error': '資料驗證失敗',
                'details': error_details
            }, status=status.HTTP_400_BAD_REQUEST)
            
        except Exception as e:
            logger.error(f"Error updating coin: {str(e)}")
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    elif request.method == 'DELETE':
        try:
            coin.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            logger.error(f"Error deleting coin: {str(e)}")
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        



@extend_schema(
    request=LoginSerializer,
    examples=[
        OpenApiExample(
            'LoginExample',
            summary='使用 account 和 password 登入',
            value={'account': 'user123', 'password': 'mypassword'},
            request_only=True,
        ),
    ],
)
@api_view(['POST'])
def login(request):
    serializer = LoginSerializer(data=request.data)
    if serializer.is_valid():
        return Response(serializer.validated_data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@extend_schema(
    request={
        'application/x-www-form-urlencoded': PurchaseHistorySerializer,
    },
    responses=PurchaseHistorySerializer(),
    summary="代購商品",
    examples=[
        OpenApiExample(
            'DisadvantageUsersExample',
            summary='範例回應',
            value={
                    "id": 1,
                    "uid": "1",
                    "itemID": "1",
                    "amount": "1"
                },
            response_only=True,
        )
    ]
)
@api_view(['POST'])
def process_purchase(request):
    jwt_payload = getattr(request, 'jwt_payload', None)

    if not jwt_payload:
        return Response({'error': 'Missing or invalid JWT'}, status=status.HTTP_401_UNAUTHORIZED)

    uid = jwt_payload.get('uid')
    username = jwt_payload.get('username')
    
    # 取得購買數量（可選，預設 1）
    amount = int(request.data.get('amount', 1))

    try:
        user = User.objects.get(id=uid, username=username)
    except User.DoesNotExist:
        return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

    try:
        item_id = request.data.get('item')
        item = ShopItem.objects.get(id=item_id)
    except ShopItem.DoesNotExist:
        return Response({'error': 'Item not found'}, status=status.HTTP_404_NOT_FOUND)

    # 建立購買紀錄
    history = purchase_item(uid, item_id, amount)

    return Response({
        'message': 'Purchase successful',
        'user': user.username,
        'item': item.itemName,
        'amount': amount,
        'history_id': history['data']['id']
    }, status=status.HTTP_201_CREATED)