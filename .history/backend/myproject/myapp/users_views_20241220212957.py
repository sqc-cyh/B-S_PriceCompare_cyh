from django.utils import timezone
import json
# from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from django.contrib.auth import get_user_model
# from .models import cashier, employee
# from django.views.decorators.csrf import csrf_exempt
import random
from django.core.mail import send_mail
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate
from datetime import timedelta
import smtplib
from .models import Users  # 确保导入 User 模型
from .models import PriceAlert
from django.db import IntegrityError
from .models import Product  # 导入新模型
from .script.suning.Suning_Product import Suning_Product_Spider  # 导入爬虫类
# from .script.jd.JD_Product import JD_Product_Spider  # 导入爬虫类
# from .script.weipinhui.VIP_Product import Vip_Product_Spider  # 导入爬虫类
import os
from django.conf import settings
import subprocess
import csv
import re
def create_user(request):
    return HttpResponse("欢迎来到主页！")

def send_captcha(request):
    if request.method == 'POST':
        # 从请求体中获取数据
        body = json.loads(request.body)
        email = body.get('email')  # 直接从请求体中解析

        if not email:
            return JsonResponse({'message': '邮箱地址不能为空'}, status=400)

        str1 = '0123456789'
        rand_str = ''.join(random.choices(str1, k=6))  # 生成6位随机验证码
        message = f"您的验证码是{rand_str}，10分钟内有效，请尽快填写"
        emailBox = [email]

        # 发送邮件（确保已配置好邮件服务）
        try:
            send_mail('时清川商品比较网站验证码', message, 'sqc_cyh@163.com', emailBox, fail_silently=False)
            # 返回成功消息和验证码
            return JsonResponse({'message': '验证码已发送', 'captcha': rand_str})
        except Exception as e:
            return JsonResponse({'message': '发送邮件失败', 'error': str(e)}, status=500)

    return JsonResponse({'message': '仅支持 POST 请求'}, status=405)

def verify_captcha(request):
    if request.method == 'POST':
        body = json.loads(request.body)
        user_captcha = body.get('captcha')
        session_captcha = request.session.get('captcha')
        
        if user_captcha == session_captcha:
            return JsonResponse({'message': '验证码验证成功'})
        
        return JsonResponse({'message': '验证码错误'}, status=400)
    
def register(request):
    if request.method == 'POST':
        body = json.loads(request.body)
        username = body.get('username')
        email = body.get('email')
        password = body.get('password')

        if not all([username, email, password]):
            return JsonResponse({'message': '所有字段均为必填'}, status=400)

        try:
            # 创建用户实例并设置密码
            user = Users(username=username, email=email)
            user.set_password(password)  # 设置加密密码
            user.save()  # 保存用户到数据库
            return JsonResponse({'message': '注册成功'}, status=201)
        except IntegrityError as e:
            if 'UNIQUE constraint failed' in str(e):
                if 'username' in str(e):
                    return JsonResponse({'message': '用户名已被注册'}, status=400)
                elif 'email' in str(e):
                    return JsonResponse({'message': '邮箱已被注册'}, status=400)
            return JsonResponse({'message': '用户名或邮箱已存在'}, status=400)
        except Exception as e:
            return JsonResponse({'message': str(e)}, status=500)

    return JsonResponse({'message': '仅支持 POST 请求'}, status=405)

User = get_user_model()

def login(request):
    if request.method == 'POST':
        body = json.loads(request.body)
        username = body.get('username')
        password = body.get('password')

        # 使用自定义查询检查用户名和密码
        try:
            user = User.objects.get(username=username)
            if user.check_password(password):  # 检查密码
                return JsonResponse({'message': '登录成功'}, status=200)
            else:
                return JsonResponse({'message': '用户名或密码不正确'}, status=400)
        except User.DoesNotExist:
            return JsonResponse({'message': '用户名或密码不正确'}, status=400)

    return JsonResponse({'message': '仅支持 POST 请求'}, status=405)


def clean_price(price_str):
    """
    清洗价格字符串，移除非数字字符，并尝试转换为 float 类型。
    """
    try:
        # 移除价格中的非数字字符（如货币符号）
        clean_price_str = re.sub(r'[^\d.]', '', price_str)
        return float(clean_price_str)
    except ValueError:
        # 如果转换失败，返回 None 或抛出异常
        return None


