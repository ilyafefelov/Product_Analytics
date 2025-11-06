# Fefelov_Final Project-2
## Трекінг план для A/B тестування онлайн-реклами

**Автор:** Fefelov  
**Дата:** 6 листопада 2025 року  
**Курс:** GoIT Product Analytics - Final Project

---

## 1. Загальна інформація

### 1.1. Мета трекінг плану

Забезпечити повноцінне відслідковування поведінки користувачів на кожному етапі воронки конверсії для порівняння ефективності роботи контрольної та тестової груп A/B експерименту онлайн-реклами.

### 1.2. Рівень відслідковування

- **Платформа:** Рекламна платформа (Facebook Ads / Google Ads або аналогічна)
- **Інтеграція:** Pixel/Tag на вебсайті для відслідковування подій
- **Періодичність:** Real-time події + daily aggregation
- **Інструменти:** Facebook Pixel, Google Analytics, власна аналітична система

---

## 2. Визначення воронки продажів

### 2.1. Етапи воронки

```
┌─────────────────┐
│  1. IMPRESSIONS │  ← Показ реклами
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  2. CLICKS      │  ← Клік на рекламу
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  3. SEARCHES    │  ← Використання пошуку на сайті
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ 4. VIEW CONTENT │  ← Перегляд контенту/продуктів
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ 5. ADD TO CART  │  ← Додавання товару в кошик
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  6. PURCHASE    │  ← Завершення покупки
└─────────────────┘
```

### 2.2. Коефіцієнти конверсії

**Відслідковувані переходи між етапами:**
- Impressions → Clicks (CTR)
- Clicks → Searches (Click-to-Search Rate)
- Searches → View Content (Search-to-View Rate)
- View Content → Add to Cart (View-to-Cart Rate)
- Add to Cart → Purchase (Cart-to-Purchase Rate)
- Clicks → Purchase (Overall Conversion Rate)

---

## 3. Детальний опис подій (Events)

### Event 1: Ad Impression

**Назва події:** `ad_impression`

**Визначення:** Показ рекламного оголошення користувачу на платформі

**Джерело даних:** Рекламна платформа (Facebook Ads Manager / Google Ads)

**Тригер:** Коли рекламне оголошення завантажується на екрані користувача та є видимим

**Обов'язкові атрибути:**

| Атрибут | Тип даних | Опис | Приклад значення |
|---------|-----------|------|------------------|
| `campaign_name` | String | Назва кампанії | "Control Campaign", "Test Campaign" |
| `campaign_id` | String | Унікальний ID кампанії | "camp_12345" |
| `ad_group_id` | String | ID групи оголошень | "adset_67890" |
| `ad_id` | String | Унікальний ID конкретного оголошення | "ad_11111" |
| `timestamp` | DateTime | Час показу (ISO 8601) | "2019-08-01T10:23:45Z" |
| `user_id` | String | Псевдонімізований ID користувача | "fb_user_xyz123" |
| `placement` | String | Розміщення реклами | "feed", "story", "sidebar" |
| `device_type` | String | Тип пристрою | "mobile", "desktop", "tablet" |
| `platform` | String | Платформа | "facebook", "instagram" |

**Опціональні атрибути:**

| Атрибут | Тип даних | Опис |
|---------|-----------|------|
| `geo_country` | String | Країна користувача |
| `geo_city` | String | Місто користувача |
| `age_range` | String | Віковий діапазон |
| `gender` | String | Стать користувача |
| `language` | String | Мова інтерфейсу |

---

### Event 2: Ad Click (Website Click)

**Назва події:** `ad_click`

**Визначення:** Користувач клікнув на рекламне оголошення та був перенаправлений на вебсайт

**Джерело даних:** Рекламна платформа + Website Analytics

**Тригер:** Click event на рекламному оголошенні

**Обов'язкові атрибути:**

