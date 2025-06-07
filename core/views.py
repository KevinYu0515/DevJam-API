from django.shortcuts import render
from django.http import JsonResponse
from rest_framework import status
from rest_framework.decorators import api_view, parser_classes
from drf_spectacular.utils import extend_schema, OpenApiExample, OpenApiResponse
from rest_framework.response import Response
from rest_framework.parsers import FormParser
from .models import Product, Order, ShopOwner, ShopItem
from .serializers import ProductSerializer, OrderSerializer, ShopOwnerSerializer, ShopItemSerializer, User, UserSerializer

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
    # 指定請求格式為 UserSerializer，回應為 UserSerializer
    request={
        'application/x-www-form-urlencoded': UserSerializer,
    },
    responses={201: UserSerializer},
    # 提供範例請求資料
    examples=[
        OpenApiExample(
            'UserCreateExample',
            summary='User 新增範例',
            request_only=True,
            value={
                "username": "johndoe",
                "password": "SafePass123",
                "email": "johndoe@example.com",
                "user_type": "normal"
            }
        )
    ]
)
@api_view(['POST'])
def adduser(request):
    # 使用剛剛定義的 UserSerializer 處理輸入資料
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()  # 實際呼叫 create_user()
        # 成功時回傳序列化後的資料和 201 狀態碼
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    # 若驗證失敗，回傳錯誤訊息和 400 狀態碼
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
def getuser(request):
    users = User.objects.filter(user_type='disadvantage')
    serializer = UserSerializer(users, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)