def search_suning(request):
    # print('sdasdsad')
    if request.method == 'POST':
        body = json.loads(request.body)
        search_query = body.get('query')
        platform = body.get('platform')  # 获取平台参数

        if not search_query:
            return JsonResponse({'message': '搜索内容不能为空'}, status=400)

        # 根据平台参数选择爬虫实例
        spiders = {
            'suning': Suning_Product_Spider,
            # 'jd': JD_Product_Spider,
            # 'taobao': Vip_Product_Spider,
            # 'vip': Vip_Product_Spider,
        }
        SpiderClass = spiders.get(platform)
        if not SpiderClass:
            return JsonResponse({'message': '不支持的平台'}, status=400)

        spider = SpiderClass(search_query)
        products = spider.get_product_data()

        # 存储到数据库并过滤掉价格为None的商品
        saved_products = []
        current_time = timezone.now()  # 获取当前时间
        for product in products:
            name = product.get('title')
            image_url = product.get('img_link')
            price = product.get('price')

            if name is None:  # 跳过价格为None的商品
                continue
            if price is None:  # 跳过价格为None的商品
                continue
            if image_url is None:  # 跳过价格为None的商品
                continue


            product_instance = Product(
                name=name,
                image_url=image_url,
                price=price,
                platform=platform,  # 保存平台信息
                search_time = current_time # 存入当前时间
            )
            product_instance.save()
            saved_products.append(product)  # 将爬取的结果添加到列表中

        # 直接返回这次爬取的数据
        results = [{'name': prod['title'], 'image': prod['img_link'], 'price': prod['price'], 'platform': prod['price']} for prod in saved_products]
        print('------------')
        print(results)
        print('------------')
        return JsonResponse({'results': results}, status=200)

    return JsonResponse({'message': '仅支持 POST 请求'}, status=405)


def search_jd(request):
    print('ssss')
    body = json.loads(request.body)
    search_query = body.get('query')

    if not search_query:
        return JsonResponse({'message': '搜索内容不能为空'}, status=400)

    # 调用 jd.py 脚本
    jd_script_path = os.path.join(settings.BASE_DIR, 'myapp/script/jingdong/jd.py')  # jd.py 脚本的路径
    csv_file_name = f'京东{search_query}销售.csv'
    csv_file_path = os.path.join(settings.BASE_DIR, 'myapp/script/jingdong/data', csv_file_name)

    # 执行 jd.py 脚本并传入搜索关键词
    subprocess.run(['python', jd_script_path, search_query])

    # 确保 CSV 文件已生成
    if not os.path.exists(csv_file_path):
        return JsonResponse({'message': 'CSV文件未生成'}, status=500)

    current_time = timezone.now()  # 获取当前时间
    # 读取 CSV 文件并存储到数据库
    products = []
    with open(csv_file_path, 'r', encoding='utf-8-sig') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            price = clean_price(row['price'])
            if price is None:
                continue  # 如果价格清洗失败，则跳过此商品
            product_instance = Product(
                name=row['name'],
                image_url=row['img'],
                price=price,
                platform='jd',  # 保存平台信息
                search_time=current_time  # 存入当前时间
            )
            product_instance.save()
            products.append({
                'name': row['name'],
                'image': row['img'],
                'price': price,  # 直接使用 float 价格
                'platform': 'jd'
            })

    # 返回这次爬取的数据
    results = {'results': products}
    return JsonResponse(results, status=200)




def history(request):
    # 获取前端传入的 image_url 参数
    image_url = request.GET.get('image_url')
    
    if not image_url:
        return JsonResponse({'error': 'image_url parameter is required'}, status=400)

    # 查询数据库中匹配的条目，不限制时间范围
    products = Product.objects.filter(image_url=image_url)

    # 提取结果
    price_history = [{'price': prod.price, 'search_time': prod.search_time} for prod in products]

    # 返回 JSON 响应
    return JsonResponse({'data': price_history})



def set_price_alert(request):
    if request.method == 'POST':
        body = json.loads(request.body)

        name = body.get('name')          # 获取商品名称
        image_url = body.get('img')      # 获取商品图片 URL
        price = body.get('price')        # 获取商品价格
        platform = body.get('platform')   # 获取平台信息
        username = body.get('username')   # 获取用户名

        # 验证请求数据
        if not all([name, image_url, price, platform, username]):
            return JsonResponse({'message': '所有字段均为必填'}, status=400)

        try:
            # 创建 PriceAlert 实例并保存
            price_alert = PriceAlert(
                username=username,  # 将用户实例赋值给 user 字段
                name=name,
                image_url=image_url,
                price=price,  # 使用前端传来的价格
            )
            price_alert.save()

            return JsonResponse({'message': '降价提醒已设置成功'}, status=201)

        except IntegrityError:
            return JsonResponse({'message': '该商品的降价提醒已存在'}, status=400)
        except Exception as e:
            return JsonResponse({'message': str(e)}, status=500)

    return JsonResponse({'message': '仅支持 POST 请求'}, status=405)