| Атрибут | Тип даних | Опис | Приклад значення |
|---------|-----------|------|------------------|
| `campaign_name` | String | Назва кампанії | "Control Campaign" |
| `campaign_id` | String | ID кампанії | "camp_12345" |
| `ad_id` | String | ID оголошення | "ad_11111" |
| `click_timestamp` | DateTime | Час кліку | "2019-08-01T10:24:12Z" |
| `user_id` | String | ID користувача | "fb_user_xyz123" |
| `session_id` | String | ID сесії на сайті | "sess_abc456" |
| `landing_page` | String | URL сторінки призначення | "/products/category-a" |
| `utm_source` | String | UTM source | "facebook" |
| `utm_medium` | String | UTM medium | "cpc" |
| `utm_campaign` | String | UTM campaign | "test_campaign_aug" |
| `device_type` | String | Тип пристрою | "mobile" |
| `referrer` | String | HTTP referrer | "https://facebook.com" |

**Опціональні атрибути:**

| Атрибут | Тип даних | Опис |
|---------|-----------|------|
| `browser` | String | Браузер користувача |
| `os` | String | Операційна система |
| `screen_resolution` | String | Роздільна здатність екрану |
| `click_position` | String | Позиція кліку на оголошенні |

---

### Event 3: Site Search

**Назва події:** `site_search`

**Визначення:** Користувач скористався функцією пошуку на вебсайті

**Джерело даних:** Website Analytics / Backend logs

**Тригер:** Submit форми пошуку або search API call

**Обов'язкові атрибути:**

| Атрибут | Тип даних | Опис | Приклад значення |
|---------|-----------|------|------------------|
| `session_id` | String | ID сесії | "sess_abc456" |
| `user_id` | String | ID користувача | "fb_user_xyz123" |
| `search_timestamp` | DateTime | Час пошуку | "2019-08-01T10:25:30Z" |
| `search_query` | String | Пошуковий запит | "winter jacket" |
| `search_results_count` | Integer | Кількість результатів | 24 |
| `search_page` | String | URL сторінки пошуку | "/search" |
| `campaign_source` | String | Джерело кампанії | "test_campaign" |

**Опціональні атрибути:**

| Атрибут | Тип даних | Опис |
|---------|-----------|------|
| `search_category` | String | Обрана категорія фільтру |
| `search_filters` | JSON | Застосовані фільтри |
| `search_sort` | String | Метод сортування результатів |
| `search_type` | String | Тип пошуку ("autocomplete", "full") |

---

### Event 4: View Content

**Назва події:** `view_content`

**Визначення:** Користувач переглянув сторінку продукту або контенту

**Джерело даних:** Facebook Pixel / Google Analytics / Custom tracking

**Тригер:** Page load події продуктової сторінки або scroll depth > 50%

**Обов'язкові атрибути:**

| Атрибут | Тип даних | Опис | Приклад значення |
|---------|-----------|------|------------------|
| `session_id` | String | ID сесії | "sess_abc456" |
| `user_id` | String | ID користувача | "fb_user_xyz123" |
| `view_timestamp` | DateTime | Час перегляду | "2019-08-01T10:26:15Z" |
| `content_type` | String | Тип контенту | "product", "category", "article" |
| `content_id` | String | ID продукту/контенту | "prod_7890" |
| `content_name` | String | Назва продукту | "Winter Jacket Blue M" |
| `content_category` | String | Категорія | "Outerwear > Jackets" |
| `page_url` | String | URL сторінки | "/products/winter-jacket-7890" |
| `campaign_source` | String | Джерело трафіку | "test_campaign" |

**Опціональні атрибути:**

| Атрибут | Тип даних | Опис |
|---------|-----------|------|
| `value` | Float | Вартість продукту (для FB Pixel) |
| `currency` | String | Валюта |
| `brand` | String | Бренд продукту |
| `time_on_page` | Integer | Час на сторінці (секунди) |
| `scroll_depth` | Float | Глибина прокрутки (%) |
| `product_variant` | String | Варіант продукту |
| `availability` | String | Наявність ("in_stock", "out_of_stock") |

---

### Event 5: Add to Cart

**Назва події:** `add_to_cart`

**Визначення:** Користувач додав продукт до кошика покупок

**Джерело даних:** Facebook Pixel / E-commerce backend / GA Enhanced Ecommerce

