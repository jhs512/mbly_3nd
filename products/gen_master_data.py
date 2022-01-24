from products.models import ProductCategoryItem, Product, ProductReal


def gen_master_product_category():
    ProductCategoryItem(name='구두').save()
    ProductCategoryItem(name='니트').save()
    ProductCategoryItem(name='롱스커트').save()
    ProductCategoryItem(name='숏스커트').save()
    ProductCategoryItem(name='청바지').save()
    ProductCategoryItem(name='청자켓').save()
    ProductCategoryItem(name='청치마').save()
    ProductCategoryItem(name='코트').save()
    ProductCategoryItem(name='백').save()
    ProductCategoryItem(name='블라우스').save()


def gen_product(market_id: int, name: str, display_name: str, price: int, opt_1_names: tuple[str, ...], is_hidden: bool,
                is_sold_out: bool, hit_count: int, review_count: int, review_point: int) -> None:
    cate_item_id = ProductCategoryItem.objects.filter(name=name).first().id

    opt_2_names = ('레드', '와인', '그린', '핑크',)
    opt_2_display_names = ('감성레드', '감성와인', '감성그린', '감성핑크',)

    product = Product(market_id=market_id, name=name, display_name=display_name, price=price, sale_price=price - 1000,
                      cate_item_id=cate_item_id, is_hidden=is_hidden, is_sold_out=is_sold_out, hit_count=hit_count,
                      review_count=review_count, review_point=review_point)
    product.save()

    for opt_1_name in opt_1_names:
        opt_1_display_name = opt_1_name
        for opt_2_index, opt_2_name in enumerate(opt_2_names):
            opt_2_display_name = opt_2_display_names[opt_2_index]
            ProductReal(product=product, option_1_name=opt_1_name, option_1_display_name=opt_1_display_name,
                        option_2_name=opt_2_name, option_2_display_name=opt_2_display_name).save()


def gen_master(apps, schema_editor):
    # 운영서버에서 테스트를 위해 임시로 허용
    # if not settings.DEBUG:
    #     return

    gen_master_product_category()

    price = 10000
    hit_count = 1000
    review_count = 100
    review_point = 3

    gen_product(1, '구두', '인스타 셀럽 구두', price, ('235, 3cm', '235, 6cm', '240, 3cm', '240, 6cm', '245, 3cm', '245, 6cm',),
                False, False, hit_count, review_count, review_point)
    gen_product(1, '구두', '아이돌 구두', price + 2000,
                ('235, 3cm', '235, 6cm', '240, 3cm', '240, 6cm', '245, 3cm', '245, 6cm',),
                False, False, hit_count + 500, review_count + 50, review_point + 1)

    price = 12000
    hit_count = 2000
    review_count = 200
    review_point = 4

    gen_product(1, '니트', '인스타 셀럽 니트', price, ('XS', 'S', 'M', 'L', 'XL',),
                False, False, hit_count, review_count, review_point)
    gen_product(1, '니트', '아이돌 니트', price + 2000,
                ('XS', 'S', 'M', 'L', 'XL',),
                False, False, hit_count + 500, review_count + 50, review_point + 1)

    price = 14000
    hit_count = 2000
    review_count = 200
    review_point = 4

    gen_product(1, '롱스커트', '인스타 셀럽 롱스커트', price, ('FREE',),
                False, False, hit_count, review_count, review_point)
    gen_product(1, '롱스커트', '아이돌 롱스커트', price + 2000,
                ('FREE',),
                False, False, hit_count + 500, review_count + 50, review_point + 1)

    price = 10000
    hit_count = 1000
    review_count = 100
    review_point = 2

    gen_product(1, '숏스커트', '인스타 셀럽 숏스커트', price, ('FREE',),
                False, False, hit_count, review_count, review_point)
    gen_product(1, '숏스커트', '아이돌 숏스커트', price + 2000,
                ('FREE',),
                False, False, hit_count + 500, review_count + 50, review_point + 1)

    price = 20000
    hit_count = 1300
    review_count = 130
    review_point = 3

    gen_product(2, '청바지', '인스타 셀럽 청바지', price, ('XS', 'S', 'M', 'L', 'XL',),
                False, False, hit_count, review_count, review_point)
    gen_product(2, '청바지', '아이돌 청바지', price + 2000,
                ('XS', 'S', 'M', 'L', 'XL',),
                False, False, hit_count + 500, review_count + 50, review_point + 1)

    price = 30000
    hit_count = 1400
    review_count = 140
    review_point = 3

    gen_product(2, '청자켓', '인스타 셀럽 청자켓', price, ('34', '36',),
                False, False, hit_count, review_count, review_point)
    gen_product(2, '청자켓', '아이돌 청자켓', price + 2000,
                ('34', '36',),
                False, False, hit_count + 500, review_count + 50, review_point + 1)

    price = 15000
    hit_count = 700
    review_count = 50
    review_point = 2

    gen_product(2, '청치마', '인스타 셀럽 청치마', price, ('FREE',),
                False, False, hit_count, review_count, review_point)
    gen_product(2, '청치마', '아이돌 청치마', price + 2000,
                ('FREE',),
                False, False, hit_count + 500, review_count + 50, review_point + 1)

    price = 75000
    hit_count = 1700
    review_count = 150
    review_point = 4

    gen_product(3, '코트', '인스타 셀럽 코트', price, ('FREE',),
                False, False, hit_count, review_count, review_point)
    gen_product(3, '코트', '아이돌 코트', price + 2000,
                ('FREE',),
                False, False, hit_count + 500, review_count + 50, review_point + 1)

    price = 175000
    hit_count = 1800
    review_count = 190
    review_point = 4

    gen_product(3, '백', '인스타 셀럽 백', price, ('FREE',),
                False, False, hit_count, review_count, review_point)
    gen_product(3, '백', '아이돌 백', price + 2000,
                ('FREE',),
                False, False, hit_count + 500, review_count + 50, review_point + 1)

    price = 25000
    hit_count = 800
    review_count = 90
    review_point = 2

    gen_product(3, '블라우스', '인스타 셀럽 블라우스', price, ('XS', 'S', 'M', 'L', 'XL',),
                False, False, hit_count, review_count, review_point)
    gen_product(3, '블라우스', '아이돌 블라우스', price + 2000,
                ('XS', 'S', 'M', 'L', 'XL',),
                False, False, hit_count + 500, review_count + 50, review_point + 1)
