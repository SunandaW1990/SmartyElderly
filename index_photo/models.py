from django.db import models

class CarouselImage(models.Model):
    title = models.CharField(max_length=100, blank=True, verbose_name="圖片說明（替代文字）")
    image = models.ImageField(upload_to='carousel/', verbose_name="圖片檔案")
    seq = models.PositiveIntegerField(default=0, verbose_name="排序（數字愈小愈前面）")
    is_active = models.BooleanField(default=True, verbose_name="啟用")
    link_url = models.URLField(blank=True, verbose_name="點擊後連結（選填）")
    creation_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['seq', 'creation_date']
        verbose_name = "輪播圖片"
        verbose_name_plural = "輪播圖片"

    def _str_(self):
        return self.title or f"圖片 {self.id}"