**Тригер:** Click на кнопку "Add to Cart" та успішне додавання

**Обов'язкові атрибути:**

| Атрибут | Тип даних | Опис | Приклад значення |
|---------|-----------|------|------------------|
| `session_id` | String | ID сесії | "sess_abc456" |
| `user_id` | String | ID користувача | "fb_user_xyz123" |
| `add_timestamp` | DateTime | Час додавання | "2019-08-01T10:27:45Z" |
| `content_id` | String | ID продукту | "prod_7890" |
| `content_name` | String | Назва продукту | "Winter Jacket Blue M" |
| `content_category` | String | Категорія | "Outerwear > Jackets" |
| `quantity` | Integer | Кількість | 1 |
| `value` | Float | Вартість товару | 129.99 |
| `currency` | String | Валюта | "USD" |
| `campaign_source` | String | Джерело кампанії | "test_campaign" |

**Опціональні атрибути:**

| Атрибут | Тип даних | Опис |
|---------|-----------|------|
| `product_variant` | String | Варіант (розмір, колір) |
| `discount_code` | String | Застосований промокод |
| `cart_total_value` | Float | Загальна вартість кошика |
| `cart_item_count` | Integer | Кількість товарів у кошику |
| `add_source` | String | Звідки додано ("pdp", "quickview") |
| `previous_page` | String | Попередня сторінка |

---

### Event 6: Purchase (Conversion)

**Назва події:** `purchase`

**Визначення:** Користувач успішно завершив покупку та оплатив замовлення

**Джерело даних:** E-commerce backend / Payment gateway / Facebook Pixel

**Тригер:** Успішна обробка платежу та створення замовлення

**Обов'язкові атрибути:**

| Атрибут | Тип даних | Опис | Приклад значення |
|---------|-----------|------|------------------|
| `session_id` | String | ID сесії | "sess_abc456" |
| `user_id` | String | ID користувача | "fb_user_xyz123" |
| `purchase_timestamp` | DateTime | Час покупки | "2019-08-01T10:30:22Z" |
| `order_id` | String | Унікальний ID замовлення | "order_555123" |
| `transaction_id` | String | ID транзакції | "txn_777888" |
| `value` | Float | Загальна сума покупки | 139.99 |
| `currency` | String | Валюта | "USD" |
| `num_items` | Integer | Кількість товарів | 1 |
| `campaign_source` | String | Джерело кампанії | "test_campaign" |
| `payment_method` | String | Метод оплати | "credit_card", "paypal" |

**Опціональні атрибути:**

| Атрибут | Тип даних | Опис |
|---------|-----------|------|
| `shipping_cost` | Float | Вартість доставки |
| `tax` | Float | Податок |
| `discount_amount` | Float | Сума знижки |
| `discount_code` | String | Використаний промокод |
| `shipping_method` | String | Метод доставки |
| `new_customer` | Boolean | Чи це перша покупка користувача |
| `content_ids` | Array | Масив ID куплених продуктів |
| `contents` | JSON | Детальна інформація про товари |

---

## 4. Додаткові події для поглибленого аналізу

### Event 7: Page View

**Назва:** `page_view`  
**Мета:** Відслідковування загальної навігації по сайту

**Ключові атрибути:**
- `session_id`, `user_id`, `page_url`, `page_title`, `referrer`, `campaign_source`

### Event 8: Cart View

**Назва:** `view_cart`  
**Мета:** Користувач відкрив кошик

**Ключові атрибути:**
- `session_id`, `cart_value`, `cart_item_count`, `campaign_source`

### Event 9: Checkout Started

**Назва:** `initiate_checkout`  
**Мета:** Користувач почав процес оформлення замовлення

**Ключові атрибути:**
- `session_id`, `checkout_value`, `num_items`, `campaign_source`

### Event 10: Session Start

**Назва:** `session_start`  
**Мета:** Початок сесії користувача на сайті

**Ключові атрибути:**
- `session_id`, `user_id`, `device_type`, `campaign_source`, `landing_page`

---

## 5. Агреговані метрики для аналізу