def reset_password(request):
    if request.method == 'POST':
        body = json.loads(request.body)
        email = body.get('email')
        captcha = body.get('captcha')
        new_password = body.get('newPassword')

        print(email)
        print(captcha)
        print(new_password)
        # 验证请求数据
        if not all([email, captcha, new_password]):
            return JsonResponse({'message': '所有字段均为必填'}, status=400)


        try:
            user = User.objects.get(email=email)
            user.set_password(new_password)
            user.save()
            return JsonResponse({'message': '密码重置成功'}, status=200)
        except User.DoesNotExist:
            return JsonResponse({'message': '用户不存在'}, status=404)
        except Exception as e:
            print(f"Error occurred: {str(e)}")  # 记录错误
        return JsonResponse({'message': str(e)}, status=500)

    return JsonResponse({'message': '仅支持 POST 请求'}, status=405)

def check_price_alert(request):
    if request.method == 'POST':
        body = json.loads(request.body)
        image_url = body.get('image')
        platform = body.get('platform')

        print(image_url)
        print(platform)
        try:
            # 检查 PriceAlert 表中是否存在该商品
            exists = PriceAlert.objects.filter(image_url=image_url, platform=platform).exists()
            return JsonResponse({'exists': exists}, status=200)

        except Exception as e:
            return JsonResponse({'message': str(e)}, status=500)

    return JsonResponse({'message': '仅支持 POST 请求'}, status=405)

def search_price_alert(request):
    # 查询所有降价提醒表的记录
    print(request)
    data = json.loads(request.body)
    user = data.get('username')  # 从请求体中获取 username
    print(data)
    print(user)
    price_alerts = PriceAlert.objects.filter(username=user)
    print(user)
    # 构建返回的数据
    data = [
        {
            'id': alert.id,
            'name': alert.name,
            'imageUrl': alert.image_url,  # 商品图片URL
            'price': str(alert.price),  # 当前价格
            'updatedAt': alert.updated_at.isoformat(),  # 最后更新时间
        }
        for alert in price_alerts
    ]

    return JsonResponse(data, safe=False)

def remove_price_alert(request):
    try:
        # 解析请求体中的 JSON 数据
        data = json.loads(request.body)
        image_url = data.get('imageUrl')
        user = data.get('username')  # 从请求体中获取 username
        print(image_url)
        print(user)
        if not image_url:
            return JsonResponse({'error': '缺少参数: imageUrl'}, status=400)
        
        # 查找并删除对应的降价提醒
        alert = PriceAlert.objects.get(image_url=image_url, username=user)  # 确保是当前用户的提醒
        alert.delete()

        return JsonResponse({'message': '降价提醒已取消'}, status=204)
    except PriceAlert.DoesNotExist:
        return JsonResponse({'error': '降价提醒未找到'}, status=404)
    except json.JSONDecodeError:
        return JsonResponse({'error': '无效的请求数据'}, status=400)

    
def get_user_info(request):
    username = request.GET.get('username')
    
    if not username:
        return JsonResponse({'error': '缺少参数: username'}, status=400)

    try:
        # 根据 username 查询用户
        user = Users.objects.get(username=username)
        # 返回用户的邮箱和状态
        return JsonResponse({
            'email': user.email,
            'status': user.is_active and '正常' or '已禁用'  # 假设状态根据 is_active 字段决定
        })
    except Users.DoesNotExist:
        return JsonResponse({'error': '用户未找到'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
    
def has_pricedown(request):
    if request.method == 'GET':
        # 从请求中获取用户名
        username = request.GET.get('username')
        if not username:
            return JsonResponse({'error': '缺少参数: username'}, status=400)

        try:
            # 查询该用户设置的降价提醒商品
            price_alerts = PriceAlert.objects.filter(username=username)
            if not price_alerts:
                return JsonResponse({'message': '该用户没有设置降价提醒'}, status=200)

            # 检查每个降价提醒商品的价格是否有降低
            products_with_price_down = []
            for alert in price_alerts:
                # 根据 URL 判断平台并调用相应的搜索函数
                if 'suning' in alert.image_url:
                    response = search_suning(request, {'query': alert.name})
                else:
                    response = search_jd(request, {'query': alert.name})

                if response.status_code == 200:
                    results = response.data.get('results', [])
                    for result in results:
                        # 检查是否有价格降低
                        if result['price'] < alert.price:
                            products_with_price_down.append(result['name'])
                            break  # 找到降价商品后不再继续搜索

            # 返回有价格降低的商品名称
            if products_with_price_down:
                return JsonResponse({'message': '存在降价商品', 'products': products_with_price_down}, status=200)
            else:
                return JsonResponse({'message': '降价列表搜索完成：没有降价商品'}, status=200)

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=200)

    return JsonResponse({'error': '仅支持 GET 请求'}, status=405)