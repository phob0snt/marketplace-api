from sqlalchemy.orm import Session
from app.models.product import Product
import logging

logger = logging.getLogger(__name__)


MOCK_PRODUCTS = [
    {
        "name": "Laptop Dell XPS 15",
        "description": "Мощный ноутбук для разработки и дизайна с процессором Intel Core i7, 16GB RAM, 512GB SSD",
        "price": 150000,
        "stock_quantity": 15,
    },
    {
        "name": "iPhone 15 Pro",
        "description": "Последняя модель iPhone с титановым корпусом, процессором A17 Pro и камерой 48MP",
        "price": 120000,
        "stock_quantity": 30,
    },
    {
        "name": "Sony WH-1000XM5",
        "description": "Беспроводные наушники с активным шумоподавлением и временем работы до 30 часов",
        "price": 35000,
        "stock_quantity": 50,
    },
    {
        "name": "Mechanical Keyboard Keychron K8",
        "description": "Механическая клавиатура с RGB подсветкой, переключатели Gateron Brown",
        "price": 8000,
        "stock_quantity": 100,
    },
    {
        "name": "Logitech MX Master 3S",
        "description": "Беспроводная мышь для профессионалов с точным сенсором 8000 DPI",
        "price": 9500,
        "stock_quantity": 75,
    },
    {
        "name": 'Samsung 27" 4K Monitor',
        "description": "4K монитор 27 дюймов с частотой обновления 144Hz для работы и игр",
        "price": 45000,
        "stock_quantity": 25,
    },
    {
        "name": "Apple AirPods Pro 2",
        "description": "Беспроводные наушники с шумоподавлением и пространственным звуком",
        "price": 25000,
        "stock_quantity": 60,
    },
    {
        "name": "USB-C Hub 7-in-1",
        "description": "Многофункциональный USB-C хаб с HDMI, USB 3.0, SD картридером",
        "price": 3500,
        "stock_quantity": 200,
    },
    {
        "name": "iPad Air 5th Gen",
        "description": 'iPad Air с процессором M1, 10.9" Liquid Retina дисплей, 64GB',
        "price": 75000,
        "stock_quantity": 20,
    },
    {
        "name": "Samsung SSD 1TB",
        "description": "Внешний SSD накопитель 1TB с интерфейсом USB 3.2 Gen 2, скорость до 1050 MB/s",
        "price": 12000,
        "stock_quantity": 80,
    },
    {
        "name": "Webcam Logitech C920",
        "description": "Full HD веб-камера 1080p с автофокусом для видеоконференций",
        "price": 7500,
        "stock_quantity": 45,
    },
    {
        "name": "Gaming Chair",
        "description": "Эргономичное игровое кресло с поддержкой поясницы и регулировкой высоты",
        "price": 25000,
        "stock_quantity": 15,
    },
    {
        "name": "Microphone Blue Yeti",
        "description": "USB микрофон для стриминга и подкастов с тремя капсюлями",
        "price": 15000,
        "stock_quantity": 35,
    },
    {
        "name": "Desk Lamp LED",
        "description": "Светодиодная настольная лампа с регулировкой яркости и температуры цвета",
        "price": 4500,
        "stock_quantity": 120,
    },
    {
        "name": "Nintendo Switch OLED",
        "description": "Игровая консоль Nintendo Switch с OLED экраном 7 дюймов",
        "price": 35000,
        "stock_quantity": 40,
    },
]


def init_db(db: Session) -> None:
    try:
        existing_products_count = db.query(Product).count()

        if existing_products_count == 0:
            logger.info("База данных пуста. Загрузка моковых данных...")

            created_count = 0
            for product_data in MOCK_PRODUCTS:
                product = Product(**product_data)
                db.add(product)
                created_count += 1

            db.commit()

            logger.info(f"Создано продуктов: {created_count}")
        else:
            logger.info(f"База данных уже содержит {existing_products_count} продуктов")

    except Exception as e:
        logger.error(f"Ошибка при инициализации БД: {str(e)}")
        db.rollback()
        raise


def clear_database(db: Session) -> None:
    try:
        deleted_count = db.query(Product).delete()
        db.commit()

        logger.info(f"Удалено продуктов: {deleted_count}")

    except Exception as e:
        logger.error(f"Ошибка при очистке БД: {str(e)}")
        db.rollback()
        raise
