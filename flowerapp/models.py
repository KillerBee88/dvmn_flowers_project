from django.db import models

TYPES = [
    ("на день рождения", "на день рождения"),
    ("на свадьбу", "на свадьбу"),
    ("в школу", "в школу"),
    ("без повода", "без повода"),
]


class Client(models.Model):
    """Данные клиента (id и username в telegram)."""
    tg_id = models.IntegerField(verbose_name="ID пользователя")
    username = models.CharField(max_length=200, verbose_name="Имя пользователя")

    def __str__(self):
        return self.username

    class Meta:
        verbose_name = "Клиент"
        verbose_name_plural = "Клиенты"


class Bouquet(models.Model):
    name = models.CharField(max_length=200, verbose_name="Название букета")
    price = models.IntegerField(verbose_name="Цена букета")
    image = models.ImageField(upload_to="bouquet_image", verbose_name="Изображение букета")
    desсription = models.TextField(verbose_name="Описание букета")
    type = models.CharField(max_length=50,
                            verbose_name="Тип букета",
                            blank=False,
                            choices=TYPES,
                            default="без повода")
    
    def __str__(self):
        return f'{self.name}\nСтоимость: {self.price}'
    
    class Meta:
        verbose_name = "Букет"
        verbose_name_plural = "Букеты"


    def get_info(self):
        return f'Букет: {self.name}\nОписание: {self.desсription}\nСтоимость: {self.price}'

class Order(models.Model):
    client = models.ForeignKey(Client,
                               on_delete=models.CASCADE,
                               related_name="orders",
                               verbose_name="Клиент")
    bouquet = models.ForeignKey(Bouquet,
                                on_delete=models.SET_NULL,
                                blank=True,
                                null=True,
                                verbose_name="Букет",
                                related_name="orders")
    address = models.TextField(verbose_name="Адрес заказа")
    phone = models.IntegerField(verbose_name="Телефон", blank=True,)
    delivery_date = models.DateField(verbose_name="Дата доставки")
    delivery_time = models.TimeField(verbose_name="Время доставки")

    def __str__(self):
        return f'Заказ №{self.id}\nОжидайте {self.bouquet.name} {self.delivery_date.strftime("%d.%m.%y")} к {self.delivery_date.strftime("%H:%M")}\nСтоимость:{self.bouquet.price}'

    class Meta:
        verbose_name = "Заказ"
        verbose_name_plural = "Заказы"