### 5.1. Щоденні метрики (Daily Aggregates)

Для кожної кампанії (Control / Test) щоденно розраховувати:

| Метрика | Формула | Опис |
|---------|---------|------|
| **Total Spend** | SUM(daily_budget_spent) | Витрати на рекламу за день |
| **Impressions** | COUNT(ad_impression) | Кількість показів |
| **Reach** | COUNT(DISTINCT user_id in ad_impression) | Унікальні користувачі |
| **Clicks** | COUNT(ad_click) | Кліки на рекламу |
| **Searches** | COUNT(site_search) | Користувачі, що використали пошук |
| **View Content** | COUNT(view_content) | Перегляди контенту |
| **Add to Cart** | COUNT(add_to_cart) | Додавання в кошик |
| **Purchases** | COUNT(purchase) | Кількість покупок |

### 5.2. Розраховані коефіцієнти

| Метрика | Формула | Значення для порівняння |
|---------|---------|-------------------------|
| **CTR** | (Clicks / Impressions) × 100% | Primary KPI |
| **Click-to-Search** | (Searches / Clicks) × 100% | Якість трафіку |
| **Search-to-View** | (View Content / Searches) × 100% | Релевантність пошуку |
| **View-to-Cart** | (Add to Cart / View Content) × 100% | Intent to purchase |
| **Cart-to-Purchase** | (Purchases / Add to Cart) × 100% | **KEY METRIC** |
| **Overall Conversion** | (Purchases / Clicks) × 100% | End-to-end ефективність |
| **Cost per Click** | Spend / Clicks | Ефективність витрат |
| **Cost per Purchase** | Spend / Purchases | ROI proxy |
| **ROAS proxy** | Purchases / Spend | Return on ad spend |

---

## 6. Атрибуція та ідентифікація користувачів

### 6.1. User ID та Session ID

**User ID:**
- **Джерело:** Facebook/Google User ID (псевдонімізований)
- **Призначення:** Зв'язування подій одного користувача через різні сесії
- **Формат:** Hash або encrypted ID для GDPR compliance

**Session ID:**
- **Джерело:** Генерується при заході на сайт (cookie/localStorage)
- **Тривалість:** 30 хвилин інактивності або закриття браузера
- **Призначення:** Групування подій в рамках одного візиту

### 6.2. Модель атрибуції

**Рекомендована модель:** Last-click attribution з використанням UTM параметрів

**Приклад UTM структури:**
```
utm_source=facebook
utm_medium=cpc
utm_campaign=test_campaign_aug2019
utm_content=ad_variant_A
utm_term=winter_jackets
```

**Збереження атрибуції:**
- First-touch: Зберігається при першому заході
- Last-touch: Оновлюється при кожному новому джерелі
- Session-based: Прив'язується до кожної сесії

---

## 7. Технічна реалізація трекінгу

### 7.1. Facebook Pixel Events

```javascript
// Event 2: Ad Click (landing)
fbq('track', 'PageView');

// Event 3: Site Search
fbq('track', 'Search', {
  search_string: 'winter jacket',
  content_category: 'Outerwear'
});

// Event 4: View Content
fbq('track', 'ViewContent', {
  content_ids: ['prod_7890'],
  content_type: 'product',
  value: 129.99,
  currency: 'USD'
});

// Event 5: Add to Cart
fbq('track', 'AddToCart', {
  content_ids: ['prod_7890'],
  content_type: 'product',
  value: 129.99,
  currency: 'USD',
  content_name: 'Winter Jacket'
});

// Event 6: Purchase
fbq('track', 'Purchase', {
  value: 139.99,
  currency: 'USD',
  content_ids: ['prod_7890'],
  content_type: 'product',
  num_items: 1
});
```

### 7.2. Google Analytics Enhanced Ecommerce

