from django.db import models
from django.core.exceptions import ValidationError


class Category(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField()

    def __str__(self):
        return self.name


class Menu(models.Model):
    name = models.CharField(max_length=50)
    image = models.ImageField(upload_to="media/",null=True,blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    description = models.TextField()
    price = models.DecimalField(max_digits=7, decimal_places=2, default=0.00)
    create_at = models.DateField(auto_now=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.name} {self.price}"
    





class Customer(models.Model):
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=15)
    email = models.EmailField(blank=True, null=True)
    is_paid = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class Table(models.Model):
    STATUS_CHOICES = (
        ("FREE", "Free"),
        ("FULL", "Full"),
    )
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default="Free")
    table_name = models.CharField(max_length=50)

    def __str__(self):
        return self.table_name


class Bill(models.Model):
    table = models.ForeignKey(Table, on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    total_sum = models.DecimalField(max_digits=7, decimal_places=2, default=0.00)
    create_at = models.DateField(auto_now=True)
    is_paid = models.BooleanField(default=False)

    def __str__(self):
        return f"Table: {self.table.table_name}, Customer: {self.customer.name}, Total: {self.total_sum}"

    def save(self, *args, **kwargs):
        if self.is_paid:
            self.table.status = "FREE"
        else:
            self.table.status = "FULL"
        
        self.table.save()
        super().save(*args, **kwargs)


class Order(models.Model):
    bill = models.ForeignKey(Bill, on_delete=models.CASCADE,related_name="orders")
    quantity = models.PositiveIntegerField()
    menu_item = models.ForeignKey(Menu, on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        if self.quantity <= 0:
            raise ValidationError("Quantity must be greater than zero.")
        
        super().save(*args, **kwargs)

        total_sum = 0
        orders = Order.objects.filter(bill=self.bill)
        for order in orders:
            total_sum += order.quantity * order.menu_item.price

        self.bill.total_sum = total_sum
        self.bill.save()


class Payment(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    bill = models.ForeignKey(Bill, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=7, decimal_places=2)
    method = models.CharField(max_length=20, choices=(("Cash", "Cash"), ("Card", "Card")), default="Cash")
    date = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if self.amount <= 0:
            raise ValidationError("Payment amount must be greater than zero.")
        if self.amount > self.bill.total_sum:
            raise ValidationError("Amount exceeds the remaining total on the bill.")

        self.bill.total_sum -= self.amount

        if self.bill.total_sum <= 0:
            self.bill.is_paid = True
            self.bill.table.status = "FULL" 
        else:
            self.bill.is_paid = False

        self.bill.save()

        if self.bill.is_paid:
            self.customer.is_paid = True
        else:
            self.customer.is_paid = False

        self.customer.save()

        super().save(*args, **kwargs)

    def __str__(self):
        return f"Customer: {self.customer.name}, Bill: {self.bill.id}, Amount: {self.amount}"