```javascript
// View Content
gtag('event', 'view_item', {
  items: [{
    id: 'prod_7890',
    name: 'Winter Jacket',
    category: 'Outerwear/Jackets',
    price: 129.99
  }]
});

// Add to Cart
gtag('event', 'add_to_cart', {
  items: [{
    id: 'prod_7890',
    name: 'Winter Jacket',
    price: 129.99,
    quantity: 1
  }]
});

// Purchase
gtag('event', 'purchase', {
  transaction_id: 'order_555123',
  value: 139.99,
  currency: 'USD',
  items: [...]
});
```

### 7.3. Custom Backend Tracking

**API endpoint:** `POST /api/events/track`

**Payload structure:**
```json
{
  "event_name": "site_search",
  "timestamp": "2019-08-01T10:25:30Z",
  "session_id": "sess_abc456",
  "user_id": "fb_user_xyz123",
  "properties": {
    "search_query": "winter jacket",
    "results_count": 24,
    "campaign_source": "test_campaign"
  }
}
```

---

## 8. Якість даних та валідація

### 8.1. Перевірки якості даних

**Щоденні перевірки:**
- ✅ Повнота даних: Чи є записи для всіх подій?
- ✅ Узгодженість: Чи є Add to Cart без View Content?
- ✅ Логічність послідовності: Purchases без попередніх Clicks?
- ✅ Відсутність дублікатів: Перевірка на duplicate events

**Алерти при аномаліях:**
- Різке падіння/зростання event counts (>50% від середнього)
- Missing data для певної кампанії
- Нульові значення в критичних полях

### 8.2. Обробка missing data

**Стратегія:**
1. **Критичні події** (Clicks, Purchases): Виключити день з аналізу якщо >80% даних відсутні
2. **Некритичні події** (Searches): Можна інтерполювати або використати median
3. **Документація:** Всі випадки missing data документувати

---

## 9. Privacy та Compliance

### 9.1. GDPR та CCPA compliance

- ✅ Отримання згоди на трекінг через Cookie Banner
- ✅ Можливість opt-out з tracking
- ✅ Псевдонімізація User ID
- ✅ Право на видалення даних (Right to be Forgotten)
- ✅ Encrypted storage всіх персональних даних

### 9.2. Знеособлення даних

- Не зберігаємо: email, phone, імена, адреси (окрім необхідного для доставки)
- Зберігаємо: Псевдонімізовані ID, агреговані метрики
- Retention policy: 2 роки для агрегатів, 90 днів для raw events

---

## 10. Дашборд та репортинг

### 10.1. Real-time дашборд

**Метрики для моніторингу:**
- Current day spend (Control vs Test)
- Running totals: Impressions, Clicks, Purchases
- Live CTR and Conversion Rates
- Alerts на anomalies

### 10.2. Daily report

**Формат:** CSV export або automated email

**Структура:**
```
Date | Campaign | Spend | Impressions | Reach | Clicks | Searches | ViewContent | AddToCart | Purchase
```

### 10.3. Analytical dashboard

**Інструмент:** Tableau / Power BI / Python Jupyter

**Візуалізації:**
- Funnel charts для Control vs Test
- Time series метрик
- Heatmaps конверсій
- Statistical significance indicators

---

## 11. Підсумок та чеклист

### 11.1. Чеклист готовності трекінгу

- [x] Facebook Pixel встановлено та налаштовано
- [x] Google Analytics Enhanced Ecommerce активовано
- [x] UTM параметри генеруються для всіх ads
- [x] Backend events логуються в database
- [x] Session та User ID коректно пробрасываються
- [x] Privacy compliance (GDPR) забезпечено
- [x] QA тестування всіх events на staging
- [x] Дашборд для моніторингу підготовлений
- [x] Alerts налаштовані на критичні метрики
- [x] Backup та disaster recovery план готовий

### 11.2. KPI для успішного трекінгу

- **Completeness:** >95% подій мають всі обов'язкові атрибути
- **Accuracy:** <1% duplicate events
- **Latency:** Events обробляються в <5 хвилин
- **Availability:** Tracking uptime >99.5%

---

**Підготував:** Fefelov  
**Версія:** 1.0  
**Дата:** 6 листопада 2025 року  
**Статус:** ✅ Готово до імплементації  
**Курс:** GoIT Product Analytics - Final Project
